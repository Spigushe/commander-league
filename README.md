# CommanderLeague
Web App for the Commander League

## Stack
The Commander League is using different stacks depending on the tools

### Frontend
Uses the following stack to serve UI:
```
   ReactJS - framework
   Bootstrap - components
   Stylus - CSS
```

### Backend
Performs search in official VTES card database and stores account/decks/inventory with:

```
   Flask - framework
   SQLite - database
```
### Discord Bot
```
    Python - language
    Discord.Py - library
    GoogleAPI - library
```

## Special Thanks
We'd like to thank the follow person for their help throughout the development of the App:
- Zankou for designing the skeleton of the Discord Bot currently use

## Installation

### Local Deployment (on Linux)

Below is local deployment for self-usage/development only!

```
    git clone https://github.com/Spigushe/commander-league.git
    cd commander-league
```

Start backend:
```
    cd flask-backend
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"
    backend
```

Start frontend:
```
    cd react-frontend
    npm install
    parcel serve index.html
```

Start discord bot:
```
    cd discord-bot
	python -m venv venv
	source venv/bin/activate
    pip install -e ".[dev]"
	league-bot
```

### Production Deployment

For production you should at least:
* setup web-server (we use `nginx`) instead of `parcel` embedded web-server
* setup wsgi-server (we use `gunicorn`) instead of `flask` embedded web-server
* build frontend for production (see your prefered bundler documentation, for `parcel` use `parcel build index.html`)
* change `app.config['SECRET_KEY']` in `config.py`

## LICENSE

MIT
