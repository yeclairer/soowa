//2021.11.11 수정완료
(function() {
  
  var canvas = document.getElementById('canvas'),
  context = canvas.getContext('2d'),
  video = document.getElementById('video'),
  vendorUrl = window.URL || window.webkitURL;
  
  var constraints = { audio: false, video: true };

  navigator.mediaDevices.getUserMedia(constraints)
      .then(function(stream) {
          var video = document.querySelector('video');
          // Older browsers may not have srcObject
          if ("srcObject" in video) {
              video.srcObject = stream;
          } else {
              // Avoid using this in new browsers, as it is going away.
              video.src = window.URL.createObjectURL(stream);
          }
          video.onloadedmetadata = function(e) {
              video.play();
          };
      })
      .catch(function(err) {
          console.log(err.name + ": " + err.message);
      });

/* version2
  navigator.getWebcam = (navigator.getUserMedia 
                        || navigator.webKitGetUserMedia 
                        || navigator.moxGetUserMedia 
                        || navigator.mozGetUserMedia 
                        || navigator.msGetUserMedia);
  if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({  audio: false, video: true })
      .then(function (stream) {
        video.srcObject = stream; 
        video.play();
      })
      .catch(function (e) { logError(e.name + ": " + e.message); });
  }
  else {
    navigator.getWebcam({ audio: true, video: true }, 
        function (stream) {
                //Display the video stream in the video object
        }, 
        function () { logError("Web cam is not accessible."); });
    }
*/
/*
  navigator.getMedia =  navigator.getUserMedia ||
                        navigator.mediaDevices.getUserMedia ||
                        navigator.webkitGetUserMedia ||
                        navigator.mozGetuserMedia ||
                        navigator.msGetUserMedia;
  
  navigator.getMedia({
    video: true,
    audio: false
  }, function(stream) {
    video.srcObject = stream; 

    video.play();
  }, function(error) {
    console.log('webcam error');
    // an error occurred
  } );
  */
  video.addEventListener('play', function() {
    draw( this, context, 650, 470 );
  }, false );
  
  function draw( video, context, width, height ) {
    
    context.drawImage( video, 0, 0, width, height );
    setTimeout( draw, 10, video, context, width, height );
  }
  
} )();
