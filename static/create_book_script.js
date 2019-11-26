$(document).ready(function () {
    var id_authors = $('#id_authors');
    var id_categories = $('#id_categories');
    var create_new_author_checkbox = $('#id_create_new_author');
    var add_author_name = $('#div_id_author_name');
    var add_author_surname = $('#div_id_author_surname');


    $(id_authors).select2();
    $(id_categories).select2();

    add_author_name.css("display", "none");
    add_author_surname.css("display", "none");

    create_new_author_checkbox.on('click', function () {
        hide_element(create_new_author_checkbox, add_author_name, add_author_surname)
    });

    function hide_element(checkbox, name, surname) {
        if (checkbox.is(":checked")) {
            name.show();
            surname.show();
        } else {
            name.hide();
            surname.hide();
        }
    }
});
