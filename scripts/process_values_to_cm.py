import yaml
import sys
import os
import boto3


def load_values_file(values_file_path):
    with open(values_file_path, 'r') as file:
        return yaml.safe_load(file)


def save_values_file(values, values_file_path):
    with open(values_file_path, 'w') as file:
        yaml.dump(values, file)


def update_values_with_config(values, config):
    # Ensure the 'configMap' and 'config_values' keys exist
    if 'configMap' not in values:
        values['configMap'] = {}
    values['configMap']['config_values'] = config
    return values


def process_config_file(config_file_path, values_file_path):
    # Load the processing-agent-config.yml as the new config
    with open(config_file_path, 'r') as file:
        new_config = yaml.safe_load(file)

    # Load the existing values.yaml
    values = load_values_file(values_file_path)

    # Update values.yaml with the new config
    updated_values = update_values_with_config(values, new_config)

    # Save the updated values.yaml back
    save_values_file(updated_values, values_file_path)


if __name__ == "__main__":
    input_config_file = sys.argv[1]  # The modified processing-agent-config.yml file
    input_values_file = sys.argv[2]  # The path to the values.yaml to be updated

    process_config_file(input_config_file, input_values_file)
