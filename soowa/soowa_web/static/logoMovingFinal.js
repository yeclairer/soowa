//2021.10.8 목표제스처와 일치하면 3초 지연 후 다음 제스처로 이동, 이미지파일 경로 리스트(imageSource) 추가
const imgElem = new Image();
var canvas2 = document.getElementById('canvas2'),
context2 = canvas2.getContext('2d');

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

//문장 리스트
var sentence_list = {};
sentence_list['1']= ['cloud','above','be','if','here','probably'];
sentence_list['2']= ['eye','light','bright','morning'];
sentence_list['3']= ['cloud','be','here','probably'];
sentence_list['4']= ['cloud','above','be','if','here','probably'];
sentence_list['5']= ['cloud','above','be','if','here','probably'];
sentence_list['6']= ['cloud','above','be','if','here','probably'];
sentence_list['7']= ['cloud','above','be','if','here','probably'];
sentence_list['8']= ['cloud','above','be','if','here','probably'];

//가이드영상 경로 리스트
var guideVideo_list = {};
guideVideo_list['1']= ['static/sentence1/cloud.mov','static/sentence1/above.mov','static/sentence1/be.mov','static/sentence1/if.mov','static/sentence1/here.mov','static/sentence1/probably.mov'];
guideVideo_list['2']= ['static/sentence2/eye.mov','static/sentence2/light.mov','static/sentence2/bright.mov','static/sentence2/morning.mov'];
guideVideo_list['3']= ['static/sentence3/cloud.mov','static/sentence3/be.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['4']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['5']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['6']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['7']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];
guideVideo_list['8']= ['static/sentence3/cloud.mov','static/sentence3/above.mov','static/sentence3/be.mov','static/sentence3/if.mov','static/sentence3/here.mov','static/sentence3/probably.mov'];

//그래픽 리스트 
var imageSource= ['static/logo_inf.png','static/logo_inf_blue.png','static/logo_inf_yellow.png'];

var sentence= sentence_list[s_num];
var guideVideo= guideVideo_list[s_num];

var goal_idx=0;
var goal_gesture=sentence[goal_idx];
var videopath = guideVideo[goal_idx];
var video = $('#guide')[0];
video.src = videopath;
video.load();
video.play();
$('#goal_gesture').html(goal_gesture);

$('#start_btn').click(function(){  
  $.ajax({
    url: escape(encodeURIComponent('sentence'+s_num)),
    type: 'GET',
    datatype: 'json',
    success: function(data){   
        imgElem.src = 0;
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
            $('#goal_gesture').html(goal_gesture);
            alert('문장을 완성했습니다!');
            imgElem.src= imageSource[0];
            return;
          }
          setTimeout(function() {
            alert(gesture_id+gesture_name+'성공! 다음 단어:'+goal_gesture);
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
      alert('에러');
    }
  });
})




