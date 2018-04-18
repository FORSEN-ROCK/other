//chrome.contextMenus.onClicked.addListener(function(e,t){var n,r,o;return r=e.menuItemId[0],n=e.menuItemId.slice(1),r=getType(r),o=getValue(e,t,r),openTab(n,r,o,t)})
/*chrome.contextMenus.onClicked.addListener(function(event,tab){
    var n,r,o;
    var testLog = {
    frameId : event.frameId,
    menuItemId : event.menuItemId,
    menuItemId : event.menuItemId,
    }
    console.log(testLog)})
*/

chrome.extension.onMessage.addListener(function(request) {
    console.log(request);
	if(request.resumeId) {//проверяется, от того ли окна и скрипта отправлено
		localStorage['request.origin'] = request.origin;
        localStorage['request.resumeId'] = request.resumeId;
        console.log('Url: ', request.origin);
        console.log('id: ', request.resumeId);
    }
});

function genericOnClick() {
        //return function(){
        var origin = localStorage['request.origin'];
        switch(localStorage['request.origin']) {
            case "https://hh.ru":
                var  request = new XMLHttpRequest();
                
                //request.open("GET", "http://api.hh.ru/resumes/resumeId".replace("resumeId",localStorage['request.resumeId']),true);
                request.open("GET", "https://hh.ru/search/resume?&area=1&clusters=true&text=Siebel&pos=full_text&logic=normal&exp_period=all_time&items_on_page=100&page=0",true);
                //request.setRequestHeader("User-Agent", "hh-recommender");
                //console.log("http://api.hh.ru/resumes/resumeId".replace("resumeId",localStorage['request.resumeId']));
                //request.send();
                request.onreadystatechange = function(){
                    if(request.readyState == 4) {
                        console.log(request.responseText);
                        //var responseFromHh = request.responseText; //По идее строка json с резюме 
                        //var dataParse = JSON.parse(responseFromHh);//Здесь получаем js объект резюме
                        //console.log(dataParse);
                    }
                }
                request.send();
                break;
            case "https://www.superjob.ru":
                //var  request = new XMLHttpRequest();
                //request.open("GET", "	https://api.superjob.ru/2.0/resumes/:id/".replase(":id",localStorage['request.resumeId']),true);
                //if(request.readyState == 4) {
                //    var responseFromHh = request.responseText; //По идее строка json с резюме 
                //    var dataParse = JSON.parse(responseFromHh);//Здесь получаем js объект резюме
                //}
                break;
            case "https://www.rabota.ru":
                break;
            case "http://www.job-mo.ru":
                break;
            case "https://career.ru":
                break;
            case "https://job.ru":
                break;
        }
        //else if(localStorage['request.origin']
        //};
    //}


    /*return function(info, tab) {
        // The srcUrl property is only available for image elements.
        var url = 'info.html#' + info.srcUrl;
        // Create a new window to the info page.
        chrome.windows.create({ url: url, width: 520, height: 660 });
        */
 //};
};
//chrome.contextMenus.onClicked.addListener(genericOnClick);
/*

});
*/


var parent = chrome.contextMenus.create({"title": "Test Seizure", "onclick": genericOnClick});

chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.create({url:chrome.extension.getURL("option.html")});
});