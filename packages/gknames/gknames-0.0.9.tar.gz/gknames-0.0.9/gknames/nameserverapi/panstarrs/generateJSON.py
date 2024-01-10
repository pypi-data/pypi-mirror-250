import json
from gkutils.commonutils import readGenericDataFile
data = readGenericDataFile('nameserver_ps1_extract_20240106.tst', delimiter='\t')
for row in data:
    print("curl -s -X POST http://127.0.0.1:8085/sne/nameserver_panstarrs/eventapi/ -d '" + json.dumps(row) + "' -H 'Content-Type: application/json' -H 'Authorization: Token 7cd5d7f979bebb7da60ac8696c4f0b7e96231bab'")
    print("echo")

