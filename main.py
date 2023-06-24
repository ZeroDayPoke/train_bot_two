#!/usr/bin/env python3
""" Entry Point """

import multiprocessing
from run_bot import run_bot
from app import create_app, db
from flask_migrate import Migrate

# Create the Flask application
app = create_app()

migrate = Migrate(app, db)

def run_app():
    """ Main Function """
    host = '127.0.0.1'
    port = '5300'
    app.run(host=host, port=port)

if __name__ == "__main__":
    # Create a process for the Discord bot
    # bot_process = multiprocessing.Process(target=run_bot)
    # bot_process.start()

    # Create a process for the Flask web application
    app_process = multiprocessing.Process(target=run_app)
    app_process.start()

    # Wait for both processes to finish
    # bot_process.join()
    app_process.join()
