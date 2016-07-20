import Cookie
import hashlib
import logging
import urlparse
import xml.etree.cElementTree as ET
from core.controllers import base
from core.platform import models
from core.controllers import ucnote
from core.domain import user_services
from core.domain import email_manager
import utils
import feconf

API_RETURN_SUCCEED = '1'
API_RETURN_FAILED = '-1'
API_RETURN_FORBIDDEN = '1'
API_SYNLOGIN = 1

# Name of the cookie that stores the user info.
_COOKIE_NAME = 'dev_appserver_login'

# (email_models,) = models.Registry.import_models([models.NAMES.email])
# email_services = models.Registry.import_email_services()
current_user_services = models.Registry.import_current_user_services()
(user_models,) = models.Registry.import_models([models.NAMES.user])


class UcApiHandler(base.BaseHandler):
    def get(self):
        code = self.request.get('code')
        code = ucnote.uc_authcode(code, 'DECODE')
        get = dict(urlparse.parse_qsl(code))
        action = get['action']
        post = self.request.body
        post = self.xml_unserilize(post)
        logging.info("call action %s", action)
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

    def xml_unserilize(self, xml):
        if not xml:
            return {}
        root = ET.fromstring(xml)
        data = {}
        for child in root:
            data[child.attrib['id']] = child.text
            if len(child) or (child is not None):
                childdata = {}
                for subchild in child:
                    childdata[subchild.attrib['id']] = subchild.text
                data[child.attrib['id']] = childdata
        return data

    def test(self, get, post):
        get.update(post)
        return API_RETURN_SUCCEED

    def deleteuser(self, get, post):
        get.update(post)
        return API_RETURN_SUCCEED

    def renameuser(self, get, post):
        get.update(post)
        return API_RETURN_SUCCEED

    def gettag(self, get, post):
        get.update(post)
        return API_RETURN_SUCCEED

    def synlogin(self, get, post):
        """uid = get['uid']"""
        get.update(post)
        email = get['email']
        username = get['username']
        userid = _create_userid_from_email(email)
        logging.warning(username)
        self.user_id = userid

        user_services.get_or_create_user(
            self.user_id, email)
        self.response.headers['Set-Cookie'] = \
            _set_user_info_cookie(email, username.lower() == 'admin')
        has_ever_registered = user_services.has_ever_registered(self.user_id)
        has_fully_registered = user_services.has_fully_registered(self.user_id)

        if has_fully_registered:
            return API_RETURN_SUCCEED

        agreed_to_terms = True
        if not isinstance(agreed_to_terms, bool) or not agreed_to_terms:
            raise self.InvalidInputException(
                'In order to edit explorations on this site, you will '
                'need to accept the license terms.')
        else:
            user_services.record_agreement_to_terms(self.user_id)

        if not user_services.get_username(self.user_id):
            try:
                user_services.set_username(self.user_id, username)
            except utils.ValidationError as e:
                raise self.InvalidInputException(e)
        can_receive_email_updates = True
        if can_receive_email_updates is not None:
            user_services.update_email_preferences(
                self.user_id, can_receive_email_updates,
                feconf.DEFAULT_EDITOR_ROLE_EMAIL_PREFERENCE,
                feconf.DEFAULT_FEEDBACK_MESSAGE_EMAIL_PREFERENCE)

        # Note that an email is only sent when the user registers for the first
        # time.
        if feconf.CAN_SEND_EMAILS_TO_USERS and not has_ever_registered:
            email_manager.send_post_signup_email(self.user_id)

        user_services.generate_initial_profile_picture(self.user_id)

        return API_RETURN_SUCCEED

    def synlogout(self, get, post):
        get.update(post)
        self.response.headers['Set-Cookie'] = \
            _clear_user_info_cookie()
        return API_RETURN_SUCCEED

    def updatepw(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatebadwords(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatehosts(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updateapps(self, get, post):
        # get.update(post)
        get.update(post)
        return API_RETURN_SUCCEED

    def updateclient(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatecredit(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def getcredit(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def getcreditsettings(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def updatecreditsettings(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED

    def addfeed(self, get, post):
        get.update(post)
        if not API_SYNLOGIN:
            return API_RETURN_FORBIDDEN
        return API_RETURN_SUCCEED


def get_user_info(http_cookie, cookie_name=_COOKIE_NAME):
    """Gets the requestor's user info from an HTTP Cookie header.

    Args:
      http_cookie: The value of the 'Cookie' HTTP request header.
      cookie_name: The name of the cookie that stores the user info.

    Returns:
      A tuple (email, admin, user_id) where:
        email: The user's email address, if any.
        admin: True if the user is an admin; False otherwise.
        user_id: The user ID, if any.
    """
    try:
        cookie = Cookie.SimpleCookie(http_cookie)
    except Cookie.CookieError:
        return '', False, ''

    cookie_dict = dict((k, v.value) for k, v in cookie.iteritems())
    return _get_user_info_from_dict(cookie_dict, cookie_name)


def _get_user_info_from_dict(cookie_dict, cookie_name=_COOKIE_NAME):
    """Gets the requestor's user info from a cookie dictionary.

    Args:
      cookie_dict: A dictionary mapping cookie names onto values.
      cookie_name: The name of the cookie that stores the user info.

    Returns:
      A tuple (email, admin, user_id) where:
        email: The user's email address, if any.
        admin: True if the user is an admin; False otherwise.
        user_id: The user ID, if any.
    """
    cookie_value = cookie_dict.get(cookie_name, '')

    email, admin, user_id = (cookie_value.split(':') + ['', '', ''])[:3]
    if '@' not in email:
        if email:
            logging.warning('Ignoring invalid login cookie: %s', cookie_value)
        return '', False, ''
    return email, (admin == 'True'), user_id


def _clear_user_info_cookie(cookie_name=_COOKIE_NAME):
    """Clears the user info cookie from the requestor, logging them out.
    Args:
      cookie_name: The name of the cookie that stores the user info.
    Returns:
      A Set-Cookie value for clearing the user info of the requestor.
    """
    logging.warning("logout..................")
    cookie = Cookie.SimpleCookie()
    cookie[cookie_name] = ''
    cookie[cookie_name]['path'] = '/'
    cookie[cookie_name]['max-age'] = '0'
    return cookie[cookie_name].OutputString()


def _create_userid_from_email(email):
    if email:
        user_id_digest = hashlib.md5(email.lower()).digest()
        user_id = '1' + ''.join(['%02d' % ord(x) for x in user_id_digest])[:20]
    else:
        user_id = ''
    return user_id


def _create_cookie_data(email, admin):
    """Creates cookie payload data.

    Args:
      email: The user's email address.
      admin: True if the user is an admin; False otherwise.

    Returns:
      A string containing the cookie payload.
    """
    user_id = _create_userid_from_email(email)
    return '%s:%s:%s' % (email, admin, user_id)


def _set_user_info_cookie(email, admin, cookie_name=_COOKIE_NAME):
    """Creates a cookie to set the user information for the requestor.

    Args:
      email: The email to set for the user.
      admin: True if the user should be admin; False otherwise.
      cookie_name: The name of the cookie that stores the user info.

    Returns:
      Set-Cookie value for setting the user info of the requestor.
    """
    cookie_value = _create_cookie_data(email, admin)
    cookie = Cookie.SimpleCookie()
    cookie[cookie_name] = cookie_value
    cookie[cookie_name]['path'] = '/'
    return cookie[cookie_name].OutputString()
