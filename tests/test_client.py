from unittest import TestCase

import mock

from bandsintown import Client, BandsintownInvalidAppIdError, BandsintownInvalidDateFormatError


# Basic assertions


class BaseTestCase(TestCase):
    def test_init_stores_properties(self):
        app_id = 1234
        client = Client(app_id)

        self.assertEqual(client.api_base_url, 'https://rest.bandsintown.com')
        self.assertEqual(client.app_id, app_id)
        self.assertEqual(client.default_params, {'app_id': app_id})


@mock.patch('requests.get')
class RequestTestCase(TestCase):
    def test_builds_and_executes_request(self, mock_requests_get):
        mock_result = {'name': 'Bad Religion'}
        mock_response = mock.MagicMock()
        mock_response.json.return_value = mock_result
        mock_requests_get.return_value = mock_response

        app_id = 5678
        client = Client(app_id)
        result = client.request('things')
        url = client.api_base_url + '/things'
        mock_requests_get.assert_called_with(
            url,
            headers={'Accept': 'application/json'},
            params=client.default_params
        )
        self.assertEqual(mock_result, result)

    def test_merges_passed_in_params(self, mock_requests_get):
        app_id = 5678
        date = '2018-01-01'
        client = Client(app_id)
        client.request('more/things', {'date': date})
        url = client.api_base_url + '/more/things'
        mock_requests_get.assert_called_with(
            url,
            headers={'Accept': 'application/json'},
            params={
                'app_id': app_id,
                'date': date
            }
        )

    def test_raises_error_for_bad_api_key(self, mock_requests_get):
        mock_result = {'message': 'Missing required request parameters: [app_id]'}
        mock_response = mock.MagicMock()
        mock_response.json.return_value = mock_result
        mock_requests_get.return_value = mock_response

        client = Client('')

        with self.assertRaises(BandsintownInvalidAppIdError):
            client.request('stuff')


@mock.patch.object(Client, 'request')
class ArtistsTestCase(TestCase):
    def test_requests_artist(self, mock_request):
        artist = 'Bad Religion'
        data = {
            'facebook_page_url': 'https://www.facebook.com/badreligion',
            'upcoming_event_count': 8,
            'name': 'Bad Religion',
            'url': 'https://www.bandsintown.com/a/658?came_from=267&app_id=bandsintown-test-client',
            'tracker_count': 476952,
            'mbid': '149e6720-4e4a-41a4-afca-6d29083fc091',
            'image_url': 'https://s3.amazonaws.com/bit-photos/large/6277078.jpeg',
            'thumb_url': 'https://s3.amazonaws.com/bit-photos/thumb/6277078.jpeg',
            'id': '658'
        }
        mock_request.return_value = data

        client = Client(1234)
        result = client.artists(artist)

        self.assertEqual(result, data)
        mock_request.assert_called_once_with('artists/Bad%20Religion')

    def test_returns_none_for_artist_not_found(self, mock_request):
        mock_request.side_effect = ValueError('No JSON object could be decoded')
        client = Client(1234)
        self.assertIsNone(client.artists('foo'))


@mock.patch.object(Client, 'request')
class EventsTestCase(TestCase):
    def test_requests_artist_events(self, mock_requests_get):
        data = [
            {
                'id': '20590797',
                'datetime': '2018-05-04T13:00:00'
            },
            {
                'id': '21752009',
                'datetime': '2018-05-05T19:00:00'
            }
        ]
        mock_requests_get.return_value = data

        client = Client('my-app-id')
        artist = 'Every Time I Die'
        result = client.artists_events(artist)

        mock_requests_get.assert_called_with('artists/Every%20Time%20I%20Die/events', {})
        self.assertEqual(result, data)

    def test_takes_date_param(self, mock_requests_get):
        data = [{'id': '1234'}]
        mock_requests_get.return_value = data

        client = Client('my-app-id')
        artist = 'Every Time I Die'
        date = '2018-01-15,2018-02-15'
        result = client.artists_events(artist, date)

        mock_requests_get.assert_called_with(
            'artists/Every%20Time%20I%20Die/events',
            {'date': date}
        )
        self.assertEqual(result, data)

    def test_returns_none_when_artist_not_found(self, mock_requests_get):
        mock_requests_get.return_value = {'errors': ['Unknown Artist']}
        client = Client('my-app-id')
        self.assertIsNone(client.artists_events('foo'))

    def test_returns_none_when_no_events_found(self, mock_requests_get):
        mock_requests_get.return_value = []
        client = Client('my-app-id')
        self.assertEqual(client.artists_events('bar'), [])

    def test_raises_error_for_invalid_date(self, mock_requests_get):
        mock_requests_get.return_value = {'errors': ['Invalid date format']}
        client = Client('my-app-id')
        with self.assertRaises(BandsintownInvalidDateFormatError):
            client.artists_events('bar', 'florp')
