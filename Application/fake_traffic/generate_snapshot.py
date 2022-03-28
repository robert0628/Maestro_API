import random
import json
import time
import sys

def random_bytes(max_size):
   """Convert the size from bytes to other units like KB, MB or GB."""
   byte = random.randint(0, max_size)
   if byte // 1024:
       return "{} KB".format(byte % 1024)
   elif byte // 1024*1024:
       return "{} MB".format(byte % (1024*1024))
   elif byte // (1024*1024*1024):
       return "{} GB".format(byte % (1024*1024*1024))
   else:
       return byte

def random_ip_ports(number_servers=3):
  IPs=[]
  ports=[]
  for i in range(number_servers):
    IPs.append( ".".join(map(str, (random.randint(0, 255) 
                            for _ in range(4)))))
    ports.append(random.randint(0, 65535))
  return IPs, ports

def random_time():
    # generate random number scaled to number of seconds in a day
    # (24*60*60) = 86,400
    
    rtime = int(random.random()*86400)
    
    hours   = int(rtime/3600)
    minutes = int((rtime - hours*3600)/60)
    seconds = rtime - hours*3600 - minutes*60
    
    time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
    return time_string
def create_fake_traffic(number_servers, max_byte_size, number_interactions):
  protocols=[ "TCP", "IP", "UDP", "POP", "SMTP", "FTP", "HTTP", "HTTPS"]
  IPs, ports = random_ip_ports(number_servers)
  fake_traffic={"items":[]}
  source_ip = random.choice(IPs)
  for i in range(number_interactions):
    IPs.remove(source_ip)
    destination_ip = random.choice(IPs)
    IPs.append(source_ip)
    fake_traffic["items"].append( {"protocol": random.choice(protocols), 
  "sourceSecurityTag": "",
  "sourceIp": source_ip,
  "sourcePort":random.choice(ports),
  "destinationSecurityTag":"",
  "destinationIp":destination_ip,
  "destinationPort":random.choice(ports),
  "duration":random_time(),
  "bytesSent":random_bytes(max_byte_size)
  })
  return fake_traffic



def main(number_snapshots=3,capture_interval=2,number_servers=3, max_byte_size=12884901888, number_interactions=10):
  for i in range(number_snapshots):
    snapshot= create_fake_traffic(number_servers, max_byte_size, number_interactions)
    nowgmt = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    with open('snapshot_{}.json'.format(nowgmt), 'w') as f:
        json.dump(snapshot, f)
    time.sleep(capture_interval)


def get_new_snapshot(number_servers=3, max_byte_size=12884901888, number_interactions=10):
  for i in range(1):
    snapshot= create_fake_traffic(number_servers, max_byte_size, number_interactions)
    return snapshot


if __name__ == '__main__':
  number_snapshots = int(sys.argv[1])
  capture_interval = int(sys.argv[2])
  number_servers = int(sys.argv[3])
  max_byte_size = int(sys.argv[4])
  number_interactions = int(sys.argv[5])
  main(number_snapshots,capture_interval, number_servers, max_byte_size, number_interactions)
