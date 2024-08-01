$(document).ready(function () {
    $(".processHeader").click(function (e) {
        $(e.target).next().toggle();
    });

});
function statusSet() {

    var processPanels = $(".processPanel")

    for (let panel of processPanels) {

        console.log(panel)
        $(panel).find(".imagePanel").hide();
        let rejectImages = $(panel).find(".rejected");
        let ApprovedImages = $(panel).find(".approved");
        let fixedImages = $(panel).find(".fixed");
        console.log(rejectImages)
        if (rejectImages[0])
            $(panel).find(".processHeader").append("<div style='color:red'>Rejected</div>").css("background-color", "#ffcccc");

        else if (fixedImages[0]) $(panel).find(".processHeader").append("<div style='color:gray'>Fixed</div>").css("background-color", "#ccffff");
        else $(panel).find(".processHeader").append("<div style='color:#0099ff'>Approved</div>").css("background-color", "#b3ecff");
        // else $(panel).find(".processHeader").append("<div style='color:gray'>Fixed</div>").css("background-color", "#f0f5f5");
    }
}
statusSet();