# Bandsintown Python Client

Simple Python client for the [Bandsintown API](http://www.bandsintown.com/api/overview) (v2).

Tested with Python 2.7 and Python 3.4

## Installation

```shell
pip install python-bandsintown
```

## Usage

```python

# Instantiate client with your app id (this can be anything)

from bandsintown.client import Client
client = Client('mybandapp')
```

### Get

Find a single artist

```python
# Find an artist by name

client.get('Bad Religion')

# Find an artist by Facebook page ID

client.get(fbid=168803467003)

# Find an artist by MusicBrainz ID

client.get(mbid='149e6720-4e4a-41a4-afca-6d29083fc091')
```

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
