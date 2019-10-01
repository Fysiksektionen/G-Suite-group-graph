
from googleapiclient.discovery import build

class CachedGroupAPI:

    def __init__(self, credentials):
        self.service = build('admin', 'directory_v1', credentials=credentials)
        self.groupsTable = dict()
        self.membersTable = dict()


    def listGroups(self, domain, customer=None):
        key = domain
        if customer != None:
            domain = None
            key = customer

        if key in self.groupsTable:
            return self.groupsTable[key]

        req = self.service.groups().list(customer=customer, domain=domain)
        res = req.execute()
        groups = res['groups']
        while "nextPageToken" in res:
            req = self.service.groups().list_next(req, res)
            res = req.execute()
            groups.extend(res['groups'])
        
        self.groupsTable[key] = groups
        return groups

        
    def listMembers(self, groupKey):
            if groupKey in self.groupsTable:
                return self.groupsTable[groupKey]

            req = self.service.members().list(groupKey=groupKey)
            res = req.execute()
            members = res['members']
            while "nextPageToken" in res:
                req = self.service.members().list_next(req, res)
                res = req.execute()
                members.extend(res['members'])
            
            self.membersTable[groupKey] = members
            return members

    
    def getSubGroups(self, groupKey):
        return filter(lambda group: group['type'] == 'GROUP', self.listMembers(groupKey))

    def getUsers(self, groupKey):
        return filter(lambda group: group['type'] == 'USER', self.listMembers(groupKey))