# post_install.py
import subprocess
import os

bashrc_path = os.path.expanduser("~/.bashrc")  # Change this if your config file is elsewhere
alias_command = 'alias pyEasyML-init=\'python3 -c "import pyEasyML.cli; pyEasyML.cli.main(\'$PWD\', \'start\')"\''

# Add the alias to the user's bashrc file
subprocess.run(['bash', '-c', f'echo "{alias_command}" >> {bashrc_path}'], check=True)
print("pyEasyML-init alias added to bashrc file.")