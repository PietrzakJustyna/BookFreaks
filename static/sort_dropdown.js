$(document).ready(function () {

    var item = window.localStorage.getItem('sortform');
    $('select[name=how]').val(item);

    $('select[name=how]').change(function() {
       window.localStorage.setItem('sortform', $(this).val());
    });
});
