import yaml

# Absolute path with relation to the code that imports config
config_file = "config/configuration.yaml"
with open(config_file) as file:
    # This is the name we're going to reference in the main.py when importing!
    configuration = yaml.load(file, Loader=yaml.FullLoader)