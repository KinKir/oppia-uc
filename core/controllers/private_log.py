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

import jinja2
from core.controllers import base
from core.controllers import editor
from core.domain import privatelog_services
from core.domain import user_services
from core.domain import config_domain
import feconf
import utils


class PrivateLogListHandler(base.BaseHandler):
    """
    处理个人日志请求列表
    """
    PAGE_NAME_FOR_CSRF = 'editor'

    def get(self):
        self.values.update({
            'logs': [t.to_dict() for t in \
                     privatelog_services. \
                         get_all_privatelog(self.user_id)]})
        self.render_json(self.values)


class CreateLogCategoryHandler(base.BaseHandler):
    PAGE_NAME_FOR_CSRF = 'editor'

    def get(self):
        self.render_json(self.values)

    def post(self):
        name = self.payload.get('name')
        privatelog_services.create_category(
            self.user_id, name)
        self.render_json(self.values)


class CreatePrivateLogHandler(base.BaseHandler):
    PAGE_NAME_FOR_CSRF = 'editor'

    def get(self, log_id):  # pylint: disable=unused-argument
        if log_id is not None and log_id != '0':
            self.values.update(
                privatelog_services.get_privatelog(log_id).to_dict())
        self.render_json(self.values)

    @base.require_user
    def post(self, log_id):  # pylint: disable=unused-argument
        text = self.payload.get('newContent')
        category = self.payload.get('newCategory')
        # 创建日志分类，如果分类已经存在，则不创建，直接返回现有分类
        obj_category = privatelog_services.try_create_category(
            self.user_id, category)
        title = self.payload.get('newTitle')
        privatelog_services.create_private_log(
            self.user_id, obj_category.id, title, text)
        self.render_json(self.values)


class PrivateLogPage(base.BaseHandler):
    PAGE_NAME_FOR_CSRF = 'editor'

    def get(self):
        if self.username in config_domain.BANNED_USERNAMES.value:
            raise self.UnauthorizedUserException("")
        elif user_services.has_fully_registered(self.user_id):
            self.values.update({
                'meta_description': '',
                'nav_mode': feconf.NAV_MODE_DASHBOARD,
                'value_generators_js': jinja2.utils.Markup(
                    editor.get_value_generators_js()),
            })
            self.render_template(
                'privatelog/log_list.html',
                redirect_url_on_logout='/')
        else:
            self.redirect(utils.set_url_query_parameter(
                feconf.SIGNUP_URL, 'return_url', '/private_log'))
