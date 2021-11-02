
const mainFrame = new Image();
mainFrame.src = 'static/frame2.png';

var canvas3 = document.getElementById('canvas3'),
context3 = canvas3.getContext('2d');

mainFrame.addEventListener('load', () => {

  context3.drawImage(mainFrame,0,0,1030,680);
});

