import json

from hscrapy.utils.commonUtil import fileToObj, transToStr

file = "./subway.json"

export = "./subway.ori.json"


lines = fileToObj(file)

for line in lines:
	for station in line["stations"]:
		if not station.get("lastTrain"):
			print(station["name"])
		else:
			del station["lastTrain"]


fd = open(export, "w+")
if (fd):
	fd.write(transToStr(lines, indent=2))