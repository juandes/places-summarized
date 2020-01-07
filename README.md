# Places Summarized 

[![Build Status](https://travis-ci.com/juandes/places-summarized.svg?branch=master)](https://travis-ci.com/juandes/places-summarized) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![](logo.png)

Places Summarized is a wrapper around Google Maps' Places API that summarizes
the attributes of the locations nearby the specified coordinate.

## Installation
Install Places Summarized via pip using

`$ pip install places-summarized`

## Requirements
- A Google Maps API key.
- Python 3

## Usage

This example uses a Google Maps API key.

```python
import pprint
from places_summarized.client import Client

pp = pprint.PrettyPrinter(indent=4)

client = Client(key='your-key')
# Google Sydney offices
summary = client.places_summary(location=(-33.8670522, 151.1957362), radius=1000)
pp.pprint(summary.result())
# Print the ratings of the locations of type "point_of_interest."
# You can find the full list of types
# at: https://developers.google.com/places/web-service/supported_types
print(summary.ratings_by_type('point_of_interest'))
# Print the average price level of all the places
print(summary.average_price_level())

```

Or, you can test it without a key, using the `TestClient`.

```python
import pprint
from places_summarized.fake_client import FakeClient

pp = pprint.PrettyPrinter(indent=4)

fclient = FakeClient()
summary = fclient.places_summary()
pp.pprint(summary.result())

```

## Documentation

TO DO... :/ maybe you want to help?

## Acknowledgements
- "Pin" icon taken from [Freepik on Flaticon](https://www.flaticon.com/authors/freepik).
- "Barchat" icon taken from [Gregor Cresnar on Flaticon](https://www.flaticon.com/authors/gregor-cresnar).
