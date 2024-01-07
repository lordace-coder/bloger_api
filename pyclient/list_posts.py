import requests
from get_auth_token import get_token

URL = 'http://localhost:8000/posts'


headers = {
    'Authorization': f'Bearer {get_token()}'
}

data = {

    "title":"edited2",

}

response = requests.get(URL, headers=headers,data=data)
requests.status_codes
if response.status_code == requests.codes.ok:
    print("status code", response.status_code)
    print(response.json())
else:
    print(response.status_code)
