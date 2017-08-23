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

 $('.dropdown-button').dropdown({
      inDuration: 300,
      outDuration: 225,
      constrainWidth: true, // Does not change width of dropdown to that of the activator
      hover: true, // Activate on hover
      gutter: 0, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: false // Stops event propagation
    }
  );
