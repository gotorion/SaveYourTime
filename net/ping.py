import subprocess

def ping(ip, count=1, timeout=1):
    """
    Ping the given IP address with specified count and timeout.
    Returns True if it's reachable, False otherwise.
    """
    command = ['ping', '-c', str(count), '-W', str(timeout), ip]

    try:
        response = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"An error occurred while pinging {ip}: {e}")
        return False


def read_network_list(file_path):
    """
    Read the network.list file and return a dictionary of name-ip pairs.
    """
    name_ip_dict = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                # Ignore empty lines and comments
                if not line or line.startswith('#'):
                    continue
                parts = line.split(':')
                if len(parts) == 2:
                    name, ip = parts[0].strip(), parts[1].strip()
                    name_ip_dict[name] = ip
                else:
                    print(f"Warning: Invalid format in line: {line}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    return name_ip_dict


def main():
    file_path = './network.list'
    name_ip_dict = read_network_list(file_path)

    if not name_ip_dict:
        print("No valid entries found or an error occurred.")
        return

    unreachable_names = []

    for name, ip in name_ip_dict.items():
        print(f"Pinging {name} ({ip})...")
        if not ping(ip):
            unreachable_names.append(name)

    if unreachable_names:
        print("\nThe following hosts are not reachable:")
        for name in unreachable_names:
            print(name)
    else:
        print("All hosts are reachable.")


if __name__ == "__main__":
    main()
