from ica.tests import *

class TestAccessController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='access', action='index'))
        # Test response...
