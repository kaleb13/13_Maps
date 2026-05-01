import json
import urllib.request
import urllib.parse
import uuid

email = f"test_{uuid.uuid4().hex[:8]}@example.com"
data = {
    'email': email,
    'password': 'Password123!',
    'full_name': 'Test User'
}
req = urllib.request.Request('http://127.0.0.1:8000/api/v1/auth/register', data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        print("Register Status:", response.status)
        resp_data = json.loads(response.read().decode())
        print("Role:", resp_data['role'])
except urllib.error.HTTPError as e:
    print("Register Status:", e.code)
    print("Response:", e.read().decode())
