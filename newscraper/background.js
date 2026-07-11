const MCP_SERVER = "https://thascraper-mcp.onrender.com";

async function pollForCommands() {
  try {
    // First, try to retrieve a command
    const response = await fetch(`${MCP_SERVER}/command`);
    if (response.ok) {
      const command = await response.json();
      if (command.action === "startScraping") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, {
            action: "scrape",
            selectors: command.selectors
          });
        });
      }
    }
  } catch (err) {
    console.error("Polling error:", err);
  }
  setTimeout(pollForCommands, 5000);  // Poll every 5 seconds
}

pollForCommands();