const doing = new Image();
const done = new Image();
const ready = new Image();

doing.src = 'static/doing.png';
done.src = 'static/done.png';
ready.src = 'static/ready.png';


var canvas5 = document.getElementById('canvas5'),
context5 = canvas5.getContext('2d');

doing.addEventListener('load', () => {
  done.addEventListener('load', () => {
    ready.addEventListener('load', () => {

      if (state == "1") {
        context5.drawImage(doing, 630, 100, 37, 37);
        context5.drawImage(ready, 680, 75, 37, 37);
        context5.drawImage(ready, 730, 60, 37, 37);
        context5.drawImage(ready, 780, 55, 37, 37);
      }
      else if (state == "2") {
        context5.drawImage(done, 630, 100, 37, 37);
        context5.drawImage(doing, 680, 75, 37, 37);
        context5.drawImage(ready, 730, 60, 37, 37);
        context5.drawImage(ready, 780, 55, 37, 37);
      }
      else if (state == "3") {
        context5.drawImage(done, 630, 100, 37, 37);
        context5.drawImage(done, 680, 75, 37, 37);
        context5.drawImage(doing, 730, 60, 37, 37);
        context5.drawImage(ready, 780, 55, 37, 37);
      }
      else if (state == "4") {
        context5.drawImage(done, 630, 100, 37, 37);
        context5.drawImage(done, 680, 75, 37, 37);
        context5.drawImage(done, 730, 60, 37, 37);
        context5.drawImage(doing, 780, 55, 37, 37);
      }
      else {}
      
    });
  });
});