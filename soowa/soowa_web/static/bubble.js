//2021.11.11 신규
function bubble(sentence_clear){
  
  const imgElem_bubble1 = new Image();
  const imgElem_bubble2 = new Image();
  const imgElem_bubble3 = new Image();
  const imgElem_bubble4 = new Image();
  const imgElem_bubble5 = new Image();

  var arr = new Array(1000);
  var arrNum = 0;

  if (sentence_clear == 1) {
    imgElem_bubble1.src = 'static/bubble1.png';
    imgElem_bubble2.src = 'static/bubble2.png';
    imgElem_bubble3.src = 'static/bubble3.png';
    imgElem_bubble4.src = 'static/bubble4.png';
    imgElem_bubble5.src = 'static/bubble5.png';
  }

  var canvas4 = document.getElementById('canvas4');
  var canvas4_1 = document.getElementById('canvas4_1');
  var canvas4_2 = document.getElementById('canvas4_2');
  var canvas4_3 = document.getElementById('canvas4_3');
  var canvas4_4 = document.getElementById('canvas4_4');
  var context4 = canvas4.getContext('2d');
  var context4_1 = canvas4_1.getContext('2d');
  var context4_2 = canvas4_2.getContext('2d');
  var context4_3 = canvas4_3.getContext('2d');
  var context4_4 = canvas4_4.getContext('2d');



    function bubble_1(drawX, drawY, randScale, aN) {
      context4.clearRect(drawX, drawY , randScale, randScale);
      context4.drawImage(imgElem_bubble1, drawX, drawY, randScale, randScale);
      randScale += 3;

      if (randScale >= arr[aN]) {
        context4.clearRect(drawX, drawY , randScale, randScale);
        return;
      }
      // console.log(drawY);

      requestAnimationFrame(bubble_1.bind(window, drawX, drawY, randScale, aN));
    }

    function bubble_2(drawX, drawY, randScale, aN) {
      context4_1.clearRect(drawX, drawY , randScale, randScale);
      context4_1.drawImage(imgElem_bubble2, drawX, drawY, randScale, randScale);
      randScale += 3;

      if (randScale >= arr[aN]) {
        context4_1.clearRect(drawX, drawY , randScale, randScale);
        return;
      }
      // console.log(drawY);

      requestAnimationFrame(bubble_2.bind(window, drawX, drawY, randScale, aN));
    }

    function bubble_3(drawX, drawY, randScale, aN) {
      context4_2.clearRect(drawX, drawY , randScale, randScale);
      context4_2.drawImage(imgElem_bubble3, drawX, drawY, randScale, randScale);
      randScale += 3;

      if (randScale >= arr[aN]) {
        context4_2.clearRect(drawX, drawY , randScale, randScale);
        return;
      }
      // console.log(drawY);

      requestAnimationFrame(bubble_3.bind(window, drawX, drawY, randScale, aN));
    }

    function bubble_4(drawX, drawY, randScale, aN) {
      context4_3.clearRect(drawX, drawY , randScale, randScale);
      context4_3.drawImage(imgElem_bubble4, drawX, drawY, randScale, randScale);
      randScale += 3;

      if (randScale >= arr[aN]) {
        context4_3.clearRect(drawX, drawY , randScale, randScale);
        return;
      }
      // console.log(drawY);

      requestAnimationFrame(bubble_4.bind(window, drawX, drawY, randScale, aN));
    }

    function bubble_5(drawX, drawY, randScale, aN) {
      context4_4.clearRect(drawX, drawY , randScale, randScale);
      context4_4.drawImage(imgElem_bubble5, drawX, drawY, randScale, randScale);
      randScale += 3;

      if (randScale >= arr[aN]) {
        context4_4.clearRect(drawX, drawY , randScale, randScale);
        return;
      }
      // console.log(drawY);

      requestAnimationFrame(bubble_5.bind(window, drawX, drawY, randScale, aN));
    }

    function drawInit() {
      var x = Math.random() * 800;
      var y = Math.random() * 600;
      var s = (Math.random() * 100) + 50;
      var lightNum = Math.random() * 10;

      if (arrNum <1000) {
        arr[arrNum] = s * 1.3;
        arrNum += 1;
      }
      else {
        arrNum = 0;
        arr[arrNum] = s * 1.3;
        arrNum += 1;
      }
      


      if (lightNum < 2) {
        bubble_1(x, y, s, arrNum);
      }
      else if (lightNum < 4) {
        bubble_2(x, y, s, arrNum);
      }
      else if (lightNum < 6) {
        bubble_3(x, y, s, arrNum);
      }
      else if (lightNum < 8) {
        bubble_4(x, y, s, arrNum);
      }
      else {
        bubble_5(x, y, s, arrNum);
      }
    }

    drawInit();

    setInterval(drawInit, 400);
}