from googleapiclient.discovery import build
from google.oauth2 import service_account

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

service = build('admin', 'directory_v1', credentials=credentials)

print(service.groups().list(customer="my_customer", domain="fysiksektionen.se").execute())
