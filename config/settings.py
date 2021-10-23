# Python's Libraries
import os

# Third-paty Libraries
from dotenv import load_dotenv

# Own's Libraries
from Utils.config import deploy
from Utils.config import directories
from Utils.config import applications
from Utils.config import logs
from Utils.config import database
from Utils.config import media
from Utils.config import templates
from Utils.config import security
from Utils.config import internationalization
from Utils.config import statics
from Utils.config import messages
from Utils.config import rest
from Utils.config import aws


# App configuration
APP_CLAVE = "BEN"
APP_NAME = "Benjie API"
APP_YEAR_RELEASE = "2021"
APP_VERSION = "0.0.01"
APP_ENVIRONMENT = deploy.Enviroment.LOCAL

JET_DEFAULT_THEME = 'light-blue'

SECRET_KEY = deploy.SECRET_KEY
ROOT_URLCONF = deploy.ROOT_URLCONF
WSGI_APPLICATION = deploy.WSGI_APPLICATION
ALLOWED_HOSTS = deploy.ALLOWED_HOSTS
DEBUG = deploy.DEBUG

INSTALLED_APPS = applications.get_InstalledApps()

LOGGING = logs.get_Config(
    APP_ENVIRONMENT,
    directories.LOCAL_LOG_PATH
)

DATABASES = database.get_MysqlConfig(
    os.getenv(f'{APP_CLAVE}_{APP_ENVIRONMENT.value}_DB_NAME', 'default'),
    os.getenv(f'{APP_CLAVE}_{APP_ENVIRONMENT.value}_DB_USER', 'dummy'),
    os.getenv(f'{APP_CLAVE}_{APP_ENVIRONMENT.value}_DB_PASS', 'password'),
    os.getenv(f'{APP_CLAVE}_{APP_ENVIRONMENT.value}_DB_HOST', 'localhost'),
    os.getenv(f'{APP_CLAVE}_{APP_ENVIRONMENT.value}_DB_PORT', 3306)
)

MIDDLEWARE = security.get_Middlewares()

TEMPLATES = templates.get_Config(directories.TAGS)

# LOGIN_URL = security.LOGIN_URL
# LOGOUT_REDIRECT_URL = security.LOGOUT_REDIRECT_URL
AUTH_USER_MODEL = security.AUTH_USER_MODEL
AUTH_PASSWORD_VALIDATORS = security.AUTH_PASSWORD_VALIDATORS
SESSION_EXPIRE_SECONDS = security.SESSION_EXPIRE_SECONDS
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = security.SESSION_EXPIRE_AFTER_LAST_ACTIVITY
SESSION_EXPIRE_AT_BROWSER_CLOSE = security.SESSION_EXPIRE_AT_BROWSER_CLOSE
PASSWORD_LIMIT_DAYS = security.PASSWORD_LIMIT_DAYS

MESSAGE_TAGS = messages.TAGS

LANGUAGE_CODE = internationalization.LANGUAGE_CODE
USE_I18N = internationalization.USE_I18N
TIME_ZONE = internationalization.TIME_ZONE
USE_TZ = internationalization.USE_TZ
USE_L10N = internationalization.USE_L10N
DATE_INPUT_FORMATS = internationalization.DATE_INPUT_FORMATS
DATETIME_INPUT_FORMATS = internationalization.DATETIME_INPUT_FORMATS
USE_THOUSAND_SEPARATOR = internationalization.USE_THOUSAND_SEPARATOR
THOUSAND_SEPARATOR = internationalization.THOUSAND_SEPARATOR
NUMBER_GROUPING = internationalization.NUMBER_GROUPING
DECIMAL_SEPARATOR = internationalization.DECIMAL_SEPARATOR

if APP_ENVIRONMENT == deploy.Enviroment.LOCAL:
    # Static settings
    STATIC_URL = '/static/'
    # STATIC_URL = 'http://127.0.0.1:9001/'

    STATIC_ROOT = directories.STATIC_ROOT
    STATICFILES_DIRS = directories.STATICFILE_DIRS
    STATICFILES_FINDERS = statics.STATICFILES_FINDERS

    #  Media settings
    MEDIA_URL = media.MEDIA_URL
    MEDIA_ROOT = directories.MEDIA_ROOT
    FILE_UPLOAD_PERMISSIONS = media.FILE_UPLOAD_PERMISSIONS

else:
    # AWS settings
    AWS_ACCESS_KEY_ID = aws.get_AccessKeyId(APP_CLAVE, APP_ENVIRONMENT)
    AWS_SECRET_ACCESS_KEY = aws.get_SecretAccessKey(APP_CLAVE, APP_ENVIRONMENT)
    AWS_DEFAULT_ACL = aws.AWS_DEFAULT_ACL
    AWS_QUERYSTRING_AUTH = aws.AWS_QUERYSTRING_AUTH
    AWS_S3_OBJECT_PARAMETERS = aws.AWS_S3_OBJECT_PARAMETERS

    AWS_STORAGE_BUCKET_NAME = aws.get_FilesBucketName(APP_CLAVE, APP_ENVIRONMENT)
    AWS_S3_CUSTOM_DOMAIN = f's3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'
    AWS_STATIC_LOCATION = aws.AWS_STATIC_LOCATION
    AWS_PUBLIC_MEDIA_LOCATION = aws.AWS_PUBLIC_MEDIA_LOCATION
    AWS_PRIVATE_MEDIA_LOCATION = aws.AWS_PRIVATE_MEDIA_LOCATION

    #  Static settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
    STATIC_ROOT = directories.STATIC_ROOT
    STATICFILES_DIRS = directories.STATICFILE_DIRS
    STATICFILES_FINDERS = statics.STATICFILES_FINDERS
    STATICFILES_STORAGE = statics.STATICFILES_STORAGE

    #  Media settings
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    MEDIA_ROOT = directories.MEDIA_ROOT
    FILE_UPLOAD_PERMISSIONS = media.FILE_UPLOAD_PERMISSIONS
    DEFAULT_FILE_STORAGE = media.DEFAULT_FILE_STORAGE
    PRIVATE_FILE_STORAGE = media.PRIVATE_FILE_STORAGE

    # Rest Settings
    CORS_ORIGIN_ALLOW_ALL = rest.CORS_ORIGIN_ALLOW_ALL
    REST_FRAMEWORK = rest.REST_FRAMEWORK
