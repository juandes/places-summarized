import unittest

from places_summarized.fake_client import FakeClient


class TestSummary(unittest.TestCase):
    def setUp(self):
        self.fclient = FakeClient()
        self.summary = self.fclient.places_summary()

    def test_average_price_level(self):
        r = self.summary.result()
        self.assertEqual(r['average_price_level'], 2.5)

    def test_average_rating(self):
        self.assertAlmostEqual(self.summary.average_rating_by_type('restaurant'), 3.93, 2)


if __name__ == '__main__':
    unittest.main()
