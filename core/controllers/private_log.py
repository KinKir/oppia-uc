# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for the feedback thread page."""

# import json

from core.controllers import base
from core.domain import privatelog_services
from core.domain import user_services
from core.domain import config_domain
import feconf
import utils


class PrivateLogListHandler(base.BaseHandler):
    """
    处理个人日志请求列表
    """
    def get(self):
        self.values.update({
            'logs': [t.to_dict() for t in \
                privatelog_services.\
                     get_all_privatelog(self.user_id)]})
        self.render_json(self.values)


class CreateLogCategoryHandler(base.BaseHandler):
    def get(self):
        self.render_json(self.values)

    def post(self):
        privatelog_services.create_category(
            self.user_id, 'name')
        self.render_json(self.values)


class CreatePrivateLogHandler(base.BaseHandler):

    def get(self, log_id):# pylint: disable=unused-argument
        self.render_json(self.values)

    def post(self, log_id):# pylint: disable=unused-argument
        text = "test"
        title = 'title'
        privatelog_services.create_private_log(
            self.user_id, 1, title, text)
        self.render_json(self.values)

class PrivateLogPage(base.BaseHandler):
    def get(self):
        if self.username in config_domain.BANNED_USERNAMES.value:
            raise self.UnauthorizedUserException("")
        elif user_services.has_fully_registered(self.user_id):
            self.values.update({
                'meta_description':'',
                'nav_mode':feconf.NAV_MODE_DASHBOARD,
            })
            self.render_template(
                'privatelog/log_list.html',
                redirect_url_on_logout='/')
        else:
            self.redirect(utils.set_url_query_parameter(
                feconf.SIGNUP_URL, 'return_url', '/private_log'))


