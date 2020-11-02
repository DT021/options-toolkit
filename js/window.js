

export class Window {
    static start_loading_animation () {
        $(".menubar").addClass("menubar_loading")
    }

    static stop_loading_animation () {
        $(".menubar").removeClass("menubar_loading")
    }
}