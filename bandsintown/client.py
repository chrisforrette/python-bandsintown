try:
    from urllib.parse import quote, urljoin
except ImportError:
    from urllib import quote
    from urlparse import urljoin

import requests


class BandsintownError(Exception):
    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message


class BandsintownInvalidAppIdError(BandsintownError):
    pass


class BandsintownInvalidDateFormatError(BandsintownError):
    pass


class Client(object):
    api_base_url = 'https://rest.bandsintown.com'

    def __init__(self, app_id):
        """
        Args:
            app_id: Required app id, can be any string
        """
        self.app_id = app_id
        self.default_params = {'app_id': self.app_id}

    def request(self, path, params={}):
        """
        Executes a request to the Bandsintown API and returns the response
        object from `requests`

        Args:
            path: The API path to append to the base API URL for the request
            params: Optional dict to tack on query string parameters to request

        Returns:
            Response object from `requests`
        """
        url = urljoin(self.api_base_url, path)
        request_params = self.default_params.copy()
        request_params.update(params)
        response = requests.get(
            url,
            headers={'Accept': 'application/json'},
            params=request_params
        )
        data = response.json()

        if 'message' in data and data['message'] == 'Missing required request parameters: [app_id]':
            message = 'Missing required API key, which must be a single string argument to Client instantiation, e.g.: client = Client("my-app-id")'
            raise BandsintownInvalidAppIdError(message, response)
        else:
            return data

    def artists(self, artistname):
        """
        Searches for a single artist using this endpoint:

            https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0#/single_artist_information/artist
        Args:
            artistname: Artist name to search for

        Returns:
            A dict of artist data when the artist is found, and returns
            None when not found

        Usage:
            client = Client(app_id='my-app-id')
            client.artists('Bad Religion')
        """
        try:
            return self.request('artists/%s' % quote(artistname))
        except ValueError:
            # Currently the API's response when the artist doesn't exist is
            # badly formed JSON. In such a case, we're catching the exception
            # and returning None
            return None

    def artists_events(self, artistname, date=None):
        """
        Searches for events for a single artist, with an optional date range,
        using this endpoint:

            https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0#/upcoming_artist_events/artistEvents

        Args:
            artistname: Artist name to search for
            date: Optional date string filter, can be a specific date in the
            format: "yyyy-mm-dd", a range "yyyy-mm-dd,yyyy-mm-dd", or can be a
            few keyword values like "upcoming" or "all"


        Returns:
            A list of event data, which could be empty, None if artist not
            found, raises `BandsintownInvalidDateFormatError` for bad `date`
            param, or raises `BandsintownError` for other unknown error

        Usage:
            client = Client(app_id=1234)
            client.artists_events('Bad Religion')
            client.artists_events('Bad Religion', date='2018-02-01,2018-02-28')
        """
        params = {}

        if date:
            params['date'] = date

        data = self.request('artists/%s/events' % quote(artistname), params)

        if 'errors' in data:
            if data['errors'][0] == 'Invalid date format':
                raise BandsintownInvalidDateFormatError(
                    'Invalid date parameter: "%s", must be in the format: "yyyy-mm-dd", or "yyyy-mm-dd,yyyy-mm-dd" for a range, or keywords "upcoming" or "all"' % date
                )
            elif data['errors'][0] == 'Unknown Artist':
                return None
            else:
                raise BandsintownError('Unknown error with request', data)

        return data
