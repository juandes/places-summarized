import json
import os

from places_summarized.client import Client
from places_summarized.summary import Summary


class FakeClient(Client):
    """
    Client used for testing purposes. Loads a local dataset containing
    the locations from a locality from Sydney.
    """

    def __init__(self, key=None):
        pass

    def places_nearby(self, location=None, radius=None, page_token=None):
        print("Method not available in FakeClient.")

    def get_more_results(self, summary):
        print("Method not available in FakeClient.")

    def places_summary(self):
        """
        Computes the summary of a vecinity loaded from a local file.
        Use for testing purposes.
        """

        with open(os.path.join(os.path.dirname(__file__), 'data/sydney.json')) as json_file:
            data = json.load(json_file)

        summary = Summary(data, "Test Location")
        summary._make_summary()
        return summary
