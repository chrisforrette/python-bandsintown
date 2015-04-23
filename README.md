# Bandsintown Python Client

Python bindings for the [Bandsintown API](http://www.bandsintown.com/api/overview) (v2)


## Usage

### Artists

#### Get

```python
Artist.get(name='Bad Religion')

Artist.get(mbid=123)

Artist.get(fbid=123)
```

#### Events

```python
# From an artist result

events = []
artists = Artist.get(name='Bad Religion')

for artist in artists:
  if artist.upcoming_events_count > 0:
    artist_events = artist.events()

# With no artist



```