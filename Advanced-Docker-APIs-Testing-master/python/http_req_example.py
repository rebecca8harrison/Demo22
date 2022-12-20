'''
Example use of Python requests API
'''

import requests

response = requests.get('http://example.com')

print(f'Status Code: {response.status_code}')

print('Response Headers:')
for k, v in response.headers.items():
  print(f'\t{k} => {v}')

print('Response Body')
print(response.text)
