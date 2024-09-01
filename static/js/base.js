function initializeMagnificPopup(){
  $('.image-popup-vertical-fit').magnificPopup({
    type: 'image',
    mainClass: 'mfp-with-zoom', 
    gallery:{ enabled:true },

    zoom: {
      enabled: true, 
      duration: 300,
      easing: 'ease-in-out',
      opener: function(openerElement) {
        return openerElement.is('img') ? openerElement : openerElement.find('img');
      }
    }

  });
}

$(document).ready(function(){
  initializeMagnificPopup();
});

document.addEventListener('htmx:afterSwap', function(event) {
  initializeMagnificPopup();
});