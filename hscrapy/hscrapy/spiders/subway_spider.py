# -*- coding: utf-8 -*-


import os
import scrapy

from hscrapy.settings import DEST_DIR
from hscrapy.utils.commonUtil import transToStr



def timetable_handler_normal(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	valueCount = len(values)

	if (not titleCount):
		return

	valuesPerLine = valueCount / titleCount

	if (titleCount != valuesPerLine):
		print("count not match[%d:%d]" % (titleCount, valuesPerLine))
		return

	for i in range(0, valuesPerLine):
		item = {
			"direction": titles[i]["direction"],
			"first": values[i * 2],
			"last": values[i * 2 + 1]
		}
		lastTrain.append(item)

def timetable_handler_line13(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	valueCount = len(values)

	if (not titleCount):
		return

	valuesPerLine = valueCount / titleCount

	for i in range(0, titleCount):
		item = {
			"direction": titles[i]["direction"],
			"first": values[i * 2],
			"last": values[i * 2 + 1]
		}
		lastTrain.append(item)


timeTableSettings = {
	u"1号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往四惠东方向"
			},
			{
				"direction": u"往苹果园方向",
			}
		],
	},
	u"5号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往天通苑北方向",
			},
			{
				"direction": u"往宋家庄方向"
			}
		],
	},
	u"7号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往北京西站方向",
			},
			{
				"direction": u"往焦化厂站方向"
			}
		],
	},
	u"8号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往南锣鼓巷方向",
			},
			{
				"direction": u"往朱辛庄方向"
			}
		],
	},
	u"9号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往郭公庄方向",
			},
			{
				"direction": u"往国家图书馆方向"
			}
		],
	},
	u"13号线": {
		"func": timetable_handler_line13,
		"titles": [
			{
				"direction": u"往西直门（全程）方向",
			},
			{
				"direction": u"往东直门（全程）方向",
			},
			{
				"direction": u"往西直门（霍营区间）方向",
			},
			{
				"direction": u"往东直门（回龙观区间）方向",
			}
		],
	},
	u"八通线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往土桥",
			},
			{
				"direction": u"往四惠"
			}
		],
	},
	u"房山线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往苏庄方向",
			},
			{
				"direction": u"往郭公庄方向"
			}
		],
	},
	u"亦庄线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往次渠方向",
			},
			{
				"direction": u"往宋家庄方向"
			}
		],
	},
	u"机场线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往市区",
			},
			{
				"direction": u"往机场"
			}
		],
	},
}

def getTimeTableSettings(lineName):
	return timeTableSettings.get(lineName)

class SubwaySpider(scrapy.Spider):

	name = "subway"

	lineId = 0

	dist_file = DEST_DIR + os.sep + "subway.json"

	lines = []

	url_timetable = "http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"
	url_disance = "http://www.bjsubway.com/station/zjgls/"


	def write(self):

		fd = open(self.dist_file, "w+")
		if (fd):
			fd.write(transToStr(self.lines, indent=2))
			fd.close()


	def start_requests(self):

		yield scrapy.http.Request(url=self.url_disance, callback=self.parseDistance)

		yield scrapy.http.Request(url=self.url_timetable, callback=self.parseTimeTable)

		self.write()

	def findStation(self, line, stationName):
		for station in line["stations"]:
			if station["name"] == stationName:
				return station
		return None


	def processTimeTable(self, time_tables, line, timeTableSettings):

		items = time_tables.xpath("tr")
		for item in items:
			lastTrain = []

			stationTable = item.xpath("th")[0]
			stationName = stationTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")

			station = self.findStation(line, stationName)
			if (not station):
				self.log("got station from line error [%s]" % stationName)
				continue

			station["lastTrain"] = lastTrain

			timeValues = item.xpath("td")

			timeHandler = timeTableSettings["func"]
			if (timeHandler):
				timeHandler(timeValues, lastTrain, timeTableSettings["titles"])
				line["timeTableDesc"] = timeTableSettings.get("desc") or ""


	def findLine(self, lineName):

		for line in self.lines:
			if (line["name"] == lineName):
				return line
		return None


	def parseTimeTable(self, response):

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.getLineName(head)
			self.log("line name [%s]" % lineName)

			line = self.findLine(lineName)
			if (not line):
				self.log("got line error for %s" % lineName)
				continue

			time_tables = table.xpath("tbody")[0]

			timeTableSettings = getTimeTableSettings(lineName)
			if (timeTableSettings):
				self.processTimeTable(time_tables, line, timeTableSettings)

		self.write()


	def processDistance(self, distances, line):
		lastStationName = "NotSet"
		stationId = 1
		for disItem in distances:
			th = disItem.xpath("th")[0]
			names = th.xpath("text()").extract()[0].split("—")
			stationName = names[0].replace("\r", "").replace("\r", "").replace(" ", "")
			lastStationName = names[-1].replace("\r", "").replace("\r", "").replace(" ", "")

			if (line["name"] == u"机场线"):  # to process name conflict
				stationName = stationName.replace("T2", "2号").replace("T3", "3号")
				lastStationName = lastStationName.replace("T2", "2号").replace("T3", "3号")

			distance = disItem.xpath("td/text()").extract()[0]
			station = {
				"id": line["id"] * 1000 + stationId,
				"name": stationName,
				"length": int(distance)
			}
			line["stations"].append(station)
			self.log("name: %s: %d" % (stationName.encode("utf-8"), int(distance)))

			stationId += 10

		if (line["stations"][0]["name"] == lastStationName): # this is a circle line
			line["stations"][-1]["endCircle"] = True
		else:
			station = {
				"id": line["id"] * 1000 + stationId,
				"name": lastStationName,
				"length": 0
			}
			line["stations"].append(station)

	def getLineName(self, td):
		lineValue = td.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		lineName = lineValue.split(u"线")[0] + u"线"
		if (lineName == u"14号线"):
			if (lineValue.find(u"东") > 0):
				lineName += u"东段"
			else:
				lineName += u"西段"

		return lineName

	def parseDistance(self, response):

		#self.log(response.body)

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.getLineName(head)
			self.log(lineName)

			self.lineId += 1

			line = {
				"name": lineName,
				"id": self.lineId,
				"stations": []
			}
			self.lines.append(line)

			distances = table.xpath("tbody/tr")
			self.processDistance(distances, line)


		self.write()
