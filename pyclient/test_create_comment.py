import requests
from get_auth_token import get_token

URL = "http://localhost:8000/comment/1"


headers = {
    'Authorization': f'Token {get_token()}'
}

data = {
    
    "comment":"yeah agreed"
}

response = requests.post(URL,data=data,headers=headers)

if response.status_code == requests.codes.created:
    print("status code",response.status_code)
    print(response.json())
else:
    print(response.text)