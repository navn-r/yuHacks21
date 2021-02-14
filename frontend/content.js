"use strict";

// FæktChɛk
// https://developer.chrome.com/docs/extensions/mv2/manifest/
 
const BASE_CLASS = "fact-check-extension";

const removeOverlay = () => {
  const existing = document.getElementById(`${BASE_CLASS}-overlay`);
  if (existing) document.body.removeChild(existing);
}

chrome.runtime.onMessage.addListener((req) => {
  if (req.requested === "createPopup") {
    const { data, info } = req.body;
    const div = `
      <div id="${BASE_CLASS}-overlay">
          <button class="${BASE_CLASS}-exit-button">x</button>
          <div class="${BASE_CLASS}-container">
              <div class="${BASE_CLASS}-header">
                <h1>FæktChɛk</h1>
              </div>
              <div class="${BASE_CLASS}-content">
                  <p>${data.text}</p>
              </div>
          </div>
      </div>
    `;
    removeOverlay();
    document.body.innerHTML = div + document.body.innerHTML;
    (document.querySelector(`.${BASE_CLASS}-exit-button`)).addEventListener('click', () => removeOverlay());
    console.log(data, info);
  }
});
