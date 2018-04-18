chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.create({url:chrome.extension.getURL("option.html")});
});

document.addEventListener("click", function(tab) {
    chrome.tabs.create({url:"background.html"});
    //chrome.tabs.create({url:"searchPageWidget.html"});
    //chrome.windows.create({ url + "option.html", width: 520, height: 660 });
});