# new-channel-bot
Slack bot that posts what new channels got created in the previous day.

## Setup

### Make a new slack bot
- Go to `https://<yourslack>.slack.com/apps/manage/custom-integrations`.
- Click 'Bots'.
- Click 'Add Configuration'.
- Name your bot.

### Setup environment
This is controlled by the following environment variables:

- `SLACK_BOT_TOKEN`: The API token for your new slack bot.
- `SLACK_POST_CHANNEL`: The channel to post to. If not set, it will default to `#general`.

### Running

### Without docker
```
pip install -r requirements.txt
python new_channel_bot.py
```

### With docker
```
docker build -t new_channel_bot .
docker -it -e SLACK_BOT_TOKEN='<your-token>' run new_channel_bot
```
