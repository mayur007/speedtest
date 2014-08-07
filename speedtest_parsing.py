import os
import re
import csv
import subprocess
import time

filename = "speedtest_data.csv"
format = re.compile('\d+(?:\.\d+)?') #format to verify only numbers
_digits = re.compile('\d')

def contains_digits(d):
    #check if string has digits
    return bool(_digits.search(d))

def csv_writer(data, path):
    '''
    	Write data to a CSV file path: 
  	format: servername, serverID,downloadspeed,upload,latency,distanceinKM
    '''
    path = path +"_"+str(time.time())
    with open(path, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

def get_testdata(server, name):
    #get download,upload,latency,distance for each server
    print "server", server
    command = 'speedtest-cli --server '
    command = command + str(server)
    result = os.popen(command).read()

    result_list = result.split(':')
    download = format.findall(result_list[3])[0].strip(' ')
    upload = format.findall(result_list[2])[0].strip(' ')
    latency = format.findall(result_list[1])[0].strip(' ')
    distance = format.findall(result_list[0])[2]
    data = [name,server,download,upload,latency,distance]
    csv_writer(data,filename)
    print "Server %s is away from Bristol at %s km and has Download speed %s upload speed %s and latency %s" % (server, distance,download,upload,latency)

def main():
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
	#print "name", name
	for idx,val in enumerate(server):  
	  print "Fetching data for server id %s and name %s" %(val, name[idx])
	  if contains_digits(val):
	    get_testdata(val,name[idx])

if __name__ == "__main__":
  main()
    
