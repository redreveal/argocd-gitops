import yaml
import sys
import os

def load_values_file(values_file_path):
    with open(values_file_path, 'r') as file:
        return yaml.safe_load(file)


def save_values_file(values, values_file_path):
    with open(values_file_path, 'w') as file:
        yaml.dump(values, file)


def update_values_with_config(values, config):
    if 'configMap' not in values:
        values['configMap'] = {}
    if 'config_values' not in values['configMap']:
        values['configMap']['config_values'] = {}

    config_values = values['configMap']['config_values']
    config_values['defaultManagerVersion'] = config.get('defaultManagerVersion')
    config_values['defaultAgentVersion'] = config.get('defaultAgentVersion')

    msa_overrides = config_values.get('msaVersionOverrides', {})
    for msa, overrides in config.get('msaVersionOverrides', {}).items():
        msa_override = {}

        msa_override['agentVersion'] = overrides.get('agentVersion', config.get('defaultAgentVersion'))

        if 'managerVersion' in overrides:
            msa_override['managerVersion'] = overrides.get('managerVersion')
        else:
            msa_override['managerVersion'] = config.get('defaultManagerVersion')

        msa_overrides[msa] = msa_override

    config_values['msaVersionOverrides'] = msa_overrides

    return values


def process_config_file(config_file_path, values_file_path):
    with open(config_file_path, 'r') as file:
        new_config = yaml.safe_load(file)

    values = load_values_file(values_file_path)
    updated_values = update_values_with_config(values, new_config)
    save_values_file(updated_values, values_file_path)


if __name__ == "__main__":
    input_config_file = sys.argv[1]  # The file that Elliot's team modifies
    input_values_file = sys.argv[2]  # The path to the remote repo where the values file is stored

    process_config_file(input_config_file, input_values_file)
