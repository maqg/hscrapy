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

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[1],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[1],
		"last": values[4]
	}

	item3 = {
		"direction": titles[3]["direction"],
		"first": values[0],
		"last": values[5]
	}

	for item in (item0, item1, item2,item3):
		lastTrain.append(item)


def timetable_handler_line15(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[3],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_changeping(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[2],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_line2(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[3],
		"last": values[4]
	}

	item3 = {
		"direction": titles[3]["direction"],
		"first": values[3],
		"last": values[5]
	}

	for item in (item0, item1, item2,item3):
		lastTrain.append(item)


def timetable_handler_line4(timeValues, lastTrain, titles):
	pass


def timetable_handler_line6(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[2],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[2],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_line10(timeValues, lastTrain, titles):

	return

	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[3],
		"last": values[4]
	}

	item3 = {
		"direction": titles[3]["direction"],
		"first": values[3],
		"last": values[5]
	}

	item4 = {
		"direction": titles[4]["direction"],
		"first": values[3],
		"last": values[5]
	}

	for item in (item0, item1, item2, item3, item4):
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
				"direction": u"往西直门方向（全程）",
			},
			{
				"direction": u"往东直门方向（全程）",
			},
			{
				"direction": u"往东直门方向（霍营区间）",
			},
			{
				"direction": u"往西直门方向（回龙观区间）",
			}
		],
	},
	u"15号线": {
		"func": timetable_handler_line15,
		"titles": [
			{
				"direction": u"往清华东路西口方向（全程）",
			},
			{
				"direction": u"往清华东路西口方向（半程,终点马泉营）",
			},
			{
				"direction": u"往俸伯方向",
			}
		]
	},
	u"昌平线": {
		"func": timetable_handler_changeping,
		"titles": [
			{
				"direction": u"往西二旗方向（全程）",
			},
			{
				"direction": u"往西二旗方向（半程,终点朱辛庄）",
			},
			{
				"direction": u"往昌平西山口方向",
			}
		]
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
	u"4号线": {
		"func": timetable_handler_line4,
		"titles": [
			{
				"direction": u"上行全程（天宫院->公益西桥->安河桥北）方向",
			},
			{
				"direction": u"下行全程（北宫门->公益西桥->天宫院）方向"
			},
			{
				"direction": u"下行半程（北宫门->公益西桥）方向"
			}
		],
	},
	u"6号线": {
		"func": timetable_handler_line6,
		"titles": [
			{
				"direction": u"往海淀五路居方向",
			},
			{
				"direction": u"往潞城方向全程"
			},
			{
				"direction": u"往潞城方向半程（终点：草房）"
			}
		],
	},
	u"2号线": {
		"func": timetable_handler_line2,
		"titles": [
			{
				"direction": u"外环全程（西直门->车公庄->复兴门->东直门->积水潭->西直门）方向"
			},
			{
				"direction": u"外环积水潭半程（西直门->车公庄->复兴门->东直门->积水潭）方向",
			},
			{
				"direction": u"内环全程（积水潭->鼓楼大街->东直门->复兴门->西直门->积水潭）方向",
			},
			{
				"direction": u"内环西直门半程（积水潭->鼓楼大街->东直门->复兴门->西直门）方向",
			}
		],
	},
	u"10号线": {
		"func": timetable_handler_line10,
		"titles": [
			{
				"direction": u"上行（外环）全程，车道沟-宋家庄-国贸-巴沟方向",
			},
			{
				"direction": u"上行（外环）终点车道沟，车道沟-宋家庄-国贸-巴沟方向",
			},
			{
				"direction": u"下行（内环）全程，巴沟-国贸-宋家庄-车道沟方向",
			},
			{
				"direction": u"下行（内环）终点巴沟，巴沟-国贸-宋家庄-车道沟方向",
			},
			{
				"direction": u"下行（内环）终点成寿寺，巴沟-国贸-宋家庄-车道沟方向",
			}
		],
	},
	u"14号线西段": {
		"func": timetable_handler_line6,
		"titles": [
			{
				"direction": u"往西局方向",
			},
			{
				"direction": u"往张郭庄方向全程",
			},
			{
				"direction": u"往张郭庄方向半程",
			}
		],
	},
	u"14号线东段": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往善各庄方向",
			},
			{
				"direction": u"往金台路方向",
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
