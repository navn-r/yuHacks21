(() => {
  chrome.storage.local.get('text', ({text}) => {
    const div = document.createElement('h1');
    div.innerText = text;
    document.body.appendChild(div);
  });
})()