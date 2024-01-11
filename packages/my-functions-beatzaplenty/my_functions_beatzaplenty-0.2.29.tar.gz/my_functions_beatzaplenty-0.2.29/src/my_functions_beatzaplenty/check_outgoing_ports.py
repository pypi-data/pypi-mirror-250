import socket

def check_outgoing_ports(hostname,ports = [465, 587]):
    '''
    Check status of outgoing ports.

    :param hostname: the hostname to query against
    :param ports: the ports to be checked. Default is 465 and 587. Format as an array EG: [465, 587]

    :return: An array of Statuses. Either "Open" or "Closed"
    '''
    results = {}

    for port in ports:
        try:
            with socket.create_connection((hostname, port), timeout=5) as connection:
                results[port] = "Open"
        except (socket.timeout, ConnectionRefusedError):
            results[port] = "Closed"
        except OSError as e:
            if "unreachable" in str(e).lower():
                results[port] = "Closed"
            else:
                # If it's a different OSError, propagate the exception
                raise

    return results

if __name__ == '__main__':
    # Example usage:
    hostname_to_check = "smtp.gmail.com"
    status_results = check_outgoing_ports(hostname_to_check)

    for port, status in status_results.items():
        print(f"Port {port}: {status}")