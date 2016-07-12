

import urlparse
from core.controllers import base
from core.platform import models
from core.controllers import ucnote

API_RETURN_SUCCEED = '1'
API_RETURN_FAILED = '-1'
API_RETURN_FORBIDDEN = '1'
API_SYNLOGIN = 1

current_user_services = models.Registry.import_current_user_services()
(user_models,) = models.Registry.import_models([models.NAMES.user])


class UcApiHandler(base.BaseHandler):
    def get(self):
        code = self.request.get('code')
        code = ucnote.uc_authcode(code, 'DECODE')
        get = urlparse.parse_qs(code)
        action = get['action'][0]
        post = self.request.body

        if action in ('test', 'deleteuser', 'renameuser', 'gettag',
                      'synlogin', 'synlogout', 'updatepw',
                      'updatebadwords', 'updatehosts',
                      'updateapps', 'updateclient',
                      'updatecredit', 'getcredit',
                      'getcreditsettings', 'updatecreditsettings',
                      'addfeed'):
            result = getattr(self, action)(get, post)
            self.response.out.write(result)
        else:
            self.response.out.write(-1)

    def test(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED
    def deleteuser(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def synlogout(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED
