# -*- coding: utf-8 -*-


import os
import scrapy

from hscrapy.settings import DEST_DIR
import json

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


def titles_handler_normal(table):

	lastTrain = []

	items = table.xpath("thead/tr/td")[2:]

	for item in items:
		value = item.xpath("text()").extract()[0]
		timeTable = {
			"direction": value
		}

		lastTrain.append(timeTable)

	return lastTrain


timeTableSettings = {
	"1号线": {
		"timeFunc": timetable_handler_normal,
		"titleFunc": titles_handler_normal,
	},
}

def getTimeFunction(lineName):
	settings = timeTableSettings.get(lineName)
	if (not settings):
		return timetable_handler_normal
	else:
		return settings["timeFunc"]


def getTitleFunction(lineName):
	settings = timeTableSettings.get(lineName)
	if (not settings):
		return titles_handler_normal
	else:
		return settings["titleFunc"]


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


	def processTimeTable(self, time_tables, line, timeTitles):

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

			timeHandler = getTimeFunction(line["name"])
			if (timeHandler):
				timeHandler(timeValues, lastTrain, timeTitles)


	def findLine(self, lineName):

		for line in self.lines:
			if (line["name"] == lineName):
				return line
		return None

	def getTitles(self, table, lineName):

		titleHandler = getTitleFunction(lineName)
		if (titleHandler):
			return titleHandler(table)
		else:
			return []

	def parseTimeTable(self, response):

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.getLineName(head)
			self.log(lineName)

			titles = self.getTitles(table, lineName)

			line = self.findLine(lineName)
			if (not line):
				self.log("got line error for %s" % lineName)
				continue

			time_tables = table.xpath("tbody")[0]
			self.processTimeTable(time_tables, line, titles)

		self.write()


	def processDistance(self, distances, line):
		lastStationName = "NotSet"
		stationId = 1
		for disItem in distances:
			th = disItem.xpath("th")[0]
			names = th.xpath("text()").extract()[0].split("—")
			stationName = names[0].replace(" ", "")
			lastStationName = names[-1].replace(" ", "")

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
		return td.xpath("text()").extract()[0].split("线")[0] + "线"

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
