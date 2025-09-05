# import os.path
# import datetime
# import pickle

# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# import face_recognition

# import util
# from test import test


# class App:
#     def __init__(self):
#         self.main_window = tk.Tk()
#         self.main_window.geometry("1200x520+350+100")

#         self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
#         self.login_button_main_window.place(x=750, y=200)

#         self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
#         self.logout_button_main_window.place(x=750, y=300)

#         self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
#                                                                     self.register_new_user, fg='black')
#         self.register_new_user_button_main_window.place(x=750, y=400)

#         self.webcam_label = util.get_img_label(self.main_window)
#         self.webcam_label.place(x=10, y=0, width=700, height=500)

#         self.add_webcam(self.webcam_label)

#         self.db_dir = './db'
#         if not os.path.exists(self.db_dir):
#             os.mkdir(self.db_dir)

#         self.log_path = './log.txt'

#     def add_webcam(self, label):
#         if 'cap' not in self.__dict__:
#             self.cap = cv2.VideoCapture(0)

#         self._label = label
#         self.process_webcam()

#     def process_webcam(self):
#         ret, frame = self.cap.read()

#         self.most_recent_capture_arr = frame
#         img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
#         self.most_recent_capture_pil = Image.fromarray(img_)
#         imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
#         self._label.imgtk = imgtk
#         self._label.configure(image=imgtk)

#         self._label.after(20, self.process_webcam)

#     def login(self):

#         label = test(
#                 image=self.most_recent_capture_arr,
#                 model_dir = r"C:\Users\User\face-attendance-system\Silent-Face-Anti-Spoofing\resources\anti_spoof_models",
#                 device_id=0
#                 )

#         if label == 1:

#             name = util.recognize(self.most_recent_capture_arr, self.db_dir)

#             if name in ['unknown_person', 'no_persons_found']:
#                 util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
#             else:
#                 util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
#                 with open(self.log_path, 'a') as f:
#                     f.write('{},{},in\n'.format(name, datetime.datetime.now()))
#                     f.close()

#         else:
#             util.msg_box('Hey, you are a spoofer!', 'You are fake !')

#     def logout(self):

#         label = test(
#                 image=self.most_recent_capture_arr,
#                 model_dir = r"C:\Users\User\face-attendance-system\Silent-Face-Anti-Spoofing\resources\anti_spoof_models",
#                 device_id=0
#                 )

#         if label == 1:

#             name = util.recognize(self.most_recent_capture_arr, self.db_dir)

#             if name in ['unknown_person', 'no_persons_found']:
#                 util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
#             else:
#                 util.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
#                 with open(self.log_path, 'a') as f:
#                     f.write('{},{},out\n'.format(name, datetime.datetime.now()))
#                     f.close()

#         else:
#             util.msg_box('Hey, you are a spoofer!', 'You are fake !')


#     def register_new_user(self):
#         self.register_new_user_window = tk.Toplevel(self.main_window)
#         self.register_new_user_window.geometry("1200x520+370+120")

#         self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
#         self.accept_button_register_new_user_window.place(x=750, y=300)

#         self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
#         self.try_again_button_register_new_user_window.place(x=750, y=400)

#         self.capture_label = util.get_img_label(self.register_new_user_window)
#         self.capture_label.place(x=10, y=0, width=700, height=500)

#         self.add_img_to_label(self.capture_label)

#         self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
#         self.entry_text_register_new_user.place(x=750, y=150)

#         self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
#         self.text_label_register_new_user.place(x=750, y=70)

#     def try_again_register_new_user(self):
#         self.register_new_user_window.destroy()

#     def add_img_to_label(self, label):
#         imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
#         label.imgtk = imgtk
#         label.configure(image=imgtk)

#         self.register_new_user_capture = self.most_recent_capture_arr.copy()

#     def start(self):
#         self.main_window.mainloop()

#     def accept_register_new_user(self):
#         name = self.entry_text_register_new_user.get(1.0, "end-1c")

#         embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

#         file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
#         pickle.dump(embeddings, file)

#         util.msg_box('Success!', 'User was registered successfully !')

#         self.register_new_user_window.destroy()


# if __name__ == "__main__":
#     app = App()
#     app.start()

import os.path
import datetime
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util
# from test import test
import requests #use for download with link
from io import BytesIO


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+180+120")
        self.main_window.title("SmartBrella Hub")
        self.main_window.configure(bg="white")
        # self.main_theme = util.get_text_labelstylish(self.main_window,"Smart Face Recognition System")    #plain words
        # self.main_theme.place(x=750,y=100)

        # url="https://jpicpedia.com/wp-content/uploads/2024/06/img_0480-1.jpg"     #*only use for research purpose
        # response = requests.get(url)
        # img_data = response.content

        # img = Image.open(BytesIO(img_data))
        # img = img.resize((280, 280), Image.LANCZOS) 
        # self.photo = ImageTk.PhotoImage(img)    #use self. to prevent data collect as garbage

        # self.main_theme = tk.Label(self.main_window, image=self.photo)
        # self.main_theme.place(x=820,y=15)

        url="https://ik.imagekit.io/meis8v81a/generated_text%20(2).png?updatedAt=1756964724506"
        response = requests.get(url)
        img_data = response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((450, 50), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(img)    #use self. to prevent data collect as garbage

        self.main_theme = tk.Label(self.main_window, image=self.photo, bg="white")
        self.main_theme.place(x=720,y=130)

        url2="https://ik.imagekit.io/meis8v81a/imgbin_732c35ba3efff32796bbd897b304874c.png?updatedAt=1756981830338"
        response2 = requests.get(url2)
        img_data2 = response2.content

        img2 = Image.open(BytesIO(img_data2))
        img2 = img2.resize((115, 105), Image.LANCZOS) 
        self.photo2 = ImageTk.PhotoImage(img2)    #use self. to prevent data collect as garbage

        self.main_theme2 = tk.Label(self.main_window, image=self.photo2, bg="white")
        self.main_theme2.place(x=660,y=385)

        url3="https://ik.imagekit.io/meis8v81a/imgbin_5a017de3f9030ec8ca2cb9049f4d182d.png?updatedAt=1756982208868"
        response3 = requests.get(url3)
        img_data3 = response3.content

        img3 = Image.open(BytesIO(img_data3))
        img3 = img3.resize((470, 100), Image.LANCZOS) 
        self.photo3 = ImageTk.PhotoImage(img3)    #use self. to prevent data collect as garbage

        self.main_theme3 = tk.Label(self.main_window, image=self.photo3, bg="white")
        self.main_theme3.place(x=710,y=20)

        url4="https://ik.imagekit.io/meis8v81a/S67d6a5ec98fd45868f79266bcf1edb60r-removebg-preview.png?updatedAt=1756984519453"
        response4 = requests.get(url4)
        img_data4 = response4.content

        img4 = Image.open(BytesIO(img_data4))
        img4 = img4.resize((200, 100), Image.LANCZOS) 
        self.photo4 = ImageTk.PhotoImage(img4)    #use self. to prevent data collect as garbage

        self.main_theme3 = tk.Label(self.main_window, image=self.photo4, bg="white")
        self.main_theme3.place(x=850,y=200)

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=790, y=300)

        # self.logout_button_main_window = util.get_button(self.main_window, 'Logout', 'red', self.logout)
        # self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=790, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=650, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):

        # label = test(             #
        #         image=self.most_recent_capture_arr,
        #         model_dir=r"C:\Users\User\face-attendance-system\Silent-Face-Anti-Spoofing\resources\anti_spoof_models",
        #         device_id=0
        #         )
        label = 1
        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)
            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                    f.close()

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')

    # def logout(self):

    #     label = test(
    #             image=self.most_recent_capture_arr,
    #             model_dir=r"C:\Users\User\face-attendance-system\Silent-Face-Anti-Spoofing\resources\anti_spoof_models",
    #             device_id=0
    #             )

    #     if label == 1:

    #         name = util.recognize(self.most_recent_capture_arr, self.db_dir)

    #         if name in ['unknown_person', 'no_persons_found']:
    #             util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
    #         else:
    #             util.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
    #             with open(self.log_path, 'a') as f:
    #                 f.write('{},{},out\n'.format(name, datetime.datetime.now()))
    #                 f.close()

    #     else:
    #         util.msg_box('Hey, you are a spoofer!', 'You are fake !')


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+180+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        url="https://ik.imagekit.io/meis8v81a/Gojo-Satoru-Emoji-Jujutsu-Kaisen-anime-cute-face-transparent-PNG-image.png?updatedAt=1756983353171"
        response = requests.get(url)
        img_data = response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.LANCZOS) 
        self.photo4 = ImageTk.PhotoImage(img)    #use self. to prevent data collect as garbage

        self.main_theme = tk.Label(self.register_new_user_window, image=self.photo4, bg="#F0F0F0")
        self.main_theme.place(x=1080,y=290)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=50)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please input Username:')
        self.text_label_register_new_user.place(x=750, y=20)

        self.entry_text_register_new_user2 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user2.place(x=750, y=140)

        self.text_label_register_new_user2 = util.get_text_label(self.register_new_user_window, 'Matrics number:')
        self.text_label_register_new_user2.place(x=750, y=110)

        self.entry_text_register_new_user3 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user3.place(x=750, y=230)

        self.text_label_register_new_user3 = util.get_text_label(self.register_new_user_window, 'Phone number:')
        self.text_label_register_new_user3.place(x=750, y=200)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        matric = self.entry_text_register_new_user2.get(1.0, "end-1c")
        phone = self.entry_text_register_new_user3.get(1.0, "end-1c")
        encodings = face_recognition.face_encodings(self.register_new_user_capture)
        if not encodings:
            util.msg_box('No face detected', 'Please make sure your face is clearly visible and try again.')
            return

        embeddings = encodings[0]
        data={"embedding":embeddings,"info": (name,matric,phone)}
        file = open(os.path.join(self.db_dir, f'{name,matric,phone}.pickle'), 'wb')
        pickle.dump(data, file)

        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()