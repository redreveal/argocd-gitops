import yaml
import sys
import os

def create_configmap(data, filepath):
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "processing-agent-config",
            # We might need to add some reveal annotations here? Ask Nick!
        },
        "data": data
    }

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as file:
        yaml.dump(configmap, file)

def main(input_file):
    with open(input_file, 'r') as file:
        values = yaml.safe_load(file)

    output_file = os.path.join(os.path.dirname(input_file), 'configmap.yaml')
    create_configmap(values, output_file)

if __name__ == "__main__":
    main(sys.argv[1])