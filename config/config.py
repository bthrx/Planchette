import configparser

config = configparser.ConfigParser()
config.read('config/keys.ini')

def get_api_key(service_name):
    return config.get(service_name, 'api_key')