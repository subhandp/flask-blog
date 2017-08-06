//The comments.js code handles POSTing the form data, serialized as JSON, to the
//REST API. It also handles taking the API response and displaying either a success or
//an error message.

Comments = window.Comments || {};

(function(exports, $){
//    Template string untuk me-render success atau error messages
    var alertMarkup = (
           '<div class="alert alert-{class} alert-dismissable">' +
           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
           '<strong>{title}</strong> {body} </div>');

//    Membuat elemen alert
function makeAlert(alertClass, title, body){
    var alertCopy = (alertMarkup
                        .replace('{class}', alertClass)
                        .replace('{title}', title)
                        .replace('{body}', body)
                    );
    return $(alertCopy);
}

//Ambil kembali (Retrieve) value from the form fields and return as an object
function getFormData(form){
    return{
        'name': form.find('input#name').val(),
        'email': form.find('input#email').val(),
        'url': form.find('input#url').val(),
        'body': form.find('textarea#body').val(),
        'entry.id': form.find('input[name=entry_id]').val()
    }
}

function bindHandler(){
//    When the comment form is submitted, serialize the form data as JSON and Post it to the API.
    $('form#comment-form').on('submit', function(){
       var form = $(this);
       var formData = getFormData(form);
       var request = $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: JSON.stringify(formData),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
       });

       request.success(function(data) {
        alertDiv = makeAlert('success', 'Success', 'Your comment was posted');
        form.before(alertDiv);
        form[0].reset();
       });

        request.fail(function(){
            alertDiv = makeAlert('danger', 'Error', 'Your comment was not posted');
            form.before(alertDiv);
        });
        return false;
    });
}

exports.bindHandler = bindHandler;

}) (Comments, jQuery);