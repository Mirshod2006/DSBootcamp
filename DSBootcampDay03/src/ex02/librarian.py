import os
import subprocess
import shutil

def main():
    # In src folder, I made mychelil env, so I expect to take this value!
    EXPECTED_ENV = "mychelil"

    # But inorder to check current env I made another variable
    current_env = os.getenv("VIRTUAL_ENV")

    # Checking exsistence of current env and whether EXPECTED_ENV is current env or not
    if not current_env or EXPECTED_ENV not in current_env:
        raise EnvironmentError(f"Error: Script must be run inside the '{EXPECTED_ENV}' virtual environment!")

    print(f"Running in the correct virtual environment: {current_env}")

    # Installs the libraries from requirements.txt
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

    # Displays all installed libraries
    print("\nInstalled Libraries:")
    installed_packages = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    print(installed_packages.stdout)

    with open("requirements.txt", "w") as req_file:
        req_file.write(installed_packages.stdout)

    archive_name = "mychelil_env"
    shutil.make_archive(archive_name, 'zip', current_env)

if __name__ == '__main__':
    main()