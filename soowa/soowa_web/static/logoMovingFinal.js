
const canvas = document.querySelector('.canvas');
const context = canvas.getContext('2d');

const imgElem = new Image();

imgElem.addEventListener('load',() => {
  function draw(drawX, drawY, randScale) {
    context.clearRect(drawX, drawY, randScale, randScale);
    context.drawImage(imgElem, drawX, drawY, randScale, randScale);
    drawY -= 3;

    if (drawY <= -1 * randScale) {
      return;
    }
    console.log(drawY);

    requestAnimationFrame(draw.bind(window, drawX, drawY, randScale));
  }

  function drawInit() {
    var x = Math.random() * 600;
    var y = Math.random() * 400;
    var s = (Math.random() * 100) + 50;
    draw (x, y, s);
  }

  drawInit();

  setInterval(drawInit, 400);

})

var sentence= {0:'JEJUDO', 1:'BLUE', 2:'NIGHT', 3:'STAR', 4:'BELOW'};
var goal_idx=0;
var goal_gesture=sentence[goal_idx];

$('#start_btn').click(function(){  
  $.ajax({
    url: "{% url 'GestureRecognition' %}",
    type: 'GET',
    datatype: 'json',
    success: function(data){
        
        var gesture_name= data['gesture'];
        var gesture_id= data['gesture_id'];
        if (gesture_id == 0) {
          imgElem.src = "static/logo_inf.png";
        }
        else if (gesture_id == 2) {
          imgElem.src = "static/logo_inf_blue.png";
        }
        else {
          imgElem.src = "static/logo_inf_yellow.png";
        }
        
        //현재 제스처와 목표 제스처 값 동기화
        $('#current_gesture').html(gesture_name);
        $('#goal_gesture').html(goal_gesture);

        //목표제스처와 현재 제스처가 일치하면 다음 제스처로
        if (goal_idx == gesture_id){
          goal_idx= goal_idx + 1;  
          goal_gesture= sentence[goal_idx];
          $('#goal_gesture').html(goal_gesture);
          alert(gesture_name+'성공! 다음 목표:'+goal_gesture);
          imgElem.src = 0;
        }
        //인식 재시작
        $("#start_btn").trigger("click");
      
    },
    error: function(){
      alert('에러');
    }
  });
})




