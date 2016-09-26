import os
import scrapy

from hscrapy.settings import PS_CONFIG, DEST_DIR
from hscrapy.utils.commonUtil import fileToObj


class News163Spider(scrapy.Spider):

	name = "subway"

	dist_file = DEST_DIR + os.sep + "subway.json"

	url_timetable = "http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"
	url_disance = "http://www.bjsubway.com/station/zjgls/"


	def start_requests(self):

		#yield scrapy.http.Request(url=self.url_timetable, callback=self.parse_timetable)

		yield scrapy.http.Request(url=self.url_disance, callback=self.parse_distance)


	def parse_timetable(self, response):
		print("runhere")
		pass


	def process_distance_table(self, distances, lineName):
		for disItem in distances:
			th = disItem.xpath("th")[0]
			stationName = th.xpath("text()").extract()[0]
			distance = disItem.xpath("td/text()").extract()[0]
			disItem = {
				"name": stationName,
				"length": distance
			}
			self.log("name: %s: %d" % (stationName.encode("utf-8"), int(distance)))

	def get_line_name(self, td):
		return td.xpath("text()").extract()[0]

	def parse_distance(self, response):

		#self.log(response.body)

		tables = response.xpath("//table")
		for table in tables:
			head = table.xpath("thead/tr/td")[0]
			lineName = self.get_line_name(head)
			self.log(lineName)

			distances = table.xpath("tbody/tr")
			self.process_distance_table(distances, lineName)
