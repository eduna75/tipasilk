__author__ = 'justus'

from flask import Blueprint, request, g, redirect, url_for, abort, render_template

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


from flask.views import MethodView

from .models import Blog


class CRUDView(MethodView):

    list_template = 'admin/list_view.html'

    def __init__(self, model, endpoint, list_template=None):
        self.model = model
        self.endpoint = endpoint
        self.path = url_for('.%s' % self.endpoint)
        if list_template:
            self.list_template = list_template

    def get(self):
        obj = self.model.query.all()
        return render_template(list_template, obj=obj, path=self.path)


view = CRUDView.as_view('blog')

admin.add_url_rule('/blog/', view_func=view, methods=['GET', 'POST'])