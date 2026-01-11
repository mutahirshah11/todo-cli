import jwt
import datetime

# Create a test token that's valid for 24 hours
payload = {
    'user_id': 'test_user',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
}
token = jwt.encode(payload, 'your-super-secret-key-change-in-production', algorithm='HS256')

print('Test Token:', token)
print('Token will expire in 24 hours')