from django.test import TestCase
# Create your tests here.

import base64
import filemaker_api.filemaker_api as filemaker


token = filemaker.login()

data = filemaker.adaptive_find_record(token, FirstName="Test", LastName='Person')

byuid = data[0]['response']['data'][0]['fieldData']['BYUID']
language = data[0]['response']['data'][0]['fieldData']['Language']
entrydate = data[0]['response']['data'][0]['fieldData']['EntryDate']

final = byuid + '&' + language + '&' +entrydate
filemaker.logout(token)

test_string = final

string_bytes = test_string.encode('ascii')

base64_bytes = base64.b64encode(string_bytes)
base64_string = base64_bytes.decode('ascii')

print(base64_string)

base64_bytes = base64_string.encode('ascii')

string_bytes = base64.b64decode(base64_bytes)

test_string = string_bytes.decode('ascii')

print(test_string)





