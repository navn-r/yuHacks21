"use strict";

const MIN_WORDS = 5;

const item = {
  id: "factCheckContextMenu",
  title: "FæktChɛk - Fact Check Selection",
  contexts: ["selection"],
};

const onClickedSelection = (
  { menuItemId: itemId, selectionText: text },
  { url, id: tabId, height, width }
) => {
  text = text.trim();
  if (itemId !== item.id || text.split(" ").length < MIN_WORDS) {
    console.log("not enough text"); // TODO: add error popup here
    return;
  }

  // TODO: fetch call here
  const checkFact = Promise.resolve({
    text, isFact: Math.round(Math.random())
  });

  checkFact.then((data) => {
    chrome.tabs.sendMessage(tabId, {
      requested: "createPopup",
      body: { data, info: { url, height, width } },
    });
  })
};

chrome.contextMenus.create(item);
chrome.contextMenus.onClicked.addListener(onClickedSelection);
