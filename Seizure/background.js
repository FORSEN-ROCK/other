
chrome.extension.onMessage.addListener(function(request) {
    console.log(request);
	if(request.resumeId) {//�����������, �� ���� �� ���� � ������� ����������
		localStorage['request.origin'] = request.origin;
        localStorage['request.resumeId'] = request.resumeId;
        console.log('Url: ', request.origin);
        console.log('id: ', request.resumeId);
    }
});

function genericOnClick(event) {
        //return function(){
            console.log(event);
        console.log(localStorage['request.origin']);
        var origin = localStorage['request.origin'];
        switch(localStorage['request.origin']) {
            case "https://hh.ru":
                var  request = new XMLHttpRequest();
                
                //request.open("GET", "http://api.hh.ru/resumes/resumeId".replace("resumeId",localStorage['request.resumeId']),true);
                //request.open("GET", "https://hh.ru/search/resume?&area=1&clusters=true&text=Siebel&pos=full_text&logic=normal&exp_period=all_time&items_on_page=100&page=0",true);
                //request.setRequestHeader("User-Agent", "hh-recommender");
                //console.log("http://api.hh.ru/resumes/resumeId".replace("resumeId",localStorage['request.resumeId']));
                //request.send();
                //request.onreadystatechange = function(){
                    //if(request.readyState == 4) {
                     //   console.log(request.responseText);
                        //var responseFromHh = request.responseText; //�� ���� ������ json � ������ 
                        //var dataParse = JSON.parse(responseFromHh);//����� �������� js ������ ������
                        //console.log(dataParse);
                    //}
                //}
                //request.send();
                break;
            case "https://www.superjob.ru":
                //var  request = new XMLHttpRequest();
                //request.open("GET", "	https://api.superjob.ru/2.0/resumes/:id/".replase(":id",localStorage['request.resumeId']),true);
                //if(request.readyState == 4) {
                //    var responseFromHh = request.responseText; //�� ���� ������ json � ������ 
                //    var dataParse = JSON.parse(responseFromHh);//����� �������� js ������ ������
                //}
                break;
            case "https://www.rabota.ru":
                break;
            case "https://www.avito.ru":
                console.info('sdqwdwde');
                chrome.tabs.create({url:"parserWidget _new_add_button.html"});
                //window.open("searchPageWidget.html");
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
