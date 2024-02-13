import requests
 
def get_token():
    if token is None:
        token = requests.get('http://127.0.0.1:5000/login')
        return token.json()['token']
def bot(input,token):
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'input': input}
        response = requests.post(headers=headers,  url='http://127.0.0.1:5000/bot', json=payload)
        return response.json()['message']