import subprocess
import toml

def get_installed_packages():
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split("\n")

def generate_toml():
    installed_packages = get_installed_packages()
    toml_data = {
        "tool": {
            "dependencies": {pkg.split("==")[0]: pkg.split("==")[1] for pkg in installed_packages}
        }
    }

    with open("pyproject.toml", "w") as toml_file:
        toml.dump(toml_data, toml_file)

    print("toml готов")

generate_toml()
