window.addEventListener("contextmenu", function(event) {
    switch(window.location.origin) {
        case "https://hh.ru":
            var parent = event.target.closest("tr[itemscope='itemscope']");
            if(parent) {
                var id = parent.dataset.hhResumeHash;
            }else{
                return;
            }
            break;
        case "https://www.superjob.ru":
            var parent = event.target.closest("div[class='ResumeListElementNew js-resume-item']");
            if(parent) {
                containerResumeId = parent.querySelector("div[class='sj_block m_t_3 ng-isolate-scope ng-hide']");
                if(containerResumeId) {
                    var id = containerResumeId.getAttribute("resume-id");
                }
            }
            else {
                return;
            }
            break;
        case "https://www.rabota.ru":
            var target = event.target;
            var containerResumeId;
            if(target.matches("div[class='b-center__box resum_rez_item  resum_rez_active']")) {
                containerResumeId = target;
            }
            else if(target.matches("div[class='b-center__box resum_rez_item ']")){
                containerResumeId = target;
            }
            else {
                if(target.closest("div[class='b-center__box resum_rez_item  resum_rez_active']")){
                    containerResumeId = target.closest("div[class='b-center__box resum_rez_item  resum_rez_active']");
                }else {
                    containerResumeId = target.closest("div[class='b-center__box resum_rez_item ']");
                }
            }
            if(!containerResumeId){
                return;
            }
            var id = containerResumeId.dataset.resumeId;
            break;
        case "http://www.job-mo.ru":
            var container = event.target.closest("tr");
            var hrefResumeId = container.querySelector("a[target='_blank']");
            if(!hrefResumeId) {
                hrefResumeId = container.previousElementSibling.querySelector("a[target='_blank']");
            }
            if(!hrefResumeId) {
                return;
            }
            var id = hrefResumeId.getAttribute("href");
            break;
        case "http://www.avito.ru":
            console.log("dwkd;lwkde");
            //var container = event.target.closest("tr");
            //var hrefResumeId = container.querySelector("a[target='_blank']");
            //if(!hrefResumeId) {
            //    hrefResumeId = container.previousElementSibling.querySelector("a[target='_blank']");
            //}
            //if(!hrefResumeId) {
            //    return;
            //}
             anchor.click(function() {chrome.tabs.create({url:"searchPageWidget.html"});});
            var id = "http://www.avito.ru";
            break;
        //case "https://career.ru":
            //handlerk
        //    break;
        //case "https://job.ru":
            //handler
        //    break;
    }
    if(id){
        chrome.extension.sendMessage({resumeId: id,origin: window.location.origin});
    }
});