# -*- coding: utf-8 -*-


import os
import scrapy

from hscrapy.settings import DEST_DIR
import json

from hscrapy.utils.commonUtil import transToStr


TIME_TABLE_TYPE_NORMAL = {}


timeTableSettings = {
	"1号线": TIME_TABLE_TYPE_NORMAL,
}


def getParseType(lineName):
	return timeTableSettings.get(lineName) or TIME_TABLE_TYPE_NORMAL


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


	def processTimeTable(self, time_tables, line, lastTrain):

		items = time_tables.xpath("tr")
		for item in items:
			stationTable = item.xpath("th")[0]
			stationName = stationTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")

			station = self.findStation(line, stationName)
			if (not station):
				self.log("got station from line error %s" % stationName)
				continue

			station["lastTrain"] = lastTrain

			timeValues = item.xpath("td")
			columes = len(lastTrain)

			index = 0
			for timeTable in timeValues:
				timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
				position = index / columes
				lastTrain[position]["first"] = timeValue
				index += 1

	def findLine(self, lineName):

		for line in self.lines:
			if (line["name"] == lineName):
				return line
		return None

	def getTitles(self, table, lineName):

		lastTrain = []

		settingType = getParseType(lineName)
		if (settingType == TIME_TABLE_TYPE_NORMAL):
			items = table.xpath("thead/tr/td")[2:]
		else:
			items = table.xpath("thead/tr/td")[2:]

		for item in items:
			value = item.xpath("text()").extract()[0]
			self.log(value)
			timeTable = {
				"direction": value
			}

			lastTrain.append(timeTable)

		return lastTrain

	def parseTimeTable(self, response):

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.getLineName(head)
			self.log(lineName)

			titles = self.getTitles(table, lineName)

			line = self.findLine(lineName)

			time_tables = table.xpath("tbody")[0]
			self.processTimeTable(time_tables, line, titles)

		self.write()


	def processDistance(self, distances, line):
		lastStationName = "NotSet"
		stationId = 1
		for disItem in distances:
			th = disItem.xpath("th")[0]
			names = th.xpath("text()").extract()[0].split("—")
			stationName = names[0]
			lastStationName = names[-1]

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
