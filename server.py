import uvicorn
from src.main import app
# Server
# in development: uvicorn server:app --reload
# in production: python server.py prod in port 80
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)