import os
from hscrapy import settings
import scrapy

from hscrapy.settings import PS_CONFIG, DEST_DIR
from hscrapy.utils.commonUtil import fileToObj


class News163Spider(scrapy.Spider):

	name = "news163"

	def loadUrls(self):
		urls = []
		urlObjs = fileToObj(PS_CONFIG)
		for url in urlObjs:
			urls.append(url)
			self.log(url)
		return urls

	def start_requests(self):
		urls = self.loadUrls()
		for url in urls:
			yield scrapy.Request(url=url["url"], callback=self.parse)


	def parse_img(self, body, baseUrl):

		bodies = body.replace(" ", "").replace("\t", "").split("\n")

		for line in bodies:
			if (len(line)) > 10 and line.find("<img") != -1:
				imgUrl = line.split("\"")[1]
				dstUrl =  DEST_DIR + os.sep + imgUrl.split("/")[-1]
				if (imgUrl.startswith("http")):
					cmd = "curl %s -o %s" % (imgUrl, dstUrl)
				else:
					if (baseUrl.endswith("/")):
						fullUrl = "%s%s" % (baseUrl, imgUrl)
					else:
						fullUrl = "%s/%s" % (baseUrl, imgUrl)
					cmd = "curl %s -o %s" % (fullUrl, dstUrl)
				print(cmd)
				os.system(cmd)

	def parse_url(self, body, baseUrl):

		bodies = body.replace(" ", "").replace("\t", "").split("\n")
		for line in bodies:
			if (len(line)) > 10 and line.find("<ahref") != -1:
				items = line.split("\"")
				if (len(items) >= 2):
					print(items[1])

	def parse(self, response):
		self.parse_url(response.body, response.url)
		self.parse_img(response.body, response.url)