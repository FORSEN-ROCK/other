//Канцептуальный дерьмокод

//Хз на сколько верен данный подход, но сделаем так

//Предопределенные объекты парсеры( регулярные вырожения)

var parserForHh = {
    pageNamber: /.+\&page=/g,
    linkResumes: /\/resume\/\w+/g,
    bodyInfo: "tr[itemscope='itemscope']",//"div[class='output__main']",//пока так нужно корректировать 
    update: "div[class='output__addition']",//пока так нужно корректировать 
    resumeLinkInnerHtml: "a[itemprop='jobTitle']",//пока так нужно корректировать 
};
var parserForZarplata = {
    pageNamber: /.+\&page=/g,
    linkResumes: null,
    bodyInfo: "div[class='ui grid']",
    update: "div[style='margin-top: 5px;']",
    resumeLinkInnerHtml: "a[target='_blank']"//<a href="http:\/\/hr.zarplata.ru\/resumes\/\?.+">.+?<\/a>/g
};
var parserForSuperjob = {
    pageNamber: /.+\&page=/g,
    linkResumes: null,
    bodyInfo: "div[class='ResumeListElementNew js-resume-item']",//>.+?/g,//пока так нужно корректировать sj_block m_b_1 sj_panel 
    update: "div[class='h_color_gray ResumeListElementNew_updated']",
    resumeLinkInnerHtml: "a[target='_blank']"//<a .+? href="https:\/\/www.superjob.ru\/resume\/.+">.+?<\/a>/g
};
var parserForRabota = {
    pageNamber: /.+\&page=/g,
    linkResumes: null,
    bodyInfo: "div[class='h-box-wrapper']",//<div class="sj_flex_col2">.+?/g,//пока так нужно корректировать 
    update: "p[class='box-wrapper__descr_12grey mt_10']",
    resumeLinkInnerHtml: "a[target='_blank']"//<a .+? href="https:\/\/www.superjob.ru\/resume\/.+">.+?<\/a>/g
};
var parserForAvito = {
    pageNamber: /.+\&page=/g,
    linkResumes: /\/moskva\/rezume\/\w+/g,
    bodyInfo: "div[class='description item_table-description']",//<div class="sj_flex_col2">.+?/g,//пока так нужно корректировать 
    update: "div[class='clearfix ']",
    resumeLinkInnerHtml: "a[class='item-description-title-link']"
};

var parseLayout = {
    hh: parserForHh,
    zarplata: parserForZarplata,
    superjob: parserForSuperjob,
    avito: parserForAvito,
    rabota: parserForRabota
};

var LinkHh = {
    link: "https://hh.ru/search/resume?area=1&clusters=true&text=searchSpec&pos=full_text&logic=normal&exp_period=all_time"
};

var LinkZarplata = {
    link: "https://www.zarplata.ru/resume?q=uri+searchSpec"
};

var LinkSuperjob = {
    link: "https://www.superjob.ru/resume/search_resume.html?sbmit=1&t[]=4&keywords[0][srws]=7&keywords[0][skwc]=and&keywords[0][keys]=searchSpec"
};

var LinkRabota = {
    link: "https://www.rabota.ru/v3_searchResumeByParamsResults.html?action=search&area=v3_searchResumeByParamsResults&p=-2005&w=&qk%5B0%5D=searchSpec"
};

var LinkAvito = {
    link: "https://www.avito.ru/moskva/rezume?s=2&q=searchSpec"
};

var links = {
    hh:LinkHh,
    zarplata:LinkZarplata,
    superjob:LinkSuperjob,
    rabota:LinkRabota,
    avito:LinkAvito
};
//Сиё вынести в отдельный файл

function generalSerchSpeack(option) { //mainCriterion: object; addCriteria: object
    mainCriterion = option.mainCriterion || null;
    searchScheme = option.searchScheme || null;
    page = option.page || null;
                
    if(searchScheme == "" || searchScheme == '') {
        return null;
    }
                
    if((!mainCriterion && searchScheme)&&(searchScheme && page)) {
        //var reg = /.+\&page=/g;
        var search = searchScheme.match(reg);
        search += String(page);
        return search;
    }
             
    var search = searchScheme;
    for(key in mainCriterion){
        if(mainCriterion[key] == 'none') {
            continue;
        }
                    
        search += "&" + key + "=" + mainCriterion[key];
    }
                
    //search += "&items_on_page=100&page=0";
    return search;
};

function handlerResponse(responseText) {
    return function(){
        rex = /<div class="sticky-container">\.+<\/div>/g;
        contein = String(responseText).match(rex);
        console.info(contein);
        
    };
};

//По идее здесь только обработчики в се остальное вынести 

function focusHandler(event) {
    var target = event.target;
    if(target.dataset.entry != undefined){
        target.value = '';    
    }
};

function clicHandler(event) {
    var target = event.target;
    if(target.dataset.command == undefined){
        return;
    }
    search = target.form[0].value;
    if(search == ""){
        return;
    }
    var limitSample = 0^(document.forms[0].limitField.value);
    if(limitSample == "" && (limitSample < 0 || limitSample > 100)){
        limitSample = 20;
    }
    console.log(search);
    searchRun(search, limitSample);
    //handlerResponse(testrex);
};
/*
function searchRun(searchSpec, limitSample) {
    var searchLinks = Object.assign({},links);
    for( var key in searchLinks){
        searchLinks[key].link = searchLinks[key].link.replace("searchSpec", searchSpec);
    }
    var rexp = /\w{4,5}:\/\/(\w+|www\.\w+)\.ru/g;
    var rexLink = /\/resume\/\w+/g;
    var quantityRecord = 20;
    for(var key in searchLinks) {
    //var key = 'hh';
        var domain = searchLinks[key].link.match(rexp);
        console.log(domain);
        request = new XMLHttpRequest();
        request.open("GET", searchLinks[key].link, false);
        request.send(null);  
        var answer = document.body.querySelector("#listAnswer");
        var buff = document.createDocumentFragment();
        if(request.readyState == 4 && request.status == 200) {
            var div = document.createElement('div');
            div.innerHTML = request.responseText;
            var resumeRecords = div.querySelectorAll(parseLayout[key].bodyInfo);
            if(resumeRecords.length >= limitSample) {
                quantityRecord = limitSample;
            } 
            else{
                quantityRecord = resumeRecords.length;
            }
            for(var i = 0; i < quantityRecord; i++){
                var item = document.createElement("il");
                var link = document.createElement("a");
                linkResume = resumeRecords[i].querySelector(parseLayout[key].resumeLinkInnerHtml);
                console.log(linkResume.href);
                var updataLink = domain + linkResume.href.match(parseLayout[key].linkResumes);
                linkResume.href = updataLink;
                console.log(updataLink);
                item.innerHTML = resumeRecords[i].innerHTML;
                buff.appendChild(item);
            }
        }
        answer.appendChild(buff);
    }
};
*/
function getSearchParametrs(){
    var parentForm = document.forms[0];
    var searchSpec = parentForm.searchField.value;
    var limitSample = 0^parentForm.limitField.value;
    if(limitSample == "" || limitSample <= 0) {
        limitSample = 20;
    }
    else if(limitSample > 100){
        limitSample = 100;
    }
    if(searchSpec.indexOf(" ",1) != -1){
        searchSpec = searchSpec.replace(" ", "+");
    }
    return {searchSpec:searchSpec, limitSample:limitSample};
};

function generalLinkOject(searchSpec){
    var linckObject = JSON.parse(JSON.stringify(links));
    for( var key in linckObject){
        linckObject[key].link = linckObject[key].link.replace("searchSpec", searchSpec);
    }
    return linckObject;
};

function searchingRequest(linckObject){
    var searchingResponse = {};
    for(var key in linckObject) {
        request = new XMLHttpRequest();
        request.open("GET", linckObject[key].link, false);
        request.send(null);  
        if(request.readyState == 4 && request.status == 200) {
            searchingResponse[key] = request.responseText;
            request.abort();
        }
    }
    return searchingResponse;
};
function showeResult(responseObject, linckObject, DOMContainerResult, limitSample){
    if(!responseObject || !DOMContainerResult){
        return;
    }
    
    var rexDomain = /\w{4,5}:\/\/(\w+|www\.\w+)\.ru/g, rexLinkResume = /\/resume\/\w+/g;
    var buff = document.createDocumentFragment();
    var count = 0;
    for(var key in responseObject){//Цикл по обекту ответов
        var domain = linckObject[key].link.match(rexDomain);
        var div = document.createElement('div');
        div.innerHTML = responseObject[key];
        //console.log(key + " = > " + responseObject[key]);
        var resumeRecords = div.querySelectorAll(parseLayout[key].bodyInfo);
        
        if(resumeRecords.length >= limitSample) {
            quantityRecord = limitSample;
        } 
        else{
            quantityRecord = resumeRecords.length;
        }
        
        for(var i = 0; i < quantityRecord; i++){
            count++;
            var itemList = document.createElement("il");
            var itemDiv = document.createElement("div");
            var link = document.createElement("a");
            if(domain != "https://www.rabota.ru" && domain != "https://www.superjob.ru"){
                linkResume = resumeRecords[i].querySelector(parseLayout[key].resumeLinkInnerHtml);
                var updataLink = domain + linkResume.href.match(parseLayout[key].linkResumes);
                linkResume.href = updataLink;
            }
            itemDiv.innerHTML = resumeRecords[i].innerHTML;
            itemDiv.className = "itemList";
            itemList.appendChild(itemDiv);
            buff.appendChild(itemList);
            /*if(i == quantityRecord - 1){
                var buttonContainer = document.createElement("li");
                var nextResult = document.createElement("input");
                nextResult.type = "button";
                nextResult.value = "Еще результаты из данного источника";
                nextResult.dataset.command = "nextResult";
                buttonContainer.appendChild(nextResult);//innerHTML = nextResult;
                buff.appendChild(buttonContainer);
            }*/

            
        }
        DOMContainerResult.appendChild(buff)
        console.log(count);
    }
};

function handlerRunButton(event){
    if(event.target.dataset.command == "ranSearch"){
        var searchingResults = document.body.querySelector("#searchingResults");//по идее тоже должны называться результатами
        //var buttonRun = document.body.querySelector("input[name='run']");
        var searchSpec = getSearchParametrs().searchSpec;
        var limitSample = getSearchParametrs().limitSample;
        if(searchSpec != ""){
            if(searchingResults.children.length != 0){
                console.log(searchingResults.children.length);
                while(searchingResults.children.length){
                    searchingResults.removeChild(searchingResults.lastChild);
                }
            }
            var linckObject = generalLinkOject(searchSpec);
            var searchingResponse = searchingRequest(linckObject);
            showeResult(searchingResponse, linckObject, searchingResults, limitSample);
            event.target.value = "Поиск";
        }
        
    }
}




document.addEventListener("focus",focusHandler);
//document.forms[0].run.addEventListener("click",handlerRunButton);
/*document.addEventListener("click", function(event) {
    if(event.target.dataset.command == "ranSearch"){
        event.target.value = "Идет поиск....";
    }
});
*/
document.addEventListener("click",handlerRunButton);


//document.addEventListener("click",clicHandler);