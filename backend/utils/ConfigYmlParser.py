import yaml

def parseEnv(filepath):
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
        return config

if __name__ == '__main__':
    print(parseEnv('../env.yml'))