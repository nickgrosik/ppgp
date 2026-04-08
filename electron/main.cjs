const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const path = require("path");

const isDev = false;

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 980,
    minWidth: 1120,
    minHeight: 760,
    backgroundColor: "#efe3d0",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  if (isDev) {
    win.loadURL("http://127.0.0.1:5173");
    win.webContents.openDevTools({ mode: "detach" });
  } else {
    const indexPath = path.resolve(__dirname, "../dist/index.html");
    win.loadFile(indexPath);
  }
}

ipcMain.handle("dialog:open-file", async (_event, options = {}) => {
  const result = await dialog.showOpenDialog({
    properties: options.directory ? ["openDirectory"] : ["openFile"],
    title: options.title || "Select a file"
  });

  if (result.canceled || result.filePaths.length === 0) {
    return null;
  }

  return result.filePaths[0];
});

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
