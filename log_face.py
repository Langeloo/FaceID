from tkinter import *
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import numpy as np


def register_user():
    user_info = user.get()
    contra_info = contra.get()

    file = open(user_info, "w")
    file.write(user_info + "\n")
    file.write(contra_info)
    file.close()

    user_enter.delete(0, END)
    contra_enter.delete(0, END)

    Label(screen1, text="User registered successfully", fg="green", font=("calibri", 11)).pack()


def face_register():
    print('entra a la funcion')
    cap = cv2.VideoCapture(0)
    print('pasa el video')

    while True:
        ret, frame = cap.read()
        cv2.imshow("Face register", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    user_img = user.get()
    cv2.imwrite(user_img + ".jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    user_enter.delete(0, END)
    contra_enter.delete(0, END)
    Label(screen1, text="Face registered successfully", fg="green", font=("calibri", 11)).pack()

    def reg_face(img, hit_list):
        data = plt.imread(img)
        for i in range(len(hit_list)):
            x, y, w, h = hit_list[i]["box"]
            x2, y2 = x + w, y + h
            plt.subplot(1, len(hit_list), i + 1)
            plt.axis("off")
            face_reg = data[y:y2, x:x2]
            face_reg = cv2.resize(face_reg, (300, 400), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(user_img+".jpg", face_reg)
            plt.imshow(data[y:y2, x:x2])
        plt.show()

    img = user_img + ".jpg"
    pixels = plt.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    reg_face(img, faces)


def register():
    global user
    global contra
    global user_enter
    global contra_enter
    global screen1

    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")

    user = StringVar()
    contra = StringVar()

    Label(screen1, text="Please enter details below").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Enter Username ").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username ").pack()
    user_enter = Entry(screen1, textvariable=user)
    user_enter.pack()
    Label(screen1, text="Password ").pack()
    contra_enter = Entry(screen1, textvariable=contra)
    contra_enter.pack()
    Label(screen1, text="").pack()
    Button(screen1, text="Register", height="1", width="15", command = register_user).pack()

    Label(screen1, text="").pack()
    Button(screen1, text="Face Register", height="1", width="15", command = face_register).pack()


def verification_login():
    log_user = verify_user.get()
    log_contra = verify_contra.get()

    user_enter2.delete(0, END)
    contra_enter2.delete(0, END)

    list_files = os.listdir()
    if log_user in list_files:
        file2 = open(log_user, "r")
        verification = file2.read().splitlines()
        if log_contra in verification:
            Label(screen2, text="Login successful", fg="green", font=("calibri", 11)).pack()
            print("Login successful", log_user)
        else:
            Label(screen2, text="Contraseña incorrecta", fg="red", font=("calibri", 11)).pack()
            print("Contraseña incorrecta")
    else:
        print("Login fallido, no encontrado")
        Label(screen2, text="Login fallido, no encontrado", fg="red", font=("calibri", 11)).pack()


def face_login():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Face login", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    user_login = verify_user.get()
    cv2.imwrite(user_login + "LOG.jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    user_enter2.delete(0, END)
    contra_enter2.delete(0, END)

    def log_face(img, hit_list):
        data = plt.imread(img)
        for i in range(len(hit_list)):
            x, y, w, h = hit_list[i]["box"]
            x2, y2 = x + w, y + h
            plt.subplot(1, len(hit_list), i + 1)
            plt.axis("off")
            face_reg = data[y:y2, x:x2]
            face_reg = cv2.resize(face_reg, (300, 400), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(user_login + "_" + str(i) + "LOG.jpg", face_reg)
            return plt.imshow(data[y:y2, x:x2])
        plt.show()

    img = user_login + "LOG.jpg"
    pixels = plt.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    log_face(img, faces)

    def orb_sim(img1, img2):
        orb = cv2.ORB_create()

        kpa, des1 = orb.detectAndCompute(img1, None)
        kpb, des2 = orb.detectAndCompute(img2, None)

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = comp.match(des1, des2)

        similar_regions = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    im_files = os.listdir()
    if user_login + ".jpg" in im_files:
        face_reg = cv2.imread(user_login + ".jpg", 0)
        face_log = cv2.imread(user_login + "LOG.jpg", 0)
        match = orb_sim(face_reg, face_log)
        if match > 0.7:
            #Label(screen1, text="Login successful", fg="green", font=("calibri", 11)).pack()
            print("Login successful", user_login)
            print("Match:", match)
        else:
            print("Login failed", user_login, match)
            Label(screen2, text="Login failed", fg="red", font=("calibri", 11)).pack()

    else:
        print("Login failed, no found", user_login)
        Label(screen2, text="Login failed, no found", fg="red", font=("calibri", 11)).pack()


def login():
    global screen2
    global verify_user
    global verify_contra
    global user_enter2
    global contra_enter2

    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    Label(screen2, text="Please enter details below to login").pack()
    Label(screen2, text="Please enter user and password").pack()
    Label(screen2, text="").pack()

    verify_user = StringVar()
    verify_contra = StringVar()

    Label(screen2, text="Username ").pack()
    user_enter2 = Entry(screen2, textvariable=verify_user)
    user_enter2.pack()
    Label(screen2, text="Password ").pack()
    contra_enter2 = Entry(screen2, textvariable=verify_contra)
    contra_enter2.pack()
    Label(screen2, text="").pack()
    Button(screen2, text="Login", height="1", width="15", command=verification_login).pack()

    Label(screen2, text="").pack()
    Button(screen2, text="Face Login", height="1", width="20", command=face_login).pack()


def principal_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("UBLI Face Recognition")
    Label(
        text="UBLI Face Recognition",
        bg="grey",
        width="300",
        height="2",
        font=("Calibri", 13),
    ).pack()

    Label(text="").pack()
    Button(text = "Login", height="2", width = "30", command = login).pack()
    Label(text="").pack()
    Button(text = "Register", height="2", width = "30", command = register).pack()

    screen.mainloop()


#face_register()
principal_screen()
