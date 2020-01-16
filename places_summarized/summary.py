# Some of the param, type descriptions and error messages are taken from
# the the Google Maps API for Python source code:
# https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/places.py
# This was done in good faith to be consistent with the Maps API.

import places_summarized
from places_summarized.errors import NoPlacesError
from statistics import StatisticsError, mean


class Summary(object):
    """
    Performs the summary using Google's nearby places data.
    """

    def __init__(self, result, location):
        self.nearby_results = result
        self.location = location
        self.next_page_token = result.get('next_page_token', None)
        self.num_locations = 0
        self.ratings = []
        self.user_ratings_totals = []
        self.price_levels = []
        self.location_types = {}

    def result(self):
        """
        Returns the summary
        """
        return self._summary

    def ratings_by_type(self, location_type):
        """
        Returns the ratings of the locations of the given type

        :param type: Location type, e.g., atm, park, or restaurant.
        You can find the full list at:
        https://developers.google.com/places/web-service/supported_types
        :type location_type: string
        """
        return self._get_stat_by_type('rating', location_type)

    def average_rating_by_type(self, location_type):
        """
        Calculates the average rating of the locations of the given type

        :param type: Location type, e.g., atm, park, or restaurant.
        You can find the full list at:
        https://developers.google.com/places/web-service/supported_types
        :type location_type: string
        """
        if self.nearby_results is None:
            raise NoPlacesError(self.location)

        ratings = self.ratings_by_type(location_type)
        try:
            return mean(ratings)
        except StatisticsError:
            print("No ratings found.")

    def average_price_level(self):
        try:
            return mean(self.price_levels)
        except StatisticsError:
            print("No ratings found.")

    def _make_summary(self):
        locations = self.nearby_results.get('results', [])
        num_locations = len(locations)

        if num_locations == 0:
            raise NoPlacesError(self.location)

        self.num_locations += num_locations

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

        self._summary = summary

    def _add_more_results(self, result):
        self.nearby_results = result
        self.next_page_token = result.get('next_page_token', None)
        self._make_summary()

    def _get_stat_by_type(self, stat, location_type):
        if self.nearby_results is None:
            raise NoPlacesError(self.location)

        values = []
        locations = self.nearby_results.get('results', [])
        for location in locations:
            if location_type in location.get('types', []):
                _append_if_key_exists(values, location, stat)

        return values


def _append_if_key_exists(l, d, key):
    if key in d.keys():
        l.append(d[key])


def _add_average_if_values(l, d, key):
    if l is None or len(l) == 0:
        return

    d[key] = mean(l)
