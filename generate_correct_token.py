import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the secret key from environment variables
secret_key = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")

# Create a test token that's valid for 24 hours
payload = {
    'user_id': 'test_user',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
}
token = jwt.encode(payload, secret_key, algorithm='HS256')

print('Test Token:', token)
print('Secret Key used:', secret_key)
print('Token will expire in 24 hours')