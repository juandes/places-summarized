import elhood
import googlemaps


class Client(object):
    """
    Stuff
    """

    def __init__(self, key=None):
        """
        :param key: Maps API key.
        :type key: string
        """

        self.key = key
        self.gmaps_client = googlemaps.Client(key=key)

    def test(self, a=1):
        print(a)

    def places_nearby(self, location=None, radius=None, page_token=None):
        """
        Stuff

        :param location: The latitude/longitude value for which you wish to
                         obtain the closest, human-readable address.
        :type location: string, dict, list, or tuple
        """
        if not location and not page_token:
            raise ValueError(
                "either a location or page_token argument is required")

        return self.gmaps_client.places_nearby(location=location, radius=radius, page_token=page_token)

    def places_summary(self, location=None, radius=None, page_token=None):
        """
        Stuff

        :param location: The latitude/longitude value for which you wish to
                         obtain the closest, human-readable address.
        :type location: string, dict, list, or tuple
        """
        if not location and not page_token:
            raise ValueError(
                "either a location or page_token argument is required")

        result = self.gmaps_client.places_nearby(location=location, radius=radius, page_token=page_token)

        
