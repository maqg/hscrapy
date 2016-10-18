#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import scrapy

from hscrapy.settings import PS_CONFIG, DEST_DIR
from hscrapy.utils.commonUtil import fileToObj


KEYWORDS = [
	u"云计算",
	u"虚拟化",
	u"信息化",
	u"大数据",
	u"云课堂",
	u"云办公",
	u"桌面云",
	u"私有云",
	u"公有云",
	u"云安全",
	u"审计",
	u"瘦终端",
	u"瘦客户机",
	u"一体机",
	u"IaaS",
	u"SaaS",
	u"云教学",
	u"教育云"
]


class OctlinkSpider(scrapy.Spider):

	name = "octlink"

	urls = {}
	urlList = []

	titles = {}

	def matchRules(self, title):
		for rule in KEYWORDS:
			if (title.find(rule) != -1):
				self.log("matched rule %s for title %s" % (rule, title))
				return True
		return False

	def getTitle(self, url):
		return self.titles.get(url)

	def getDir_byUrl(self, url):
		urlObj = self.urls.get(url)
		if (urlObj):
			return urlObj["dir"]
		else:
			return DEST_DIR

	def getParentUrl(self, url):
		urlObj = self.urls.get(url)
		if (urlObj):
			return urlObj["parent"]
		else:
			return url

	def handUrl(self, url, parent=None):

		pages = url.get("pages") or 0

		for pId in range(1, pages + 2):
			newUrl = {
				"name": url["name"],
			}
			if (pages):
				newUrl["url"] = url["url"] % pId
			else:
				newUrl["url"] = url["url"]

			self.urlList.append(newUrl)

		for pId in range(1, pages + 2):
			urlObj = {
				"name": url["name"],
			}
			if (pages):
				urlObj["url"] = url["url"] % pId
			else:
				urlObj["url"] = url["url"]

			if (parent):
				urlObj["dir"] = DEST_DIR + os.sep + parent["name"] + os.sep + url["name"]
				urlObj["parent"] = parent["url"]
			else:
				urlObj["dir"] = DEST_DIR + os.sep + url["name"]
				urlObj["parent"] = url["url"]

			if (not os.path.exists(urlObj["dir"])):
				os.makedirs(urlObj["dir"])

			self.urls[urlObj["url"]] = urlObj

		if (url.has_key("subUrls")):
			for subUrl in url["subUrls"]:
				self.handUrl(subUrl, url)

	def loadUrls(self):
		urlObjs = fileToObj(PS_CONFIG)
		for url in urlObjs:
			self.handUrl(url)

	def start_requests(self):
		self.loadUrls()
		for url in self.urlList:
			yield scrapy.http.Request(url=url["url"], callback=self.parse)

	def parseUrl(self, body, baseUrl):

		self.log(baseUrl)

		bodies = body.replace(" ", "").replace("\t", "").split("\n")
		for line in bodies:
			if (len(line)) > 10 and line.find("<ahref") != -1:
				items = line.split("\"")
				if (len(items) < 2):
					continue
				if (not items[1].startswith("http")):
					subUrl = baseUrl + items[1]
				else:
					subUrl = items[1]
				print(subUrl)
				yield scrapy.http.Request(url=subUrl, callback=self.parse_content)

	def parse_content(self, response):

		dstUrlPath = None

		title = self.getTitle(response.url)
		if (not title):
			self.log("not title got, skip this url %s" % response.url)
			return

		self.log("got new content %s, store to %s" % (title["name"], title["dir"]))
		format = response.url.split(".")[-1]
		if (format in ["jpg", "gif", "png"]):
			dstPath = title["dir"] + os.sep + title["name"] + "." + format
		else:
			dstPath = title["dir"] + os.sep + title["name"] + "." + "html"
			dstUrlPath = title["dir"] + os.sep + title["name"] + "." + "URL" + "." + "html"

		if (os.path.exists(dstPath)):
			self.log("this url already exist, just skip it %s" % response.url)
			return

		self.log(dstPath)
		fd = open(dstPath, "w+")
		fd.write(response.body)
		fd.close()

		if (dstUrlPath):
			content = """
<html>
<script>
	window.location = "%s"
	</script>
</html>
""" % response.url
			fd = open(dstUrlPath, "w+")
			fd.write(content)
			fd.close()

	def parse(self, response):

		baseUrl = response.url
		self.log(baseUrl)

		urls = response.xpath("//a")

		for url in urls:
			names = url.xpath("text()").extract()
			if (not len(names)):
				continue

			name = names[0].replace("\r", "").replace("\n", "")
			if (not name or name == "<"): # no name specified
				continue

			if (not self.matchRules(name)):
				continue

			href = url.xpath("@href").extract()[0]
			if (href == "#"):
				continue

			parentUrl = self.getParentUrl(baseUrl)
			subUrl = parentUrl + href
			if (self.getTitle(subUrl)): # already read it
				continue

			title = {
				"dir": self.getDir_byUrl(baseUrl),
				"name": name
			}
			self.titles[subUrl] = title
			yield scrapy.http.Request(url=subUrl, callback=self.parse_content)