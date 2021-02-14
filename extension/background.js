"use strict";

const MIN_WORDS = 5;
const BASE_HREF = "http://127.0.0.1:5000";

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

  const checkFact = fetch(BASE_HREF + '/check', {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-Type': 'application/json'
    },
    body: "{\"text\": \""+ text + "\"}"
  }).then(res => res.json());

  checkFact.then((result) => {
    chrome.tabs.sendMessage(tabId, {
      requested: "createPopup",
      body: { data: { text, isFact: result.score }, info: { url, height, width } },
    });
  })
};

chrome.contextMenus.create(item);
chrome.contextMenus.onClicked.addListener(onClickedSelection);
