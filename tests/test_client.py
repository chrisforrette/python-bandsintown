import pytest

import mock

from bandsintown import Client


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


# Endpoint methods

def test_artists_get_artist_id_string():
    client = Client('epitaph')
    assert client._get_artist_identifier('Bad Religion') == 'Bad%20Religion'


def test_artists_get_artist_id_fbid():
    client = Client('epitaph')
    assert client._get_artist_identifier(fbid=1234) == 'fbid_1234'


def test_artists_get_artist_id_mbid():
    client = Client('epitaph')
    assert client._get_artist_identifier(mbid=1234) == 'mbid_1234'


@mock.patch.object(Client, 'request')
def test_artists_events(fake_request):
    client = Client('epitaph')
    client.events('Bad Religion')
    fake_request.assert_called_with('artists/Bad%20Religion/events', {})


@mock.patch.object(Client, 'request')
def test_artists_events_with_date(fake_request):
    client = Client('epitaph')
    client.events('Bad Religion', date='2015-01-01')
    fake_request.assert_called_with('artists/Bad%20Religion/events', {'date': '2015-01-01'})


@mock.patch.object(Client, 'request')
def test_artists_search(fake_request):
    client = Client('epitaph')
    client.search('Bad Religion', location='Portland,OR')
    fake_request.assert_called_with('artists/Bad%20Religion/events/search', {'location': 'Portland,OR'})


@mock.patch.object(Client, 'request')
def test_artists_search_with_radius(fake_request):
    client = Client('epitaph')
    client.search('Bad Religion', location='Portland,OR', radius=100)
    fake_request.assert_called_with('artists/Bad%20Religion/events/search', {'location': 'Portland,OR', 'radius': 100})


@mock.patch.object(Client, 'request')
def test_artists_search_with_date(fake_request):
    client = Client('epitaph')
    client.search('Bad Religion', location='Portland,OR', radius=100, date='2015-02-03')
    fake_request.assert_called_with('artists/Bad%20Religion/events/search', {'location': 'Portland,OR', 'radius': 100, 'date': '2015-02-03'})


@mock.patch.object(Client, 'request')
def test_artists_recommended(fake_request):
    client = Client('epitaph')
    client.recommended('Bad Religion', location='Portland,OR')
    fake_request.assert_called_with('artists/Bad%20Religion/events/recommended', {'location': 'Portland,OR'})


@mock.patch.object(Client, 'request')
def test_artists_recommended_with_radius(fake_request):
    client = Client('epitaph')
    client.recommended('Bad Religion', location='Portland,OR', radius=125)
    fake_request.assert_called_with('artists/Bad%20Religion/events/recommended', {'location': 'Portland,OR', 'radius': 125})


@mock.patch.object(Client, 'request')
def test_artists_recommended_with_date(fake_request):
    client = Client('epitaph')
    client.recommended('Bad Religion', location='Portland,OR', radius=125, date='2015-10-10')
    fake_request.assert_called_with('artists/Bad%20Religion/events/recommended', {'location': 'Portland,OR', 'radius': 125, 'date': '2015-10-10'})


@mock.patch.object(Client, 'request')
def test_artists_recommended_with_only_recs(fake_request):
    client = Client('epitaph')
    client.recommended('Bad Religion', location='Portland,OR', radius=125, date='2015-10-10', only_recs=True)
    fake_request.assert_called_with('artists/Bad%20Religion/events/recommended', {'location': 'Portland,OR', 'radius': 125, 'date': '2015-10-10', 'only_recs': 'true'})


@mock.patch.object(Client, 'request')
def test_artists_recommended_with_only_recs_false(fake_request):
    client = Client('epitaph')
    client.recommended('Bad Religion', location='Portland,OR', radius=125, date='2015-10-10', only_recs=False)
    fake_request.assert_called_with('artists/Bad%20Religion/events/recommended', {'location': 'Portland,OR', 'radius': 125, 'date': '2015-10-10', 'only_recs': 'false'})
