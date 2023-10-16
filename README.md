# WG-bots

This is a collection of three bots that I have used to search for (shared) flats in Munich. The bots are inspired by [immobot](https://github.com/nickirk/immo). The pipeline is designed to work on a headless linux systems with a chrome browser and a gmail account. Of course, it can be adapted to other platforms, browsers, and email providers.

## wgzimmerbot

This bot checks the platform wg-gesucht.de every 60 seconds for new rooms. If a new offer has been found, it sends you a notification email. This is allows you to write customized texts, which is recommended for shared flats. The bot is approximately 15 minutes faster than the built-in notification system. 

### Usage

1. Install the requirements with `pip install -r requirements.txt`
2. Enter the URL of your search query in [`wg-gesucht-spider.py`](wgzimmerbot/wgzimmerbot/spiders/wg-gesucht-spider.py)
3. Enter your gmail address and password in [`run_bot.sh`](wgzimmerbot/run_bot.sh)
4. Run the bot with `./wgzimmerbot/run_bot.sh`

## wgwohnungsbot

This bot checks the platform wg-gesucht.de every 60 seconds for new flats. If a new offer has been found, it sends you a notification email and contacts the offer directly with a prespecified message. A placeholder for the name of the contact person can be used to personalized the message. Further, the bot allows for attaching a "Gesuch", which contains more information about yourself. This is recommended for flats, as it allows you to stand out from the crowd.

### Usage

1. Install the requirements with `pip install -r requirements.txt`
2. Enter the URL of your search query in [`wg-gesucht-spider.py`](wgwohnungsbot/wgwohnungsbot/spiders/wg-gesucht-spider.py)
2. Enter the prespecified message you want to send in [`message.txt`](wgwohnungsbot/message.txt) (you can use the placeholder `NAME` for the name of the contact person followed by a colon)
3. Enter your gmail address and password in [`run_bot.sh`](wgwohnungsbot/run_bot.sh)
4. Enter your wg-gesucht.de username and password in [`run_bot.sh`](wgwohnungsbot/run_bot.sh)
5. Run the bot with `./wgwohnungsbot/run_bot.sh`

## wochenanzeigerbot

This bot checks the website of [Wochenanzeiger](https://www.wochenanzeiger.de/mietangebote/) every five minutes for new offers. If new offers are found, it sends you a notification email with the descriptions along with a link to the website. This is helpful, as the website does not have a notification system.

### Usage

1. Install the requirements with `pip install -r requirements.txt`
2. Enter your gmail address and password in [`run_bot.sh`](wgzimmerbot/run_bot.sh)
3. Run the bot with `./wochenanzeigerbot/run_bot.sh`