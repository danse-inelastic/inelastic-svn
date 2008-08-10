// -*- JavaScript -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                         (C) 2008 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


// slidableGallery

// Developed from jquery ui example: http://jqueryfordesigners.com/slider-gallery/
// Convert a list (<li>) of items to be contained in a slider
// 

// requires:
//   jquery main:
//     jquery.js
//   jquery ui:
//     ui.core.js
//     ui.slider.js
//
// 


(function($) {

  // turn a division with a list of images into a "slider"
  // the division must have a section of <ul>, each <li> should be an image
  // The division must have a subdivision containing a slider division and
  //   a few "categories". Here is an example:
  //             <div class="slider">
  //                 <div class="handle"></div>
  //                 <span class="slider-lbl1">Wi-Fi</span>
  //                 <span class="slider-lbl3">Macs</span>
  //                 <span class="slider-lbl4">Applications</span>
  //                 <span class="slider-lbl5">Servers</span>
  //             </div>
  $.fn.slidableGallery = function () {

    container = this;

    // everytime an item loaded, check whether all items are loaded
    // if all items are loaded, emit "slider-images-all-loaded"
    container.bind( 'slider-item-loaded', function() {
	$this = $(this);
	nloaded = $this.data( 'number-of-images-loaded' );
	if (nloaded == undefined) nloaded = 0;
	nloaded += 1;
	$this.data( 'number-of-images-loaded', nloaded );
	if (nloaded == $($this.children('ul')).find('img').length) {
	  $this.trigger( 'slider-images-all-loaded' );
	}
      } );

    // when all items loaded, add a slider and set up machineries fo
    // sliding.
    container.bind( 'slider-images-all-loaded', function() {
	
	// debug
	console.log( 'debug' );
	
	var container = $(this); 
	var ul = $('ul', container);
            
	var itemsWidth = ul.innerWidth() - container.outerWidth();
            
	$('.slider', container).slider( {
	    min: 0,
	    max: itemsWidth,
	    handle: '.handle',
	    stop: function (event, ui) {
	      ul.animate({'left' : ui.value * -1}, 500);
	    },
	    slide: function (event, ui) {
	      ul.css('left', ui.value * -1);
	    }
	  });
      });

    // find all images and ask them to emit slider-items-loaded when loaded
    container.find( 'img' ).load( function () {
	
	container.trigger( 'slider-item-loaded' );

      });

  };

 }) (jQuery);

// version
// $Id$

// End of file 
