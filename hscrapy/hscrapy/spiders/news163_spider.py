import os

import scrapy


class News163Spider(scrapy.Spider):
	name = "news163"

	def start_requests(self):
		urls = [
			'http://lady.163.com',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		bodies = response.body.replace(" ", "").replace("\t", "").split("\n")
		for line in bodies:
			if (len(line)) > 10 and line.startswith("<img"):
				imgUrl = line.split("\"")[1]
				if (not imgUrl.startswith("http")):
					continue
				cmd = "curl %s -o %s" % (imgUrl, imgUrl.split("/")[-1])
				print(cmd)
				#os.system(cmd)
		# page = response.url.split("
		#  filename = 'new163-%s.html' % page
		#  with open(filename, 'wb') as f:
		#   f.write(response.body)
		# self.log('Saved file %s' % filename)

