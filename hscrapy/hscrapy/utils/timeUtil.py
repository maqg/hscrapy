#!/usr/bin/python
# -*- coding: utf-8 -*-

import time


def get_current_time():
	return int(float(time.time()) * 1000)


def getStrTime(milisecs):
	if (not milisecs):
		return ""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(milisecs) / 1000))


def getStrDate(milisecs):
	if (not milisecs):
		return ""
	return time.strftime("%Y-%m-%d", time.localtime(int(milisecs) / 1000))


def getCurrentStrDate():
	return getStrDate(get_current_time())


def getCurrentStrTime():
	return getStrTime(get_current_time())


def toMiliSeconds(timeStr, format="%Y-%m-%d"):
	if (not timeStr or len(timeStr) == 0):
		return 0

	ts = time.strptime(timeStr, format)
	return int(float(time.mktime(ts)) * 1000)


def howLongAgo(miliSeconds, lang="CN"):
	before = (get_current_time() - miliSeconds) / 1000
	if (before < 0):
		return "发生在未来？"

	if (not miliSeconds):
		return ""

	days = before / 86400
	hours = before / 3600
	minutes = before / 60
	seconds = before

	ago = ""

	if (days):
		ago += "%d 天 " % (days)

	if (hours % 24):
		ago += "%d 小时 " % (hours % 24)

	if (minutes % 60):
		ago += "%d 分钟 " % (minutes % 60)

	if (seconds % 60):
		ago += "%d 秒 " % (seconds % 60)

	ago += "以前"

	return ago


def transDate(dateStr, inteval="-"):
	return inteval.join([dateStr[0:4], dateStr[4:6], dateStr[6:]])
