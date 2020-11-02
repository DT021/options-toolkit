const { remote } = require("electron")
import { Utilities } from "./utilities.js"

// Window

const win = remote.getCurrentWindow()

$("#menubar_itmm_toggle_dev").on("click", () =>
    remote.getCurrentWebContents().toggleDevTools()
)

$(".codicon-chrome-close").on("click", () => 
    win.close()
)

$(".codicon-chrome-minimize").on("click", () =>
    win.minimize()
)

$(".codicon-chrome-maximize").on("click", () => {
    if (win.isMaximized())
        win.unmaximize()
    else
        win.maximize()
})

win.on("maximize", () => {
    let x = $(".codicon-chrome-maximize")
    x.removeClass("codicon-chrome-maximize")
    x.addClass("codicon-chrome-restore")
})

win.on("unmaximize", () => {
    let x = $(".codicon-chrome-restore")
    x.removeClass("codicon-chrome-restore")
    x.addClass("codicon-chrome-maximize")
})

// welcome

import { Welcome } from "../js/welcome.js"

$(() => {
    Welcome.init()
    Welcome.render()
})



