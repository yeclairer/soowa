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
    #model1 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/cloudONE.h5')
    #model2 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/cloudTWO.h5')
    model1 = load_model('/templates/soowa_web/cloudONE.h5')
    model2 = load_model('/templates/soowa_web/cloudTWO.h5')
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
    #model1 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/shineONE.h5')
    #model2 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/shineTWO.h5')
    model1 = load_model('/templates/soowa_web/shineONE.h5')
    model2 = load_model('/templates/soowa_web/shineTWO.h5')
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


def sentence0(request):
    CLOUD, SHINE, RAINBOW, LIKE, SNOW, FORSYTHIA, SPRING, GALAXY, ONE, TWO, ALL = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
    actionsONE, actionsTWO = defaultdict(int), defaultdict(int)
    Actions = []

    cloudONE = {0:'white', 1:'be', 2:'here', 3:'probably', 4:'aboveONE'}
    cloudTWO = {0:'cloud', 1:'cloud', 2:'above', 3:'if'}    # cloud_1: 오른손 위, cloud_2:왼손 위

    shineONE = {0:'eye', 1:'light', 2:'morning'}
    shineTWO = {0:'bright', 1:'morning'}

    rainbowONE = {0:'wish', 1:'rainbow'}
    rainbowTWO = {0:'sincerely', 1:'if', 2:'rise', 3:'will', 4:'will'}

    likeONE = {0:'I', 1:'you', 2:'like'}
    likeTWO = {0:'always', 1:'bright', 2:'above'}

    snowONE = {0:'white', 1:'leaf', 2:'color'}
    snowTWO = {0:'flower', 1:'snow_', 2:'as_', 3:'fly'}

    forsythiaONE = {0:'yellow', 1:'black', 2:'shadow_', 3:'below'}
    forsythiaTWO = {0:'flower', 1:'shadow_', 2:'below'}

    springONE = {0:'leaf', 1:'wish', 2:'rainbow'}
    springTWO = {0:'season', 1:'warm', 2:'wind', 3:'because', 4:'because', 5:'flower', 6:'together', 7:'bright', 8:'smile'}

    galaxyONE = {0:'blue', 1:'color', 2:'star'}
    galaxyTWO = {0:'bright', 1:'gorup'}

    ## 추가 !! ##
    SLONE = {0:'white', 1:'be', 2:'here', 3:'probably', 4:'above',
            5:'eye', 6:'light', 7:'morning', 8:'wish', 9:'rainbow',
            10:'I', 11:'you', 12:'like', 13:'leaf', 14:'color',
            15:'yellow', 16:'black', 17:'shadow', 18:'below', 19:'blue',
            20:'star'}
    KWONE = {0:'finger_heart', 1:'finger_heart', 2:'hi', 3:'hi', 4:'meosseug',
            5:'meosseug', 6:'kosseug', 7:'kosseeug', 8:'fuckyou', 9:'fuckyou',
            10:'jawV', 11:'jawV', 12:'V', 13:'V'}

    SLTWO = {0:'cloud', 1:'cloud', 2:'above', 3:'if', 4:'bright',
            5:'morning', 6:'sincerely', 8:'rise', 9:'will',
            10:'will', 11:'always', 12:'flower', 13:'snow', 14:'as',
            15:'fly', 16:'shadow', 17:'below', 18:'season', 19:'warm',
            20:'wind', 21:'because', 22:'because', 23:'together', 24:'smile',
            25:'group', 26:'jewel'}
    KWTWO = {0:'finger_heart', 1:'small_heart', 2:'middle_heart', 3:'big_heart',
            4:'hi', 5:'flower_cup', 6:'V', 7:'V', 8:'fuckyou'}

    k=0
    for v in chain(cloudTWO.values(), cloudONE.values()):
        CLOUD[k] = v
        k+=1
    k=0
    for v in chain(shineTWO.values(), shineONE.values()):
        SHINE[k] = v
        k+=1
    k=0
    for v in chain(rainbowTWO.values(), rainbowONE.values()):
        RAINBOW[k] = v
        k+=1
    k=0
    for v in chain(likeTWO.values(), likeONE.values()):
        LIKE[k] = v
        k+=1
    k=0
    for v in chain(snowTWO.values(), snowONE.values()):
        SNOW[k] = v
        k+=1
    k=0
    for v in chain(forsythiaTWO.values(), forsythiaONE.values()):
        FORSYTHIA[k] = v
        k+=1
    k=0
    for v in chain(springTWO.values(), springONE.values()):
        SPRING[k] = v
        k+=1
    k=0
    for v in chain(galaxyTWO.values(), galaxyONE.values()):
        GALAXY[k] = v
        k+=1

    ## 추가!! ##
    ## ALL ##
    k=0
    for v in chain(SLONE.values(), KWONE.values()):
        ONE[k] = v
        k+=1
    k=0
    for v in chain(SLTWO.values(), KWTWO.values()):
        TWO[k] = v
        k+=1
    k=0
    for v in chain(TWO.values(), ONE.values()):
        ALL[k] = v
        k+=1

    #################### 설정 #################
    actionsTWO = TWO       # TWO, cloudTWO, shineTWO, rainbowTWO, likeTWO, snowTWO, forsythiaTWO, springTWO, galaxyTWO
    actionsONE = ONE       # ONE, cloudONE, shineONE, rainbowONE, likeONE, snowONE, forsythiaONE, springONE, galaxyONE
    for v in ALL.values():    # ALL, CLOUD, SHINE, RAINBOW, LIKE, SNOW, FORSYTHIA, SPIRNG
        Actions.append(v)

    #model1 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/ALLONE_4.h5')   # cloudONE / shineONE/ rainbowONE / likeONE / snowONE / forsythiaONE / springONE / galaxyONE
    #model2 = load_model('/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/ALLTWO_4.h5')   # cloudTWO / shineTWO / rainbowTWO / likeTWO / snowTWO / forsythiaTWO / springTWO / galaxyTWO
    model1 = load_model('/templates/soowa_web/ALLONE_4.h5')   # cloudONE / shineONE/ rainbowONE / likeONE / snowONE / forsythiaONE / springONE / galaxyONE
    model2 = load_model('/templates/soowa_web/ALLTWO_4.h5')   # cloudTWO / shineTWO / rainbowTWO / likeTWO / snowTWO / forsythiaTWO / springTWO / galaxyTWO
    ###########################################

    seq_length = 10
    seqONE, seqTWO = [], []

    # MediaPipe hands model
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    cap = cv2.VideoCapture(0)

    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
       
        while cap.isOpened():
    # Inference gesture
            Angle= detection(cap)

            # Inference gesture
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
                    'fingerLeftX': 200,
                    'fingerRightX': 100,
                    'fingerLeftY': 200,                       
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
                    'fingerLeftX': 200,
                    'fingerRightX': 100,
                    'fingerLeftY': 200,           
                }
                return JsonResponse(detect_result)

            if cv2.waitKey(10) and 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()