import subprocess

from otto_login import settings


def login():
    run_cmd(f'cpfw-login '
            f'--url {settings.firewall_url} '
            f'--user {settings.ocn_user} '
            f'--password {ocn_password()} '
            f'--insecure')


def ocn_password():
    return run_cmd(settings.ocn_pass)


def run_cmd(cmd):
    try:
        process = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return process.stdout
    except:
        pass

# import datetime
# import requests
# from Cryptodome.Cipher import PKCS1_v1_5
# from Cryptodome.Hash import SHA
# from Cryptodome.PublicKey import RSA
#
# from otto_login import settings

#     login_params = get_login_params()
#
#     r = do_login(settings.ocn_user, crypt(login_params, password))
#
#     print(r)
#
#
# def do_login(username, password):
#     url = f'{settings.firewall_url}/Login'
#
#     payload = {
#         'realm': 'passwordRealm',
#         'username': username,
#         'password': password
#     }
#
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Referer': f'{settings.firewall_url}/PortalMain',
#         'Origin': f'{settings.firewall_url}/PortalMain',
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36'
#     }
#
#     jar = requests.cookies.RequestsCookieJar()
#
#     jar.set(
#         'cpnacportal_login_type',
#         'password',
#         path='/',
#         domain=settings.firewall_domain,
#         expires=datetime.datetime.now().timestamp() + 5 * 60 * 60,
#         rest={
#             'HostOnly': True,
#             'SameSite': ''
#         },
#     )
#
#     jar.set(
#         'cpnacportal_username',
#         username,
#         domain=settings.firewall_domain,
#         path='/',
#         expires=datetime.datetime.now().timestamp() + 5 * 60 * 60,
#         rest={
#             'HostOnly': True,
#             'SameSite': ''
#         },
#     )
#
#     return requests.post(url, data=payload, headers=headers, cookies=jar)
#
#
# def get_login_params():
#     url = f'{settings.firewall_url}/RSASettings'
#     r = requests.get(url, verify=False)
#
#     return r.json()
#
#
# def crypt(login_params, password):
#     message = f"{login_params['loginToken']}{password}".encode('utf-8')
#
#     h = SHA.new(message)
#
#     key = RSA.generate(1024)
#
#     return reverse(PKCS1_v1_5.new(key).encrypt(message+h.digest()).hex())
#
#
# def reverse(s):
#     r = ''
#     j = len(s) - 2
#     while j >= 0:
#         r += s[j:j+2]
#         j -= 2
#
#     return r
