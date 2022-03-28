from netmiko import ConnectHandler
import paramiko
import json
import threading
import time

from .pcap_parser import generate_json
from .get_pcap_asa import get_cisco_asa_pcap

def send_command(device):
    commands = device['commands']
    del device['commands']
    ssh_connect = ConnectHandler(**device, fast_cli=True)
    delay = 0.025
    for command in commands:
        ssh_connect.send_command_timing(command, delay_factor=delay)
    ssh_connect.disconnect()

def connect_to_ftd():
    config = json.load(open('ssh_config.json', 'r'))
    devices = config['devices']
    for device in devices:
        thread = threading.Thread(target=send_command, args=(device,))
        thread.start()
    thread.join()
    # time.sleep(4)

def ftp_connect(hostname, username, password, port):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password, port=port)
        ftp = ssh.open_sftp()
        return ftp
    except Exception as e:
        print('Connection Failed')
        print(e)

def download_files():
    config = json.load(open('ssh_config.json', 'r'))
    conn_data = config["ftp"]
    ftp = ftp_connect(**conn_data)

    files = config["files"]
    for file in files:
        ftp.get(file, file)

def get_new_pcaps():
    connect_to_ftd()
    download_files()

def get_new_jsons():
    try:
        start = time.time()

        get_new_pcaps()
        get_cisco_asa_pcap()
        generate_json()

        total = time.time() - start
        print("FINISHED IN %.2f SECONDS" % round(total, 2))
    except:
        print("COULD NOT DOWNLOAD FILES, RETRYING")
        get_new_pcaps()