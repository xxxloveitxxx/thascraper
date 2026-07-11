chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scrape") {
    const data = {};
    for (const [key, selector] of Object.entries(request.selectors)) {
      data[key] = Array.from(document.querySelectorAll(selector))
        .map(el => el.textContent.trim());
    }
    fetch("https://thascraper-mcp.onrender.com/results", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  }
});