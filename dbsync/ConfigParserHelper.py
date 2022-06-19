import configparser


class ConfigParserHelper:
    def __init__(self, file_name):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    def get_config(self, group, property_name):
        try:
            return self.config[group][property_name]
        except KeyError as error:
            raise KeyError(f'Key {property_name} not found in group {group} in configuration file')

