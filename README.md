# USYD Puzzle Soc Discord Bot

A bot created for USYD Puzzle Society. Performs message scheduling and various other features.

## Installation guide

To get a local copy of the repository, first do:

    git clone https://github.com/eluric/weekly-puzzle-bot.git

then, download the required dependencies using:

    cd weekly-puzzle-bot/
    pip install -r requirements.txt

and finally, provide the bot token in a `.token` file in the root level directory.

## Running the bot

To run the bot, simply do:

    cd weekly-puzzle-bot/
    python3 main.py


## Connecting to a database

The Discord Bot uses MongoDB Atlas by default. To connect to your own Atlas instance, include the following content in a .env file:

    DB_URI = <your-uri-string>