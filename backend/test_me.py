import json
import urllib.request
import urllib.parse

data = urllib.parse.urlencode({'username': 'admin@addisexpress.et', 'password': 'AdminPass123!'}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/api/v1/auth/token', data=data)
with urllib.request.urlopen(req) as response:
    resp_data = json.loads(response.read().decode())
    token = resp_data['access_token']

headers = {'Authorization': f'Bearer {token}'}
req2 = urllib.request.Request('http://127.0.0.1:8000/api/v1/users/me', headers=headers)
try:
    with urllib.request.urlopen(req2) as response:
        print("Me Status:", response.status)
        print("Response:", response.read().decode())
except urllib.error.HTTPError as e:
    print("Me Status:", e.code)
    print("Response:", e.read().decode())
