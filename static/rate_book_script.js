$(document).ready(function () {
    var star_rating = Array.from($("[name='rating']"));

    star_rating.forEach(function (star) {
        $(star).on('click', function (event) {
            var book_id = event.target.dataset.id;
            var rating = event.target.value;
            var url = "/book_rate/"+book_id+"/"+rating;

            $.ajax({
                headers: {"X-CSRFToken":CSRF_TOKEN},
                url: url,
                data: {},
                type: "POST",
                dataType: "json"
            }).done(function(result) {
                var avg_rating_template = $("#avg_rating");
                var avg_rating_result = result.rating_avg.toFixed(1);
                avg_rating_template.text(avg_rating_result)
            }).fail(function (xhr, status, err) {
            });
        });
        });

});




