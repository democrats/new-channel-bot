""" Posts a list of channels created in the last day to slack. """
import datetime
import os
import slackclient


def post_new_channels(token, post_channel):
    """ Fetches list of slack channels and posts the new ones.

    Args:
        token (string): Slack API token.
        post_channel (string): Channel to post announcements to.
    """
    slack = slackclient.SlackClient(token)

    response = slack.api_call('channels.list')
    channels = response.get('channels')

    for channel in channels:
        created = datetime.datetime.utcfromtimestamp(channel['created'])
        purpose = channel.get('purpose', {}).get('value', {})
        name = channel['name']
        descriptor = "<#{}|{}>".format(channel['id'], name)

        if created + datetime.timedelta(days=1) > datetime.datetime.now():
            if purpose:
                text = "New channel {}. Purpose: '{}'".format(
                    descriptor, purpose
                )
            else:
                text = "New channel {}".format(descriptor)

            response = slack.api_call(
                'chat.postMessage',
                channel=post_channel,
                text=text,
                as_user=True
            )


if __name__ == "__main__":
    post_new_channels(
        os.environ.get('SLACK_BOT_TOKEN'),
        os.environ.get("SLACK_POST_CHANNEL", "#general")
    )
