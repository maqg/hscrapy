# -*- coding: utf-8 -*-


def timetable_handler_normal(timeValues, lastTrain, titles):

	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	lastTrain.append({
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	})

	lastTrain.append({
		"direction": titles[1]["direction"],
		"first": values[2],
		"last": values[3]
	})


def timetable_handler_line13(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[1],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[1],
		"last": values[4]
	}

	item3 = {
		"direction": titles[3]["direction"],
		"first": values[0],
		"last": values[5]
	}

	for item in (item0, item1, item2, item3):
		lastTrain.append(item)


def timetable_handler_line15(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[3],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_changeping(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[1],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_line2(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[0],
		"last": values[2]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[3],
		"last": values[4]
	}

	item3 = {
		"direction": titles[3]["direction"],
		"first": values[3],
		"last": values[5]
	}

	for item in (item0, item1, item2, item3):
		lastTrain.append(item)


def timetable_handler_line4(timeValues, lastTrain, titles):
	timeCount = len(timeValues)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not len(titles)):
		return

	if (timeCount == 2):
		lastTrain.append({
			"direction": titles[0]["direction"],
			"first": values[0],
			"last": values[1]
		})
	else:
		lastTrain.append({
			"direction": titles[1]["direction"],
			"first": values[0],
			"last": values[1]
		})

		lastTrain.append({
			"direction": titles[2]["direction"],
			"first": values[0],
			"last": values[2]
		})


def timetable_handler_line6(timeValues, lastTrain, titles):
	titleCount = len(titles)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not titleCount):
		return

	item0 = {
		"direction": titles[0]["direction"],
		"first": values[0],
		"last": values[1]
	}

	item1 = {
		"direction": titles[1]["direction"],
		"first": values[2],
		"last": values[3]
	}

	item2 = {
		"direction": titles[2]["direction"],
		"first": values[2],
		"last": values[4]
	}

	for item in (item0, item1, item2):
		lastTrain.append(item)


def timetable_handler_line10(timeValues, lastTrain, titles):
	timeCount = len(timeValues)

	values = []
	for timeTable in timeValues:
		timeValue = timeTable.xpath("text()").extract()[0].replace("\r", "").replace("\n", "").replace(" ", "")
		values.append(timeValue)

	if (not len(titles)):
		return

	if (timeCount == 4):
		lastTrain.append({
			"direction": titles[0]["direction"],
			"first": values[0],
			"last": values[1]
		})

		lastTrain.append({
			"direction": titles[1]["direction"],
			"first": values[0],
			"last": values[2]
		})

		lastTrain.append({
			"direction": titles[2]["direction"],
			"first": values[0],
			"last": values[3]
		})
	else:
		lastTrain.append({
			"direction": titles[3]["direction"],
			"first": values[0],
			"last": values[1]
		})

		lastTrain.append({
			"direction": titles[4]["direction"],
			"first": values[0],
			"last": values[2]
		})


timeTableSettings = {
	u"1号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往四惠东方向"
			},
			{
				"direction": u"往苹果园方向",
			}
		],
	},
	u"5号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往天通苑北方向",
			},
			{
				"direction": u"往宋家庄方向"
			}
		],
	},
	u"7号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往北京西站方向",
			},
			{
				"direction": u"往焦化厂站方向"
			}
		],
	},
	u"8号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往南锣鼓巷方向",
			},
			{
				"direction": u"往朱辛庄方向"
			}
		],
	},
	u"9号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往郭公庄方向",
			},
			{
				"direction": u"往国家图书馆方向"
			}
		],
	},
	u"13号线": {
		"func": timetable_handler_line13,
		"titles": [
			{
				"direction": u"往西直门方向（全程）",
			},
			{
				"direction": u"往东直门方向（全程）",
			},
			{
				"direction": u"往东直门方向（霍营区间）",
			},
			{
				"direction": u"往西直门方向（回龙观区间）",
			}
		],
	},
	u"15号线": {
		"func": timetable_handler_line15,
		"titles": [
			{
				"direction": u"往清华东路西口方向（全程）",
			},
			{
				"direction": u"往清华东路西口方向（半程,终点马泉营）",
			},
			{
				"direction": u"往俸伯方向",
			}
		]
	},
	u"昌平线": {
		"func": timetable_handler_changeping,
		"titles": [
			{
				"direction": u"往西二旗方向（全程）",
			},
			{
				"direction": u"往西二旗方向（半程,终点朱辛庄）",
			},
			{
				"direction": u"往昌平西山口方向",
			}
		]
	},
	u"八通线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往土桥",
			},
			{
				"direction": u"往四惠"
			}
		],
	},
	u"房山线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往苏庄方向",
			},
			{
				"direction": u"往郭公庄方向"
			}
		],
	},
	u"燕房线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往燕山方向",
			},
			{
				"direction": u"往阎村东方向"
			}
		],
	},
	u"S1线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往石厂方向",
			},
			{
				"direction": u"往金安桥方向"
			}
		],
	},
	u"亦庄线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往次渠方向",
			},
			{
				"direction": u"往宋家庄方向"
			}
		],
	},
	u"机场线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往市区",
			},
			{
				"direction": u"往机场"
			}
		],
	},
	u"4号线": {
		"func": timetable_handler_line4,
		"titles": [
			{
				"direction": u"上行全程（天宫院->公益西桥->安河桥北）方向",
			},
			{
				"direction": u"下行全程（北宫门->公益西桥->天宫院）方向"
			},
			{
				"direction": u"下行半程（北宫门->公益西桥）方向"
			}
		],
	},
	u"大兴线": {
		"func": timetable_handler_line4,
		"titles": [
			{
				"direction": u"上行全程（天宫院->公益西桥->安河桥北）方向",
			},
			{
				"direction": u"下行全程（北宫门->公益西桥->天宫院）方向"
			},
			{
				"direction": u"下行半程（北宫门->公益西桥）方向"
			}
		],
	},
	u"6号线": {
		"func": timetable_handler_line6,
		"titles": [
			{
				"direction": u"往海淀五路居方向",
			},
			{
				"direction": u"往潞城方向全程"
			},
			{
				"direction": u"往潞城方向半程（终点：草房）"
			}
		],
	},
	u"2号线": {
		"func": timetable_handler_line2,
		"titles": [
			{
				"direction": u"外环全程（西直门->车公庄->复兴门->东直门->积水潭->西直门）方向"
			},
			{
				"direction": u"外环积水潭半程（西直门->车公庄->复兴门->东直门->积水潭）方向",
			},
			{
				"direction": u"内环全程（积水潭->鼓楼大街->东直门->复兴门->西直门->积水潭）方向",
			},
			{
				"direction": u"内环西直门半程（积水潭->鼓楼大街->东直门->复兴门->西直门）方向",
			}
		],
	},
	u"10号线": {
		"func": timetable_handler_line10,
		"titles": [
			{
				"direction": u"下行（内环）全程，巴沟-国贸-宋家庄-车道沟方向",
			},
			{
				"direction": u"下行（内环）终点巴沟，巴沟-国贸-宋家庄-车道沟方向",
			},
			{
				"direction": u"下行（内环）终点成寿寺，巴沟-国贸-宋家庄-车道沟方向",
			},
			{
				"direction": u"上行（外环）全程，车道沟-宋家庄-国贸-巴沟方向",
			},
			{
				"direction": u"上行（外环）终点车道沟，车道沟-宋家庄-国贸-巴沟方向",
			}
		],
	},
	u"14号线西段": {
		"func": timetable_handler_line6,
		"titles": [
			{
				"direction": u"往西局方向",
			},
			{
				"direction": u"往张郭庄方向全程",
			},
			{
				"direction": u"往张郭庄方向半程",
			}
		],
	},
	u"14号线东段": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往善各庄方向",
			},
			{
				"direction": u"往金台路方向",
			}
		],
	},
	u"16号线": {
		"func": timetable_handler_normal,
		"titles": [
			{
				"direction": u"往北安河方向",
			},
			{
				"direction": u"往西苑方向"
			}
		]
	},
}


def getTimeTableSettings(lineName):
	return timeTableSettings.get(lineName)
