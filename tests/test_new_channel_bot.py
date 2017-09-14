""" Tests for new channel bot """
import datetime
import time
import unittest
import mock
import new_channel_bot


def _make_fake_api(channels, posts):
    """
    Construct a fake slack API

    Args: channels (dict): List of channels to mock in.
          posts (array): Collection of all calls to the postMessage api.
    """
    def api(method, **kwargs):
        """
        Simple fake API for the methods we care about
        Args:
            method (string) Slack API method.
             **kwargs: Arbitrary keyword arguments.
        """
        if method == 'channels.list':
            return channels
        elif method == 'chat.postMessage':
            posts.append(kwargs)
            return
        else:
            raise Exception('Unexpected method: {}'.format(method))
    return api


class NewChannelBotTests(unittest.TestCase):
    """ Tests for new channel bot """

    @mock.patch.object(new_channel_bot.slackclient.SlackClient, 'api_call')
    def test_skips_old_channels(self, api):
        """ Verify we only post new channels """
        posts = []
        old_channel_time = (
            time.time() - datetime.timedelta(days=2).total_seconds()
        )
        new_channel_time = (
            time.time() - datetime.timedelta(hours=23).total_seconds()
        )
        channels = {
            'channels': [
                {
                    'name': 'old-channel',
                    'purpose': {'value': 'not recently made!'},
                    'id': '1',
                    'created': old_channel_time
                },
                {
                    'name': 'new-channel',
                    'purpose': {'value': 'recently made!'},
                    'id': '2',
                    'created': new_channel_time
                }
            ]
        }

        api.side_effect = _make_fake_api(channels, posts)
        new_channel_bot.post_new_channels(channels, '#__TEST__')

        self.assertEqual(len(posts), 1)
        self.assertEqual('#__TEST__', posts[0].get('channel'))
        self.assertIn('new-channel', posts[0].get('text'))

    @mock.patch.object(new_channel_bot.slackclient.SlackClient, 'api_call')
    def test_message_formatting(self, api):
        """ Verify that we properly format messages """
        posts = []
        channels = {
            'channels': [
                {
                    'name': 'really-purposeless',
                    'id': '1',
                    'created': time.time()
                },
                {
                    'name': 'purposeless',
                    'purpose': {'value': ''},
                    'id': '2',
                    'created': time.time()
                },
                {
                    'name': 'purposeful',
                    'purpose': {'value': 'recently made!'},
                    'id': '3',
                    'created': time.time()
                }
            ]
        }

        api.side_effect = _make_fake_api(channels, posts)
        new_channel_bot.post_new_channels(channels, '#__TEST__')

        self.assertEqual(len(posts), 3)
        self.assertEqual(
            'New channel <#1|really-purposeless>',
            posts[0].get('text')
        )
        self.assertEqual(
            'New channel <#2|purposeless>',
            posts[1].get('text')
        )
        self.assertEqual(
            "New channel <#3|purposeful>. Purpose: 'recently made!'",
            posts[2].get('text')
        )

    @mock.patch.object(new_channel_bot.slackclient.SlackClient, 'api_call')
    def test_unicode(self, api):
        """ Tests that we can handle unicode names """
        posts = []
        channels = {
            'channels': [
                {
                    'name': u'\U0001f604',
                    'id': '1',
                    'created': time.time(),
                    'purpose': {'value': u'something\U0001f604'},
                }
            ]
        }

        api.side_effect = _make_fake_api(channels, posts)
        new_channel_bot.post_new_channels(channels, '#__TEST__')

        self.assertEqual(len(posts), 1)
        self.assertEqual(
            u"New channel <#1|\U0001f604>. Purpose: 'something\U0001f604'",
            posts[0].get('text')
        )
