$(document).on('click', '.menu-link,.crud-update', function(event) {
    event.preventDefault();

    var url = $(this).attr('href');

    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {

            var content = $(data).find('#content').html();
            var menu = $(data).find('#mainmenu').html();

            $('#mainmenu').html(menu);
            $('#content').html(content);

            history.pushState(null, '', url);

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

$(window).on('popstate', function() {
    event.preventDefault();

    var url = window.location.href;
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            var content = $(data).find('#content').html();
            $('#content').html(content);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

$('#search_form').submit(function(event) {
    event.preventDefault();

    var query = $('input[name="query"]').val();

    $.ajax({
        url: searchUrl,
        type: 'GET',
        data: { query: query },
        success: function(data) {
            var paginator = $(data).find('#pagination').html();

            if (typeof paginator === 'undefined') {
                $('#pagination').hide();
            } else {
                $('#pagination').html(paginator).show();
            }

            var search_result = $(data).find('#dataset-list').html();

            $('#dataset-list').html(search_result);

            var newUrl = searchUrl + '?query=' + query;
            history.pushState(null, '', newUrl);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

$('#add_form').submit(function(event) {
    event.preventDefault();

    var form = $('#add_form');
    var url = form.attr('action');

    $.ajax({
        url: url,
        type: 'POST',
        data: form.serialize(),
        success: function(data) {
            var paginator = $(data).find('#pagination').html();

            if (typeof paginator === 'undefined') {
                $('#pagination').hide();
            } else {
                $('#pagination').html(paginator).show();
            }

            var content = $(data).find('#content').html();

            $('#content').html(content);

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

$('#update_form').submit(function(event) {
    event.preventDefault();

    var form = $('#update_form');
    var url = form.attr('action');

    $.ajax({
        url: url,
        type: 'POST',
        data: form.serialize(),
        success: function(data) {
            var paginator = $(data).find('#pagination').html();

            if (typeof paginator === 'undefined') {
                $('#pagination').hide();
            } else {
                $('#pagination').html(paginator).show();
            }

            var content = $(data).find('#content').html();

            $('#content').html(content);

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

$('#delete_form').submit(function(event) {
    event.preventDefault();

    var form = $('#delete_form');
    var url = form.attr('action');

    $.ajax({
        url: url,
        type: 'POST',
        data: form.serialize(),
        success: function(data) {
            var paginator = $(data).find('#pagination').html();

            if (typeof paginator === 'undefined') {
                $('#pagination').hide();
            } else {
                $('#pagination').html(paginator).show();
            }

            var datasets = $(data).find('#dataset-list').html();

            $('#dataset-list').html(datasets);

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

function load_profile() {
    event.preventDefault();

    $.ajax({
        url: profileURL,
        type: 'GET',
        success: function(data) {
            var content = $(data).find('#content').html();
            $('#content').html(content);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
};

$(document).on('click', '.api-delete,.api-generate', function(event) {
    event.preventDefault();

    var url = $(this).attr('href');

    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            load_profile();
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});
