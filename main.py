
from google.oauth2 import service_account
from CachedGroupAPI import CachedGroupAPI
from asyncio import get_event_loop
from Graph import Graph

# TODO(developer): Set key_path to the path to the service account key
#                  file.
key_path = "./service_account.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=[
        "https://www.googleapis.com/auth/admin.directory.group.readonly",
        "https://www.googleapis.com/auth/admin.directory.group.member.readonly"
    ]
)
credentials=credentials.with_subject('morriser@fysiksektionen.se')

def aw(coro):
    loop = get_event_loop()
    return loop.run_until_complete(coro)


async def buildGraph():
    api = CachedGroupAPI(credentials)
    graph = Graph(directed=True)

    start_groups_keys = set([x['id'] for x in await api.listGroups("fysiksektionen.se")])

    api.preLoad(start_groups_keys)

    not_seen = start_groups_keys.copy()
    seen = set()

    while not_seen:
        group_key = not_seen.pop()
        group = await api.getGroup(group_key)
        graph.addNode(group_key, group, label=group['name'])

        print(group['name'])

        children = await api.getSubGroups(group_key)
        for child in children:
            key = child['id']
            not_seen.add(key)
            graph.addEdge(group_key, key)
        
        users = await api.getUsers(group_key)
        group['users'] = [x['email'] for x in users]

        seen.add(group_key)
        not_seen -= seen

    dot = str(graph)
    print(dot)
    print(f"{len(start_groups_keys)} vs. {len(seen)}")
    return dot

if __name__ == "__main__":
    dot = aw(buildGraph())