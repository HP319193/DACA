$(document).ready(function () {
    $('.here').click(function () {
        var file = $(this).find('img').attr('alt');

        var modal_img = $('<img>').attr('src', 'download/' + file).addClass('img').attr('alt', file);
        var modal_but = $('<button>').addClass('rejectbut').text('Reject / Cancel').click(function () {

            var file = $(this).parent().find('img').attr('alt');
            var id = file.split('.')[0];

            if ($('#' + id).hasClass('imagebar')) {
                $('#' + id).removeClass('imagebar');
                $('#' + id).addClass('rejected_imagebar');
            }
            else {
                $('#' + id).removeClass('rejected_imagebar');
                $('#' + id).addClass('imagebar');
            }

            $('#modal').hide();
        });

        $(".modal-content").html("");
        $(".modal-content").append(modal_img);
        $(".modal-content").append(modal_but);

        $('#modal').show();
    });


    $('#submit').click(function () {
        var items = $('#itemsbar').find('.imagebar');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        items.each(function (index, item) {
            var key = $(item).find('img').attr('alt');
            var value = true;

            $.ajax({
                url: '/submit',
                headers: { 'X-CSRFToken': csrfToken },
                method: 'POST',
                async: false,
                data: { key: key, value: value },
                success: function (result) {
                    console.log(result);
                }

            });
        });

        var rejected_items = $('#itemsbar').find('.rejected_imagebar');

        rejected_items.each(function (index, item) {
            var key = $(item).find('img').attr('alt');
            var value = false;

            $.ajax({
                url: '/submit',
                method: 'POST',
                async: false,
                data: { key: key, value: value },
                success: function (result) {
                    console.log(result);
                }

            });
        });

        $('#submit').hide();
        $('#itemsbar').hide();

        $('body').append("<div class='header' id='noimage'><h1>No awaiting images</h1></div>");
    });
});

window.onclick = function (event) {
    if (event.target == document.getElementById("modal")) {
        modal.style.display = "none";
    }
}
