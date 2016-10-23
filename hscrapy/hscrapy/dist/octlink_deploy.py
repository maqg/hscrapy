#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from hscrapy.utils.commonUtil import fileToObj, transToStr
from hscrapy.utils.timeUtil import getStrDate, getCurrentStrDate

SOURCE_FONFIG_FILE = "octlink_sources_temp.json"

PC_CONFIG_FILE = "../pc.json"

INDEX_FILE = "index_template.html"
TODAYLATEST_FILE = "todaylatest_template.html"
QUERY_FILE = "query_template.html"
PAGES_FILE = "pages_template.html"


pageCount = 0


def parseUrl(filePath):

	filePath = filePath[:-5] + "_URL.html"

	if (not os.path.exists(filePath)):
		return "#"

	fd = open(filePath, "r")
	for line in fd.readlines():
		temp = line.strip()
		if (temp.startswith("window.location")):
			fd.close()
			return temp.split("\"")[1]

	fd.close()

	return "#"

def parseFetchTime(filePath):
	return getStrDate(os.path.getctime(filePath) * 1000)

def append_pages(submodule, todayList, today, site=None):

	submodule["pages"] = []

	if (site):
		baseDir = site["name"] + os.sep + submodule["name"]
	else:
		baseDir = submodule["name"]

	for file in os.listdir(baseDir):
		if (os.path.isdir(baseDir + os.sep + file)):
			continue

		if (file.endswith("_URL.html")):
			continue

		item = {
			"name": "".join(file.split("_")[1:])[:-5],
			"url": parseUrl(baseDir + os.sep + file),
			"localUrl": baseDir + os.sep + file,
			"publishTime": file.split("_")[0],
			"fetchTime": parseFetchTime(baseDir + os.sep + file)
		}

		submodule["pages"].append(item)

		global pageCount
		pageCount += 1

		if (site and today == item["fetchTime"]):
			item["webSite"] = site["name"]
			item["className"] = submodule["name"]
			todayList.append(item)

def append_classes(website, site, todayList, today):

	for subUrl in site["subUrls"]:
		submodule = {
			"name": subUrl["name"],
			"url": subUrl["url"],
		}
		website["classes"].append(submodule)

		append_pages(submodule, todayList, today, site)


def getDatas(filePath):
	fd = open(filePath, "r")
	segs = fd.read().split("__DATA__")
	fd.close()
	return segs


def write_index(statistics):

	segs = getDatas(INDEX_FILE)

	fd = open(INDEX_FILE.replace("_template", ""), "w+")
	fd.write(segs[0])
	fd.write(json.dumps(statistics, indent=4, ensure_ascii=False))
	fd.write(segs[1])
	fd.close()

def write_query(data):
	segs = getDatas(QUERY_FILE)
	fd = open(QUERY_FILE.replace("_template", ""), "w+")
	fd.write(segs[0])
	fd.write(json.dumps(data, indent=4, ensure_ascii=False))
	fd.write(segs[1])
	fd.close()


def write_todaylatest(data):
	segs = getDatas(TODAYLATEST_FILE)
	fd = open(TODAYLATEST_FILE.replace("_template", ""), "w+")
	fd.write(segs[0])
	fd.write(json.dumps(data, indent=4, ensure_ascii=False))
	fd.write(segs[1])
	fd.close()


def write_pages(data):
	segs = getDatas(PAGES_FILE)
	fd = open(PAGES_FILE.replace("_template", ""), "w+")
	fd.write(segs[0])
	fd.write(json.dumps(data, indent=4, ensure_ascii=False))
	fd.write(segs[1])
	fd.close()



def deploy_octlink():

	today = getCurrentStrDate()

	todayLatest = []
	statistics = {}
	webSites = []

	pages = {}

	octlink_sources = {
		"todayLatest": todayLatest,
		"webSites": webSites,
		"statistics": statistics
	}

	pcObjs = fileToObj(PC_CONFIG_FILE)

	for site in pcObjs:
		if (not site["state"]):
			continue
		website = {
			"name": site["name"],
			"url": site["url"],
			"classes": []
		}

		append_classes(website, site, todayLatest, today)

		append_pages(website, todayLatest, today)

		webSites.append(website)

		pages[site["name"]] = site["url"]

	statistics["网站数量"] = len(webSites)
	statistics["今日更新"] = len(todayLatest)
	statistics["标书数量"] = pageCount

	write_index(statistics)

	write_query(webSites)

	write_pages(pages)

	write_todaylatest(todayLatest)

	fd = open(SOURCE_FONFIG_FILE, "w+")
	fd.write(transToStr(octlink_sources, indent=2))
	fd.close()



	print("generate pages OK")


if __name__ == "__main__":

	deploy_octlink()

	print("Octlink Deployed OK!")