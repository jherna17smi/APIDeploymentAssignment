from app import create_app
from config import TestingConfig

app = create_app(TestingConfig)

if __name__ == "__main__":
	app.run(debug=True, host="127.0.0.1", port=5000)
