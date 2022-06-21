#!/usr/local/bin/python3
import urllib.request
from urllib.error import URLError
urls = [
    "http://localhost:5555/api/mono_2_micro",
    "http://localhost:5555/api/live_graph",
    "http://localhost:5555/api/auto_graph",
    "http://localhost:5555/api/hardware_2_cloud",
    "http://localhost:5555/api/get_containerization_model",
    "http://localhost:5555/api/app_rationalization",
    "http://localhost:5555/api/cui"
]
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
total = len(urls)
success = 0
for u in urls:
  try:
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req) as r:
      print(f'STATUS: {r.status} REASON: {r.reason} ({u})')
      success += 1
  except URLError as e:
    # import pdb; pdb.set_trace()
    print(f'STATUS: {e.reason} REASON: {e.reason} ({e}) ({u})')
print(f'{success}/{total} URLs up')