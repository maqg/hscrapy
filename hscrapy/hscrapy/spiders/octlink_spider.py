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
	u"教育云",
	u"课程",
	u"美术"
]


class OctlinkSpider(scrapy.Spider):

	name = "octlink"

	urlSettings = {}
	requestList = []

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
		urlObj = self.urlSettings.get(url)
		if (urlObj):
			return urlObj["dir"]
		else:
			return DEST_DIR

	def getUrlSettings(self, url):
		return self.urlSettings.get(url)

	def getParentUrl(self, url):
		urlObj = self.urlSettings.get(url)
		if (urlObj):
			return urlObj["parent"]
		else:
			return url

	def handUrl(self, url, parent=None):

		pages = url.get("pages") or 0

		for pId in range(1, pages + 2):
			request = {
				"name": url["name"],
			}

			if (parent):
				if (parent.get("parser")):
					request["parser"] = self.parser_hebeisheng
				else:
					request["parser"] = self.parse_new
			else:
				request["parser"] = self.parse

			if (pages):
				request["url"] = url["url"] % pId
			else:
				request["url"] = url["url"]

			self.requestList.append(request)

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
				urlObj["publishTimeRegex"] = parent.get("publishTimeRegex")
				urlObj["titleRegex"] = parent.get("titleRegex")
			else:
				urlObj["dir"] = DEST_DIR + os.sep + url["name"]
				urlObj["parent"] = url["url"]

			if (not os.path.exists(urlObj["dir"])):
				os.makedirs(urlObj["dir"])

			self.urlSettings[urlObj["url"]] = urlObj

		if (url.has_key("subUrls")):
			for subUrl in url["subUrls"]:
				self.handUrl(subUrl, url)

	def loadUrls(self):
		urlObjs = fileToObj(PS_CONFIG)
		for url in urlObjs:
			if (not url.get("state")):
				continue
			self.handUrl(url)

	def start_requests(self):
		self.loadUrls()
		for url in self.requestList:
			yield scrapy.http.Request(url=url["url"], callback=url["parser"])

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
			redUrl = response.meta["redirect_urls"]
			title = self.getTitle(redUrl[0]) # redirected page
			if (not title):
				self.log("not title got, skip this url %s" % response.url)
				return

		self.log("got new content %s, store to %s" % (title["name"], title["dir"]))
		format = response.url.split(".")[-1]
		if (format in ["jpg", "gif", "png"]):
			dstPath = title["dir"] + os.sep + title["name"] + "." + format
		else:
			dstPath = title["dir"] + os.sep + title["time"] + "_" + title["name"] + ".html"
			dstUrlPath = title["dir"] + os.sep + title["time"] + "_" + title["name"] + "_" + "URL" + ".html"

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

	def parser_hebeisheng(self, response):

		def parseJS():
			item = response.body.find("$(\"#contentform\").attr(")
			lineEnd = response.body[item:].find("\r\n")
			raw = response.body[item: item + lineEnd]

			urlFormat = raw.split(",")[-1].replace("+flag+", "__FLAG__").replace("+fid+", "__FID__").replace("\"", "")[:-2]
			self.log("got url Format %s" % urlFormat)

			return urlFormat

		def makeUrl(flag, fid=None):
			tmp = urlFormat.replace("__FLAG__", str(flag))
			if (fid):
				tmp = tmp.replace("__FID__", str(fid))
			return tmp

		baseUrl = response.url
		self.log(baseUrl)

		urlFormat = parseJS()
		urls = response.xpath("//table/tr[contains(@onclick, 'watchContent')]")
		attrs = response.xpath("//table/tr[@bgcolor='#E3EDF6']")

		if (len(urls) != len(attrs)):
			itemCount = min(len(urls), len(attrs))
		else:
			itemCount = len(urls)

		for i in range(0, itemCount):

			url = urls[i]
			attr = attrs[i]

			onclickItems = url.xpath("@onclick").extract()[0].replace("(", ",").replace(")", ",").replace("'", "").split(",")
			if (len(onclickItems) == 4):
				fid = int(onclickItems[1])
				flag = int(onclickItems[2])
			else:
				flag = None
				fid = int(onclickItems[1])

			names = url.xpath("td/a/text()").extract()
			if (not len(names)):
				continue
			name = names[0].replace("\r", "").replace("\n", "").replace("\\", "或").replace("/", "或").replace(":", "").replace(" ", "").replace("\t", "")
			if (not name or name == "<"): # no name specified
				continue

			items = attr.xpath("td/span")
			if (not items):
				timeInfo = "NotSet"
			else:
				timeInfo = items[0].xpath("text()").extract()[0].replace("\r", "").replace("\n", "")

			if (not self.matchRules(name)):
				continue

			nextUrl = makeUrl(flag, fid)
			if (nextUrl.startswith("http")):
				subUrl = nextUrl
			else:
				subUrl = self.getParentUrl(baseUrl) + nextUrl
			if (self.getTitle(subUrl)): # already read it
				continue

			title = {
				"dir": self.getDir_byUrl(baseUrl),
				"name": name,
				"time": timeInfo,
			}
			self.titles[subUrl] = title

			dstPath = title["dir"] + os.sep + title["time"] + "_" + title["name"] + ".html"
			if (os.path.exists(dstPath)):
				self.log("this url already exist, just skip it %s" % subUrl)
				continue

			yield scrapy.http.Request(url=subUrl, callback=self.parse_content)


	def parse_publishtime(self, response, regex):
		publishTimes = []
		items = response.xpath(regex)
		for item in items:
			datas = item.xpath("text()").extract()
			data = "".join(datas).split(" ")[0].replace("\r", "").replace("\n", "").replace("\"", "")
			if (data.startswith("20")):
				publishTimes.append(data)
		return publishTimes

	def parse_new(self, response):

		baseUrl = response.url
		self.log(baseUrl)

		urlSettings = self.getUrlSettings(baseUrl)
		if (not urlSettings):
			self.log("no url settings found for url %s " % baseUrl)
			return

		urls = response.xpath(urlSettings["titleRegex"])
		publishTimes = self.parse_publishtime(response, urlSettings["publishTimeRegex"])

		titleCount = min(len(urls), len(publishTimes))

		for i in range(0, titleCount):
			url = urls[i]
			publishTime = publishTimes[i]

			names = url.xpath("text()").extract()
			if (not len(names)):
				continue

			name = names[0].replace("\r", "").replace("\n", "").replace("\\", "或").replace("/", "或").replace(":", "").replace(" ", "").replace("\t", "")

			if (not name or name == "<"): # no name specified
				continue

			if (not self.matchRules(name)):
				continue

			hrefs = url.xpath("@href").extract()
			if (not hrefs):
				continue

			href = hrefs[0]
			if (href == "#"):
				continue

			if (href[0] == "."):
				newBaseUrl = baseUrl.split("index")[0]
				subUrl = newBaseUrl + href[1:]
			else:
				subUrl = self.getParentUrl(baseUrl) + href

			if (self.getTitle(subUrl)): # already read it
				continue

			title = {
				"dir": self.getDir_byUrl(baseUrl),
				"name": name,
				"time": publishTime,
			}
			self.titles[subUrl] = title
			yield scrapy.http.Request(url=subUrl, callback=self.parse_content)

	def parse(self, response):

		baseUrl = response.url
		self.log(baseUrl)

		urls = response.xpath("//a")

		for url in urls:
			names = url.xpath("text()").extract()
			if (not len(names)):
				continue

			name = names[0].replace("\r", "").replace("\n", "").replace("\\", "或").replace("/", "或").replace(":", "").replace(" ", "").replace("\t", "")
			if (not name or name == "<"): # no name specified
				continue

			if (not self.matchRules(name)):
				continue

			hrefs = url.xpath("@href").extract()
			if (not hrefs):
				continue

			href = hrefs[0]
			if (href == "#"):
				continue

			if (href[0] == "."):
				newBaseUrl = baseUrl.split("index")[0]
				subUrl = newBaseUrl + href[1:]
			else:
				subUrl = self.getParentUrl(baseUrl) + href

			if (self.getTitle(subUrl)): # already read it
				continue

			title = {
				"dir": self.getDir_byUrl(baseUrl),
				"name": name,
				"time": "NotSet"
			}
			self.titles[subUrl] = title
			yield scrapy.http.Request(url=subUrl, callback=self.parse_content)