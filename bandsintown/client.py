import os

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import requests


API_VERSION = '2.0'
APP_ID = None


class Client(object):
    API_BASE_URL = 'http://api.bandsintown.com'
    API_VERSION = '2.0'

    def __init__(self, app_id):
        self.app_id = app_id
        self.params = {
            'app_id': self.app_id,
            'api_version': self.API_VERSION
        }

        self.artists = Artist(self)

    def request(self, path, params={}):
        pass

    def parse(self, response):
        pass


class BaseAPIObject(object):
    def __init__(self, client):
        self.client = client

class Artist(BaseAPIObject):
    def _get_artist_identifier(self, *args, **kwargs):
        """
        """
        if 'fbid' in kwargs:
            return 'fbid_%s' % kwargs['fbid']
        elif 'mbid' in kwargs:
            return 'mbid_%s' % kwargs['mbid']
        elif len(args):
            return quote(args[0])
        else:
            raise TypeError('No artist identifier passed in')

    def get(self, *args, **kwargs):
        """
        Searches for an artist via this endpoint:

            https://www.bandsintown.com/api/requests#artists-get

        Accepts one of the following:
            * A single string argument of an artist's name
            * A `fbid` kwarg with the artist's Facebook ID
            * A `mbid` kwarg with the artist's MusicBrainz ID
        """
        return self.client.request(self._get_artist_identifier(*args, **kwargs))

    def events():
        pass

    def search():
        pass

    def recommended():
        pass


class Event(object):
    pass
