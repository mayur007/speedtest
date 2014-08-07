import os
import re
import csv
import subprocess
import sys

format = re.compile('\d+(?:\.\d+)?') #format to verify only numbers
_digits = re.compile('\d')

def contains_digits(d):
    return bool(_digits.search(d))

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

def get_testdata(server, name):

    omit_list = ["4866"]
    print "server", server
    command = 'speedtest-cli --server '
    if server in omit_list:
      return
    command = command + str(server)
    result = os.popen(command).read()
    try:
        result_list = result.split(':')
        download = format.findall(result_list[3])[0].strip(' ')
        upload = format.findall(result_list[2])[0].strip(' ')
        latency = format.findall(result_list[1])[0].strip(' ')
        distance = format.findall(result_list[0])[2]
        data = [name,server,download,upload,latency,distance]
        print "Server %s is away from Bristol at %s km and has Download speed %s upload speed %s and latency %s" % (server, distance,download,upload,latency)
        return data
    except IndexError,e:
        print "index error reading data in get_testdata", e

def get_server_info():
    p2 = subprocess.Popen(["speedtest-cli", "--list"], stdout=subprocess.PIPE)
    rp = p2.communicate()
    prc_data = rp[0].split('\n')
    name = []
    server = []
    #rpp = rp[0].split('\n')
    for data in prc_data:
      tmp = data.split(')')	
      for idx,val in enumerate(tmp):
        if idx == 0:
          server.append(val)
        if idx == 1:
          name.append(val)
    
    return (server, name)

def get_serverid(country,capital):   #def takes country name and capital 
    cmd = "speedtest-cli --list | grep "+ country
    p2 = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    rp = p2.communicate()
    rpout = rp[0].split('\n')
    if rpout is None or rpout[0] == "":
        return None
    for idx,val in enumerate(rpout):
        y = rpout[idx].split(')')
        for yval in y:
            if yval.find(capital)>1:
                return y[0]
            
        return y[0]        
            
def parse_country(countries='countrylist.csv'):  #return dict with {country_name:capital}
    country = {} # dict of country with capital
    with open(countries,'rb') as f:
        reader = csv.reader(f)
        for r in reader:
            country[r[1]] = r[6]  
    return country            
            

def main(countries, csvfile):   
    country = parse_country(countries)
    print "country",country
    for key in country:
        server_id = get_serverid(key, country[key])
        if server_id is None:
            continue
        print "getting data for country %s with capital %s with ID:%s" % (key, country[key], server_id)
        data = get_testdata(server_id, key)
        csv_writer(data,csvfile) 
    
if __name__ == "__main__":
  if len(sys.argv)>2:
    print "fetching country list from %s and storing data in %s" %(sys.argv[1], sys.argv[2])
    main(sys.argv[1],sys.argv[2])
  else:
    print "format is python filename <list of countries.csv> <csvfilename>"
    