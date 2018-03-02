# Bandsintown Python Client

Simple Python client for version 3 of the [Bandsintown API](http://www.artists.bandsintown.com/bandsintown-api/).

See [the official API documentation for more details](https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0).

## Requirements

Python 2.x or 3.x

## Installation

```sh
pip install python-bandsintown
```

## Usage

### Instantiate client with your app id

Your app id can be anything, but usage requires written permission from Bandsintown, see here: http://www.artists.bandsintown.com/bandsintown-api/#1-pick-application-id

```python
from bandsintown import Client
client = Client('mybandapp')
```

### Find a single artist

Find a single artist by name:

```python
client.artists('Bad Religion')
```

See: https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0#/single_artist_information/artist

### Events

Get a single artist's events

```python

client.events('Bad Religion')

# Filter by date

client.events('Bad Religion', date='2015-08-30')

# ...or a date range

# Filter by date

client.events('Bad Religion', date='2015-08-30,2015-12-25')
```

### Search

Get a single artist's events with a few additional filter options: `location`, `radius`, and `date`

```python
client.search('Bad Religion', location='Portland,OR')

# Pass an optional radius (in miles)

client.search('Bad Religion', location='Portland,OR', radius=100)

```

### Recommended

Get a set of recommended events based on an artist with a few filters: `location`, `radius`, `date`
and `only_recs` (when set to `True`, only recommended shows will be returned, when `False`, the 
passed in artist's will be included as well)

```python
client.recommended('Bad Religion', location='Portland,OR')

# Only show recommendations

client.recommended('Bad Religion', location='Portland,OR', only_recs=True)
```
