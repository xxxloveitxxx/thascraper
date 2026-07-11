// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scrape") {
    scrapePage(request.selectors);
  }
});

// Listen for direct events (for testing)
document.addEventListener('scrapeEvent', (e) => {
  scrapePage(e.detail.selectors);
});

function scrapePage(selectors) {
  const data = {};
  for (const [key, selector] of Object.entries(selectors)) {
    data[key] = Array.from(document.querySelectorAll(selector))
      .map(el => el.textContent.trim());
  }
  
  // Send data to MCP server
  fetch("https://thascraper-mcp.onrender.com/results", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  }).then(response => {
    if (!response.ok) {
      console.error("Failed to send data to MCP server");
    }
  }).catch(err => {
    console.error("Error:", err);
  });
}