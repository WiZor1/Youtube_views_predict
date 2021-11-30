$(function () {
    $('.header__form-moreinfo').on('click', function () {
        $(this).toggleClass('header__form-moreinfo--active');
    });

    $('.header__form-moreinfo').on('click', function () {
        $('.header__form-moreinfo__content-box').animate({
            height: "toggle",
            opacity: "toggle",
        }, "slow");
    });

});

