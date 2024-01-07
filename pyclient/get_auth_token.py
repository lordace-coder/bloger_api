import requests

endpoint = "http://localhost:8000/auth/get_token/"


def get_token():
    data = {
    'username':"lordace",
    'password':"lordacemax",
    
}
    response = requests.post(endpoint,json=data)
    if response.status_code == 200:
        response = response.json()
        with open("tokens.txt",'w') as file:
            file.write(f"{response}")
        return response.get('access')
    else:
        print(response.json(),response.status_code)

if __name__ == "__main__":
    get_token()