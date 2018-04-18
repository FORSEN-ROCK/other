chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.create({url:chrome.extension.getURL("option.html")});
});

document.addEventListener("click", function(tab) {
    chrome.tabs.create({url:chrome.extension.getURL("option.html")});
};