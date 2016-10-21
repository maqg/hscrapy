/**
 * Created by henry on 2015/5/12.
 */


var VMLIST_REFRESH_TIMEOUT = 5000; // 5 seconds
var CDROM_ADD_REFRESH_TIMEOUT = 3000;
var TASK_UPDATE_REFRESH_TIMEOUT = 1000;

var ERROR_MSG_CONN_SERVER = "连接服务器错误";
var ERROR_MSG_NO_DATABODY = "未返回数据部分";
var ERROR_MSG_PASS_NOT_SPECIFIED = "密码不能为空";
var ERROR_MSG_VM_NOT_RUNNING = "虚拟机未运行";
var ERROR_MSG_HARDVIRTUAL_NEED = "只有关机状态下的全虚拟化虚拟机，才能设置CDROM。";
var ERROR_MSG_HARDVIRTUAL_NEED2 = "只有关机状态下的全虚拟化虚拟机，才能修改启动顺序。";
var ERROR_MSG_MUST_WITH_IE = "远程桌面插件只能使用IE浏览器。";

function getCRCString($url) {
    return "00000000000000000000000000000000";
}

var userStateListStr = ["已失效", "正常"];

function userState_d2s(state) {
    if (state >= userStateListStr.length) {
        return userStateListStr[0];
    } else {
        return userStateListStr[state];
    }
}

var shareStateList = ["否", "是"];
function shareState_d2s(state) {
    if (state >= shareStateList.length) {
        return shareStateList[1];
    } else {
        return shareStateList[state];
    }
}

var hostStateList = ["在线", "离线"];
function hostState_d2s(state) {
    if (state >= hostStateList.length) {
        return hostStateList[1];
    } else {
        return hostStateList[state];
    }
}

var licenseFeatureStateList = ["禁用", "可用"];
function licenseFeatureState_d2s(state) {
    if (state >= licenseFeatureStateList.length) {
        return licenseFeatureStateList[1];
    } else {
        return licenseFeatureStateList[state];
    }
}

var licenseStateList = ["已验证", "状态异常", "已过期"];
function licenseState_d2s(state) {
    state = Math.abs(state);
    if (state >= licenseStateList.length) {
        return licenseStateList[1];
    } else {
        return licenseStateList[state];
    }
}

Array.prototype.indexOf = function(e) {
    for(var i=0,j; j=this[i]; i++){
        if(j==e){return i;}
    }
    return 0;
};

Array.prototype.lastIndexOf = function(e){
    for(var i=this.length-1,j; j=this[i]; i--){
        if(j==e){return i;}
    }
    return -1;
};

function userState_s2d(state) {
    return stateListStr.indexOf(state);
}

function userInfo2Array(userObj) {
    var dataArray = [];

    dataArray.push(userObj.name);
    dataArray.push(userObj.id);
    dataArray.push(userState_d2s(userObj.state));
    dataArray.push(userObj.email);
    dataArray.push(userObj.phone);
    dataArray.push(userObj.createTime);
    dataArray.push(userObj.desc);

    return dataArray;
}

var vmStateListStr = ["关闭", "暂停", "运行", "挂起", "崩溃", "未知"];
var vmStateListColorStr = ["red", "greenyellow", "green", "#f0f040", "#f04040", "grey"];

var VM_STATE_RUNNING = 2;
var VM_STATE_CLOSED = 0;

function vmState_s2d(state) {
    return vmStateListStr.indexOf(state);
}

function vmState_d2s(state) {
    if (state >= vmStateListStr.length) {
        return vmStateListStr[0];
    } else {
        return vmStateListStr[state];
    }
}

function getVmStateColor(state) {
    if (state >= vmStateListColorStr.length) {
        return vmStateListColorStr[0];
    } else {
        return vmStateListColorStr[state];
    }
}

var dcListStr = ["任意", "Default", "北京", "上海"];

function dc_s2d(dc) {
    return dcListStr.indexOf(dc);
}

function dc_d2s(dc) {
    if (dc >= dcListStr.length) {
        return dcListStr[0];
    } else {
        return dcListStr[dc];
    }
}

var vmPowerOperaionsStr = ["强制关闭", "关闭", "挂起", "强制重启", "重启", "恢复", "启动", "暂停", "解除暂停"];
var VM_POWER_FORCEOFF = 0;
var VM_POWER_OFF = 1;
var VM_POWER_SUSPEND = 2;
var VM_POWER_FORCEREBOOT = 3;
var VM_POWER_REBOOT = 4;
var VM_POWER_UNSUSPEND = 5;
var VM_POWER_ON = 6;
var VM_POWER_PAUSE = 7;
var VM_POWER_UNPAUSE = 8;

function vmPowerOperation_s2d(operation) {
    return vmPowerOperaionsStr.indexOf(operation);
}

function vmPowerOperation_d2s(operation) {
    if (operation >= vmPowerOperaionsStr.length) {
        return vmPowerOperaionsStr[0];
    } else {
        return vmPowerOperaionsStr[operation];
    }
}

var vmPowerPromptMsg = [];
function getVmPowerPromptMsg(opertaion) {
    if (opertaion >= vmPowerPromptMsg.length) {
        return vmPowerPromptMsg[0];
    } else {
        return vmPowerPromptMsg[opertaion];
    }
}

var virtualTypeStr = ["半虚拟化", "全虚拟化", "未知"];

function virtualType_s2d(type) {
    return vmStateListStr.indexOf(type);
}

function virtualType_d2s(type) {
    if (type >= virtualTypeStr.length) {
        return virtualTypeStr[0];
    } else {
        return virtualTypeStr[type];
    }
}

function getCDROMIso(vm) {
    iso = item.iso;
    if (iso.length == 0) {
        return "无";
    } else {
        var isoFile = iso[0].isoFile.split("/");
        if (isoFile.length == 0) {
        	return "无"
		} else {
        	return isoFile[isoFile.length - 1];
		}
    }
}

function getCDROM(vm) {
    iso = item.iso;
    if (iso.length == 0) {
        return null;
    } else {
        var cdrom = iso[0].device;
        if (cdrom == null || cdrom.length == 0) {
        	return null;
		} else {
			return cdrom;
		}
    }
}

function isIsoFile(isoFile) {
    var fileNameSplited = isoFile.fileName.split(".");
    if (fileNameSplited[fileNameSplited.length - 1].toLowerCase() == "iso") {
        return true;
    } else {
        return false;
    }
}

function isIsoSelected(isoFile, vm) {
    var incomingFileName = isoFile;
    var oldFileName = getCDROMIso(item);

    if (incomingFileName == oldFileName) {
        return true;
    } else {
        return false;
    }
}

/******
c disk
d cdrom
n network
**/
function getBootLoaderStr(bootArgs) {

    var bootArgsStr = "";

    for (var i = 0; i < bootArgs.length; i++) {

        if (bootArgs[i] == "c") {
            bootArgsStr += "硬盘";
        } else if (bootArgs[i] == "d") {
            bootArgsStr += "光驱";
        } else if (bootArgs[i] == "n") {
            bootArgsStr += "网络";
        }

        if (i != bootArgs.length - 1) {
            bootArgsStr += "，";
        }
    }

    return bootArgsStr;
}

var bootOptionStrList = ["无", "硬盘", "光驱", "网络"];
function bootOption_d2s(index) {
    if (index >= bootOptionStrList.length) {
        return bootOptionStrList[0];
    } else {
        return bootOptionStrList[index];
    }
}

function bootOption_s2d(option) {
    var index = bootOptionStrList.indexOf(option);
    if (index == 0 || index == -1) {
        return "";
    }
    var bootArgs = "cdn";

    return bootArgs[index - 1];
}

function bootOption_c2s(option) {
    if (option == "c") {
        return "硬盘";
    } else if (option == "d") {
        return "光驱";
    } else if (option == "n") {
        return "网络";
    } else {
        return "无";
    }
}

function getBoodOption(bootArgs, index) {
    if (bootArgs.length - 1 < index) {
        return "无";
    }
    return bootOption_c2s(bootArgs[index]);
}

function getFirstBootOption(bootArgs) {
    return getBoodOption(bootArgs, 0);
}

function getSecondBootOption(bootArgs) {
    return getBoodOption(bootArgs, 1);
}

function getThirdBootOption(bootArgs) {
    return getBoodOption(bootArgs, 2);
}

function getSelectedOption(id) {
    return $(id + " option:selected").val();
}

function getFirstSelectedOption() {
    return getSelectedOption("#vmBootLoaderFirst");
}

function getSecondSelectedOption() {
    return getSelectedOption("#vmBootLoaderSecond");
}

function getThirdSelectedOption() {
    return getSelectedOption("#vmBootLoaderThird");
}

TASK_STATE_CREATED = 0;
TASK_STATE_CANCEALED = 1;
TASK_STATE_FAILURE = 2;
TASK_STATE_TIMEOUT = 3;
TASK_STATE_SYNCED = 4;
TASK_STATE_FINISHED = 5;
TASK_STATE_BUILTIN = 6;
TASK_STATE_SERVERRUNNING = 7;
TASK_STATE_LOADED = 8;

var taskStateListStr = ["新建", "已取消", "执行失败", "已超时", "已同步", "成功结束", "内置", "服务器运行", "已装载"];
var taskStateListColorStr = ["blue", "darkgray", "red", "yellowgreen", "purple", "green", "black", "black", "black"];

function taskState_s2d(state) {
    return taskStateListStr.indexOf(state);
}

function taskState_d2s(state) {
    if (state >= taskStateListStr.length) {
        return taskStateListStr[0];
    } else {
        return taskStateListStr[state];
    }
}

function getTaskStateColor(state) {
    if (state >= taskStateListColorStr.length) {
        return taskStateListColorStr[0];
    } else {
        return taskStateListColorStr[state];
    }
}

var fileStateListStr = ["禁用", "新建", "已同步", "已加载"];
var fileStateListColorStr = ["red", "blue", "purple", "green"];

function licenseFileState_d2s(state) {
    if (state >= fileStateListStr.length) {
        return fileStateListStr[0];
    } else {
        return fileStateListStr[state];
    }
}

function getLicenseFileStateColor(state) {
    if (state >= fileStateListColorStr.length) {
        return fileStateListColorStr[0];
    } else {
        return fileStateListColorStr[state];
    }
}

function getMiliSecondString() {
    return new Date().getTime().toString();
}

function addAPIPara() {
    var apiRequest = $("#apiRequest");

    var bodyStr = "";
    var idString = getMiliSecondString();

    bodyStr += "<tr id=" + idString + ">";
    bodyStr += "<td><input type='text' name='name' placeholder=\"请输入名称\" value=></td>";
    bodyStr += "<td><select class='form-control' name='type'>"+ getDataTypeOptionList(null) + "</select></td>";
    bodyStr += "<td><input type='text' name='value' placeholder=\"请输入示例值\" value=></td>";
    bodyStr += "<td><input type='text' name='valueDesc' placeholder=\"请输入描述信息\" value=></td>";
    bodyStr += "<td><div onclick='removeAPIPara(\"" + idString + "\");' class='btn btn-danger'>删除</div></td></tr>";

    $newtr = $(bodyStr);

    apiRequest.append($newtr);
}

function getDataTypeOptionList(type) {
    optionStr = "";
    typeList = ["int", "string", "bool", "list"];

    for (var i = 0; i < typeList.length; i++) {
        name = typeList[i];
        if (name == type) {
            optionStr += "<option selected value=" + name + ">" + name + "</option>";
        } else {
            optionStr += "<option value=" + name + ">" + name + "</option>";
        }
    }

    return optionStr;
}

function createAPIBody(data, type) {

    var bodyStr = "";

    bodyStr += "<table id='apiRequest' style='word-break: break-all; table-layout: fixed' class=\"table table-striped\">";
    bodyStr += "<tr><th width='15%'>名称</th>";
    bodyStr += "<th width='10%'>类型</th>";
    bodyStr += "<th style='word-break: break-all'>Value示例</th>";
    bodyStr += "<th width='25%' style='word-break: break-all'>描述</th>";
    bodyStr += "<th width='10%'>操作</th></tr>";

    for (var item in data) {
        bodyStr += "<tr id=" + item + "><td><input type='text' name='name' placeholder=" + item  + " value = " + item + "></td>";
        bodyStr += "<td><select name='type' class='form-control'>" + getDataTypeOptionList(data[item]["type"]) + "</select></td>";
        bodyStr += "<td><input type='text' name='value' placeholder='" + data[item]["value"]  + "' value = '" + data[item]["value"] + "'></td>";
        bodyStr += "<td><input type='text' name='valueDesc' placeholder='" + data[item]["valueDesc"]  + "' value = '" + data[item]["valueDesc"] + "'></td>";
        bodyStr += "<td><div onclick='removeAPIPara(\"" + item + "\");' class='btn btn-danger'>删除</div></td></tr>";
    }

    bodyStr += "</div></table>";

    bodyStr += "<div onclick='addAPIPara();' style='float: right; margin-right: 50px' class='btn btn-primary'>添加</div><br><br>";

    return bodyStr;
}

function createApiFooter(type, apiId) {
    var bodyStr = "";

    bodyStr += "<button style=\"font-size: 120%\" id=\"confirmPost\" class=\"btn btn-primary\" onclick=\"commitApiRequest('" + type + "','" +  apiId + "');\"";
    bodyStr += "aria-hidden=\"true\">确认修改</button>";
    bodyStr += "<button style=\"font-size: 120%\" class=\"btn btn-success\" data-dismiss=\"modal\" aria-hidden=\"true\">取消</button>";

    return bodyStr;
}

function createAPIReply(reply, replyDesc) {

    var bodyStr = "";

    bodyStr += "<label style='float: left' '>回复：</label><br><br>";
    bodyStr += "<div style='padding-left:50px; padding-right: 50px;'><textarea id='apiReplyBody' style='height: 300px; padding: 5px'>" + reply + "</textarea></div><br>";

    bodyStr += "<label style='float: left' '>回复描述：</label><br><br>";
    bodyStr += "<div style='padding-left:50px; padding-right: 50px;'><textarea id='apiReplyDesc' style='height: 100px; padding: 5px'>" + replyDesc + "</textarea></div><br>";

    return bodyStr;
}


function raiseAPI(apiId, type) {

    var bodyStr = "";
    var label = "API请求";
    var data = null;

    api = getApi(apiId);
    if (api == null) {
        raiseErrorAlarm(null, "获取API失败！");
        return;
    }

    if (type == "reply") {
        label = "API回复--" + api["name"];
        data = api["replyStr"];
        replyDesc = api["replyDesc"];
        bodyStr = createAPIReply(data, replyDesc);
    } else if (type == "request") {
        label = "API请求--" + api["name"];
        data = api["request"];
        bodyStr = createAPIBody(data, type);
    } else {
        label = "URL参数列表--" + api["name"];
        data = api["urlParas"];
        bodyStr = createAPIBody(data, type);
    }

    var footer = createApiFooter(type, apiId);

    return raiseAPIModal(label, bodyStr, footer);
}

function strDate_2_second(dateStr) {
    return Date.parse(dateStr) / 1000;
}

function isExpired(dateStr, expireDate) {
    var now = strDate_2_second(dateStr);
    var expire = strDate_2_second(expireDate);
    result = now > expire;
    return result;
}

function isWillExpired(dateStr, expireDate) {
    var now = strDate_2_second(dateStr) + 60 * 60 * 24 * 30; // 30 days
    var expire = strDate_2_second(expireDate);
    result = expire < now;
    return result;
}

function getCurrentDate() {
    today = new Date();
    return today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
}

function isLicenseExpired(expireDate) {
    today = getCurrentDate();
    return isExpired(today, expireDate);
}

function isLicenseWillExpired(expireDate) {
    today = getCurrentDate();
    return isWillExpired(today, expireDate);
}


function getApiString(type, apiId) {

    var json = {};

    api = getApi(apiId);
    if (api == null) {
        return "";
    }

    if (type == "reply") {
        json["reply"] = api["reply"];
        json["replyDesc"] = api["replyDesc"];
    } else if (type == "request") {
        json = api["request"];
    } else {
        json = api["urlParas"];
    }

    return JSON.stringify(json);
}

function commitApiRequest(type, apiId) {

    var bodyStr = "{";
    var json = {};
    var $apiTable = $("#apiRequest");

    if (type == "request" || type == "urlparas") {
        var $trs = $apiTable.children("tbody").children("tr");
        $trs.each(function(index){
            var $tr = $(this);
            if (index != 0) {
                $tds = $tr.children("td");

                name = $tds[0].children[0].value;
                if (name.length > 0) {
                    valueType = $tds[1].children[0].value;
                    value = $tds[2].children[0].value;
                    valueDesc = $tds[3].children[0].value;

                    jsonItem = {
                        "type": valueType,
                        "valueDesc": valueDesc,
                        "value": value
                    };

                    json[name] = jsonItem;
                }
            }
        });


    } else {
        var replyBody = $("#apiReplyBody").val();
        var replyDesc = $("#apiReplyDesc").val();

        try {
            replyBodyJson = JSON.parse(replyBody);
        } catch (e){
            alert("错误的JSON串！");
            return;
        }

        json["reply"] = replyBodyJson;
        json["replyDesc"] = replyDesc;
    }

    bodyStr = JSON.stringify(json);
    oldStr = getApiString(type, apiId);

    console.log(oldStr);
    console.log(bodyStr);

    if (bodyStr == oldStr) {
        $("#modalApi").modal("hide");
        return;
    }

    httpPost("/ui/api/" + apiId + "/" + type + "/", bodyStr, function(){
        window.location.href = "/ui/api/" + window.location.search;
    });
}

function append_conditions() {
    conditions = window.location.search;
    if (conditions == "") {
        return;
    }
    var conditionAttr = $(".need_append_condition");
    for (var i = 0; i < conditionAttr.length; i++) {
        tochange = conditionAttr[i];
        if (tochange.href) {
            tochange.href += conditions;
        }

        if (tochange.action) {
            tochange.action += conditions;
        }
    }
}