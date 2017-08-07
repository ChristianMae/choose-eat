$(document).ready(function(){
    $('.parallax').parallax();
    $(".button-collapse").sideNav();
});

function getLocations() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            document.getElementById("id_latitude").value = position.coords.latitude;
            document.getElementById("id_longitude").value = position.coords.longitude;
        });        
    } else { 
        alert("Geolocation is not supported by this browser.");
    }
}

var options = [
    {selector: '#about', offset: 250, callback: function(el) {
        Materialize.showStaggeredList('#about-items');
     } },
    {selector: '#stats', offset: 180, callback: function(el) {
        $('.Count').each(function () {
            var $this = $(this);
            jQuery({ Counter: 0 }).animate({ Counter: $this.text() }, {
               duration: 2000,
	 easing: 'swing',
	 step: function () {
	     $this.text(Math.ceil(this.Counter));
	 }
            });
       });
    } },
    {selector: '#stats', offset: 200, callback: function(el) {
        Materialize.showStaggeredList('#stats-items');
     } }
];
Materialize.scrollFire(options);

$('a[href*=#]').click(function(event){
    $('html, body').animate({
        scrollTop: $( $.attr(this, 'href') ).offset().top-100
    }, 500);
   event.preventDefault();
 });
