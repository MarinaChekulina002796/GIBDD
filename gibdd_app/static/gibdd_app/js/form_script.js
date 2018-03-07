/**
 * Created by Марина on 28.12.2016.
 */
$(function () {
    function validateForm() {
        $('.text-error').remove();
        var c_title = false;
        var c_image = false;
        var c_category = false;
        var c_text = false;
        var c_video = false;
        var c_date = false;

        var el_t = $('#title');
        if (el_t.val().length > 100) {
            c_title = true;
            $('.channel-title').after('<span class="text-error">Название канала должно быть меньше 100 символов</span>');
        }
        if (el_t.val().length == 0) {
            c_title = true;
            $('.channel-title').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        if ($('form input[type=file]').val().length == 0) {
            c_image = true;
            $('.channel-image').after('<span class="text-error">Выберите файл</span>');
        }

        var el_cat = $('#category');
        if (el_cat.val().length > 50) {
            c_category = true;
            $('.channel-category').after('<span class="text-error">Название категории должно быть меньше 50 символов</span>');
        }
        if (el_cat.val().length == 0) {
            c_category = true;
            $('.channel-category').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_tex = $('#text');
        if (el_tex.val().length == 0) {
            c_text = true;
            $('.channel-text').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_v = $('#video');
        if (el_v.val().length == 0) {
            c_video = true;
            $('.channel-video').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_dat = $('#date');
        if (el_dat.val().length == 0) {
            c_date = true;
            $('.channel-date').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var patt = /^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$/i;
        if (!patt.test(el_dat.val())) {
            c_date = true;
            $('.channel-date').after('<span class="text-error">Введите дату в правильном формате!</span>');
        }

        return (c_title || c_image || c_category || c_text || c_video || c_date);
    }

    $('.add_channel').on('submit', function (event) {
        if (validateForm()) {
            event.preventDefault();
        }
    });

    $('.btn-close').click(function () {
        $('#title').val('');
        $('.text-error').remove();
    });

    /*Бесконечная прокрутка*/
    var last_channel_id = 3;
    $(window).scroll(function () {
        var windowScroll = $(window).scrollTop();
        var windowHeight = $(window).height();
        var documentHeight = $(document).height();

        console.log(windowScroll + ' ' + windowHeight + ' ' + documentHeight);

        if ((windowScroll + windowHeight) >= (documentHeight - 0.2)) {
            $.ajax({
                url: '/add_content',
                type: 'POST',
                dataType: 'json',
                data: {
                    'last_channel_id': last_channel_id,
                    'csrfmiddlewaretoken': $('.add_channel input[name=csrfmiddlewaretoken]').val()
                },
                error: function () {
                    console.log('Error_form_script')
                },
                success: function (data) {
                    if (data.message != 'stop') {
                        $('.channels_list').append(
                            '<div class="row">' +
                            '<div class="col-md-4">' +
                            '<img class="channel_img" src="' + data.message.channel_image + '">' +
                            '</div>' +
                            '<div class="col-md-8">' +
                            '<h2>' +
                            data.message.channel_title +
                            '</h2>' +
                            '<p>' +
                            data.message.channel_text +
                            '</p>' +
                            '<p>' +
                            '<a class="btn btn-default" role="button" href="/item/' + data.message.channel_id + '">' +
                            'View details &raquo;' +
                            '</' + 'a>' +
                            '</p>' +
                            '</div>' +
                            '</div>'
                        );
                        last_channel_id += 1;
                    }
                }
            });
        }
    });

});













