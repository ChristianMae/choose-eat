$(document).ready(function(){
    $('.parallax').parallax();
    $(".button-collapse").sideNav();
});

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