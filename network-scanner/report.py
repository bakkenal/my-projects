import texttable
import sys
import json

if len(sys.argv) != 3:
    print("wrong inputs!")
    sys.exit(1)

with open(sys.argv[1]) as jsonFile:
    data = jsonFile.read()
outputs = json.loads(data)

types = (   "scan_time", "ipv4_addresses", "ipv6_addresses", 
            "http_server", "insecure_http", "redirect_to_https",
            "hsts", "tls_versions", "root_ca", "rdns_names",
            "rtt_range", "geo_locations")

outputFile = open(sys.argv[2], 'w')
# outputting all the data
for address in outputs:
    outputFile.write(address + "\n")
    for section in types:
        outputFile.write("\t" + section + ":\n")
        if isinstance(outputs[address][section], list):
            for entry in outputs[address][section]:
                outputFile.write("\t\t" + str(entry) + "\n")
        else:
            outputFile.write("\t\t" + str(outputs[address][section]) + "\n")
    outputFile.write("\n")
outputFile.write("\n\n")

# constructing tables
# sorting minimum rtt times
minRTT = []
for address in outputs:
    if len(outputs[address]["rtt_range"]) == 2:
        min = outputs[address]["rtt_range"][0]
        minRTT.append([min, address])
    else:
        continue
sorted(minRTT, key=lambda address: address[0])
# make table
minTable = texttable.Texttable()
minTable.add_row(["address", "time"])
for input in minRTT:
    minTable.add_row([input[1], input[0]])

# root_ca occurences
root_cas = {}
rootTable = texttable.Texttable()
for address in outputs:
    root_ca = outputs[address]["root_ca"]
    if root_ca == []:
        continue
    if root_ca not in root_cas:
        root_cas[root_ca] = 1
    elif root_ca in root_cas:
        root_cas[root_ca] += 1
# sort occurences descending
rootArray = []
for address in root_cas:
    rootArray.append([address, root_cas[address]])
sorted(rootArray,key=lambda address:address[1], reverse=True)
# create table
rootTable.add_row(["root certificate authority", "occurences"])
for index in rootArray:
    rootTable.add_row([index[0], index[1]])

# web server occurences
http_servers = {}
httpTable = texttable.Texttable()
for address in outputs:
    http_server = outputs[address]["http_server"]
    if http_server not in http_servers:
        http_servers[http_server] = 1
    elif http_server in http_servers:
        http_servers[http_server] += 1
# sort occurences descending
httpArray = []
for address in http_servers:
    httpArray.append([address, http_servers[address]])
sorted(rootArray, key=lambda address:address[1], reverse=True)
# create table
httpTable.add_row(["http server name", "occurences"])
for index in httpArray:
    httpTable.add_row([index[0], index[1]])

# percentage of scanned domains
percent_table = texttable.Texttable()

total_val = float(len(outputs.keys()))

tls_version_10 = 0
tls_version_11 = 0
tls_version_12 = 0
tls_version_13 = 0
insecure_http = 0
redirect = 0
hsts = 0
ipv6 = 0

for address in outputs:
    tls_versions = outputs[address]['tls_versions']
    if 'TLSv1.0' in tls_versions:
        tls_version_10 += 1
    
    if 'TLSv1.1' in tls_versions:
        tls_version_11 += 1
    
    if 'TLSv1.2' in tls_versions:
        tls_version_12 += 1
    
    if 'TlSv1.3' in tls_versions:
        tls_version_13 += 1

    secure = outputs[address]['insecure_http']
    if secure:
        insecure_http += 1

    redirection = outputs[address]['redirect_to_https']
    if redirection:
        redirect += 1

    hsts_support = outputs[address]['hsts']
    if hsts_support:
        hsts += 1

    ipv6_info = outputs[address]['ipv6_addresses']
    if len(ipv6_info) != 0:
        ipv6 += 1

headers = ['Type', 'Percentage']
row1 = ['TLSv1.0', "{:.3f}".format(100 * tls_version_10 / total_val) + '%']
row2 = ['TLSv1.1', "{:.3f}".format(100 * tls_version_11 / total_val) + '%']
row3 = ['TLSv1.2', "{:.3f}".format(100 * tls_version_12 / total_val) + '%']
row4 = ['TLSv1.3', "{:.3f}".format(100 * tls_version_13 / total_val) + '%']
row5 = ['Insecure_Http', "{:.3f}".format(100 * insecure_http / total_val) + '%']
row6 = ['Redirect to Https', "{:.3f}".format(100 * redirect / total_val) + '%']
row7 = ['Hsts', "{:.3f}".format(100 * hsts / total_val) + '%']
row8 = ['IPV6', "{:.3f}".format(100 * ipv6/ total_val) + '%']
percent_table.add_rows([headers, row1, row2, row3, row4, row5, row6, row7, row8])

# drawing tables
outputFile.write("\n")
outputFile.write(minTable.draw())
outputFile.write("\n\n")
outputFile.write(rootTable.draw())
outputFile.write("\n\n")
outputFile.write(httpTable.draw())
outputFile.write("\n\n")
outputFile.write(percent_table.draw())



    

