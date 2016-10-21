#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from hscrapy.utils.commonUtil import fileToObj, transToStr

SOURCE_FONFIG_FILE = "octlink_sources_temp.json"

PC_CONFIG_FILE = "../pc.json"


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
	return "NOTSETTTT"

def append_pages(website, page=None):
	website["pages"] = []

	if (page):
		baseDir = page["name"] + os.sep + website["name"]
	else:
		baseDir = website["name"]

	for file in os.listdir(baseDir):
		if (os.path.isdir(baseDir + os.sep + file)):
			continue

		if (file.endswith("_URL.html")):
			continue

		page = {
			"name": "".join(file.split("_")[1:])[:-5],
			"url": parseUrl(baseDir + os.sep + file),
			"publishTime": file.split("_")[0],
			"fetchTime": parseFetchTime(baseDir + os.sep + file)
		}

		website["pages"].append(page)

def append_classes(website, page):
	for subUrl in page["subUrls"]:
		submodule = {
			"name": subUrl["name"],
			"url": subUrl["url"],
		}
		website["classes"].append(submodule)

		append_pages(submodule, page)


def deploy_octlink():

	octlink_sources = {
		"todayLatest": [],
		"webSites": [],
		"statistics": {}
	}

	pcObjs = fileToObj(PC_CONFIG_FILE)

	for page in pcObjs:
		if (not page["state"]):
			continue
		website = {
			"name": page["name"],
			"url": page["url"],
			"classes": []
		}

		append_classes(website, page)

		append_pages(website)

		octlink_sources["webSites"].append(website)

	fd = open(SOURCE_FONFIG_FILE, "w+")
	fd.write(transToStr(octlink_sources, indent=2))
	fd.close()

	print("generate pages OK")


if __name__ == "__main__":

	deploy_octlink()

	print("Octlink Deployed OK!")