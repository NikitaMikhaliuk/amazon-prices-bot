## Amazon Prices Bot
### What this bot can do?
This bot helps to find products on Amazon, using a third-party API: [Real-Time Amazon Data](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data)

### Установка
- Clone this repo using `git clone` or your IDE
- Create and acivate __Python 3.11__ virtual environment in the project's folder
- Run `pip install -r requirements.txt` to instal project's dependencies
- In project's root folder, create a `.env` file  that should look like this:
```
BOT_TOKEN="<your telegram bot token>"
API_HOST="real-time-amazon-data.p.rapidapi.com"
API_KEY="<your API key>"
PY_ENV="PRODUCTION"
LOG_LEVEL="DEBUG"
```
- To start the bot, run `python main.py` in activated virtual env

### Bot's commands
#### Bot can run the following commands:

__/low__ - searches the prouct with the lowest price. Required params: *product to search, search results display limit*

__/high__ - searches the prouct with the highest price. Required params: *product to search, search results display limit*

__/custom__ - searches the product within specified prices range. Required params: *product to search, minimum price, maximum price, search results display limit*

For __/low__, __/high__ and __/custom__ commands, instead of using usual dialog, you can also inline all the params with the command like this:
__/custom__ *product min_price max_price limit*

__/cancel__ - cancels current search dialog

__/history__ - shows your last 5 search requests with the parameters inlined

__/help__ - shows bot's commands description
