# Some of the param, type descriptions and error messages are taken from
# the the Google Maps API for Python source code:
# https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/places.py
# This was done in good faith to be consistent with the Maps API.

import places_summarized
import googlemaps
from statistics import mean
from places_summarized.errors import NoPlacesError


class Client(object):
    """
    Connects to Google Maps, does requests to Google Places API and performs the summary
    """

    def __init__(self, key=None):
        """
        :param key: Maps API key.
        :type key: string
        """

        self.key = key
        self.gmaps_client = googlemaps.Client(key=key)
        self.result = None
        self.location = None

    def places_nearby(self, location=None, radius=None, page_token=None):
        """
        Get the places near the location given.

        :param location: The latitude/longitude value for which you wish to
                         obtain the nearby locations.
        :type location: string, dict, list, or tuple

        :param radius: Distance (in meters) from the location.
        :type radius: int

        :param page_token: Token from a previous search that when provided will
        returns the next page of results for the same search.
        """
        if not location and not page_token:
            raise ValueError(
                "either a location or page_token argument is required")

        return self.gmaps_client.places_nearby(location=location,
                                               radius=radius,
                                               page_token=page_token)

    def places_summary(self, location=None, radius=None, page_token=None):
        """
        Summarizes the ...

        :param location: The latitude/longitude value for which you wish to
                         obtain a summary of the nearby locations.
        :type location: string, dict, list, or tuple
        """
        if not location and not page_token:
            raise ValueError(
                "either a location or page_token argument is required")

        # This is done to avoid calling the API when the location is the same
        # and there's a result already.
        if (self.location == location and self.result is not None):
            return self._make_summary()

        self.location = location
        result = self.places_nearby(
            location=location, radius=radius, page_token=page_token)

        locations = result.get('results', [])
        num_locations = len(locations)

        if num_locations == 0:
            # Set result to None even if there was already one.
            self.result = None
            raise NoPlacesError(self.location)

        self.result = result
        self.num_locations = num_locations
        self.ratings = []
        self.user_ratings_totals = []
        self.price_levels = []
        self.location_types = {}
        self.next_page_token = result.get('next_page_token', '')

        for location in locations:
            _append_if_key_exists(self.ratings, location, 'rating')
            _append_if_key_exists(self.user_ratings_totals,
                                  location, 'user_ratings_total')
            _append_if_key_exists(self.price_levels, location, 'price_level')

            for location_type in location.get('types', []):
                # Check if location_types has a type of that location.
                # If it does, increase it counter, if it doesnt, a new
                # key is created with value 1.
                self.location_types[location_type] = self.location_types.get(
                    location_type, 0) + 1

        return self._make_summary()

    def ratings_by_type(self, location_type):
        return self._get_stat_by_type('rating', location_type)

    def average_rating_by_type(self, location_type):
        if self.result is None:
            raise NoPlacesError(self.location)

        ratings = self.ratings_by_type(location_type)
        return mean(ratings)

    def _get_stat_by_type(self, stat, location_type):
        if self.result is None:
            raise NoPlacesError(self.location)

        values = []
        locations = self.result.get('results', [])
        for location in locations:
            if location_type in location.get('types', []):
                _append_if_key_exists(values, location, stat)

        return values

    def _make_summary(self):
        summary = {
            'ratings': self.ratings,
            'user_ratings_total': self.user_ratings_totals,
            'price_levels': self.price_levels,
            'location_types': self.location_types
        }

        _add_average_if_values(self.ratings, summary,
                               'average_rating')
        _add_average_if_values(self.user_ratings_totals, summary,
                               'average_user_ratings_total')
        _add_average_if_values(self.price_levels, summary,
                               'average_price_level')

        return summary


def _append_if_key_exists(l, d, key):
    if key in d.keys():
        l.append(d[key])


def _add_average_if_values(l, d, key):
    if l is None or len(l) == 0:
        return

    d[key] = mean(l)
