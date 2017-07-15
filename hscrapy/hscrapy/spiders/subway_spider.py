# -*- coding: utf-8 -*-


import os

import scrapy

from hscrapy.settings import DEST_DIR
from hscrapy.spiders.timetable_settings import getTimeTableSettings
from hscrapy.utils.commonUtil import transToStr

LINE16 = {
    "timeTableDesc": "",
    "stations": [
      {
        "length": 2810,
        "id": 100001,
        "name": "西苑"
      },
      {
        "length": 1520,
        "id": 100011,
        "name": "农大南路"
      },
      {
        "length": 2341,
        "id": 100021,
        "name": "马连洼"
      },
      {
        "length": 2000,
        "id": 100031,
        "name": "西北旺"
      },
      {
        "length": 1299,
        "id": 100041,
        "name": "永丰南"
      },
      {
        "length": 2010,
        "id": 100051,
        "name": "永丰"
      },
      {
        "length": 2420,
        "id": 100061,
        "name": "屯佃"
      },
      {
        "length": 2298,
        "id": 100071,
        "name": "稻香湖路"
      },
      {
        "length": 2615,
        "id": 100081,
        "name": "温阳路"
      },
      {
        "length": 0,
        "id": 100091,
        "name": "北安河"
      }
    ],
    "id": 100,
    "name": "16号线"
  }


class SubwaySpider(scrapy.Spider):
	name = "subway"

	line4Checked = False

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

	def parseStationName(self, item):
		segs = item.xpath("text()").extract()

		return "".join(segs).replace("\r", "").replace("\n", "").replace(" ", "").replace("生物医院", "生物医药")

	def processTimeTable(self, time_tables, line, timeTableSettings):

		items = time_tables.xpath("tr")
		for item in items:
			stationTable = item.xpath("th")
			stationName = self.parseStationName(stationTable[0])

			if (line["name"] == "10号线"):
				stationName2 = self.parseStationName(stationTable[1])
				station2 = self.findStation(line, stationName2)
				lastTrain2 = station2.get("lastTrain") or []
				station2["lastTrain"] = lastTrain2
			elif (line["name"] in ("4号线", "大兴线")):
				stationName2 = self.parseStationName(stationTable[1])
				station2 = self.findStation(line, stationName2)
				if (station2):
					lastTrain2 = station2.get("lastTrain") or []
					station2["lastTrain"] = lastTrain2

			station = self.findStation(line, stationName)
			if (station):
				lastTrain = station.get("lastTrain") or []
				station["lastTrain"] = lastTrain

			timeValues = item.xpath("td")
			timeHandler = timeTableSettings["func"]
			if (timeHandler):
				if (line["name"] == "10号线"):
					if (station):
						timeHandler(timeValues[:4], lastTrain, timeTableSettings["titles"])
					if (station2):
						timeHandler(timeValues[4:], lastTrain2, timeTableSettings["titles"])
				elif (line["name"] in ("4号线", "大兴线")):
					if (station):
						timeHandler(timeValues[:2], lastTrain, timeTableSettings["titles"])
					if (station2):
						timeHandler(timeValues[2:], lastTrain2, timeTableSettings["titles"])
				else:
					if (station):
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

			if (lineName == "4号线"):
				if (self.line4Checked):
					lineName = u"大兴线"
				self.line4Checked = True

			self.log("line name [%s]" % lineName)

			line = self.findLine(lineName)
			if (not line):
				self.log("got line error for %s" % lineName)
				continue

			time_tables = table.xpath("tbody")[0]

			timeTableSettings = getTimeTableSettings(lineName)
			if (timeTableSettings):
				self.processTimeTable(time_tables, line, timeTableSettings)

			if (lineName == "机场线"):
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

		if (line["stations"][0]["name"] == lastStationName):  # this is a circle line
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

		# self.log(response.body)

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

			if lineName == "15号线":
				self.lines.append(LINE16)