#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import socket
import struct
import uuid
from hashlib import md5 as MD5

import time

from hscrapy.utils.timeUtil import get_current_time


def listFiles(fileDir, keyword=None):
	fileList = []

	for file in os.listdir(fileDir):
		if (not os.path.isdir(file) and (not keyword or file.find(keyword) != -1)):
			fileList.append(file)

	return fileList


def ip2long(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]


def removeFile(filepath):
	if (filepath == None or os.path.exists(filepath) == False):
		return

	os.remove(filepath)


def transToObj(string):
	if (string == None):
		return None

	if (type(string) != type("a") and type(string) != type('a')):
		string = string.encode()

	if (len(string) < 2):
		return None

	try:
		obj = json.loads(string, encoding="utf-8")
	except:
		obj = { }

	return obj


def tryToDump(string):
	if (string == None):
		return { }

	if (type(string) != type("a")):
		string = string.encode()

	if (len(string) < 2):
		return { }

	try:
		obj = json.loads(string)
	except:
		obj = string

	return json.dumps(obj, sort_keys=True, indent=4)


def isSystemWindows():
	import platform
	if (platform.system() == "Windows"):
		return True
	else:
		return False


def transToStr(obj, indent=False):
	if (indent != False):
		return json.dumps(obj, ensure_ascii=False, indent=indent)
	else:
		return json.dumps(obj, ensure_ascii=False)


def oct_trim(inStr):
	segs = inStr.split(" ")
	result = ""

	for seg in segs:
		if (seg == ''):
			continue
		result += seg
		result += " "

	return result.rstrip()


def OCT_SYSTEM(formatStr, arg=None):
	TEMPFILE_NAME = "/tmp/OCTTEMP_FILE_%ld%s" % (get_current_time(), getUuid())

	if (arg):
		CMD = formatStr % arg
	else:
		CMD = formatStr

	CMD += " > %s" % (TEMPFILE_NAME)
	ret = os.system(CMD)

	fp = open(TEMPFILE_NAME, 'r')
	if (fp == None):
		return (ret >> 8 & 0XFF, None)

	data = fp.read()
	fp.close()
	os.remove(TEMPFILE_NAME)

	if (len(data) == 0):
		return (ret >> 8 & 0XFF, None)

	if (data[-1] == '\n'):
		data = data[:-1]  # to remove last "\n"

	if (len(data) == 0):
		data = None

	return (ret >> 8 & 0XFF, data)


def OCT_PIPERUN(cmd):
	import subprocess

	if (cmd == None):
		return (0, None)

	args = cmd.split()
	p = subprocess.Popen(args, close_fds=True, stdout=subprocess.PIPE,
	                     stderr=subprocess.PIPE, shell=False)
	p.wait()

	ret = p.returncode
	msg = p.stdout.read()

	return (ret, msg)


def getUuid(spilt=None):
	if (spilt):
		return str(uuid.uuid4())
	else:
		x = uuid.uuid4().hex
		return x


def allocVmMac(vmId, nicId):
	m = MD5()
	string = "%s/%s" % (vmId, nicId)
	m.update(string.encode())
	v = m.hexdigest()
	return "e0:%s:%s:%s:%s:%s" % (v[0:2], v[4:6], v[8:10], v[12:14], v[16:18])


def trimUuid(uuid):
	segs = uuid.split("-")
	if (len(segs) != 5):
		return uuid
	return "%s%s%s%s%s" % (uuid[0:8],
	                       uuid[9:13],
	                       uuid[14:18],
	                       uuid[19:23],
	                       uuid[24:36])


def expandUuid(uuid):
	if (uuid[8] == '-'):
		return uuid
	return "%s-%s-%s-%s-%s" % (uuid[0:8],
	                           uuid[8:12],
	                           uuid[12:16],
	                           uuid[16:20],
	                           uuid[20:32])


def jsonStringFormat(objString):
	if (type(objString) == str):
		obj = transToObj(objString)
		toString = objString
	else:
		obj = objString
		toString = transToStr(objString)

	try:
		result = json.dumps(obj, sort_keys=True, indent=2)
	except:
		result = toString

	return result


def fileToObj(filePath):
	if (not os.path.exists(filePath)):
		print(("file %s not exist" % (filePath)))
		return None

	fd = open(filePath, "r")
	if (not fd):
		print(("open file %s error" % (filePath)))
		return None

	obj = transToObj(fd.read())

	fd.close()

	return obj


def isValidJson(string):
	if (string == None):
		return False

	try:
		eval(string)
	except Exception as e:
		return False

	return True


if __name__ == "__main__":
	mac = allocVmMac(getUuid(), "3")
	print(mac)
