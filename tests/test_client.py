import pytest

import mock

from bandsintown.client import Client, Artist


# Client

def test_client_init_stores_properties():
    app_id = 1234
    client = Client(app_id=app_id)

    assert client.app_id == app_id
    assert client.params['app_id'] == app_id
    assert client.params['api_version'] == client.API_VERSION


def test_request_generates_url():
    with mock.patch('requests.get') as fake_requests_get:
        client = Client(app_id=5678)
        client.request('thing')
        url = client.API_BASE_URL + '/thing.json'
        fake_requests_get.assert_called_with(url, params=client.params)


def test_request_passes_params():
    with mock.patch('requests.get') as fake_requests_get:
        client = Client(app_id=5678)
        client.request('thing', {'hello': 'there'})
        url = client.API_BASE_URL + '/thing.json'
        params = client.params.copy()
        params['hello'] = 'there'
        fake_requests_get.assert_called_with(url, params=params)


# Artist

def test_artist_get_artist_id_string():
    artist = Artist(client='')
    assert artist._get_artist_identifier('Bad Religion') == 'Bad%20Religion'


def test_artist_get_artist_id_fbid():
    artist = Artist(client='')
    assert artist._get_artist_identifier(fbid=1234) == 'fbid_1234'


def test_artist_get_artist_id_mbid():
    artist = Artist(client='')
    assert artist._get_artist_identifier(mbid=1234) == 'mbid_1234'
