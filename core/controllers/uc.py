

import urlparse
from core.controllers import base
from core.platform import models
from core.controllers import ucnote


current_user_services = models.Registry.import_current_user_services()
(user_models,) = models.Registry.import_models([models.NAMES.user])

class UcApiHandler(base.BaseHandler):
    def get(self):
        code = self.request.get('code')
        code = ucnote.uc_authcode(code, 'DECODE')
        get = urlparse.parse_qs(code)
        action = get['action'][0]
        if action in ('test', 'deleteuser', 'renameuser', 'gettag', 'synlogin', 'synlogout', 'updatepw',
                 'updatebadwords', 'updatehosts', 
                 'updateapps', 'updateclient', 
                 'updatecredit', 'getcredit',
                 'getcreditsettings', 'updatecreditsettings', 
                 'addfeed'):
            self.response.out.write(1)
        else:
            self.response.out.write(-1)


