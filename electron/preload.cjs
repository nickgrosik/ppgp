const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("ppgpDesktop", {
  getBackendBaseUrl: () => "http://127.0.0.1:8000",
  browseFile: (options) => ipcRenderer.invoke("dialog:open-file", options)
});
