import os
import sys
import json
import signal

import time
import subprocess
import re

import http.client
import requests

import maxminddb

import traceback

# get inputs
if len(sys.argv) != 3:
    print("wrong inputs!")
    sys.exit(1)

with open(sys.argv[1]) as reader:
    inputs = str(reader.read()).splitlines()
print(inputs)

types = (   "scan_time", "ipv4_addresses", "ipv6_addresses", 
            "http_server", "insecure_http", "redirect_to_https",
            "hsts", "tls_versions", "root_ca", "rdns_names",
            "rtt_range", "geo_locations")
outputs = {}
for input in inputs:
    outputs[input] = {}
    for scanner in types:
        outputs[input][scanner] = []

#Define all types of TLS
tls_versions = {}
tls_versions['TLSv1.0'] = '-tls1'
tls_versions['TLSv1.1'] = '-tls1_1'
tls_versions['TLSv1.2'] = '-tls1_2'
tls_versions['TLSv1.3'] = '-tls1_3'

# creating public dns resolvers array
public_dns_resolvers = []
with open("public_dns_resolvers.txt") as reader:
    public_dns_resolvers = str(reader.read()).splitlines()

#Grab this
reader = maxminddb.open_database('GeoLite2-City.mmdb')

for address in inputs:
    print('address is ' + address)

    # 0 scan time          - int or floating point
    outputs[address]["scan_time"] = time.time()

    # 1 ipv4 address       - ipv4 address and 
    # 2 ipv6 address       - ipv6 address
    for dns_resolver in public_dns_resolvers:
        # check if nslookup is actually on the computer
        try:
            result = subprocess.check_output(["nslookup", address, dns_resolver], timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
        except:
            print("problem with nslookup and " + address + " and " + dns_resolver)
            continue
        # parsing result
        parse = result.split("Non-authoritative answer:\n")[1]
        parse = parse.split("\n")
        for line in parse:
            if "Name:" in line or "canonical name" in line or line == "":
                continue
            line = line.lstrip("Address: ")
            line.rstrip("\n")
            # ipv4
            if ":" not in line:
                if line not in outputs[address]["ipv4_addresses"]:
                    outputs[address]["ipv4_addresses"].append(line)
            # ipv6
            elif line not in outputs[address]["ipv6_addresses"]:
                outputs[address]["ipv6_addresses"].append(line)
    
    #3 http_server        - string or null
    try:
        redirect = False
        status_code = 0
        result = subprocess.check_output(['curl', '-I', address], timeout=2).decode("utf-8")
        
        headers_arr = result.split('\n')
        server_name = None
        status_code = headers_arr[0].split(' ')[1]
        
        for elem in headers_arr:
            if len(elem) >= 10:
                if elem[0:7] == 'Server:' or elem[0:7] == 'server:':
                    server_name = elem[8:]
                    outputs[address]['http_server'] = server_name[:-1]
                    break
        
        if server_name is None and status_code[0] == 3:
                print('redirecting')
                new_location = ''
                for elem in headers_arr:
                    if len(elem) >= 16:
                        if elem[0:9] == 'Location:' or  elem[0:9] == 'location:':
                            new_location = elem[10:]
                            new_location = new_location[:-1]
                
                for i in range(9):
                    result = subprocess.check_output(['curl', '-I', new_location], timeout=2).decode("utf-8")
                    headers_arr = result.split('\n')
                    status_code = headers_arr[0].split(' ')[1]
                    
                    for elem in headers_arr:
                        if len(elem) >= 10:
                            if elem[0:7] == 'Server:' or elem[0:7] == 'server:':
                                server_name = elem[8:]
                                outputs[address]['http_server'] = server_name[:-1]
                                break
                    
                    if server_name is None:
                        for elem in headers_arr:
                            if len(elem) >= 16:
                                if elem[0:9] == 'Location:' or  elem[0:9] == 'location:':
                                    new_location = elem[10:]
                                    new_location = new_location[:-1]
                                    break
                    else:
                        break

    except:
        print('touch')
        outputs[address]['http_server'] = None
    if(outputs[address]['http_server'] == []):
        outputs[address]['http_server'] = None
    print('server is ')
    print(outputs[address]['http_server'])
    
    # 4 insecure_http      - boolean
    insecure_http = True
    try:
        headers = {'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.9', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
        connection = http.client.HTTPConnection(address, timeout=2)
        connection.request("GET", "/", headers=headers)
        response = connection.getresponse()
    except Exception as e:
        print(e)
        insecure_http = False
        traceback.print_exc() 

    outputs[address]["insecure_http"] = insecure_http
    print('insecure http is ' + str(insecure_http))


    
    # 5 redirect_to_https  - string or false
    try:
        result = subprocess.check_output(['curl', '-I', address], timeout=2).decode("utf-8")
        headers_arr = result.split('\n')
        status_code = headers_arr[0].split(' ')[1]
        done = False
        for i in range(10):
            if status_code[0] == '3':
                for elem in headers_arr:
                    if len(elem) >= 16:
                        if elem[0:9] == 'Location:' or  elem[0:9] == 'location:':
                            new_location = elem[10:]
                            new_location = new_location[:-1]
                            if new_location[0:5] == 'https':
                                outputs[address]['redirect_to_https'] = True
                                done = True
                                break
                if done:
                    break
                else:
                    print('new location is ' + new_location)
                    result = subprocess.check_output(['curl', '-I', new_location], timeout=2).decode("utf-8")
                    headers_arr = result.split('\n')
                    status_code = headers_arr[0].split(' ')[1]

            else:
                outputs[address]['redirect_to_https'] = False
                break
        
        if not done:
            outputs[address]['redirect_to_https'] = False
    except Exception as e:
        print(e)
        outputs[address]['redirect_to_https'] = False
    
    # 6 hsts               - boolean
    hsts = False
    try:
        result = subprocess.check_output(['curl', '-I', address], timeout=2).decode("utf-8")
        headers_arr = result.split('\n')
        status_code = headers_arr[0].split(' ')[1]
        
        for i in range(10):
            for elem in headers_arr:
                    if len(elem) >= 25:
                        if elem[0:24] == 'strict-transport-security':
                            hsts = True
                            break
        i = 9
        while not hsts and status_code[0] == '3' and i > 0:
            print('here')
            i -= 1
            
            #Find new location
            new_location = ''
            for elem in headers_arr:
                if len(elem) >= 16:
                    if elem[0:9] == 'Location:' or  elem[0:9] == 'location:':
                        new_location = elem[10:]
                        new_location = new_location[:-1]
                        break

            print('new location is ' + new_location)
            result = subprocess.check_output(['curl', '-I', new_location], timeout=2).decode("utf-8")
            headers_arr = result.split('\n')
            status_code = headers_arr[0].split(' ')[1]
            #print(headers_arr)
            for elem in headers_arr:
                if len(elem) >= 25:
                    if elem[0:25] == 'strict-transport-security':
                        hsts = True
                        break

    except Exception as e:
        print(e)

    outputs[address]['hsts'] = hsts
    print('hsts is ')
    print(hsts)
    
    # 7 tls_versions       - array
    print('Starting TLS Vetsion analysis')
    tls_connects = []
    for version, command in tls_versions.items():
        try:
            result = subprocess.check_output(['openssl', 's_client', command, '-connect', address + ':443'], input = b'', timeout=2).decode("utf-8")
            search_arr = result.split('\n')
            for elem in search_arr:
                if len(elem) > 20 and elem[:20] == 'Secure Renegotiation':
                    if 'NOT' in elem[20:] or 'not' in elem[20:]:
                        break
                    else:
                        tls_connects.append(version)
                        break
        except Exception as e:
            print(e)
    outputs[address]['tls_versions'] = tls_connects

    # # 8 root_ca            - string
    result = None
    command = f"echo | openssl s_client -connect {address}:443"
    start = time.monotonic()
    with subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, preexec_fn=os.setsid) as process:
        try:
            result = process.communicate(timeout=1)[0].decode("utf-8")
        except subprocess.TimeoutExpired:
            print("failure to get root ca from " + address)
            os.killpg(process.pid, signal.SIGINT) # send signal to the process group
    if result != None:
        if not ("No client certificate" in result or "Certificate chain" not in result):
            certChain = result.split("Certificate chain\n")[0]
            depths = certChain.split("depth=")
            print("\n\n\n")
            print(depths)
            maxdepth = depths[1]
            orgName = maxdepth.split("O = ")[1].split(",")[0]
            outputs[address]["root_ca"] = orgName
            print("root ca for " + address + " is " + orgName)
    else:
        outputs[address]["root_ca"] = None
    
    # 9 rdns_names         - array
    ipv4list = outputs[address]['ipv4_addresses']
    print(ipv4list)
    rdns_names = []
    for ipv4 in ipv4list:
        print('trying this ipv4 ' + ipv4)
        try:
            result = subprocess.check_output(['nslookup',  ipv4], timeout=2).decode("utf-8")
            search_arr = result.split('\n')
            for line in search_arr:
                if 'name = ' in line:
                    index = line.find('name = ')
                    if len(line) >= index + 8:
                        res = line[index + 7:]
                        rdns_names.append(res)
        except Exception as e:
            print(e)
    outputs[address]['rdns_names'] = rdns_names
    print(rdns_names)
    
    # 10 rtt_range          - [min, max]
    min = 5000
    max = 0
    for ipv4 in outputs[address]["ipv4_addresses"]:
        rtttime = 0
        # checking times
        command22 = f"sh -c \"time echo -e \'\\x1dclose\\x0d\' | telnet {ipv4}\""
        command80 = f"sh -c \"time echo -e \'\\x1dclose\\x0d\' | telnet {ipv4} 80\""
        command443 = f"sh -c \"time echo -e \'\\x1dclose\\x0d\' | telnet {ipv4} 443\""
        # checks on port 443
        start = time.monotonic()
        with subprocess.Popen(command443, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, preexec_fn=os.setsid) as process:
            try:
                runCommand = process.communicate(timeout=1)[0].decode("utf-8")
            except subprocess.TimeoutExpired:
                print("rtt timeout with " + ipv4 + " and port 443")
                os.killpg(process.pid, signal.SIGINT) # send signal to the process group
                runCommand = None
        # check port 80
        if runCommand == None:
            start = time.monotonic()
            with subprocess.Popen(command80, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, preexec_fn=os.setsid) as process:
                try:
                    runCommand = process.communicate(timeout=1)[0].decode("utf-8")
                except subprocess.TimeoutExpired:
                    print("rtt timeout with " + ipv4 + " and port 80")
                    os.killpg(process.pid, signal.SIGINT) # send signal to the process group
                    runCommand = None
        # check port 22
        if runCommand == None:
            start = time.monotonic()
            with subprocess.Popen(command22, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, preexec_fn=os.setsid) as process:
                try:
                    runCommand = process.communicate(timeout=1)[0].decode("utf-8")
                except subprocess.TimeoutExpired:
                    print("rtt timeout with " + ipv4 + " and port 22")
                    os.killpg(process.pid, signal.SIGINT) # send signal to the process group
                    continue
        strTime = str(runCommand).split("real\t")[1].split("\nuser")[0]
        timeArray = strTime.split("s")[0].split("m")
        # we want time in seconds
        rtttime = float(timeArray[0]) * 60 + float(timeArray[1])
        # updating min max
        if rtttime < min:
            min = rtttime
        if rtttime > max:
            max = rtttime
    if min == 5000 and max == 0:
        print("rtt range of " + address + " failed")
        outputs[address]["rtt_range"] = [None]
    else:
        outputs[address]["rtt_range"] = [min, max]
        print("printing rtt of " + address)
        print(outputs[address]["rtt_range"])
    
    # 11 geo_locations      - array of strings
    locations = []
    for ipv4 in ipv4list:
        print('trying ' + ipv4)
        try:
            city = ''
            country = ''
            state = ''
            result = reader.get(ipv4)
            is_city = False
            is_country = False
            is_state = False
            if 'city' in result:
                city = result['city']['names']['en']
                is_city = True           
            if 'country' in result:
                country = result['country']['names']['en']
                is_country = True          
            try:
                if 'subdivisions' in result:
                    state = result['subdivisions'][0]['names']['en']
                    is_state = True
            except:
                print('oh no, not good!')
            location_string = ''
            if is_city:
                location_string += city + ', '
            if is_state:
                location_string += state + ', '
            if is_country:
                location_string += country + ', '
            if location_string == '':
                continue
            final_string = location_string[:-2]           
            if final_string not in locations:
                locations.append(final_string)
        except Exception as e:
            print(e)
    outputs[address]['geo_locations'] = locations
    print('locations are ')
    print(locations)

# output to stuff
outputData = open(sys.argv[2], 'w')
# write data
json.dump(outputs, outputData)

#end the reader
reader.close()

sys.exit(0)