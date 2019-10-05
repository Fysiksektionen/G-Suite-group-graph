
from google.oauth2 import service_account
from CachedGroupAPI import CachedGroupAPI

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

api = CachedGroupAPI(credentials)

print(api.listGroups("fysiksektionen.se"))

for group in api.listGroups("fysiksektionen.se"):
    print(group)

print(api.getSubGroups(api.listGroups("fysiksektionen.se")[0]['id']))