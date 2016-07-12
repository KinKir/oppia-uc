import urlparse
import xml.etree.cElementTree as ET
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
        get = dict(urlparse.parse_qsl(code))
        action = get['action']
        post = self.request.body
        post = self.xml_unserilizae(post)
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

    def xml_unserilizae(self, xml):
        xmlnode = ET.fromstring(xml)
        root = xmlnode.getroot()
        data = {}
        for child in root:
            data[child.attrib['id']] = child.text
            if subchild in child:
                childdata = {}
                for subchild in child:
                    childdata[subchild.attrib['id']] = subchild.text
                data[child.attrib['id']] = childdata
        return data

    def test(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def deleteuser(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def renameuser(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def gettag(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def synlogin(self, get, post):
        get = get + post
        return API_RETURN_SUCCEED

    def synlogout(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatepw(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatebadwords(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatehosts(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updateapps(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updateclient(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatecredit(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def getcredit(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def getcreditsettings(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatecreditsettings(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def addfeed(self, get, post):
        get = get + post
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED
