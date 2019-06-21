import json


def load_json(file_name) -> object:
    config_file = open(file_name, encoding='utf-8')
    config = json.load(config_file)
    return config


def save_json(config):
    with open('config.json', 'w', ) as outfile:
        json.dump(config, outfile)
