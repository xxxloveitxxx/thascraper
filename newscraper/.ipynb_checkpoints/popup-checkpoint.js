document.getElementById('startScraping').addEventListener('click', () => {
    chrome.runtime.sendMessage({
        action: "startScraping",
        selectors: {
            price: ".price",
            address: ".address"
        }
    });
});