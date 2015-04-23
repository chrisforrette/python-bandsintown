import pytest

from bandsintown.client import Client, Artist, Event


# Artist

def test_get_artist_id_string():
    artist = Artist(client='')
    assert artist._get_artist_identifier('Bad Religion') == 'Bad%20Religion'


def test_get_artist_id_fbid():
    artist = Artist(client='')
    assert artist._get_artist_identifier(fbid=1234) == 'fbid_1234'


def test_get_artist_id_mbid():
    artist = Artist(client='')
    assert artist._get_artist_identifier(mbid=1234) == 'mbid_1234'
