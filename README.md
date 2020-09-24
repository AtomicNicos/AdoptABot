# Adopt A Skill Bot

## Author

| Name | GitLab | GitHub | Twitter |
|:--- |:---:|:---:|:---:|
| Nicolas Boeckh | [To GitLab](https://gitlab.unige.ch/Nicolas.Boeckh) | [To GitHub](https://github.com/AtomicNicos/) | [To Twitter](https://www.twitter.com/AtomicNicos)

## What is this `?`

This is a Discord bot whose sole purpose is to juggle people through voice channels in a predefined sequence (as defined in `order.yaml`).

## How to run `?`

### Requirements

#### *(Optional)* [Poetry](https://python-poetry.org/)

If installed simply run:

```bash
cd AdoptABot
poetry install
poetry shell
python3 ./adoptabot/bot.py
```

#### [Python 3.8](https://www.python.org/downloads/release/python-380/)

### Run

Install the following dependencies:

```bash
pip install discord python-dotenv PyYAML
```

Then execute the following :

```bash
cd AdoptABot
python3 ./adoptabot/bot.py
```
