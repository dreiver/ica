from ica.tests import *

class TestCommentsController(TestController):

    def test_index(self):
        response = self.app.get(url('api_comments'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_api_comments', format='xml'))

    def test_create(self):
        response = self.app.post(url('api_comments'))

    def test_new(self):
        response = self.app.get(url('api_new_comment'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_api_new_comment', format='xml'))

    def test_update(self):
        response = self.app.put(url('api_comment', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('api_comment', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('api_comment', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('api_comment', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('api_comment', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_api_comment', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('api_edit_comment', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_api_edit_comment', id=1, format='xml'))
