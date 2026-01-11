import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../.env')  # Try loading from parent directory

print("JWT_SECRET_KEY from environment:", os.getenv("JWT_SECRET_KEY"))
print("JWT_ALGORITHM from environment:", os.getenv("JWT_ALGORITHM"))

# Also try loading from current directory
load_dotenv()

print("JWT_SECRET_KEY from environment (after reloading):", os.getenv("JWT_SECRET_KEY"))
print("JWT_ALGORITHM from environment (after reloading):", os.getenv("JWT_ALGORITHM"))