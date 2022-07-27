import cv2
cap = cv2.VideoCapture(0)
flag = cap.isOpened()
 
index = 1
while(flag):
    ret, frame = cap.read()
    cv2.imshow("Capture_Paizhao",frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord ('s'): #Presione la tecla s para ingresar a la siguiente operación de guardado de imágenes
        cv2.imwrite(str(index) + ".jpg", frame)
        print(cap.get(3))
        print(cap.get(4))
        print("save" + str(index) + ".jpg successfuly!")
        print("-------------------------")
        index += 1
    elif k == ord ('q'): #Presione la tecla q, el programa sale
        break
cap.release()
cv2.destroyAllWindows()