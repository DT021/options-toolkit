$(document).ready(function(){
    $.ajaxSetup({
        headers: { 'X-CSRFToken': $("meta[name='csrf_token']").attr("content") }
    });
});

function ajax_freeze (){
    $("#main_content").addClass("ajax_freeze");
    $("#main_content").find("input, button, select").prop("disabled", true);
    $("#nav_loading_indicator").css("visibility", "visible");
}

function ajax_unfreeze (object_to_focus){
    $("#main_content").removeClass("ajax_freeze");
    $("#main_content").find("input, button, select").prop("disabled", false);
    $("#nav_loading_indicator").css("visibility", "hidden");
    object_to_focus.focus();
}