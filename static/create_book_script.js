
document.addEventListener('DOMContentLoaded', function () {
    var add_author_checkbox = document.querySelector("[name = 'authors'][value = 'None']");
    var add_author_name_form = document.querySelector("#div_id_author_name");
    var add_author_surname_form = document.querySelector("#div_id_author_surname");
    add_author_name_form.style.display = "none";
    add_author_surname_form.style.display = "none";

    function newAuthorNeeded(add_author_checkbox, add_author_name_form, add_author_surname_form){
        if (add_author_checkbox.checked == true){
            add_author_name_form.style.display = "block";
            add_author_surname_form.style.display = "block";
        }
        else {
            add_author_name_form.style.display = "none";
            add_author_surname_form.style.display = "none";
        }
    }

    add_author_checkbox.addEventListener('click', function () {
        newAuthorNeeded(this, add_author_name_form, add_author_surname_form)
    })

});
