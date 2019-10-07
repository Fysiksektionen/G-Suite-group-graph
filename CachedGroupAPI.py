
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CachedGroupAPI:

    def __init__(self, credentials):
        self.service = build('admin', 'directory_v1', credentials=credentials)
        self.groupsTable = dict()
        self.groups = dict()
        self.membersTable = dict()


    async def listGroups(self, domain, customer=None):
        key = domain
        if customer != None:
            domain = None
            key = customer

        if key in self.groupsTable:
            return self.groupsTable[key]

        req = self.service.groups().list(customer=customer, domain=domain)
        res, err = await handle(req.execute)
        if err:
            print(err)
            return []
        groups = res['groups']
        while "nextPageToken" in res:
            req = self.service.groups().list_next(req, res)
            res = req.execute()
            groups.extend(res['groups'])
        
        self.groupsTable[key] = groups
        self.groups.update([(x['id'], x) for x in groups])
        return groups


    async def getGroup(self, groupKey):
        if groupKey in self.groups:
            return self.groups[groupKey]
        req = self.service.groups().get(groupKey=groupKey)
        res, err = await handle(req.execute)
        if err:
            print(err)
            return None
        self.groups[res['id]']] = res

        
    async def listMembers(self, groupKey):
        if groupKey in self.membersTable:
            return self.membersTable[groupKey]

        req = self.service.members().list(groupKey=groupKey)
        res, err = await handle(req.execute)
        if err:
            print(err)
            return []
        if "members" not in res:
            return []
        members = res['members']
        while "nextPageToken" in res and res["nextPageToken"]:
            req = self.service.members().list_next(req, res)
            res = req.execute()
            members.extend(res['members'])
        
        self.membersTable[groupKey] = members
        return members

    
    async def preLoad(self, start_groups_keys):
        for key in start_groups_keys:
            self.listMembers(key) # Does not work like intended (javascript inspired)


    async def getSubGroups(self, groupKey):
        return [group for group in await self.listMembers(groupKey) if group['type'] == 'GROUP']

    async def getUsers(self, groupKey):
        return [group for group in await self.listMembers(groupKey) if group['type'] == 'USER']


async def handle(callback, *args, **kwargs):
    try:
        res = [callback(*args, **kwargs), None]
    except HttpError as err:
        res = [None, err]
    return res