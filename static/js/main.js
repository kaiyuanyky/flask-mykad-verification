this.swiperData = '';

// Initialize the swiper with the specified attributes
function initializeSwiper(){
	this.swiperData = new Swiper('.mySwiperContainer', {    
		simulateTouch: false,

		slidesPerView: 'auto',
		slidesPerGroup: 1,
		spaceBetween: 50,

		preventClicks: true,
		preventClicksPropagation: false,

		pagination: {
			el: '.swiper-pagination',
			clickable: true,
		},
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		on:{
			init: function(){},
			resize: function(){},
		},
	});
}

function scrollUp() {
	window.scrollTo({
		top: 0,
		behavior: 'smooth'
	});
}

// Return false if no images are selected
function validate() {
	if($('#front').val() === '' || $('#rear').val() === ''){
		$('#errorModal').modal('show'); 
		return false;
	}
	
	return true;
}

// When going back to the loaded page
function pageShown(evt){
	if (evt.persisted) {
		console.log("pageshow event handler called.  The page was just restored from the Page Cache (eg. From the Back button.");
		$("#loader").fadeOut();
	}
}

window.addEventListener("pageshow", pageShown, false);

window.addEventListener('DOMContentLoaded', (e) => {
	$(document).ready(function(){
		// Back to top button
		$('.btn-up').hide();
		$(window).scroll(function() {
			$(this).scrollTop() >= 150 ? $(".btn-up").fadeIn(200) : $(".btn-up").fadeOut(200);
		});

		// Fade in the loader when submitting the form
		$("#verifyForm").on("submit", function(){
			if($('#front').val() !== '' && $('#rear').val() !== '') {
				$("#loader").fadeIn();
			}
		});
	});

	// Only the page of verification needs swiper initialization
	if(window.location.pathname == '/verification')
		this.initializeSwiper();
});