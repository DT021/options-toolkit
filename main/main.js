const { app, BrowserWindow, ipcMain } = require('electron')
const fs = require("fs")

function createWindow () { 
  const win = new BrowserWindow({
    width: 1400, // TODO: restore size from the previous session.
    height: 1000,
    minWidth: 800,
    minHeight: 600,
    frame: false, // https://www.electronjs.org/docs/api/frameless-window
    menuBarVisible: false,
    backgroundColor: "#222222",
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true
    }
  })
  win.loadFile('html/index.html')
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

ipcMain.on("welcome:render", (e) => {
  e.reply("welcome:render:complete",
    fs.readFileSync(`./html/welcome.html`, {encoding: "utf8", flag: "r"})
  )
})