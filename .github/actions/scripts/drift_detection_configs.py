import yaml
import sys

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file) or {}
    return data

def extract_relevant_data(yaml_data):
    relevant_data = {
        'defaultManagerVersion': yaml_data.get('defaultManagerVersion'),
        'defaultAgentVersion': yaml_data.get('defaultAgentVersion'),
        'msaVersionOverrides': yaml_data.get('msaVersionOverrides')
    }
    return relevant_data

def compare_yaml_data(source_data, target_data):
    source_values = extract_relevant_data(source_data)
    target_values = extract_relevant_data(target_data.get('configMap', {}).get('config_values', {}))
    differences = {}
    for key, source_value in source_values.items():
        target_value = target_values.get(key)
        if source_value != target_value:
            differences[key] = {'source': source_value, 'target': target_value}
    return differences

if __name__ == "__main__":
    source_file = sys.argv[1]
    target_file = sys.argv[2]

    source_data = load_yaml_file(source_file)
    target_data = load_yaml_file(target_file)

    differences = compare_yaml_data(source_data, target_data)
    if differences:
        print("DIFFERENCES_DETECTED", source_file, target_file)  # Print the file paths with differences
    else:
        print("NO_DIFFERENCES")
