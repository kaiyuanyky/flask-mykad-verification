var front_filename = ""
var rear_filename = ""

// Remove the fade and tick on the round checkbox from the slides
function resetImageChecked(val) {
    let swiperParent = val.parent().parent().parent();
    let slide = swiperParent.children('.swiper-slide');
    let content = swiperParent.children('.swiper-slide').children('.round-check-content').children('.round-check');

    $(slide, $('.swiper-slide')).each(function () {
        $(this).removeClass('check-fade');
    });

    $(content, $('.round-check')).each(function () {
        $(this).children('.fa').removeClass('overlay fa-check');
    });
}

// If the round checkbox in the slide is clicked, remove fade/tick on other slides, then add fade/tick on current slide
$('.round-check').click(function(){
    resetImageChecked($(this));

    $('#front').val($(this).attr('front-path'));
    $('#rear').val($(this).attr('rear-path'));

    $(this).children('.fa').addClass('overlay fa-check');
    $(this).parent().parent().addClass('check-fade');
});