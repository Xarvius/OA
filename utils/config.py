import json

file_name = './utils/config.json'


def load_config() -> object:
    with open(file_name, encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config


def save_config(config):
    with open(file_name, 'w', ) as outfile:
        json.dump(config, outfile)
