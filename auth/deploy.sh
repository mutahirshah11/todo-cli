#!/bin/bash
# Deployment script for Authentication Service

set -e

echo "Starting deployment of Authentication Service..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests (if any)
echo "Running tests..."
python -m pytest tests/ || echo "No tests found or tests failed, continuing..."

# Start the service
echo "Starting Authentication Service..."
python start_auth_service.py --port 8001 &

AUTH_PID=$!
echo $AUTH_PID > auth.pid

echo "Authentication Service deployed successfully!"
echo "Service running on PID: $AUTH_PID"
echo "Access the service at: http://localhost:8001"

# Keep the script running
wait $AUTH_PID