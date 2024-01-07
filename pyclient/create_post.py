import requests
from get_auth_token import get_token

URL = "http://localhost:8000/create_post/"


headers = {
    'Authorization': f'Token {get_token()}'
}

data = {
    "post": """Certainly! If you prefer using the fetch API instead of axios for making HTTP requests in your React project, you can modify the authentication code accordingly. Here's an example using fetch:
export default Login;
In this example, we replace the axios.post() call with the fetch() function to make the POST request. We set the appropriate headers for the request using the 'Content-Type': 'application/json' key-value pair. The response is then handled based on the response.ok property to check if the request was successful.
Remember to adjust the API endpoint URL ('/api/auth/login/') and the error handling approach according to your specific backend API structure and requirements.
Using fetch, you can handle HTTP requests in your React project without adding an additional library like axios.
I hope this helps! Let me know if you have any further questions.""",
    "title":"To be edited",

}

response = requests.post(URL, data=data, headers=headers)

if response.status_code == requests.codes.created:
    print("status code", response.status_code)
    print(response.json())
else:
    print(response.text)
