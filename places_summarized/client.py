# Some of the param, type descriptions and error messages are taken from
# the the Google Maps API for Python source code:
# https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/places.py
# This was done in good faith to be consistent with the Maps API.

import json
import logging
import os

import googlemaps
import places_summarized
from places_summarized.summary import Summary


class Client(object):
    """
    Connects to Google Maps, does requests to Google Places API.
    """

    def __init__(self, key=None):
        """
        :param key: Maps API key.
        :type key: string
        """

        self.key = key
        self.gmaps_client = googlemaps.Client(key=key)

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
        Get the places near the location given, and compute it summary.

        :param location: The latitude/longitude value for which you wish to
                         obtain a summary of the nearby locations.
        :type location: string, dict, list, or tuple

        :param radius: Distance (in meters) from the location.
        :type radius: int

        :param page_token: Token from a previous search that when provided will
        returns the next page of results for the same search.

        :return: A Summary object.
        :rtype: places_summarized.summary.Summary
        """
        if not location and not page_token:
            raise ValueError(
                "either a location or page_token argument is required")

        result = self.places_nearby(
            location=location, radius=radius, page_token=page_token)

        summary = Summary(result, location)
        summary._make_summary()
        return summary

    def get_more_results(self, summary):
        if summary.next_page_token is None:
            logging.warning("No more results.")
            return

        result = self.places_nearby(
                    page_token=summary.next_page_token)
        summary._add_more_results(result)
