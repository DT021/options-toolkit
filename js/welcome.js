const { ipcRenderer } = require("electron")

import { Utilities } from "../js/utilities.js"

export class Welcome {
    static init () {
        Utilities.ipc_on("welcome:render:complete", (e, result) => {
            $(".main_view").append(result)
        })
    }

    static render () {
        Utilities.ipc_send("welcome:render")
    }
}
