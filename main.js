const { app, BrowserWindow } = require("electron");
const path = require("path");
const { startBackend, stopBackend } = require("./backend-launcher");

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, "preload.js")
    }
  });

  win.loadURL("http://127.0.0.1:8000/docs");

  win.on("closed", () => {
    stopBackend();
    win = null;
  });
}

app.whenReady().then(() => {
  startBackend();
  setTimeout(createWindow, 1200); // give backend time to boot
});

app.on("window-all-closed", () => {
  stopBackend();
  app.quit();
});
