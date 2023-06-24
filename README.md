# Project Train Bot mk 2

## Description

This is a project management application built with Flask and integrated with a Discord bot. It allows users to create, update, view, and delete projects. Each project can have multiple related users and roles. The application also includes user authentication and role-based access control. Users can interact with the application through a web interface or via the Discord bot.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ZeroDayPoke/train_bot_two
   ```

2. Navigate to the project directory:

   ```bash
   cd train_bot_two
   ```

3. Install the requirements:

   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

1. Set the FLASK_APP environment variable:

   ```bash
   export FLASK_APP=main.py
   ```

2. Run the application:

   ```bash
   flask run
   ```

3. Open a web browser and navigate to `http://localhost:5000`.

## Discord Bot Usage

1. Invite the bot to your Discord server.
2. Use the bot's commands to interact with the project management system. For example:
   - `tb create Project name=we_uwu_train_bot`: Creates a new project.
   - `tb all Role`: Outputs the representation of all Role objects.
   - `tb update User <user_id> role=HIGHLANDER`: Add the HIGHLANDER role to the corresponding user.
   - `tb delete Project <project_id>`: Removes the project with the associated id from the db.

## Features

- User registration and authentication
- Role-based access control
- Project creation, updating, viewing, and deletion
- Association of multiple users and roles with each project
- Discord bot integration for interacting with the project management system

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Author

- **Chris Stamper** [ZeroDayPoke](https://github.com/ZeroDayPoke)
