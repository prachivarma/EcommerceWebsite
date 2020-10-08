$(".menu-toggle").click(function (e) {
    e.preventDefault();
    var className = $("#wrapper").attr('class');
    if (className == 'd-none') {
        $("#wrapper").removeClass('d-none')
        $("#wrapper").addClass('active')
    } else {
        $("#wrapper").removeClass('active')
        $("#wrapper").addClass('d-none')
    }
});