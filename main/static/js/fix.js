$(document).ready(function () {
    $('.imagebar').click(function () {
        console.log("Clicked");
        var file = $(this).find('img').attr('alt');

        var img = $('<img>').attr('src', 'source/' + file).addClass('modal_img').attr('alt', file);
        var label = $('<label>').addClass('upload');

        var inside_span = $('<span>').addClass('title').text('Browse...');
        var span = $('<span>').addClass('upload_content');

        span.append(inside_span);

        var input = $('<input>').attr('type', 'file').attr('accept', 'image/*').attr('id', file).change(function () {
            var fileData = new FormData();
            var name = this.id;
            var file = $(this).prop('files')[0];
            fileData.append('files[]', file);
            fileData.append('name', name);

            $.ajax({
                url: '/processFix',
                method: 'POST',
                data: fileData,
                processData: false,
                contentType: false,
                success: function (result) {
                    $('.modal').hide();
                    $('#imagebar_' + name).remove();
                    location.reload();
                }
            });
        });

        label.append(span);
        label.append(input);

        $('.modal-content').html("");
        $('.modal-content').append(img);
        $('.modal-content').append(label);

        $('.modal').show();

    });
});