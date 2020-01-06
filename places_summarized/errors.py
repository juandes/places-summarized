import places_summarized


class NoPlacesError(Exception):
    def __init__(self, location):
        self.location = location

    def __str__(self):
        return "No places found for location {}".format(self.location)
