import logging
from dotenv import load_dotenv
import os
from app.main import create_app
from app import blueprint


load_dotenv()
app = create_app(os.getenv('CURRENT_ENV') or 'dev')
app.register_blueprint(blueprint)

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000, use_reloader=False)
