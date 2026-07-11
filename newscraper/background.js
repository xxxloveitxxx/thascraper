const MCP_SERVER = "wss://thascraper-mcp.onrender.com/ws";  // Render URL
let socket;

function connectWebSocket() {
  socket = new WebSocket(MCP_SERVER);

  socket.onmessage = (event) => {
    const command = JSON.parse(event.data);
    if (command.action === "startScraping") {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {
          action: "scrape",
          selectors: command.selectors
        });
      });
    }
  };

  socket.onclose = () => {
    setTimeout(connectWebSocket, 5000);  // Reconnect
  };
}

connectWebSocket();