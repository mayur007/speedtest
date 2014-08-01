speedtest
=========

speedtest data logger

#Objective: 

Gets all server list from speedtest.net. Runs speed test on each of them from your nearest speedtest server and writes the result (servername, serverID,downloadspeed,uploadspeed,latency,distanceinKM) to a csv file.

#Requirements:
requires python speedtest-cli installed
'pip install speedtest-cli'

refer:https://github.com/sivel/speedtest-cli

#Installation & Execution:
Change default("speedtest_data.csv") CSV filename
python speedtest_parsing.py
