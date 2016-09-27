# -*- coding: utf-8 -*-


import os
import scrapy

from hscrapy.settings import DEST_DIR
import json

from hscrapy.utils.commonUtil import transToStr


class News163Spider(scrapy.Spider):

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

		yield scrapy.http.Request(url=self.url_timetable, callback=self.parse_timetable)

		yield scrapy.http.Request(url=self.url_disance, callback=self.parse_distance)

		self.write()


	def parse_timetable(self, response):
		pass


	def process_distance_table(self, distances, line):
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
				"length": distance
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

	def get_line_name(self, td):
		return td.xpath("text()").extract()[0].split("线")[0] + "线"

	def parse_distance(self, response):

		#self.log(response.body)

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.get_line_name(head)
			self.log(lineName)

			self.lineId += 1

			line = {
				"name": lineName,
				"id": self.lineId,
				"stations": []
			}
			self.lines.append(line)

			distances = table.xpath("tbody/tr")
			self.process_distance_table(distances, line)


		self.write()
