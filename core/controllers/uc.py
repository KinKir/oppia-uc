import logging 


from core.controllers import base
from core.domain import config_domain
from core.domain import dependency_registry
from core.domain import email_manager
from core.domain import event_services
from core.domain import exp_domain 
from core.domain import exp_services
from core.domain import fs_domain
from core.domain import gadget_registry
from core.domain import interaction_registry
from core.domain import obj_services
from core.domain import rights_manager
from core.domain import rte_component_registry
from core.domain import stats_services
from core.domain import user_services
from core.domain import value_generators_domain
from core.platform import models
from core.controllers import ucnote

import urlparse
import feconf
import utils

current_user_services = models.Registry.import_current_user_services()
(user_models,) = models.Registry.import_models([models.NAMES.user])

class UcApiHandler(base.BaseHandler):
    def get(self):
        code = self.request.get('code')
        code = ucnote.uc_authcode(code,'DECODE')
        get = urlparse.parse_qs(code)
        action = get['action'][0]
        self.response.out.write(get)
        if action in ('test', 'deleteuser', 'renameuser', 'gettag', 'synlogin', 'synlogout', 'updatepw', 'updatebadwords', 'updatehosts', 'updateapps', 'updateclient', 'updatecredit', 'getcredit', 'getcreditsettings', 'updatecreditsettings', 'addfeed'):
            self.response.out.write(1)
        else:
            self.response.out.write(-1)


