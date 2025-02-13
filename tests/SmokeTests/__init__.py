import os
import unittest
import time
import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

SELENIUM_GRID_HOST = os.environ.get('SELENIUM_GRID_HOST', 'localhost')


class SmokeTests(unittest.TestCase):
    def smoke_test_container(self, port):
        max_attempts = 3
        sleep_interval = 3
        status_fetched = False
        status_json = None

        for _ in range(max_attempts):
            try:
                response = urlopen(f'http://{SELENIUM_GRID_HOST}:{port}/status')
                status_json = json.loads(response.read())
                self.assertTrue(
                    status_json['value']['ready'],
                    f"Container is not ready on port {port}",
                )
                status_fetched = True
            except Exception as e:
                time.sleep(sleep_interval)

        self.assertTrue(
            status_fetched, f"Container status was not fetched on port {port}"
        )
        self.assertTrue(
            status_json['value']['ready'], f"Container is not ready on port {port}"
        )


class GridTest(SmokeTests):
    def test_grid_is_up(self):
        self.smoke_test_container(4444)
