$(document).ready(function () {
    $('#processingbar').hide();
    $('#loaderbar').hide();
    $('#itemsbar').hide();
    $('#submit').hide();
    $('#fix_but').hide();

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

                    var label = $('<label>').text("QTY: 1").addClass("imagelabel").attr('id', 'qtylabel_' + id);
                    var img = $('<img>').attr('src', 'download/' + file).addClass('img').attr('alt', file).attr('id', 'monitor_' + file);

                    var div = $('<div>').attr('id', id).addClass('imagebar').click(function () {
                        var file = $(this).find('img').attr('alt');

                        var modal_img = $('<img>').attr('src', 'download/' + file).addClass('img').attr('alt', file);
                        var accept_but = $('<button>').addClass('rejectbut').text('Accept').click(function () {

                            var file = $(this).parent().find('img').attr('alt');
                            var id = file.split('.')[0];

                            if ($('#' + id).hasClass('rejected_imagebar')) {
                                $('#' + id).removeClass('rejected_imagebar');
                                $('#' + id).addClass('imagebar');
                            }

                            var rejected_items = $('#itemsbar').find('.rejected_imagebar');

                            if (rejected_items.length == 0) {
                                $('#approve_but').show();
                                $('#fix_but').hide();
                            }

                            $('#modal').hide();
                        });

                        var reject_but = $('<button>').addClass('rejectbut').text('Reject').click(function () {

                            var file = $(this).parent().find('img').attr('alt');
                            var id = file.split('.')[0];

                            if ($('#' + id).hasClass('imagebar')) {
                                $('#' + id).removeClass('imagebar');
                                $('#' + id).addClass('rejected_imagebar');
                            }

                            $('#approve_but').hide();
                            $('#fix_but').show();

                            $('#modal').hide();
                        });

                        var qty_label = $('<label>').addClass('qty_label').text('QTY : ');
                        var qty_input = $('<input>').attr('type', 'number').val(1).addClass('qty_input').attr('min', '0').change(function () {
                            var updated_quantity = $(this).val();

                            $.ajax({
                                url: '/updateQuantity',
                                method: 'POST',
                                data: { name: file, quantity: updated_quantity },
                                success: function (result) {
                                    if (result.status === "good") {
                                        console.log(result.status);
                                        $("#qtylabel_" + id).text("QTY: " + updated_quantity);
                                    }
                                }
                            });

                        });

                        var qty_div = $('<div>');
                        qty_div.append(qty_label);
                        qty_div.append(qty_input);

                        $(".modal-content").html("");
                        $(".modal-content").append(qty_div);
                        $(".modal-content").append(modal_img);
                        $(".modal-content").append(accept_but);
                        $(".modal-content").append(reject_but);

                        $('#modal').show();
                    });



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
        var items = $('#itemsbar').find('.imagebar');

        items.each(function (index, item) {
            var key = $(item).find('img').attr('alt');
            var value = true;

            $.ajax({
                url: '/submit',
                method: 'POST',
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
