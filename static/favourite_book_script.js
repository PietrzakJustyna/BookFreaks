$(document).ready(function () {
    var heart = $(".heart.fa");

    heart.on("click", function () {
        var book_id = this.dataset.id;

        if (this.value !== 1) {
            this.value = 1;
            this.className = "heart fa fa-heart"
        } else {
            this.value = 0;
            this.className = "heart fa fa-heart-o"
        }

        var fav = this.value;
        console.log(fav);
        var url = "/book_fav/" + book_id + "/" + fav;

        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            url: url,
            data: {},
            type: "POST",
            dataType: "json"
        }).done(function (result) {
        }).fail(function (xhr, status, err) {
        });
    });

});
