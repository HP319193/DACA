$(document).ready(function () {
    $('#processingbar').hide();
    $('#loaderbar').hide();
    $('#itemsbar').hide();
    $('#submit').hide();

    $('#imageUpload').change(function () {
        var fileData = new FormData();

        var files = $(this).prop('files');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrfToken);
        for (var i = 0; i < files.length; i++) {
            fileData.append('files[]', files[i]);
        }

        $('#browserbar').hide();
        $('#processingbar').show();
        $('#loaderbar').show();

        $.ajax({
            url: '/processImage',
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            data: fileData,
            processData: false,
            contentType: false,
            success: function (result) {
                $('#processingbar').hide();
                $('#loaderbar').hide();
                $('#itemsbar').show();
                $('#itemsbar').html("");
                $('#submit').show();

                $.each(result.filelist, function (index, file) {
                    console.log(typeof (file));

                    var id = file.split('.')[0];

                    var div = $('<div>').attr('id', id).addClass('imagebar').click(function () {
                        var file = $(this).find('img').attr('alt');
                        var modal_img = $('<img>').attr('src', 'download/' + file).addClass('img').attr('alt', file);
                        var modal_but = $('<button>').addClass('rejectbut').text('Reject').click(function () {

                            var file = $(this).parent().find('img').attr('alt');
                            var id = file.split('.')[0];

                            $('#' + id).css('background-color', 'red');
                            $('#modal').hide();
                        });

                        $(".modal-content").html("");
                        $(".modal-content").append(modal_img);
                        $(".modal-content").append(modal_but);

                        $('#modal').show();
                    });
                    var label = $('<label>').text("QTY: 1").addClass("imagelabel");
                    var img = $('<img>').attr('src', 'download/' + file).addClass('img').attr('alt', file);

                    div.append(label);
                    div.append(img);

                    $('#itemsbar').append(div);
                });
            },
            error: function (xhr, status, error) {
                console.error('Error occurred: ', error);
            }
        });
    });

    $('#submit').click(function () {
        console.log("Here");
        var items = $('#itemsbar').find('.imagebar');

        items.each(function (index, item) {
            console.log($(item).css('background-color'));

            var key = $(item).find('img').attr('alt');

            var value = true;
            if ($(item).css('background-color') == "rgb(255, 0, 0)")
                value = false;

            $.ajax({
                url: '/submit',
                method: 'POST',
                data: { key: key, value: value },
                success: function (result) {
                    console.log(result);
                }

            });
        });

        $('#submit').hide();
        $('#itemsbar').hide();
        $('#browserbar').show();
    });
});

window.onclick = function (event) {
    if (event.target == document.getElementById("modal")) {
        modal.style.display = "none";
    }
}
