import json
import urllib.request
import urllib.parse

# 1. Login as driver
data = urllib.parse.urlencode({'username': 'driver@addisexpress.et', 'password': 'DriverPass123!'}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/api/v1/auth/token', data=data)
with urllib.request.urlopen(req) as response:
    resp_data = json.loads(response.read().decode())
    token = resp_data['access_token']

# 2. Call optimize
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
payload = {
    "locations": [
        {"latitude": 8.9778, "longitude": 38.7992},
        {"latitude": 9.0100, "longitude": 38.7350}
    ]
}
req2 = urllib.request.Request('http://127.0.0.1:8000/api/v1/optimize/', headers=headers, data=json.dumps(payload).encode(), method='POST')
try:
    with urllib.request.urlopen(req2) as response:
        print("Optimize Status:", response.status)
        print("Response Success!")
except urllib.error.HTTPError as e:
    print("Optimize Status:", e.code)
    print("Response:", e.read().decode())
