import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from collections import defaultdict
from itertools import chain
from django.http import JsonResponse
from .detection import detection
#1. 구름 위가 있다면 여기일까
#2. 눈이 부시게 빛나는 아침

def sentence1(request):
    CLOUD = defaultdict(int) 
    actionsONE, actionsTWO = defaultdict(int), defaultdict(int)
    Actions = []

    cloudONE = {0:'white', 1:'be', 2:'here', 3:'probably'}
    cloudTWO = {0:'cloud_1', 1:'cloud_2', 2:'above', 3:'if'}    # cloud_1: 오른손 위, cloud_2:왼손 위

    k=0
    for v in chain(cloudTWO.values(), cloudONE.values()):
    #for v in chain(cloudONE.values(), cloudTWO.values()):
        CLOUD[k] = v
        k+=1

    #################### 설정 #################
    actionsTWO = cloudTWO
    actionsONE = cloudONE
    for v in CLOUD.values():
        Actions.append(v)
    model1 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/cloudONE.h5')
    model2 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/cloudTWO.h5')
    ###########################################

    seq_length = 10
    seqONE, seqTWO = [], []

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
    # Inference gesture
        Angle= detection(cap)
        if len(Angle) == 143:    # with BOTH HANDS
            print("TWO HAND")
            angleTWO = np.array([Angle], dtype=np.float32)
            angleTWO = np.array(angleTWO.flatten())
            seqTWO.append(angleTWO)

            input_data = np.expand_dims(np.array(seqTWO[-seq_length:], dtype=np.float32), axis=0)
            y_pred = model2.predict(input_data).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]

            if conf < 0.99:
                continue

            action = actionsTWO[i_pred]
            if i_pred== 0 or i_pred== 1:
                action= 'cloud'
                i_pred= 1

            detect_result = {
                        'gesture_id': i_pred,
                        'gesture': action,                       
            }
            cap.release()
            cv2.destroyAllWindows()
            return JsonResponse(detect_result)

        elif len(Angle) == 89:
            print("ONE HAND")
            angleONE = np.array([Angle], dtype=np.float32)
            angleONE = np.array(angleONE.flatten())
            seqONE.append(angleONE)
            input_data = np.expand_dims(np.array(seqONE[-seq_length:], dtype=np.float32), axis=0)
            y_pred = model1.predict(input_data).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]
            print(conf)
            if conf < 0.99:
                continue
            
            idx= i_pred+len(actionsTWO)
            action = Actions[idx]
            detect_result = {
                        'gesture_id': idx,
                        'gesture': action,                       
            }
            cap.release()
            cv2.destroyAllWindows()
            return JsonResponse(detect_result)

        if cv2.waitKey(10) and 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def sentence2(request):
    SHINE = defaultdict(int) 
    actionsONE, actionsTWO = defaultdict(int), defaultdict(int)
    Actions = []

    shineONE = {0:'eye', 1:'light', 2:'morning'}
    shineTWO = {0:'bright', 1:'morning'}
    k=0
    for v in chain(shineTWO.values(), shineONE.values()):
        SHINE[k] = v
        k+=1

    #################### 설정 #################
    actionsTWO = shineTWO
    actionsONE = shineONE
    for v in SHINE.values():
        Actions.append(v)
    model1 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/shineONE.h5')
    model2 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/shineTWO.h5')
    ###########################################

    seq_length = 10
    seqONE, seqTWO = [], []

    cap = cv2.VideoCapture(0)
   
    while cap.isOpened():
    # Inference gesture
        Angle= detection(cap)
        if len(Angle) == 143:    # with BOTH HANDS
            print("TWO HAND")
            angleTWO = np.array([Angle], dtype=np.float32)
            angleTWO = np.array(angleTWO.flatten())
            seqTWO.append(angleTWO)

            input_data = np.expand_dims(np.array(seqTWO[-seq_length:], dtype=np.float32), axis=0)
            y_pred = model2.predict(input_data).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]

            if conf < 0.99:
                continue

            action = actionsTWO[i_pred]
            detect_result = {
                'gesture_id': i_pred,
                'gesture': action,                       
            }
            return JsonResponse(detect_result)

        elif len(Angle) == 89:
            print("ONE HAND")
            angleONE = np.array([Angle], dtype=np.float32)
            angleONE = np.array(angleONE.flatten())
            seqONE.append(angleONE)
            input_data = np.expand_dims(np.array(seqONE[-seq_length:], dtype=np.float32), axis=0)
            y_pred = model1.predict(input_data).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]

            if conf < 0.99:
                continue
            
            idx= i_pred+len(actionsTWO)
            action = Actions[idx]
            detect_result = {
                'gesture_id': idx,
                'gesture': action,                       
            }
            return JsonResponse(detect_result)

        if cv2.waitKey(10) and 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()