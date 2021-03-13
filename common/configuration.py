import os
import json
class Configuration(object):
    def __init__(self):
        path_configuration_folder = os.environ['conf_folder']
        path_configuration_file=os.path.join(path_configuration_folder,'configuration.json')
        self.read_conf(path_configuration_file)



    def read_conf(self, path_configuration_file):
        path_conf_folder = os.path.dirname(path_configuration_file)
        with open(path_configuration_file) as conf_json_file:
            conf_json =  json.load(conf_json_file)
            for k in conf_json:
                setattr(self,k, conf_json[k])

