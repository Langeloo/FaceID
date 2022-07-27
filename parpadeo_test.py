import cv2
import mediapipe as mp
import math
import time

#-- realizamos la video captura
cap = cv2.VideoCapture(0)
cap.set(3, 800)  #ancho de la ventana
cap.set(4, 720)  #alto de la ventana

#-- variable de conteo
parpadeo = p_left = p_right = p_detected = p_front = False
conteo = tiempo = inicio = final = muestra = 0
index = 1

#-- funcion de dibujo
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1,color=(255, 0, 0))

#-- malla facial
mpMallaFacial = mp.solutions.face_mesh  #funcion de malla
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

while True:
    ret, frame = cap.read()
    #-- correccion de color
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #--observamos los resultados
    resultados = MallaFacial.process(frameRGB)
    
    #-- lista donde se almacenan resultados
    px = []
    py = []
    lista = []
    r = 3
    t = 5
    
    if resultados.multi_face_landmarks: #si detectamos al menos una cara
        for rostros in resultados.multi_face_landmarks: # mostramos el rostro detectado
            mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)
            
            #-- estraer los puntos del rostro detectado
            for id, puntos in enumerate(rostros.landmark):
                #print(puntos)  #nos entrega una porcion
                al, an, c = frame.shape
                x,y = int(puntos.x*an), int(puntos.y*al)
                px.append(x)
                py.append(y)
                lista.append([id,x,y])
                if len(lista) == 468:
                    if p_front and conteo == 3 and longitud1 >= 29 and longitud2 >= 29:
                        #cv2.imwrite(str(index) + ".jpg", frame)
                        print(cap.get(3))
                        print(cap.get(4))
                        print("save" + str(index) + ".jpg successfuly!")
                        print("-------------------------")
                        index += 1
                    #-- ojo derecho
                    x1, y1 = lista[145][1:]
                    x2, y2 = lista[159][1:]
                    cx, cy = (x1+x2)//2, (y1+y2)//2
                    #-- inicio comentarios
                    #cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), t)
                    #cv2.circle(frame, (x1, y1), r, (0, 0, 0), cv2.FILLED)
                    #cv2.circle(frame, (x2, y2), r, (0, 0, 0), cv2.FILLED)
                    #cv2.circle(frame, (cx, cy), r, (0, 0, 0), cv2.FILLED)
                    #-- fin comentarios
                    longitud1 = math.hypot(x2 - x1, y2 - y1)
                    #-- ojo izquierdo
                    x3, y3 = lista[374][1:]
                    x4, y4 = lista[386][1:]
                    cx2, cy2 = (x3+x4)//2, (y3+y4)//2
                    #-- inicio comentarios
                    #cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), t)
                    #cv2.circle(frame, (x1, y1), r, (0, 0, 0), cv2.FILLED)
                    #cv2.circle(frame, (x2, y2), r, (0, 0, 0), cv2.FILLED)
                    #cv2.circle(frame, (cx, cy), r, (0, 0, 0), cv2.FILLED)
                    #-- fin comentarios
                    longitud2 = math.hypot(x2 - x1, y2 - y1)
                    
                    #-- face1-horizontal_1
                    x7, y7 = lista[4][1:]
                    x8, y8 = lista[137][1:]
                    cx4, cy4 = (x7+x8)//2, (y7+y8)//2
                    longitud4 = math.hypot(x8 - x7, y8 - y7)
                    #cv2.line(frame, (x7, y7), (x8, y8), (0, 0, 0), t)
                    
                    #-- face1-horizontal_2
                    x9, y9 = lista[4][1:]
                    x10, y10 = lista[366][1:]
                    cx5, cy5 = (x9+x10)//2, (y9+y10)//2
                    longitud5 = math.hypot(x10 - x9, y10 - y9)
                    #cv2.line(frame, (x9, y9), (x10, y10), (0, 0, 0), t)
                    
                    #-- conteo de parpadeos
                    cv2.putText(frame, f'Parpadeos: {int(conteo)}', (30, 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'Med Ojo: {int(longitud1)}', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    #cv2.putText(frame, f'Face horizontal_1: {int(longitud4)}', (450, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'Face horizontal_2: {int(longitud5)}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    
                    x_up, y_up = lista[10][1:]
                    x_down, y_down = lista[152][1:]
                    x_med, y_med = lista[4][1:]
                    #cv2.putText(frame, f'x, y up: {x_up}, {y_up}', (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'x, y down: {x_down}, {y_down}', (50, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'x, y med: {x_med}, {y_med}', (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'Movimiento izquierda: {p_left}', (30, 520), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #cv2.putText(frame, f'Movimiento derecha: {p_right}', (30, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    
                    if x_up > 200 and x_med > 150 and x_down > 200 and x_up < 600 and x_med < 650 and x_down < 600 and y_up > 10 and y_up < 250 and y_med > 200 and y_med < 400 and y_down > 350 and y_down < 580:
                        cv2.putText(frame, 'Cara Identificable', (30, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        p_detected = True
                    else:
                        cv2.putText(frame, 'Cara No Identificable', (30, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        p_detected = p_left = p_right = False                     
                        
                    if p_detected and longitud5 >= 0 and longitud5 <= 50:
                        p_left = True
                    
                              
                    if p_detected and longitud4 >= 0 and longitud4 <= 50:
                        p_right = True

                    
                    if x_up > 300 and x_med > 300 and x_down > 300 and x_up < 500 and x_med < 500 and x_down < 500 and y_up > 0 and y_up < 140 and y_med > 200 and y_med < 400 and y_down > 500 and y_down < 580:
                        cv2.putText(frame, 'Posicion Reconocible', (30, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        p_front = True
                    else:
                        cv2.putText(frame, 'Posicion NO Reconocible', (30, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        p_front = False
                        conteo = 0                
                        
                    if p_left:
                        cv2.putText(frame, 'Movimiento Izquierda', (30, 520), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    else:
                        cv2.putText(frame, 'Movimiento Izquierda', (30, 520), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        
                    if p_right:
                        cv2.putText(frame, 'Movimiento Derecha', (30, 490), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    else:
                        cv2.putText(frame, 'Movimiento Derecha', (30, 490), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        
                    if conteo >= 3:
                        cv2.putText(frame, f'Parpadeos: {int(conteo)}', (30, 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        cv2.putText(frame, 'CAPTURANDO IMAGEN...', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    else:
                        cv2.putText(frame, f'Parpadeos: {int(conteo)}', (30, 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    '''
                        
                    if p_front and p_right and longitud1 <= 25 and longitud2 <= 25 and not parpadeo: 
                        parpadeo = True
                        inicio = time.time()
                    elif p_front and p_right and longitud1 > 25 and longitud2 > 25 and parpadeo:
                        parpadeo = False
                        final = time.time()
                    '''
                        
                    if p_right and p_left and longitud1 <= 20 and longitud2 <= 20 and not parpadeo:
                        conteo += 1
                        parpadeo = True
                    elif longitud2 > 20 and longitud1 > 20 and parpadeo:
                        parpadeo = False
                        
    cv2.imshow('MediaPipe Face Mesh', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()