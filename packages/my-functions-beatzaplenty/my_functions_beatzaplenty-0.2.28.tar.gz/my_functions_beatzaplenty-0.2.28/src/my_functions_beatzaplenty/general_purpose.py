import subprocess, configparser, os, importlib, shlex, time, platform
import paramiko
import my_functions_beatzaplenty.update_containers as update_containers

def run_command(command):
    '''
    Run any command and output to console. 

    :param command: A string. Command to run.
    :return: Bool for succesful execution
    '''
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Read and print output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            
        for line in iter(process.stderr.readline, ''):
            print(line, end='')
        
        process.wait()
        
        # Check for errors
        if process.returncode != 0:
            print("Error executing command. Return code: {}".format(process.returncode))
            return False
        
        return True
    
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("Error: {}".format(e))
        return False
    
    except Exception as e:
        print("Error: {}".format(e))
        raise

def create_config_file(config_data, file_path):
    '''
    Create a config file. 
    param: config_data: the data to use in the file
    param: file_path: Where to put the file
    '''
    config = configparser.ConfigParser()

    for section, settings in config_data.items():
        config[section] = settings

    try:
        with open(file_path, 'w') as config_file:
            config.write(config_file)
        print(f"Config file successfully created at {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def is_repo_up_to_date(path):
    '''
    Check if your Git Hub repo is up to date. 
    :param path: THe path to check
    '''
    try:
        cwd = os.getcwd()
        os.chdir(path)
        # Check if the local repository is up to date
        subprocess.run(['git', 'fetch'], check=True)
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True, check=True)

        # If the repository is not up to date, pull the changes
        if "Your branch is behind" in result.stdout:
            print("Local repository is not up to date. Pulling changes...")
            subprocess.run(['git', 'pull'], check=True)
            print("Changes pulled successfully.")
        else:
            print("Local repository is up to date.")
        os.chdir(cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def install_required_modules(requirements):
    '''
    Install required python modules. 
    
    :param requirements: The requirements.txt to use
    '''
    if not os.path.exists(requirements):
        raise FileNotFoundError(f"The requirements file '{requirements}' does not exist.")

    with open(requirements) as f:
        required_modules = f.read().splitlines()

    for module in required_modules:
        name = module.split("==")[0]

        spec = importlib.util.find_spec(name)
        if spec is None:
            print(f"Module {name} not found. Installing...")
            subprocess.call(['pip', 'install', module])
        else:
            print(f"Module {name} is already installed.")

def check_command_exists(command):
    '''
    Check if a command exists. 

    :param command: The command to test
    
    :return: Bool indicating if the command exists
    '''
    try:
        subprocess.run(shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_ssh_connection(hostname, username, keyfile, max_retries=10, retry_interval=5, port=22):
    '''
    Create an SSH connection. 
    
    :param hostname: the hostname to connect to
    :param username: the username to connect as
    :param keyfile: the keyfile to use in the conneciton attempt. Auto discovers any keys in $HOME/.ssh
    :param max_retries: default is 10
    :param retry_interval: Specified in seconds. Default is 5 seconds.
    :param port: Port to connect to. Default is 22
    
    :return: A paramiko.SSHClient object that can be used to execute commands
    '''
    retries = 0
    while retries < max_retries:
        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            # Automatically add the server's host key (this is insecure, see comments below)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print(f"Connecting to {hostname} with username {username} and keyfile {keyfile}")
            # Connect to the server with the specified keyfile
            ssh.connect(hostname, username=username, key_filename=keyfile,port=port)

            return ssh

        except Exception as e:
            print(f"Error creating SSH connection: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

    raise RuntimeError(f"Failed to create SSH connection after {max_retries} attempts.")

def execute_ssh_command(ssh, command):
    '''
    Execute a command via SSH and output to console. 
    
    :param ssh: A paramiko.SSHClient object create using the general_purpose.create_ssh_connection function
    :param command: The command to run
    '''
    try:
        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.exec_command(command)

        # Print each line of the command output in real-time
        while True:
            if channel.recv_ready():
                line = channel.recv(1024).decode()
                if not line:
                    break
                print(line.strip())

            if channel.exit_status_ready():
                break

        # Print any errors
        error_output = channel.recv_stderr(1024).decode()
        if error_output:
            print(f"Error: {error_output}")
        return channel.recv_exit_status()
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SSH connection
        ssh.close()

def parse_tuple(input):
    '''
    Parse a Tuple from a CSV list. 
    
    :param input: The input to Parse
    
    :return: A Tuple
    '''
    return tuple(k.strip() for k in input[1:-1].split(','))

def remote_update(config):
    '''
    Run Updates on remote machine. .
    
    :param config: A configparser config section
    '''
    if config.get("ssh_port") is None:
        ssh_port = 22
    else:
        ssh_port =  config.get("ssh_port") 
    if config.get('update_script') is None:
        update_script = f"-m my_functions_beatzaplenty.remote_update {config.get('containers')}"
    else:
        update_script = config.get('update_script')
    
    print(f"****************** Updating {config.get('ssh_username')} *******************")
    ssh = create_ssh_connection(config.get('ssh_hostname'), 
                        config.get('ssh_username'),
                        config.get('keyfile'),
                        port=ssh_port)
    execute_ssh_command(ssh, command=f"python3 {update_script}")

def run_updates(containers):
    '''
    Run updates on machine. Runs all apt, flatpak and spice updates and updates given containers. 
    
    :param containers: the containers to update
    '''
    os_release_id = platform.freedesktop_os_release().get('ID')

    update_commands = [('sudo','apt-get','update'),
                        ('sudo','apt-get','upgrade','-y'),
                        ('sudo','apt-get','autoremove','-y')]
                # Add flatpaks and spices if mint
    if os_release_id == "linuxmint":
        update_commands+=[('flatpak','update','-y'),
                        ('sudo','flatpak','remove','--unused','-y'),
                        ('cinnamon-spice-updater','--update-all')]
    try:
        for cmd in update_commands:
            run_command(cmd)
        if check_command_exists("docker"):
            update_containers.main(containers)
    except Exception as e:
        print("Error: {}".format(e))
