const { spawn } = require("child_process");
const path = require("path");
const { app } = require("electron");

let backendProcess = null;

function startBackend() {
  const isDev = !app.isPackaged;

  const backendPath = isDev
    ? path.join(__dirname, "..", "backend")
    : path.join(process.resourcesPath, "app.asar.unpacked", "backend");

  const pythonPath = isDev
    ? path.join(__dirname, "python", "python.exe")
    : path.join(process.resourcesPath, "app.asar.unpacked", "python", "python.exe");

  backendProcess = spawn(
    pythonPath,
    ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    {
      cwd: backendPath,
      detached: false,
      stdio: "pipe"
    }
  );

  backendProcess.stdout.on("data", data => {
    console.log("[Backend]", data.toString());
  });

  backendProcess.stderr.on("data", data => {
    console.error("[Backend ERROR]", data.toString());
  });
}

function stopBackend() {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
}

module.exports = { startBackend, stopBackend };
