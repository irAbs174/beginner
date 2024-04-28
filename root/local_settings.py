"""
2020 Black
Application settings configuration
developer : #ABS
"""

# LOCAL ACCOUNT USERNAME BLACKLIST
LOCAL_ACCOUNT_USERNAME_BLACKLIST = ["admin", 'security', 'secure', 'protection', 'safeguard',
 'privacy', 'confidential', 'shield', 'lock', 'encrypted', 'defender', 'guard', 'safety',
  'firewall', 'securex', 'sentinel', 'secureguard', 'securetech', 'cyber', 'hacker',
   'securecode', 'protect', 'securenet', 'securezone', 'securelock', 'securedata', 'securecloud',
    'securelink', 'secureaccess', 'securelogin', 'secureweb', 'accesscontrol', 'authentication',
     'authorization', 'biometric', 'cryptography', 'cybersecurity', 'dataprotection',
      'digitalcertificate', 'digitalsignature', 'end-to-endencryption', 'forensics',
       'identitymanagement', 'informationsecurity', 'integrity', 'intrusiondetection', 'malware',
        'networksecurity', 'password', 'phishing', 'ransomware', 'riskmanagement',
         'securityaudit', 'securitybreach', 'securityclearance', 'securitypolicy',
          'socialengineering','spyware', 'threatintelligence',
           'virus', 'vulnerabilityassessment', 'zeroday', "god"]

# CSRF LOCAL TRUSTED ORIGINS :
CSRF_LOCAL_TRUSTED_ORIGINS = ['https://8001-cs-256274267521-default.cs-europe-west4-bhnf.cloudshell.dev', 'https://www.8001-cs-256274267521-default.cs-europe-west4-bhnf.cloudshell.dev']

# ALLOWED LOCAL HOSTS :
ALLOWED_LOCAL_HOSTS = ['127.0.0.1', '8001-cs-256274267521-default.cs-europe-west4-bhnf.cloudshell.dev', 'www.8001-cs-256274267521-default.cs-europe-west4-bhnf.cloudshell.dev']

# SECRET KEY
SEC_KEY = '!!!!!!!!!!!!!!!!YOUR_SEC_KEY_HERE!!!!!!!!!!!!!!!'

# LOCAL HOST IP :
LOCAL_HOST = ('127.0.0.1', '10.0.2.2')

# LOCAL SITE NAME :
LOCAL_SITE_NAME = 'kikpick'

# LOGIN_URL :
LOCAL_LOGIN_URL = '/accounts/'

# USERNAME MIN LENGTH :
USERNAME_MIN_LENGTH = 11

# ADMINS_PANEL :
ADMINS_PANEL = 'UNIQUEADMINISTRATOR174/'

# DEVELOPERS PANEL :
DEVELOPERS_PANEL = 'UNIQUEDEVELOPER174/'

# Support_page :
SUPPORT_PAGE = 'UNIQUESUPPORT174/'

# Site Traffic
SITE_TRAFFIC = 'UNIQUETRAFFIC174/'

# BASE_SITE
BASE_ACTIVE_SITE = '8001-cs-256274267521-default.cs-europe-west4-bhnf.cloudshell.dev'

# SITE API URL
SITE_API = 'UNIQUEAPI174/'

# SITE DEBUG
SITE_DEBIG = True




