import configparser

def get_api_key(service_name):
    config = configparser.ConfigParser()
    config.read('config/keys.ini')
    return config.get(service_name, 'api_key').strip("'\"")