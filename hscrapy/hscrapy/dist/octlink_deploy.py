#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from hscrapy.utils.commonUtil import fileToObj

SOURCE_FONFIG_FILE = "octlink_sources.json"

def deploy_octlink():
	obj = fileToObj(SOURCE_FONFIG_FILE)
	print(json.dumps(obj['webSites'], indent=4, ensure_ascii=False))
	print(json.dumps(obj["webSites"], ensure_ascii=False).replace("\"", "\\\""))

if __name__ == "__main__":

	deploy_octlink()

	print("Octlink Deployed OK!")