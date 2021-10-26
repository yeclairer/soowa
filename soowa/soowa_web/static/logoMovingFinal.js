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
//var sentence_new={'SINCERLY': 0 , 'LONG FOR': 1, 'IF': 2, 'RAINBOW': 3 , 'RISE': 4,'WILL': 5 }
var sentence_new=['SINCERELY','LONG FOR', 'RAINBOW','RISE','WILL','IF'];
//if인식 잘 안되서 맨뒤로 빼놓음 
//var sentence= {0:'JEJUDO', 1:'BLUE', 2:'NIGHT', 3:'STAR', 4:'BELOW'};
var imageSource= ['static/logo_inf.png','static/logo_inf_blue.png','static/logo_inf_yellow.png']
var goal_idx=0;
var goal_gesture=sentence_new[goal_idx];

$('#start_btn').click(function(){  
  $.ajax({
    url: "{% url 'oneortwo' %}",
    type: 'GET',
    datatype: 'json',
    success: function(data){   
        imgElem.src = 0;
        var gesture_name= data['gesture'];
        var gesture_id= data['gesture_id'];

        imgElem.src = imageSource[(gesture_id+1)/3];
        //현재 제스처와 목표 제스처 값 동기화
        $('#current_gesture').html(gesture_name);
        $('#goal_gesture').html(goal_gesture);
        
        //목표제스처와 현재 제스처가 일치하면 다음 제스처로
        if (gesture_name == goal_gesture){
          goal_idx= goal_idx + 1;  
          goal_gesture= sentence_new[goal_idx];
          setTimeout(function() {
            alert(gesture_id+gesture_name+'성공! 다음 목표:'+goal_gesture);
            $('#goal_gesture').html(goal_gesture);
            $("#start_btn").trigger("click");
          }, 3000);     
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




