
def get_MysqlConfig(_name, _user, _password, _host, _port):
    return {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': _name,
            'USER': _user,
            'PASSWORD': _password,
            'HOST': _host,
            'PORT': _port,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
