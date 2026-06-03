🧠 Why This Is Important

Many public APIs use API keys:

✅ Weather APIs
✅ Payment APIs
✅ Maps APIs
✅ SaaS APIs

Instead of logging in every request, clients send an API key.

Example:
GET /data
X-API-Key: abc123xyz

🛠 Tech Stack
Python
Flask
SQLAlchemy
UUID

📂 Project Structure
api-key-auth-system/
├── app.py
├── api_keys.db
└── README.md
