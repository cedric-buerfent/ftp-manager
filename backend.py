#!/usr/bin/python
# -*- coding: utf-8 -*-

#Library web.py for python Webserver
import web
#Systemcall library
import os

import string
import re

import time
import datetime

import traceback #for debug
import sys

import codecs #utf-8
import io
#javascript object notation library write and read
import json

#For windows we do:
#cd C:\programmieren\PYTHON\200625_PYYAML_GRAFANA
#call venv\Scripts\activate.bat
#python backend.py 8081

# ----  every html Homepage gets a branch. There a class is named:
urls = (	
	'/', 'test',
	'/test/index.html', 'test',
	'/launch_command1','launch_command1',
	'/list_userhomes','list_userhomes'
)
 
#classname given by tree entry
class test:
	# class simply returns a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')
		
		#get client IP
		client_IP = web.ctx['ip']

		#return '{"Command":"GET","RES":"[OK] Test fine!"}'
		return '{"Command":"GET","RES":"[OK] Test fine!","IP":"'+client_IP+'"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
	
	# --------------------- POST ------------------------------------
	def POST(self):
		#server side allow Cross Origin queries		
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')

		print(web.input())
		
		#return json text MIME
		web.header('Content-Type', 'application/json')
		
		return '{"Command":"POST","Say":"Test OK!"}'
		
#classname given by tree entry
class launch_command1:
# class simply returns a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

		#web.header('Content-Security-Policy: img-src','self')
        
		#return json text MIME
		web.header('Content-Type', 'application/json')

				
		#get client IP
		client_IP = web.ctx['ip']
		#create a cache file to output the systemcall result into
		#           listuserhomes_127.0.0.1.txt
		filename = "listuserhomes_"+client_IP+".txt"
		
		#launch systemcall and write overall status in status
		status = ""
		status = listuserhomes(filename)
		print("[INFO] Syscall says: "+status)
				
		#read back result filed cleaned into memory
		lines_cleaned = []
		lines_cleaned = readfile_cleaned_into_memory(filename)
		
						
		#construct associative array for json string
		d = {}		
		#d = {"file":"test.txt"}
		#d={"file":"test.txt","lines":["1","2","3"]}
		d["file"] = filename
		d["lines"] = lines_cleaned
		#last line contains executed script overall result status like OK BAD WARN
		#e.g. [OK] Homes listes! We may adapt script result mappings here.
		overallstatus = d["lines"][-1]
		if "OK" in overallstatus:
			d["result"] = "OK"
		elif "BAD" in overallstatus:
			d["result"] = "BAD"
		else:
			d["result"] = "WARNING"
		 							
		#construct our json string		
		json_return = ""
		#converts our associative array to a json string
		json_return=json.dumps(d)		
		return json_return

# ---------------------   List Users with Homedir ---------------------------
#     Parameters: (none)
#     Result: json with: e.g.
#     ..."102;monatsheft;/data/ftp/quota_transfert/monatsheft;True"
# ---------------------   List Users with Homedir ---------------------------
#classname given by tree entry
class list_userhomes:
# class simply returns a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

		#web.header('Content-Security-Policy: img-src','self')
        
		#return json text MIME
		web.header('Content-Type', 'application/json')
				
		#get client IP
		client_IP = web.ctx['ip']
		#create a cache file to output the systemcall result into
		#   e.g.    listuserhomes_127.0.0.1.txt
		filename = "listuserhomes_"+client_IP+".txt"
		
		#launch systemcall and write syscall status in status
		status = ""
		status = listuserhomes(filename)
		print("[INFO] Syscall says: "+status)
				
		#read back result filed cleaned into memory
		lines_cleaned = []
		lines_cleaned = readfile_cleaned_into_memory(filename)
								
		#construct associative array for json string
		d = {}				
		#syntax like d={"file":"test.txt","lines":["1","2","3"]}
		d["file"] = filename
		d["lines"] = lines_cleaned
		#last line contains executed script overall result status like OK BAD WARN
		#e.g. [OK] Homes listes! 
		#We may adapt script result mappings here:
		overallstatus = d["lines"][-1]
		if "OK" in overallstatus:
			d["result"] = "OK"
		elif "BAD" in overallstatus:
			d["result"] = "BAD"
		else:
			d["result"] = "WARNING"
		 							
		#construct our json string		
		json_return = ""
		#converts our associative array to a json string
		json_return=json.dumps(d)		
		return json_return		
					
		
# ---------------------------   global functions ----------------------------
def readfile_into_memory(aFileName):
	temporary=[]
	try:
		#read rawfile into temp array
		f = open(aFileName)		
		temporary=f.readlines()
		f.close()
	except:					
		print("[BAD] File read problem for "+aFileName)
		traceback.print_exc(file=sys.stdout)
		#return empty array in this case
		return []			
	#epure
	lines=[]
	for l in temporary:
		if l == None or l == "" or l == "\n":
			#nop
			pass
		else:
			l2 = l.rstrip()
			lines.append(l2)
	return lines
	
#takes a string and returns any value cleaned of bad characters		
def removeNonAscii(s):
        s2=""
        for i in s:
                if ord(i) < 128:
                        s2 +=i
                else:
                        s2 +='_'
        return s2
        
def readfile_cleaned_into_memory(aFileName):
	#read back result file into memory
	lines = []
	lines = readfile_into_memory(aFileName)
				
				
	# -- repair bad chars for json		
	lines_cleaned = []
	for i in lines:
		try:
			s = ""
			s = json-dumps(i)
			lines_cleaned.append(s)
		except:
			s = ""
			s = removeNonAscii(i)
			lines_cleaned.append(s)
		#convert cleaned array to json
		#json_return=json.dumps(lines_cleaned)
		#print json_return
	return lines_cleaned
		

# ---------------------------------------------------------------------------
# System Call Function: Returns the output of the call
# via a tmp.txt file
# ---------------------------------------------------------------------------
def aexec_command(aCommand,tempfile):
	global script_cachefolder
	#global script_syscall
	#tmp_txt = script_cachefolder + "tmp.txt"
	#print tmp_txt
	try:
		tmp_txt = tempfile	
		#cmd = "dir > tmp.txt"
		#cmd = "%s"%aCommand
		#system(aCommand+" > tmp.txt")
		#os.system(aCommand+" >"+ tmp_txt + " 2>&1")
		os.system(aCommand+" >"+ tmp_txt)
		afile = open(tmp_txt)
		data=afile.read()
		afile.close()
		data_lines=[]
		data_lines = data.split("\n")
		#for e in data_lines:
		#	print e
		return data_lines
	except:
		print("error in systemcall "+aCommand)
		traceback.print_exc(file=sys.stdout)
		data_lines=[]
		return data_lines
		
def listuserhomes(Logfile):
	print("[INFO] executing systemcall")
	results = []
	aOS = os.name
	if re.compile("posix").search(aOS.lower()):
		#Linux
		print("[INFO] [Linux] OS found.")
		#results = aexec_command("/root/bin/configcheck.sh 2>&1|tee ","CACHE/configcheck.txt")
	elif re.compile("nt").search(aOS):	
		#Windows
		print("[INFO] [Windows] OS found.")
		#results = aexec_command("configcheck_prometheus.bat","CACHE/configcheck.txt")
		#results = aexec_command("launch.bat","CACHE/out.txt")
		#results = aexec_command("launch.bat",Logfile)
		results = aexec_command("win_listuserhomes.bat",Logfile)
		if isinstance(results,list):
			return "OK"
		else:
			return "BAD"
	else:
		#NOP
		pass
		print("[INFO] [UNKNOWN OS]")
	#return results
	return "UNKNOWN"


		
	
		
		
if __name__ == "__main__":
	#to launch functions without webserver
	simulate = False
	if simulate:
		#Test class
		#a = index()		
		#print c.file_lines
		#print a.convert_array_to_big_jsonstring(c.file_lines)
		print("simulate standalone mode")	
				
	else:
		#Start Webservice
		app = web.application(urls, globals())
		#change port via: python app.py 8081
		app.run()
		#Test Windows: http://127.0.0.1:8080/		

