__author__ = 'justus'

from flask import Blueprint, request, g, redirect, url_for, abort, render_template

admin = Blueprint('admin', __name__, template_folder='admin/templates', url_prefix='/admin')


from flask.views import MethodView

from models import Blog


class CRUDView(MethodView):

    def __init__(self, list_template=None):
        self.list_template = '/admin/listview.html'
        if list_template:
            self.list_template = list_template

    def get(self):
        obj = 'this and that'
        return render_template(self.list_template, obj=obj)


admin.add_url_rule('/blog/', view_func=CRUDView.as_view('blog'), methods=['GET', 'POST'])