# MonoTanks API wrapper in Python for HackArena 2.0

This API wrapper for MonoTanks game for the HackArena 2.0, organized by
KN init. It is implemented as a WebSocket client written in Python programming
language and can be used to create bots for the game.

To fully test and run the game, you will also need the game server and GUI
client, as the GUI provides a visual representation of gameplay. You can find
more information about the server and GUI client in the [Server and GUI Client Repository](https://github.com/INIT-SGGW/HackArena2.0-MonoTanks).

The guide to the game mechanics and tournament rules can be found on the [instruction page](https://hackarena.pl/Assets/Game/HackArena%202.0%20-%20instrukcja.pdf).

## Development

Clone this repo using git:
```sh
git clone https://github.com/INIT-SGGW/HackArena2.0-MonoTanks-Python.git
```

The logic of the bot should be implemented in the `main.py` file.

**main.py**:

```py

from hackathon_bot import *


class MyBot(HackathonBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        pass

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass


if __name__ == "__main__":
    bot = MyBot()
    bot.run()

```

The `main.py` file contains a class `MyBot` that inherits from the `HackathonBot`
class. The `HackathonBot` class is a wrapper for the WebSocket client that
handles communication with the game server.

The `MyBot` class should implement the following methods:

- `on_lobby_data_received(lobby_data: LobbyData) -> None`:
  This method is called when the bot receives the lobby data from the server.
  The `LobbyData` object contains information about the game lobby,
  such as the map size, number of players, and other settings.

- `next_move(game_state: GameState) -> ResponseAction`:
  This method is called when the bot receives the game state from the server.
  The `GameState` object contains information about the current game state.
  The method should return a `ResponseAction` object that represents the bot's next move.

- `on_game_ended(game_result: GameResult) -> None`: 
  This method is called when the game ends.
  The `GameResult` object contains information about the game
  result, such as the winner and the final scores.

- `on_warning_received(warning: WarningType, message: str | None) -> None`:
  This method is called when the bot receives a warning from the server. The
  `WarningType` object represents the type of warning, and the `message` string
  contains the warning message (if any).

You can also overwrite the `on_game_starting` method to perform some actions
before the game starts. See its documentation in the `hackathon_bot.py`
file for more information.

## Running the Bot (Local)

To run the bot locally, you must have Python 3.10 or higher installed on your
system.

Additionally, you can create a virtual environment to install the required
dependencies:

```sh
python -m venv .venv
```

Activate the virtual environment:

- On Windows:
  ```sh
  .venv\Scripts\activate
  ```
- On macOS and Linux:
  ```sh
    source .venv/bin/activate
  ```

Install the required dependencies:

```sh
pip install -r hackathon_bot/requirements.txt
```

Run the bot:

```sh
python main.py --nickname <nickname>
```

You can also run the bot with the `--help` flag to see the available options:
- `--host`: The host of the game server (default: `localhost`).
- `--port`: The port of the game server (default: `5000`).
- `--nickname`: The nickname of the bot (required).
- `--code`: The join code of the game lobby (default: `None`).

## Running the Bot (Docker container)

To run the bot manually in a Docker container, ensure Docker is installed on
your system.

Steps:

1. Build the Docker image:
   ```sh
   docker build -t bot .
   ```
2. Run the Docker container:
   ```sh
   docker run --rm bot --nickname <nickname>
   ```

If the server is running on your local machine, use the
`--host host.docker.internal` flag to connect the Docker container to your local
host.

## Example

An example bot implementation is provided in the `example.py` file.
The bot prints the map and returns a random move each turn.
Use the following command to run the example bot:

```sh
python example.py
```

## FAQ

### What can we modify?

You can modify the `main.py` file to implement your own bot logic
as well as create new files and directories in the root directory
to implement additional functionality.

If your bot requires additional dependencies, you can add them to the
`requirements.txt` file. Take note, that in the `hackathon_bot` directory
there is a `requirements.txt` file that is used to install the dependencies
for the API wrapper, so do not duplicate the dependencies in the root
`requirements.txt` file.

Please, do not modify any files in the `hackathon_bot` directory, as they
contain the API wrapper implementation.

### In what format we will need to submit our bot?

You will need to submit a zip file containing the whole repository. Of course,
please, delete the `.venv` directory before submitting the zip file.
