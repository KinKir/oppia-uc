import math
import time
import urllib
import urllib2
import xml.etree.cElementTree as ET
import feconf

URL = feconf.UC_URL
UC_CLIENT_RELEASE = feconf.UC_CLIENT_RELEASE
UC_KEY = feconf.UC_KEY
UC_APPID = feconf.UC_APPID
UC_IP = feconf.UC_IP
USER_AGENT = 'Python-urllib/2.7'


def uc_user_login(username, password, isuid=0, checkques=0,
                  questionid='', answer='', local_ip=''):
    return uc_api_post("user", "login",
                       {'username': username,
                        'password': password, "isuid": isuid,
                        'checkques': checkques,
                        'questionid': questionid,
                        'answer': answer, 'ip': local_ip})


def xml_unserilize(xml):
    if not xml:
        return {}
    root = ET.fromstring(xml)
    data = {}
    for child in root:
        data[child.attrib['id']] = child.text
        if len(child):
            childdata = {}
            for subchild in child:
                childdata[subchild.attrib['id']] = subchild.text
            data[child.attrib['id']] = childdata
    return data


def uc_app_ls():
    returns = uc_api_post('app', 'ls', {})
    return returns


def uc_feed_add(icon, uid, username, title_template='',
                title_data='', body_template='',
                body_data='', body_general='', target_ids='', images=None):
    if images is None:
        images = []

    return uc_api_post('feed', 'add',
                       {'icon': icon,
                        'appid': UC_APPID, 'uid': uid,
                        'username': username,
                        'title_template': title_template,
                        'title_data': title_data,
                        'body_template': body_template,
                        'body_data': body_data,
                        'body_general': body_general,
                        'target_ids': target_ids,
                        'image_1': images[0]['url'],
                        'image_1_link': images[0]['link'],
                        'image_2': images[1]['url'],
                        'image_2_link': images[1]['link'],
                        'image_3': images[2]['url'],
                        'image_3_link': images[2]['link'],
                        'image_4': images[3]['url'],
                        'image_4_link': images[3]['link']})


def uc_feed_get(limit=100, delete=True):
    returns = uc_api_post('feed', 'get', {'limit': limit, 'delete': delete})
    return returns


def uc_user_register(username, password, email, questionid='',
                     answer='', regip=''):
    returns = uc_api_post('user', 'register',
                          {'username': username, 'password': password,
                           'email': email, 'questionid': questionid,
                           'answer': answer, 'regip': regip})
    return returns


def uc_user_synlogin(uid):
    uid = int(uid)
    return uc_api_post('user', 'synlogin', {'uid': uid})


def uc_user_synlogout():
    return uc_api_post('user', 'synlogout', [])


def uc_user_edit(username, oldpw, newpw, email,
                 ignoreoldpw=0, questionid='', answer=''):
    return uc_api_post('user', 'edit', {'username': username,
                                        'oldpw': oldpw,
                                        'questionid': questionid,
                                        'ignoreolepw': ignoreoldpw,
                                        'newpw': newpw, 'email': email,
                                        'answer': answer})


def uc_user_delete(uid):
    return uc_api_post('user', 'delete', {'uid': uid})


def uc_user_deleteavatar(uid):
    return uc_api_post('user', 'deleteavatar', {'uid': uid})


def uc_user_checkname(username):
    return uc_api_post('user', 'check_username', {'username': username})


def uc_user_checkemail(email):
    return uc_api_post('user', 'check_email', {'email': email})


def uc_user_addprotected(username, admin=''):
    return uc_api_post('user', 'addprotected',
                       {'username': username, 'admin': admin})


def uc_user_deleteprotected(username):
    return uc_api_post('user', 'deleteprotected', {'username': username})


def uc_user_getprotected():
    return uc_api_post('user', 'getprotected', {'1': 1})


def uc_get_user(username, isuid=0):
    returns = uc_api_post('user', 'get_user',
                          {'username': username, 'isuid': isuid})
    return returns


def uc_user_merge(oldusername, newusername, uid, password, email):
    returns = uc_api_post('user', 'merge',
                          {'oldusername': oldusername,
                           'newusername': newusername,
                           'uid': uid, 'password': password, 'email': email})
    return returns


def uc_user_merge_remove(username):
    return uc_api_post('user', 'merge_remove', {'username': username})


def uc_user_getcredit(appid, uid, credit):
    return uc_api_post('user', 'getcredit',
                       {'appid': appid, 'uid': uid, 'credit': credit})


def uc_user_logincheck(username, local_ip):
    return uc_api_post('user', 'logincheck',
                       {'username': username, 'ip': local_ip})


def uc_api_post(module, action, arg=None):
    if arg is None:
        arg = []
    s = sep = ''
    for (k, v) in arg.items():
        k = urllib.quote_plus(k)
        if isinstance(v, (frozenset, list, set, tuple)):
            s2 = sep2 = ''
            for k2, v2 in v:
                k2 = urllib.quote_plus(k2)
                s2 = s2 + sep2 + "{" + k + "}[" + \
                     k2 + "]=" + urllib.urlencode(v2)
                sep2 = '&'
            s = s + sep + s2
        else:
            s = s + sep + k + "=" + urllib.quote_plus(str(v))
        sep = '&'
    postdata = uc_api_requestdata(module, action, s)
    return uc_fopen2(URL, postdata)


def uc_fopen2(url, post='', timeout=15):
    # todo add times parameter
    return uc_fopen(url, post, timeout)


def uc_fopen(url, post='', timeout=15):
    req = urllib2.Request(url=url, headers={'User-Agent': USER_AGENT})
    # data = urllib.quote(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data=post, timeout=timeout)
    return response.read()


def uc_api_requestdata(module, action, arg='', extra=''):
    post = "m=" + module + "&a=" + action + "&inajax=2&release=" \
           + UC_CLIENT_RELEASE
    post += "&input=" + uc_api_input(arg) + "&appid=" + UC_APPID + extra
    return post


def md5(md5str):
    import hashlib
    m = hashlib.md5()
    m.update(md5str)
    return m.hexdigest()


def uc_api_input(data):
    return urllib.quote_plus(uc_authcode(data + "&agent=" +
                                         md5(USER_AGENT) +
                                         "&time=" + str(int(time.time())),
                                         "ENCODE", UC_KEY))


def microtime(get_as_float=False):
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())


def substr(string, start, length=None):
    """Returns the portion of string specified by the start and length
    parameters.
    """
    if len(string) < start:
        return False

    if not length:
        return string[start:]
    elif length > 0:
        return string[start:start + length]
    else:
        return string[start:length]


def base64_decode(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return data.decode('base64')


def base64_encode(data):
    return data.encode('base64')


def uc_authcode(string, operation='DECODE', key='', expiry=0):
    ckey_length = 4
    key = md5(UC_KEY if key == '' else key)
    keya = md5(substr(key, 0, 16))
    keyb = md5(substr(key, 16, 16))
    keyc = substr(string, 0, ckey_length) if operation == 'DECODE' \
        else substr(md5(microtime()), -ckey_length)
    cryptkey = keya + md5(keya + keyc)
    key_length = len(cryptkey)
    string = base64_decode(substr(string, ckey_length)) if \
        operation == 'DECODE' else \
        ('%010d' % (expiry + int(time.time()) if expiry else 0)) \
        + substr(md5(string + keyb), 0, 16) + string
    string_length = len(string)

    result = ''
    box = range(0, 256)

    rndkey = []
    for i in range(0, 256):
        rndkey.append(ord(cryptkey[i % key_length]))
    j = 0
    for i in range(0, 256):
        j = (j + box[i] + rndkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp
    a = j = 0
    for i in range(0, string_length):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result = result + chr(ord(string[i]) ^ \
                              (box[(box[a] + box[j]) % 256]))
    if operation == 'DECODE':
        if (int(substr(result, 0, 10)) == 0 or \
                            int(substr(result, 0, 10)) - \
                                int(time.time()) > 0) and \
                        substr(result, 10, 16) == \
                        substr(md5(substr(result, 26) + keyb), 0, 16):
            return substr(result, 26)
        else:
            return ''
    else:
        return keyc + base64_encode(result).replace('=', '')


def test():
    res = uc_user_login("admin", "admin")
    print res
    res = uc_user_logincheck('admin', '127.0.0.1')
    print res


if __name__ == "__main__":
    test()
