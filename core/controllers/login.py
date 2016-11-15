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
import re
from core.controllers import base
from core.controllers import ucnote
from core.controllers import uc
from core.domain import user_services

from core.platform import models

current_user_services = models.Registry.import_current_user_services()


class LoginHandler(base.BaseHandler):
    REQUIRE_PAYLOAD_CSRF_CHECK = False
    REDIRECT_UNFINISHED_SIGNUPS = False

    def get(self):
        login_url = '/splash'
        continue_url = self.request.get('return_url') or login_url
        self.values.update({'return_url':continue_url})
        self.render_template('login.html')

    def post(self):
        username = self.payload.get('username')
        email = ''
        login_url = '/splash'
        continue_url = self.payload.get('return_url')
        redirect_url = continue_url or login_url
        if isinstance(redirect_url, unicode):
            redirect_url = redirect_url.encode('ascii')
        password = self.payload.get('password')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            uid = uc.create_userid_from_email(username)
            email = username
            username = user_services.get_username(uid)
        else:
            email = user_services.get_user_id_from_username(username)
            uid = uc.create_userid_from_email(username)
        if user_services.is_user_registered(uid) is False:
            self.values.update({
                'res': 'false', 'msg': '未找到用户信息'})
            self.render_json(self.values)
            return
        else:
            logRes = ucnote.uc_user_login(username, password)
            logResObj = ucnote.xml_unserilize(logRes)
            msg = '登录成功'
            success = 'true'
            if logResObj['0'] == '-1':
                msg = '用户不存在，或者被删除'
                success = 'false'
            elif logResObj['0'] == '-2':
                msg = '密码错'
                success = 'false'
            elif logResObj['0'] == '-3':
                msg = '安全提问错'
                success = 'false'
            else:
                success = 'true'
                self.response.headers['Set-Cookie'] = \
                    uc.set_user_info_cookie(email, username.lower() == 'admin')
                msg = ucnote.uc_user_synlogin(int(logResObj['0']))
                # self.response.status = 302
                self.response.status_message = 'Redirecting to continue URL'
                msg += '<script>window.location=\'%s\'</script>' % redirect_url
            self.values.update(
                {'res': success, \
                 'msg': msg})
            self.render_json(self.values)
