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
    const isFact = +data.isFact < 0.3 ? "FAKE NEWS" : +data.isFact > 0.7 ? "REAL NEWS" : "POSSIBLY FAKE";
    const factClass = +data.isFact < 0.3 ? "-fake" : +data.isFact > 0.7 ? "-real" : "-maybe-fake";
    const div = `
      <div id="${BASE_CLASS}-overlay">
          <button class="${BASE_CLASS}-exit-button">x</button>
          <div class="${BASE_CLASS}-container">
              <div class="${BASE_CLASS}-header">
                <h1>FæktChɛk</h1>
              </div>
              <div class="${BASE_CLASS}-content">
                  <h4>Your search for the check:</h4>
                  <p>"${data.text.substring(0, 201) + (data.text.length > 200 ? "..." : "")}"</p>
                  <h4>is <strong class="${BASE_CLASS + factClass}">${isFact}</strong></h4>
                  <h5>with an average truth score of ${Math.round(100*+data.isFact)}%</h5>
              </div>
          </div>
      </div>
    `;
    removeOverlay();
    document.body.innerHTML = div + document.body.innerHTML;
    (document.querySelector(`.${BASE_CLASS}-exit-button`)).addEventListener('click', () => removeOverlay());
  }
});
