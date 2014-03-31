from ica.tests import *

class TestStaticController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='static', action='index'))
        # Test response...
