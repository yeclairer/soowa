//2021.11.11 수정완료
(function() {
  
  var canvas = document.getElementById('canvas'),
  context = canvas.getContext('2d'),
  video = document.getElementById('video'),
  vendorUrl = window.URL || window.webkitURL;
  
  navigator.getMedia =  navigator.getUserMedia ||
                        navigator.webkitGetUserMedia ||
                        navigator.mozGetuserMedia ||
                        navigator.msGetUserMedia;
  
  navigator.getMedia({
    video: true,
    audio: false
  }, function(stream) {
    video.srcObject = stream; video.play();

    video.play();
  }, function(error) {
    // an error occurred
  } );
  
  video.addEventListener('play', function() {
    draw( this, context, 650, 470 );
  }, false );
  
  function draw( video, context, width, height ) {
    
    context.drawImage( video, 0, 0, width, height );
    setTimeout( draw, 10, video, context, width, height );
  }
  
} )();