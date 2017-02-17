# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "f3xy7mbz*yo$%h&+e(w4epfh^td!#7&smkc^lar&85_g1$(rik"
NEVERCACHE_KEY = "j=7=#xv9ti#r24_75a3=o9)sey8av9z#0av8n-tb-zm(=4*o&s"
SHOP_HANDLER_PAYMENT = 'cartridge.shop.payment.stripe_api.process'
STRIPE_API_KEY = 'sk_test_MdtkxO8xERhwquOoI3joUFav'

#Email setting
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'airbespoke@gmail.com'
EMAIL_HOST_PASSWORD = 'Saigon25'
EMAIL_PORT = 587
#SQLite

# DATABASES = {
#     "default": {
#         # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
#         "ENGINE": "django.db.backends.sqlite3",
#         # DB name or path to database file if using sqlite3.
#         "NAME": "dev.db",
#         # Not used with sqlite3.
#         "USER": "",
#         # Not used with sqlite3.
#         "PASSWORD": "",
#         # Set to empty string for localhost. Not used with sqlite3.
#         "HOST": "",
#         # Set to empty string for default. Not used with sqlite3.
#         "PORT": "",
# 		}
# }

#POSTGRESS
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dca0qmahmcoe2j',
        'USER': 'ilbmcmonocawbw',
        'PASSWORD': 'S62b9ogBQXR_iXBWTmD5use1v3',
        'HOST': 'ec2-54-235-254-56.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
# ALLOWED_HOSTS = [""]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "DEPLOY_TOOL": "rsync",  # Deploy with "git", "hg", or "rsync"
#     "SSH_USER": "",  # VPS SSH username
#     "HOSTS": [""],  # The IP address of your VPS
#     "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
#     "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
#     "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
#     "DB_PASS": "",  # Live database password
#     "ADMIN_PASS": "",  # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }
