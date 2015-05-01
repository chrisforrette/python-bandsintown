import os

try:
    from urllib.parse import quote, urljoin
except ImportError:
    from urllib import quote
    from urlparse import urljoin

import requests


class Client(object):
    API_BASE_URL = 'http://api.bandsintown.com'
    API_VERSION = '2.0'

    def __init__(self, app_id):
        self.app_id = app_id
        self.params = {
            'app_id': self.app_id,
            'api_version': self.API_VERSION
        }

        self.artists = Artists(self)

    def request(self, path, params={}):
        url = urljoin(self.API_BASE_URL, path) + '.json'
        request_params = self.params.copy()
        request_params.update(params)
        return self.parse(requests.get(url, params=request_params))

    def parse(self, response):
        return response.json()


class BaseAPIObject(object):
    def __init__(self, client):
        self.client = client

class Artists(BaseAPIObject):
    def get(self, *args, **kwargs):
        """
        Searches for a single artist via this endpoint:

            https://www.bandsintown.com/api/requests#artists-get

        Requires one of the following artist identifiers:

            - A single string argument of an artist's name
            - A `fbid` kwarg with the artist's Facebook ID
            - A `mbid` kwarg with the artist's MusicBrainz ID

        Returns a dict or None if not found

        Usage:

            client = Client(app_id=1234)
            client.artists.get('Bad Religion')
            client.artists.get(fbid=168803467003)
            client.artists.get(mbid='149e6720-4e4a-41a4-afca-6d29083fc091')
        """
        artist_identifier = self._get_artist_identifier(*args, **kwargs)
        return self.client.request('artists/%s' % artist_identifier)

    def events(self, *args, **kwargs):
        """
        Get events for a single artist, calling this endpoint:

            https://www.bandsintown.com/api/requests#artists-events

        Requires an artist identifier, similar to the `get` method, 
        and accepts the following keyword arguments:

            date (string) (optional)
                Can be one of the following:
                    - "upcoming"
                    - "all"
                    - A date string in the format: yyyy-mm-dd
                    - A date range string in the format: yyyy-mm-dd,yyyy-mm-dd

        Returns a list or None if not found

        Usage:

            client = Client(app_id=1234)
            client.artists.events('Bad Religion')
            client.artists.events('Bad Religion', location='Portland,OR')
        """
        artist_identifier = self._get_artist_identifier(*args, **kwargs)
        params = {}
        if 'date' in kwargs:
            params['date'] = kwargs['date']
        return self.client.request('artists/%s/events' % artist_identifier, params)

    def search(self, *args, **kwargs):
        """
        Gets events for a single artist with search criteria using this endpoint:

            https://www.bandsintown.com/api/requests#artists-event-search

        Requires an artist identifier, similar to the `get` method, 
        and accepts the following keyword arguments:

            location (string)
                A location string in one of the following formats:
                    - city,state (US or CA)
                    - city,country
                    - lat,lon
                    - IP address

            radius (string/integer) (optional)
                Number of miles radius around location to search within. 
                Defaults to 25, max is 150
            
            date (string) (optional)
                Can be one of the following:
                    - "upcoming"
                    - "all"
                    - A date string in the format: yyyy-mm-dd
                    - A date range string in the format: yyyy-mm-dd,yyyy-mm-dd
        """
        artist_identifier = self._get_artist_identifier(*args, **kwargs)
        params = {'location': kwargs['location']}
        for param in ['radius', 'date']:
            if param in kwargs:
                params[param] = kwargs[param]
        return self.client.request('artists/%s/events/search' % artist_identifier, params)

    def recommended(self, *args, **kwargs):
        """
        Gets recommended events based on single artist and location and other 
        optional search criteria using this endpoint:

            https://www.bandsintown.com/api/requests#artists-recommended-events

        Requires an artist identifier, similar to the `get` method, 
        and accepts the following keyword arguments:

            location (string)
                A location string in one of the following formats:
                    - city,state (US or CA)
                    - city,country
                    - lat,lon
                    - IP address

            radius (string/integer) (optional)
                Number of miles radius around location to search within. 
                Defaults to 25, max is 150
            
            date (string) (optional)
                Can be one of the following:
                    - "upcoming"
                    - "all"
                    - A date string in the format: yyyy-mm-dd
                    - A date range string in the format: yyyy-mm-dd,yyyy-mm-dd

            only_recs (boolean) (optional)
                If True, only recommended events are returned, if False the artist's 
                events are included along with the recommended ones
        """
        artist_identifier = self._get_artist_identifier(*args, **kwargs)
        params = {'location': kwargs['location']}

        for param in ['radius', 'date']:
            if param in kwargs:
                params[param] = kwargs[param]

        if 'only_recs' in kwargs:
            params['only_recs'] = 'true' if kwargs['only_recs'] else 'false'

        return self.client.request('artists/%s/events/recommended' % artist_identifier, params)

    def _get_artist_identifier(self, *args, **kwargs):
        """
        Get artist identifier based on passed in args/kwargs. Can be a string positional argument, 
        an `fbid` kwarg (Facebook ID), or an `mbid` (MusicBrainz ID)
        """
        if 'fbid' in kwargs:
            return 'fbid_%s' % kwargs['fbid']
        elif 'mbid' in kwargs:
            return 'mbid_%s' % kwargs['mbid']
        elif len(args):
            return quote(args[0])
        else:
            raise TypeError('No artist identifier passed in')

