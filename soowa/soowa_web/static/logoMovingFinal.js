//원래

const imgElem = new Image();
const doing = new Image();
const done = new Image();
const ready = new Image();
//원래꺼
var canvas2 = document.getElementById('canvas2'),
context2 = canvas2.getContext('2d');


var sentence_clear=0;
imgElem.addEventListener('load', () => {
  
  function drawItem(drawX, drawY, randScale) {
    context2.clearRect(drawX, drawY, randScale, randScale);
    context2.drawImage(imgElem, drawX, drawY, randScale, randScale);
    drawY -= 3;

    if (drawY <= -1 * randScale) {
      return;
    }
    requestAnimationFrame(drawItem.bind(window, drawX, drawY, randScale));
  }

  function drawInit() {
    var x = Math.random() * 800;
    var y = Math.random() * 600;
    var s = (Math.random() * 100) + 50;
    drawItem (x, y, s);
  }

  drawInit();
  setInterval(drawInit, 1000);

});

function heart(keyword,fingerLeftX,fingerRightX,fingerLeftY){
  const FWHeart = new Image();
  const SWHeart = new Image();
  const FPHeart = new Image();
  const SPHeart = new Image();
  
  FWHeart.src = 'static/fingerHeartWhite.png';
  SWHeart.src = 'static/fingerHeartWhiteFull.png';
  FPHeart.src = 'static/fingerHeart.png';
  SPHeart.src = 'static/fingerHeartFull.png';

  var arr = new Array(1000);
  var arrNum = 0;

  var canvas2 = document.getElementById('canvas2');
  var canvas2_1 = document.getElementById('canvas2_1');
  var canvas2_2 = document.getElementById('canvas2_2');
  var canvas2_3 = document.getElementById('canvas2_3');
  var canvas2_4 = document.getElementById('canvas2_4');

  var context2 = canvas2.getContext('2d');
  var context2_1 = canvas2_1.getContext('2d');
  var context2_2 = canvas2_2.getContext('2d');
  var context2_3 = canvas2_3.getContext('2d');
  var context2_4 = canvas2_4.getContext('2d');

  if (keyword == "hi") {
    imgElem.addEventListener('load', () => {
    
      function drawItem(drawX, drawY, randScale) {
        context2.clearRect(drawX, drawY, randScale, randScale);
        context2.drawImage(imgElem, drawX, drawY, randScale, randScale);
        drawY -= 3;
    
        if (drawY <= -1 * randScale) {
          context2.clearRect(drawX, drawY , randScale, randScale);
          return;
        }
        requestAnimationFrame(drawItem.bind(window, drawX, drawY, randScale));
      }
    
      function drawInit() {
        var x = Math.random() * 800;
        var y = Math.random() * 600;
        var s = (Math.random() * 100) + 50;
        drawItem (x, y, s);
      }
    
      drawInit();
      setInterval(drawInit, 400);
    
    });

  }

  else if (keyword == "big_heart") {

    FWHeart.addEventListener('load', () => {
      SWHeart.addEventListener('load', () => {
        FPHeart.addEventListener('load', () => {
          SPHeart.addEventListener('load', () => {

            function drawSPHeart(x, y, s) {
              context2.clearRect(x, y, s, s);
              context2.drawImage(FWHeart, x, y, s, s);
              y -= 3;

              if (y <= -1 * s) {
                context2_1.clearRect(x, y , s, s);
                return;
              }

              requestAnimationFrame(drawSPHeart.bind(window, x, y, s));
            }

            function drawFWHeart(x, y, s) {
              context2_1.clearRect(x, y, s, s);
              context2_1.drawImage(FWHeart, x, y, s, s);
              y -= 3;

              if (y <= -1 * s) {
                context2_1.clearRect(x, y , s, s);
                return;
              }

              requestAnimationFrame(drawFWHeart.bind(window, x, y, s));
            }
          

            function drawFPHeart(x, y, s) {
              context2_2.clearRect(x, y, s, s);
              context2_2.drawImage(FWHeart, x, y, s, s);
              y -= 3;

              if (y <= -1 * s) {
                context2_2.clearRect(x, y , s, s);
                return;
              }

              requestAnimationFrame(drawFPHeart.bind(window, x, y, s));
            }

            function drawSWHeart(x, y, s) {
              context2_3.clearRect(x, y, s, s);
              context2_3.drawImage(FWHeart, x, y, s, s);
              y -= 3;

              if (y <= -1 * s) {
                context2_3.clearRect(x, y , s, s);
                return;
              }

              requestAnimationFrame(drawSWHeart.bind(window, x, y, s));
            }

            function drawHeartInit() {
              var x = Math.random() * 800;
              var y = Math.random() * 600;
              var s = (Math.random() * 100);
              var sequenceNum = Math.random() * 800;
              
          
          
              if (sequenceNum < 200) {
                drawFWHeart(x,y,s,arrNum);
              }
              else if (sequenceNum < 400) {
                drawFPHeart(x,y,s,arrNum);
              }
              else if (sequenceNum < 400) {
                drawSPHeart(x,y,s,arrNum);
              }
              else {
                drawSWHeart(x,y,s,arrNum);
              }
            }
            setInterval(drawHeartInit, 400);

          });
        });
      });
    });
  }


  else if (keyword == "small_heart") {
    FWHeart.addEventListener('load', () => {
      SWHeart.addEventListener('load', () => {
        FPHeart.addEventListener('load', () => {
          SPHeart.addEventListener('load', () => {
            var smallScale = fingerRightX - fingerLeftX;
            //갱신x

            function drawSHeart(x, y, scale) {
              context2.clearRect(x, y, scale, scale);
              context2.drawImage(SPHeart, x, y, scale, scale);
              scale += 1;
              x -= 0.5;
              y -= 0.5;

              if ( scale > smallScale * 1.5) {
                context2.clearRect(x, y, scale, scale);
                return;
              }

              requestAnimationFrame(drawSHeart.bind(window, x, y, scale));
            }

            function drawFWHeart(x, y, s, aN) {
              context2_1.clearRect(x, y , s, s);
              context2_1.drawImage(FWHeart, x, y, s, s);
              s += 1;
              x -= 0.5;
              y -= 0.5;
          
              if (s >= arr[aN]) {
                context2_1.clearRect(x, y , s, s);
                return;
              }
              requestAnimationFrame(drawFWHeart.bind(window, x, y, s, aN));
            }
          

            function drawFPHeart(x, y, s, aN) {
              context2_2.clearRect(x, y , s, s);
              context2_2.drawImage(FPHeart, x, y, s, s);
              s += 1;
              x -= 0.5;
              y -= 0.5;
          
              if (s >= arr[aN]) {
                context2_2.clearRect(x, y , s, s);
                return;
              }
              requestAnimationFrame(drawFPHeart.bind(window, x, y, s, aN));
            }

            function drawSWHeart(x, y, s, aN) {
              context2_3.clearRect(x, y , s, s);
              context2_3.drawImage(SWHeart, x, y, s, s);
              s += 1;
              x -= 0.5;
              y -= 0.5;
          
              if (s >= arr[aN]) {
                context2_3.clearRect(x, y , s, s);
                return;
              }
              requestAnimationFrame(drawSWHeart.bind(window, x, y, s, aN));
            }

            function drawHeartInit() {
              var x = fingerLeftX + Math.random() * smallScale;
              var y = fingerLeftY + Math.random() * smallScale;
              var s = (Math.random() * 30) ;
              var sequenceNum = Math.random() * 600;
          
              if (arrNum <1000) {
                arr[arrNum] = s * 1.1;
                arrNum += 1;
              }
              else {
                arrNum = 0;
                arr[arrNum] = s * 1.1;
                arrNum += 1;
              }

              if (sequenceNum < 200) {
                drawFWHeart(x,y,s,arrNum);
              }
              else if (sequenceNum < 400) {
                drawFPHeart(x,y,s,arrNum);
              }
              else {
                drawSWHeart(x,y,s,arrNum);
              }
            }

            drawSHeart(fingerLeftX, fingerLeftY, smallScale);
            setInterval(drawHeartInit, 400);
          });
        });
      });
    });
    
  }

  else if (keyword == "finger_heart") {
  
    FWHeart.addEventListener('load', () => {
      SWHeart.addEventListener('load', () => {
        FPHeart.addEventListener('load', () => {
          SPHeart.addEventListener('load', () => {

            function drawSPHeart(x, y, s) {
              context2.clearRect(x, y, s+2, s+2);
              context2.drawImage(SPHeart, x, y, s, s);
              s -= 2;
              x += 1;
              y -= 1;

              if ( s < 5 ) {
                context2.clearRect(x, y, s+2, s+2);
                return;
              }

              requestAnimationFrame(drawSPHeart.bind(window, x, y, s));
            }

            function drawFWHeart(x, y, s) {
              context2_1.clearRect(x, y, s+2, s+2);
              context2_1.drawImage(FWHeart, x, y, s, s);
              s -= 2;
              x += 1;
              y -= 1;

              if ( s < 5 ) {
                context2_1.clearRect(x, y, s+2, s+2);
                return;
              }
              requestAnimationFrame(drawFWHeart.bind(window, x, y, s));
            }
          

            function drawFPHeart(x, y, s) {
              context2_2.clearRect(x, y, s+2, s+2);
              context2_2.drawImage(FPHeart, x, y, s, s);
              s -= 2;
              x += 1;
              y -= 1;

              if ( s < 5 ) {
                context2_2.clearRect(x, y, s+2, s+2);
                return;
              }
              requestAnimationFrame(drawFPHeart.bind(window, x, y, s));
            }

            function drawSWHeart(x, y, s) {
              context2_3.clearRect(x, y, s+2, s+2);
              context2_3.clearRect(x, y, s+2, s+2);
              s -= 2;
              x += 1;
              y -= 1;

              if ( s < 5 ) {
                context2_3.clearRect(x, y , s, s);
                return;
              }
              requestAnimationFrame(drawSWHeart.bind(window, x, y, s));
            }

            function drawHeartInit() {
              var x = fingerLeftX - 10 + Math.random()*20 ;
              var y = fingerLeftY;
              var s = (Math.random() * 80) ;
              var sequenceNum = Math.random() * 800;
          

              if (sequenceNum < 200) {
                drawFWHeart(x,y,s);
              }
              else if (sequenceNum < 400) {
                drawFPHeart(x,y,s);
              }
              else if (sequenceNum < 600) {
                drawSPHeart(x,y,s);
              }
              else {
                drawSWHeart(x,y,s);
              }
            }


            setInterval(drawHeartInit, 200);



          });
        });
      });
    });
    
  }
}
function statusupdate(goal_idx){
  var state= goal_idx+1;
  //상태표시
  var canvas5 = document.getElementById('canvas5'),
  context5 = canvas5.getContext('2d');
  doing.src = 'static/doing.png';
  done.src = 'static/done.png';
  ready.src = 'static/ready.png';

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
          
          return;
        });
      });
    });
  }

//2021.10.8 목표제스처와 일치하면 3초 지연 후 다음 제스처로 이동, 이미지파일 경로 리스트(imageSource) 추가
//2021.11.11 수정


//문장 리스트
var sentence_list = {};
sentence_list['0']= 0;
sentence_list['1']= ['cloud','above','be','if','here','probably'];
sentence_list['2']= ['light','light','bright','morning'];
sentence_list['3']= ['cloud','be','here','probably'];
sentence_list['4']= ['cloud','above','be','if','here','probably'];
sentence_list['5']= ['cloud','above','be','if','here','probably'];
sentence_list['6']= ['cloud','above','be','if','here','probably'];
sentence_list['7']= ['cloud','above','be','if','here','probably'];
sentence_list['8']= ['cloud','above','be','if','here','probably'];

//가이드영상 경로 리스트
var guideVideo_list = {};
guideVideo_list['0']= 0;
guideVideo_list['1']= ['static/sentence1/cloud.mov','static/sentence1/above.mov','static/sentence1/be.mov','static/sentence1/if.mov','static/sentence1/here.mov','static/sentence1/probably.mov'];
guideVideo_list['2']= ['static/sentence2/eye.mov','static/sentence2/light.mov','static/sentence2/bright.mov','static/sentence2/morning.mov'];
guideVideo_list['3']= ['static/sentence3/cloud.mov','static/sentence3/be.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['4']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['5']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['6']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['7']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['8']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];

//그래픽 리스트 
var imageSource= ['static/bubble1.png','static/fingerHeartWhiteFull.png','static/fingerHeart.png','static/fingerHeartFull.png','static/logo_inf.png','static/logo_inf_blue.png','static/logo_inf_yellow.png'];
var keywordlist= ['hi','small_heart','big_heart','finger_heart','jewel'];
var sentence= sentence_list[s_num];
var guideVideo= guideVideo_list[s_num];
var goal_idx=0;
var goal_gesture=sentence[goal_idx];

if (s_num != 0){
  var videopath = guideVideo[goal_idx];
  var video = $('#guide')[0];
  video.src = videopath;
  video.load();
  video.play();
  var videopath = guideVideo[goal_idx];
  $('#goal_gesture').html(goal_gesture);
};

$('#keyword_start_btn').click(function(){  
  $.ajax({
    url: 'sentence0',
    type: 'GET',
    datatype: 'json',
    success: function(data){ 
      imgElem.src = 0;
      var keyword= data['gesture'];
      var fingerLeftX= data['fingerLeftX'];
      var fingerRightX= data['fingerRightX'];
      var fingerLeftY= data['fingerLeftY'];
      $('#current_gesture').html(keyword);

      if (keyword!= "hi" && keyword!= "small_heart" && keyword!= "big_heart" && keyword!= "finger_heart"){
        $("#keyword_start_btn").trigger("click");
      }
      else {
        alert(keyword+'성공!');
        heart(keyword,fingerLeftX,fingerRightX,fingerLeftY);
        setTimeout(function() { 
          $("#keyword_start_btn").trigger("click");
        }, 3000);  
      }

        
      
    },
    error: function(){
      
    }
  });
})

$('#start_btn').click(function(){  
  $.ajax({
    url: escape(encodeURIComponent('sentence'+s_num)),
    type: 'GET',
    datatype: 'json',
    success: function(data){   
        imgElem.src = 0;
        statusupdate(goal_idx);
        var gesture_name= data['gesture'];
        var gesture_id= data['gesture_id'];
       
        //현재 제스처와 목표 제스처 값 동기화
        $('#current_gesture').html(gesture_name);
        $('#goal_gesture').html(goal_gesture);
        
        //목표제스처와 현재 제스처가 일치하면 다음 제스처로
        if (gesture_name == goal_gesture){
          goal_idx= goal_idx + 1;  
          goal_gesture= sentence[goal_idx];
          
          if(goal_idx >= sentence.length){
            sentence_clear=1;
            $('#goal_gesture').html(goal_gesture);
            alert('문장을 완성했습니다!');
            video.src = 0;
            video.load();
            video.play();
            bubble(sentence_clear);
            return;
          }
          setTimeout(function() {
            alert(gesture_name+'성공! 다음 단어:'+goal_gesture);
            $('#goal_gesture').html(goal_gesture);
            videopath = guideVideo[goal_idx];
            video.src = videopath;
            video.load();
            video.play();
            $("#start_btn").trigger("click");
          }, 2000);     
        }
        else {
          $("#start_btn").trigger("click");
        }    
    },
    error: function(){
     
    }
  });
})




