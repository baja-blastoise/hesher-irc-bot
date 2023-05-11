# hesher-irc-bot
An IRC bot that scrapes the Metal Archives for information on bands, artists, and albums, and dumps it in the IRC channel.  The bot utilizes the [metal-archives-lookup](https://github.com/baja-blastoise/metal-archives-lookup) python library to pull the requested information.

## Dependencies
Hesher uses Python3 and the following libraries:
1. socket
2. time
3. [metal-archives-lookup](https://github.com/baja-blastoise/metal-archives-lookup) *(requires its own dependencies)*

## Installation
Install the required dependencies in your python environment.  Clone this repository using:

`git clone https://github.com/baja-blastoise/hesher-irc-bot`

Copy **malookup.py** into the same directory you will run the bot from, or otherwise add it to your environment.  Proceed to the configuration section below.

## Configuration
Rename *example_config.txt* to *config.txt*, and fill out the settings for your specific use case.
- **server** - The IP address of the IRC server you wish to connect to.
- **channel** - The channel you want hesher to join.  Currently each instance of the bot can only join a single channel.
- **botnick** - Allows you to change the nickname the bot will use.
- **port** - Port to connect on.
- **print** - Controls the amount of print statements sent to the console that launched the bot.  When set to **0**, the bot will only print command messages when it detects it has received a command.  When set to **1** the bot will print a copy of the return message in the console, useful for monitoring or debugging.

## Usage
Once you have finished configuring the bot, launch it in your terminal with:

`python3 hesher.py`

The bot will stay active as long as the process is active.

The bot supports the following commands.  Detailed usage syntax with examples can be found in the help.txt file, or using the `!help` command in the IRC channel itself.
- **!help** - displays info contained in *help.txt*
- **!band** - returns basic information about a band
- **!discog** - returns a band's discograpy
- **!members** - returns a band's lineup
- **!similar** - returns similar bands based on Metal Arcives ratings
- **!artist** - returns basic artist information as well as band membership
- **!album** - returns album track listing and lineup


## Issues / Quirks
I haven't figured out a way to send more than one line at a time.  The bot output is often formatted in tables which must be printed one line at a time to retain the formatting.  Depending on your server's flood control settings, this will cause the return message to print slowly or potentially trigger a trigger happy kick.

Web scraping is an imprecise practice (and I'm not good at it) and the archives have 20 years of submissions of varying quality.  Some of the formatting might not work for some of the less detailed bands.

Bands written in a script besides latin, or those using diacritics, can be difficult to use.  The library works by inferring the appropriate URL based on band/artist/album name.  Usually diacritics are ignored completely and other scripts are usually Romanized.  But it might take some trial and error to find the right string.

Share the command string if you encounter unexpected output.
