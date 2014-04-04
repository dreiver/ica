import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController
from ica.lib.api.util import api, response_error

log = logging.getLogger(__name__)

class CommentsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('comment', 'comments', controller='api/comments', 
    #         path_prefix='/api', name_prefix='api_')

    @api
    def index(self, format='json'):
        """GET /api/comments: All items in the collection"""
        data = { 'label': '', 'data': [] }
        return data

    def create(self, token=True):
        """POST /api/comments: Create a new item"""
        # url('api_comments')

    @api
    def new(self, format='json'):
        """GET /api/comments/new: Form to create a new item"""
        # url('api_new_comment')

    def update(self, id):
        """PUT /api/comments/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('api_comment', id=ID),
        #           method='put')
        # url('api_comment', id=ID)

    def delete(self, id):
        """DELETE /api/comments/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('api_comment', id=ID),
        #           method='delete')
        # url('api_comment', id=ID)

    @api
    def show(self, id, format='json'):
        """GET /api/comments/id: Show a specific item"""
        # url('api_comment', id=ID)

    @api
    def edit(self, id, format='json'):
        """GET /api/comments/id/edit: Form to edit an existing item"""
        # url('api_edit_comment', id=ID)
