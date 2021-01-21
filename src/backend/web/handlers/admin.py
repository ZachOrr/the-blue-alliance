import datetime

from firebase_admin import auth
from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from pyre_extensions import none_throws
from werkzeug.wrappers import Response

from backend.common.consts.account_permission import PERMISSIONS as ACCOUNT_PERMISSIONS
from backend.common.models.account import Account
from backend.web.decorators import require_admin
from backend.web.models.user import User


blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.before_request
# @require_admin
def before_request():
    """ Protect all of the admin endpoints. """
    pass


@blueprint.route("")
def index() -> str:
    return render_template("admin/empty.html")


@blueprint.route("users", defaults={"page_num": 0})
@blueprint.route("users/<int:page_num>")
def users(page_num: int) -> str:
    PAGE_SIZE = 1000

    num_users = Account.query().count()
    max_page = int(num_users / PAGE_SIZE)
    page_num = min(page_num, max_page)
    offset = PAGE_SIZE * page_num

    users = Account.query().order(Account.created).fetch(PAGE_SIZE, offset=offset)

    template_values = {
        "num_users": num_users,
        "users": users,
        "page_num": page_num,
        "page_labels": [p + 1 for p in range(max_page + 1)]
    }
    return render_template("admin/user_list.html", **template_values)


@blueprint.route("user/lookup", methods=["GET", "POST"])
def user_lookup() -> str:
    if request.method == "POST":
        user_email = request.form.get('email', None)
        if not user_email:
            abort(404)

        users = Account.query(Account.email == user_email).fetch(limit=1)
        if not users:
            abort(404)

        user = users[0]
        return redirect(url_for("admin.user", user_id=user.key.id()))

    return render_template("admin/user_lookup.html")


@blueprint.route("user/<user_id>")
def user(user_id: str) -> str:
    user = Account.get_by_id(user_id)
    if not user:
        abort(404)

    # Attempt to fetch using the Account ID which
    firebase_user = auth.get_user(user.key.id())
    if not firebase_user:
        firebase_user = auth.get_user_by_email(user.email)

    custom_claims = firebase_user.custom_claims if firebase_user.custom_claims else {}
    firebase_user_is_admin = User.claims_is_admin(custom_claims)

    template_values = {
        "user": user,
        "firebase_user": firebase_user,
        "firebase_user_is_admin": firebase_user_is_admin,
        "firebase_user_providers": [pd.provider_id for pd in firebase_user.provider_data],
        "permissions": ACCOUNT_PERMISSIONS
    }
    return render_template("admin/user_details.html", **template_values)


@blueprint.route("user/<user_id>/edit", methods=["GET", "POST"])
def user_edit(user_id: str) -> str:
    if request.method == "POST":
        user = Account.get_by_id(user_id)
        if not user:
            abort(404)

        user.display_name = request.form.get("display_name")
        user.shadow_banned = True if request.form.get("shadow_banned") else False
        user.permissions = []
        for enum in ACCOUNT_PERMISSIONS:
            permcheck = request.form.get("perm-" + str(enum))
            if permcheck:
                user.permissions.append(enum)
        user.put()

        return redirect(url_for("admin.user", user_id=user.key.id()))

    user = Account.get_by_id(user_id)
    if not user:
        abort(404)

    template_values = {
        "user": user,
        "permissions": ACCOUNT_PERMISSIONS
    }
    return render_template("admin/user_edit.html", **template_values)


# @blueprint.route("user/<user_id>/admin", methods=["POST"])
# def user_edit(user_id: str) -> str:
#     if request.method == "POST":
#         user = Account.get_by_id(user_id)
#         if not user:
#             abort(404)
#
#         user.display_name = request.form.get("display_name")
#         user.shadow_banned = True if request.form.get("shadow_banned") else False
#         user.permissions = []
#         for enum in ACCOUNT_PERMISSIONS:
#             permcheck = request.form.get("perm-" + str(enum))
#             if permcheck:
#                 user.permissions.append(enum)
#         user.put()
#
#         return redirect(url_for("admin.user", user_id=user.key.id()))
#
#     user = Account.get_by_id(user_id)
#     if not user:
#         abort(404)
#
#     template_values = {
#         "user": user,
#         "permissions": ACCOUNT_PERMISSIONS
#     }
#     return render_template("admin/user_edit.html", **template_values)


# import os
# import json
# import re
# import logging
# import datetime
# import tba_config
#
# from google.appengine.api import memcache
# from google.appengine.ext.webapp import template
#
# from controllers.base_controller import LoggedInHandler
# from database.database_query import DatabaseQuery
# from helpers.suggestions.suggestion_fetcher import SuggestionFetcher
# from models.account import Account
# from models.sitevar import Sitevar
# from models.suggestion import Suggestion
#
#
# class AdminMain(LoggedInHandler):
#     def get(self):
#         self._require_admin()
#
#         self.template_values['memcache_stats'] = memcache.get_stats()
#         self.template_values['databasequery_stats'] = {
#             'hits': sum(filter(None, [memcache.get(key) for key in DatabaseQuery.DATABASE_HITS_MEMCACHE_KEYS])),
#             'misses': sum(filter(None, [memcache.get(key) for key in DatabaseQuery.DATABASE_MISSES_MEMCACHE_KEYS]))
#         }
#
#         # Gets the 5 recently created users
#         users = Account.query().order(-Account.created).fetch(5)
#         self.template_values['users'] = users
#
#         self.template_values['suggestions_count'] = Suggestion.query().filter(
#             Suggestion.review_state == Suggestion.REVIEW_PENDING).count()
#
#         # Continuous deployment info
#         status_sitevar = Sitevar.get_by_id('apistatus')
#         self.template_values['contbuild_enabled'] = status_sitevar.contents.get('contbuild_enabled') if status_sitevar else None
#
#         # version info
#         try:
#             fname = os.path.join(os.path.dirname(__file__), '../../version_info.json')
#
#             with open(fname, 'r') as f:
#                 data = json.loads(f.read().replace('\r\n', '\n'))
#
#             self.template_values['git_branch_name'] = data['git_branch_name']
#             self.template_values['build_time'] = data['build_time']
#             self.template_values['build_number'] = data.get('build_number')
#
#             commit_parts = re.split("[\n]+", data['git_last_commit'])
#             self.template_values['commit_hash'] = commit_parts[0].split(" ")
#             self.template_values['commit_author'] = commit_parts[1]
#             self.template_values['commit_date'] = commit_parts[2]
#             self.template_values['commit_msg'] = commit_parts[3]
#
#         except Exception, e:
#             logging.warning("version_info.json parsing failed: %s" % e)
#             pass
#
#         self.template_values['debug'] = tba_config.DEBUG
#
#         path = os.path.join(os.path.dirname(__file__), '../../templates/admin/index.html')
#         self.response.out.write(template.render(path, self.template_values))
#
#
# class AdminDebugHandler(LoggedInHandler):
#     def get(self):
#         self._require_admin()
#         self.template_values['cur_year'] = datetime.datetime.now().year
#         self.template_values['years'] = range(datetime.datetime.now().year, 2005, -1)
#         path = os.path.join(os.path.dirname(__file__), '../../templates/admin/debug.html')
#         self.response.out.write(template.render(path, self.template_values))
#
#
# class AdminTasksHandler(LoggedInHandler):
#     def get(self):
#         self._require_admin()
#         path = os.path.join(os.path.dirname(__file__), '../../templates/admin/tasks.html')
#         self.response.out.write(template.render(path, self.template_values))

# class AdminUserPermissionsList(LoggedInHandler):
#     """
#     List all Users with Permissions.
#     """
#     def get(self):
#         self._require_admin()
#         users = Account.query(Account.permissions != None).fetch()
#
#         self.template_values.update({
#             "users": users,
#             "permissions": AccountPermissions.permissions,
#         })
#
#         path = os.path.join(os.path.dirname(__file__), '../../templates/admin/user_permissions_list.html')
#         self.response.out.write(template.render(path, self.template_values))
#
#
# class AdminUserEdit(LoggedInHandler):
#     """
#     Edit a User.
#     """
#     def get(self, user_id):
#         self._require_admin()
#         user = Account.get_by_id(user_id)
#         self.template_values.update({
#             "user": user,
#             "permissions": AccountPermissions.permissions
#         })
#
#         path = os.path.join(os.path.dirname(__file__), '../../templates/admin/user_edit.html')
#         self.response.out.write(template.render(path, self.template_values))
#
#     def post(self, user_id):
#         self._require_admin()
#         user = Account.get_by_id(user_id)
#
#         user.display_name = self.request.get("display_name")
#         user.shadow_banned = True if self.request.get("shadow_banned") else False
#         user.permissions = []
#         for enum in AccountPermissions.permissions:
#             permcheck = self.request.get("perm-" + str(enum))
#             if permcheck:
#                 user.permissions.append(enum)
#         user.put()
#
#         self.redirect("/admin/user/" + user_id)
