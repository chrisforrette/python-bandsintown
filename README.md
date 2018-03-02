# Bandsintown Python Client

Simple Python client for version 3 of the [Bandsintown API](http://www.artists.bandsintown.com/bandsintown-api/).

See [the official API documentation for more details](https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0).

## Requirements

Python 2.x or 3.x

## Installation

```sh
pip install python-bandsintown
```

## Instantiation

Your app id can be anything, but usage requires written permission from Bandsintown, see here: http://www.artists.bandsintown.com/bandsintown-api/#1-pick-application-id

```python
from bandsintown import Client
client = Client('mybandapp')
```

## API

### `artists`

Find a single artist by name:

```python
client.artists('Bad Religion')
```

See the official API documentation for this endpoint here: https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0#/single_artist_information/artist

### `artist_events`

Get a single artist's events, with an optional `date` parameter that can be a single date in the format: `yyyy-mm-dd`, a date range in the format: `yyyy-mm-dd,yyyy-mm-dd`, or a keyword value of `all` or `upcoming`.

```python
client.artist_events('Bad Religion')
```

#### Fetch events for a specific date

```python
client.artists_events('Bad Religion', date='2015-08-30')
```

#### Fetch events within a date range

```python
client.artists_events('Bad Religion', date='2015-08-30,2015-12-25')
```

See the official API documentation for this endpoint here: https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0#/upcoming_artist_events

## Errors

### `BandsintownError`

This serves as the base class for other exceptions, so can be used to catch all errors from this client. Currently it's only raised in the `artists_events` in the event of an unknown error.

### `BandsintownInvalidAppIdError`

This error is raised whenever a request is made with an invalid app id specified at client instantiation.

### `BandsintownInvalidDateFormatError`

This error is raised by the `artists_events` method when a `date` parameter is passed in an invalid format.
