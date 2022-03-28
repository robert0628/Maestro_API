import json
import requests
import threading
from requests.auth import HTTPBasicAuth

cliUrl = "https://71.25.48.225/api/cli"
pcapLocation = "https://71.25.48.225/capture/pc-traffic2/pcap"

def get_cisco_asa_pcap():
	with requests.Session() as session:
		session.verify = False

		headers = {
		'User-Agent': 'REST API Agent',
		'Content-Type': 'application/json'
		}

		payload1 = {"commands": ["no capture pc-traffic"]}
		payload2 = {"commands": ["capture pc-traffic2 interface INSIDE buffer 512000 circular-buffer match ip any any "]}

		response = session.request("GET", pcapLocation, auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),  headers=headers)

		if (response.status_code == 200):
			with open('pcap_0.pcap', 'wb') as file:
				file.write(response.content)
		else:
			print("[ERROR] Failed to get the pcap from CISCO ASA.")

		response = session.post(url=cliUrl,
							auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),
							headers=headers,
							data=json.dumps(payload2),
							)
		if (response.status_code != 200):
			print("[ERROR]Failed to start the new traffic capture from CISCO ASA.")