from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import *
import sqlite3
import os
import cv2
import face_recognition
import numpy as np
import imutils
import time


global Vorname_eingabe
global Nachname_eingabe
global Geburstdatum_eingabe
global kal
global blobData
global my_lab
global path
global images
global classnames
global mylist
global encodelist
global ret
global Bild_lbl
global Info_ID_Label
global Info_Vorname_Label
global Info_Nachname_Label
global Info_Geburstdatum_Label
global Info_Bild_lbl
global test_image
global image1_enc
global USB_path
global video_source
global id_image
global matches_index


verbindung = sqlite3.connect("Tamplate.db")
c = verbindung.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Tamplate 
            (ID  INTEGER NOT NULL PRIMARY KEY  ,
                Vorname TEXT  NOT NULL ,
                Nachname TEXT NOT NULL ,
                Geburstdatum INTEGER NOT NULL,
                bild BLOB

                 )
           """)


class template:
    """--------------- Fenster Erstellen ------------------"""

    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700')
        self.root.resizable(False, False)
        self.root.title('Template ')
        # self.root.iconbitmap('C:\\Databases\\venv\\icon\\web_camera.ico')
        self.root.configure(background="silver")

        tab_Eltren = ttk.Notebook(root)
        tab1 = ttk.Frame(tab_Eltren)
        tab2 = ttk.Frame(tab_Eltren)
        tab_Eltren.add(tab1, text='     Info    ')
        tab_Eltren.add(tab2, text=' Gesichterkennung ')
        tab_Eltren.pack(expand=1, fill='both')

        global Vorname_eingabe
        global Nachname_eingabe
        global Geburstdatum_eingabe
        global kal
        global blobData
        global my_lab
        global path
        global images
        global classnames
        global mylist
        global encodelist
        global ret
        global Bild_lbl
        global Info_ID_Label
        global Info_Vorname_Label
        global Info_Nachname_Label
        global Info_Geburstdatum_Label
        global Info_Bild_lbl
        global test_image
        global image1_enc
        global USB_path
        global video_source
        global id_image
        global index
# alle Vraiables und liste werden hier als leer definiert
        video_source = 0
        global codesavepath
        # codesavepath = "/Tamplate code/"
        path = "Bilder"
        images = []
        classnames = []
        encodelist = []
        global matches_index
        matches_index = 0
        index = []

# ales erstes wird das Programm Bilder gesucht und geprüft

        try:
            Programm_Bilder = os.listdir("Programm Bilder")

# wenn es nicht existert wird ein Folder erstellt und alle Bilder aus der Datebass heruntergeladen
        except Exception:
            print(" file not exist ")
            os.mkdir("Programm Bilder")
            verbindung = sqlite3.connect("Tamplate.db")
            c = verbindung.cursor()
            c.execute("select * from Programm_bild")
            rows = c.fetchall()
            for row in rows:
                myresult = row[2]
                namebild = 'Programm Bilder/', row[1]
                pathbild = ''.join(namebild)
                with open(pathbild, 'wb') as F:
                    F.write(myresult)
                    F.close
            verbindung.commit()
            c.close()
            verbindung.close()

# der Bild des Webcam wird hier for die ganze programm global erkannt
        global web_img

        web_image_path = 'Programm Bilder/webcam_icon.jpg'
        web_img = Image.open(web_image_path)
        web_img.thumbnail((700, 700))
        web_img = ImageTk.PhotoImage(web_img)

# der Bild des Profile  wird hier for die ganze programm global erkannt
        id_image = Image.open("Programm Bilder/Download.png")
        id_image.thumbnail((250, 250))
        id_image = ImageTk.PhotoImage(id_image)

        """ ______________________________Variable _____________________________"""
# Eingabe variable definieren

        self.vorname_var = StringVar()
        self.Nachname_var = StringVar()
        self.Geburstdatum_var = StringVar()
        self.blobData = StringVar()
        self.suchen_var = StringVar()
        self.Del_Nachname_var = StringVar()
        self.Del_vorname_var = StringVar()


# zeit messen
        start = time.time()
        """ hier wird alle Bilder und Namen in ein liste gespeichert. 
                  """
        try:
            mylist = os.listdir(path)
            if len(mylist) != 0:
                for cls in mylist:
                    name = path, '/', cls
                    imgpath = ''.join(name)
                    curimg = face_recognition.load_image_file(imgpath)
                    images.append(curimg)
                    classnames.append(os.path.splitext(cls)[0])
                self.findencodknown(images)
            else:
                pass

        except Exception:
            """ falls die Diroctory nicht existert wird eine hergestelt und alle Bilder aus Datebass gerufen"""
            print(" file not exist ")
            os.mkdir(path)
            verbindung = sqlite3.connect("Tamplate.db")
            c = verbindung.cursor()
            c.execute("select * from Tamplate")
            rows = c.fetchall()
            if len(rows)!=0:
                for row in rows:
                    myresult = row[4]
                    namebild = 'Bilder/', row[1], '.', row[2], '.jpg'
                    pathbild = ''.join(namebild)
                    with open(pathbild, 'wb') as F:
                        F.write(myresult)
                        F.close
            verbindung.commit()
            c.close()
            verbindung.close()

            mylist = os.listdir(path)
            if len(mylist) != 0:
                for cls in mylist:
                    name = path, '/', cls
                    imgpath = ''.join(name)
                    curimg = face_recognition.load_image_file(imgpath)
                    images.append(curimg)
                    classnames.append(os.path.splitext(cls)[0])
                self.findencodknown(images)
            else:
                pass

        end = time.time()
        print(end - start)



# benutzer_Fram --------------------------
        benutzer_Fram = Frame(tab1, bg='#E0E0F8')
        benutzer_Fram.place(x=1, y=1, height=200, width=270)
# Vorname --------------------------
        Vorname_Label = Label(benutzer_Fram, text='Vorname : ', font=('helvetica', 11), bg='#E0E0F8')
        Vorname_Label.pack()
        Vorname_eingabe = Entry(benutzer_Fram, textvariable=self.vorname_var, bd=2, justify='center')
        Vorname_eingabe.pack()
# Nachname --------------------------
        Nachname_Label = Label(benutzer_Fram, text='Nachname : ', font=('helvetica', 11), bg='#E0E0F8')
        Nachname_Label.pack()
        Nachname_eingabe = Entry(benutzer_Fram, textvariable=self.Nachname_var, bd=2, justify='center')
        Nachname_eingabe.pack()
# Geburstdatum --------------------------
        Geburstdatum_Label = Label(benutzer_Fram, text='Geburstdatum : ', font=('helvetica', 11), bg='#E0E0F8')
        Geburstdatum_Label.pack()
        my_lab = Label(benutzer_Fram, bg='#ffffff')
        my_lab.place(x=72, y=110, height=20, width=125)
        Geburstdatum_Button = Button(benutzer_Fram, command=self.datum, text='  ', font=('helvetica', 11), bg='#A9BCF5')
        Geburstdatum_Button.place(x=205, y=110, height=20, width=20)
# Bild --------------------------

        Bild_lbl = Label(tab1, bg='#f2f2f2')
        Bild_lbl.place(x=1, y=235, height=260, width=270)
        Bild_lbl.configure(image=id_image)
        Bild_lbl.image = id_image
        bild_button = Button(benutzer_Fram, text='Bild suchen', command=self.Showimage, font='Times', bg='#A9BCF5')
        bild_button.place(x=90, y=155)

# ______________________________Buttons_________________________________

        buttons_fram = Frame(tab1, bg='#E0E0F8')
        buttons_fram.place(x=1, y=500, height=150, width=270)
# add_button _______________________________________________________________

        add_button = Button(buttons_fram, command=self.Add, text='Add Data', font='Times', bg='#A9BCF5')
        add_button.place(x=30, y=20, height=30, width=200)

# clear_button  _______________________________________________________________

        clear_button = Button(buttons_fram, text='Clear', command=self.clear, font='Times', bg='#A9BCF5')
        clear_button.place(x=30, y=55, height=30, width=200)

# Schlißen_button _______________________________________________________________

        schlissen_button = Button(buttons_fram, text='Schlißen', command=self.exit, font='Times', bg='#A9BCF5')
        schlissen_button.place(x=30, y=90, height=30, width=200)

# __________________________ Suchen Fram __________________________________

        suchen_fram = Frame(tab1, bg='#E0E0F8')
        suchen_fram.place(x=275, y=1, height=60, width=1022)
# Suchen_Label ____________________________________________________________

        Suchen_Label = Label(suchen_fram, text='Suche  : ', font=('Times', 12), bg='#E0E0F8')
        Suchen_Label.place(x=20, y=20)
# suchen_type ____________________________________________________________

        self.suchen_type = ttk.Combobox(suchen_fram, justify='right')
        self.suchen_type['value'] = ('Vorname', 'Nachname', ' Geburstdatum')
        self.suchen_type.place(x=80, y=20)
# suchen_eingabe ________________________________________________________

        suchen_eingabe = Entry(suchen_fram, textvariable=self.suchen_var, bd=2, justify='center')
        suchen_eingabe.place(x=250, y=20)
# suchen_button _______________________________________________________

        suchen_button = Button(suchen_fram, text='Suchen', command=self.suchen, font=('Times'), bg='#A9BCF5')
        suchen_button.place(x=400, y=15, height=30, width=70)
        refresh_button = Button(suchen_fram, text='Aktualisieren', command=self.Aktualisier, font='Times',
                                bg='#A9BCF5')
        refresh_button.place(x=490, y=15, height=30, width=120)

# __________________________ Table Fenster Frame _________________________________________
        """"  Table Fenster Frame wird alle Information aus der Databass in Form eine Tabelle zeigen """

        fenster = Frame(tab1, bg='#FAFAFA')
        fenster.place(x=275, y=70, height=550, width=722)
        # -------------- Scroll ------------
        scroll_x = Scrollbar(fenster, orient=HORIZONTAL)
        scroll_y = Scrollbar(fenster, orient=VERTICAL)
        # --------------- Review Table ------------------------

# tabell erstellen und mit der Datebass in verbindung setzen

        self.person_table = ttk.Treeview(fenster,
                                         columns=(
                                             'ID', 'Vorname', 'Nachname', 'Geburstdatum'),
                                         xscrollcommand=scroll_x.set,
                                         yscrollcommand=scroll_y.set)

        self.person_table.place(x=0, y=0, height=530, width=700)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.person_table.xview)
        scroll_y.config(command=self.person_table.yview)
        self.person_table['show'] = 'headings'

        self.person_table.heading('ID', text='ID')
        self.person_table.column('ID', width=20)

        self.person_table.heading('Vorname', text='Vorname')
        self.person_table.column('Vorname', width=50)

        self.person_table.heading('Nachname', text='Nachname')
        self.person_table.column('Nachname', width=50)

        self.person_table.heading('Geburstdatum', text='Geburstdatum')
        self.person_table.column('Geburstdatum', width=50)

# mit einem Mouse click wird den gedrückte Name auf der Info Browser präsentiert

        self.person_table.bind("<ButtonRelease-1>", self.Info)
        self.fetch_all()
# Info_Fenster _____________________________________________________

        info_Fenster = Frame(tab1, bg='#A9BCF5')
        title = Label(info_Fenster,
                      text='Info Browser',
                      bg='#EFF5FB',
                      font=('helvetica', 15),
                      fg='black'
                      )
        title.pack(fill=X)
        info_Fenster.place(x=1000, y=70, height=540, width=297)
        Info_Bild_lbl = Label(info_Fenster, bg='#A9BCF5')
        Info_Bild_lbl.place(x=20, y=40, height=250, width=250)

        Info_Bild_lbl.configure(image=id_image)
        Info_Bild_lbl.image = id_image
# ID --------------------------
        id_Label = Label(info_Fenster, text='ID : ', font=('serif', 15), bg='#A9BCF5')
        id_Label.place(x=10, y=290)
        Info_ID_Label = Label(info_Fenster, font=('serif', 15), bg='#A9BCF5')
        Info_ID_Label.place(x=150, y=290)
# Vorname --------------------------
        Vorname_Label = Label(info_Fenster, text='Vorname : ', font=('serif', 15), bg='#A9BCF5')
        Vorname_Label.place(x=10, y=320)
        Info_Vorname_Label = Label(info_Fenster, font=('serif', 15), bg='#A9BCF5')
        Info_Vorname_Label.place(x=150, y=320)
# Nachname --------------------------
        Nachname_Label = Label(info_Fenster, text='Nachname : ', font=('serif', 15), bg='#A9BCF5')
        Nachname_Label.place(x=10, y=350)
        Info_Nachname_Label = Label(info_Fenster, font=('serif', 15), bg='#A9BCF5')
        Info_Nachname_Label.place(x=150, y=350)
# Geburstdatum --------------------------
        Geburstdatum_Label = Label(info_Fenster, text='Geb.datum : ', font=('serif', 15), bg='#A9BCF5')
        Geburstdatum_Label.place(x=10, y=380)
        Info_Geburstdatum_Label = Label(info_Fenster, font=('serif', 15), bg='#A9BCF5')
        Info_Geburstdatum_Label.place(x=150, y=380)
# update_button _______________________________________________________________
        update_button = Button(info_Fenster, text='Update Data', font='Times', bg='#99ff99', command=self.update)
        update_button.place(x=48.5, y=460, height=30, width=200)
# del_button _______________________________________________________________
        del_button = Button(info_Fenster, command=self.delete, text='Delete Data', font='Times', bg='#ff4d4d')
        del_button.place(x=48.5, y=495, height=30, width=200)
# __________________________________________________________________________________________________________________
    # Tabe 2 Gesichterkennung
        person_fram = Frame(tab2, bg='#66d9ff')
        person_fram.place(x=1, y=1, height=400, width=270)

        result_info_fram = Frame(tab2, bg='#33ccff')
        result_info_fram.place(x=275, y=1, height=495, width=300)

        function_button_fram = Frame(tab2, bg='#4dd2ff')
        function_button_fram.place(x=1, y=405, height=300, width=270)

# ___________________________ Result Bild _____________________________

        global result_Info_Bild_lbl
        global result_image

        self.result_Info_Bild_lbl = Label(result_info_fram, bg='#33ccff')
        self.result_Info_Bild_lbl.place(x=20, y=40, height=250, width=250)
        self.result_Info_Bild_lbl.configure(image=id_image)
        self.result_Info_Bild_lbl.image = id_image

# -------------------------- result_id  --------------------------

        result_id_Label = Label(result_info_fram, text='ID : ', font=('serif', 15), bg='#33ccff')
        result_id_Label.place(x=10, y=290)

        self.res_ID_Label = Label(result_info_fram, font=('serif', 15), bg='#33ccff')
        self.res_ID_Label.place(x=140, y=290)

# -------------------------- result_Vorname --------------------------

        result_Vorname_Label = Label(result_info_fram, text='Vorname : ', font=('serif', 15), bg='#33ccff')
        result_Vorname_Label.place(x=10, y=320)
        self.res_Vorname_Label = Label(result_info_fram, font=('serif', 15), bg='#33ccff')

        self.res_Vorname_Label.place(x=140, y=320)

# -------------------------- result_Nachname --------------------------

        result_Nachname_Label = Label(result_info_fram, text='Nachname : ', font=('serif', 15), bg='#33ccff')
        result_Nachname_Label.place(x=10, y=350)
        self.res_Nachname_Label = Label(result_info_fram, font=('serif', 15), bg='#33ccff')
        self.res_Nachname_Label.place(x=140, y=350)

# -------------------------- result_Geburstdatum --------------------------

        result_Geburstdatum_Label = Label(result_info_fram, text='Geb.datum : ', font=('serif', 15), bg='#33ccff')
        result_Geburstdatum_Label.place(x=10, y=380)

        self.res_Geburstdatum_Label = Label(result_info_fram, font=('serif', 15), bg='#33ccff')
        self.res_Geburstdatum_Label.place(x=140, y=380)
# __________________________________________________________________

        test_image = Label(person_fram)
        test_image.place(x=10, y=5, height=250, width=250)
        image_path = "Programm Bilder/gesichtserkennung.jpg"
        img = Image.open(image_path)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        test_image.configure(image=img)
        test_image.image = img
        anweisung_label = Label(person_fram)
        anweisung_label.place(x=10, y=300, height=50, width=250)
# ______________________________________________________________

        add_image = Button(function_button_fram, text='Bild einfügen', font='Times', bg='#b3ecff',
                           command=self.Gesichtimage)
        add_image.place(x=35, y=10, height=30, width=200)

# ______________________________________________________________

        image_erkennen = Button(function_button_fram, text='Gesichtserkennung', font='Times', bg='#b3ecff',
                                command=self.erkennen)
        image_erkennen.place(x=35, y=45, height=30, width=200)
# ______________________________________________________________

        clear_image_button = Button(function_button_fram, text='Clear', command=self.clear_image, font='Times',
                                    bg='#A9BCF5')
        clear_image_button.place(x=35, y=80, height=30, width=200)

# Schlißen_button _______________________________________________________________

        schlissen_button = Button(function_button_fram, text='Schlißen', command=self.exit, font='Times', bg='#A9BCF5')
        schlissen_button.place(x=35, y=115, height=30, width=200)

        Web_Video_fram = Frame(tab2, bg='#33ccff')
        Web_Video_fram.place(x=275, y=500, height=130, width=300)

        self.select = IntVar()
        self.Gesichtserkennung = Checkbutton(Web_Video_fram, text = "Gesichtserkennung", variable=self.select,
                                             bg='#A9BCF5')
        self.Gesichtserkennung.place(x=50, y=10, height=25, width=200)

        self.web_button = Button(Web_Video_fram, text='Webcam', command=self.web, font='Times', state="active",
                                 bg='#A9BCF5')
        self.web_button.place(x=50, y=40, height=25, width=200)

        self.play_video_btn = Button(Web_Video_fram, text='Video ', command=self.play_video, font='Times',
                                     state="active", bg='#A9BCF5')
        self.play_video_btn.place(x=50, y=70, height=25, width=200)

        self.web_close_btn = Button(Web_Video_fram, text='stop', command=self.web_Video_close, font='Times',
                                    bg='#A9BCF5', state="disabled")
        self.web_close_btn.place(x=50, y=100, height=25, width=200)

# __________________________________________________________________

        self.labimg = Label(tab2, font='Times', bg='#A9BCF5')
        self.labimg.place(x=600, y=0, width=700, height=500)
        self.labimg.configure(image=web_img)
        self.labimg.image = web_img

# _____________________________________________

        Gesicht_table_fram = Frame(tab2, bg='#FAFAFA')
        Gesicht_table_fram.place(x=600, y=505, height=200, width=700)
        # -------------- Scroll ------------
        scroll_x = Scrollbar(Gesicht_table_fram, orient=HORIZONTAL)
        scroll_y = Scrollbar(Gesicht_table_fram, orient=VERTICAL)
        # --------------- Review Table ------------------------
        self.Gesicht_table = ttk.Treeview(Gesicht_table_fram,
                                         columns=(
                                             'ID', 'Vorname', 'Nachname', 'Geburstdatum'),
                                         xscrollcommand=scroll_x.set,
                                         yscrollcommand=scroll_y.set)

        self.Gesicht_table.place(x=0, y=0, height=200, width=700)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Gesicht_table.xview)
        scroll_y.config(command=self.Gesicht_table.yview)
        self.Gesicht_table['show'] = 'headings'

        self.Gesicht_table.heading('ID', text='ID')
        self.Gesicht_table.column('ID', width=20)

        self.Gesicht_table.heading('Vorname', text='Vorname')
        self.Gesicht_table.column('Vorname', width=50)

        self.Gesicht_table.heading('Nachname', text='Nachname')
        self.Gesicht_table.column('Nachname', width=50)

        self.Gesicht_table.heading('Geburstdatum', text='Geburstdatum')
        self.Gesicht_table.column('Geburstdatum', width=50)

        self.Gesicht_table.bind("<ButtonRelease-1>", self.erkannte_Gesicht_Info)
# _____________________    erkennen     ____________________

    def erkennen(self):
        matches_index = 0
        verbindung = sqlite3.connect("Tamplate.db")
        c = verbindung.cursor()
        try:
            for encodeFace, Faceloc in zip(image1_enc, image1_face):

                matches = face_recognition.compare_faces(encodelist, encodeFace)
                faceDis = face_recognition.face_distance(encodelist, encodeFace)
                matches_index = np.argmin(faceDis)

                if matches[matches_index]:

                    name = classnames[matches_index]
                    result_vorname_erkennung = os.path.splitext(name)[0]
                    result_nachname_erkennung = os.path.splitext(name)[1]
                    result_nachname_erkennung = result_nachname_erkennung.split('.', 1)[1]

                    c.execute(
                        "select * from Tamplate WHERE Vorname = '" + result_vorname_erkennung + "' AND Nachname = '" + result_nachname_erkennung + "'")
                    rows = c.fetchall()[0]
                    self.Gesicht_table.insert("", END, value=rows)
                else:
                    rows = ['x', 'nicht bekannt', 'nicht bekannt', 'nicht bekannt']
                    self.Gesicht_table.insert("", END, value=rows)
        except Exception:
            pass
        c.close()
        verbindung.close()

# _____________________    face_recognition     ____________________

    def face_recognition(self):
        verbindung = sqlite3.connect("Tamplate.db")
        c = verbindung.cursor()

        face_loc_cuframe = face_recognition.face_locations(self.frame)
        face_cuframe = face_recognition.face_encodings(self.frame, face_loc_cuframe)
        for encodeFace, Faceloc in zip(face_cuframe, face_loc_cuframe):

            matches = face_recognition.compare_faces(encodelist, encodeFace)
            faceDis = face_recognition.face_distance(encodelist, encodeFace)
            matches_index = np.argmin(faceDis)

            if matches[matches_index]:
                name = classnames[matches_index]
                y1, x2, y2, x1 = Faceloc
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                result_vorname_erkennung = os.path.splitext(name)[0]
                result_nachname_erkennung = os.path.splitext(name)[1]
                result_nachname_erkennung = result_nachname_erkennung.split('.', 1)[1]

                c.execute(
                    "select * from Tamplate WHERE Vorname = '" + result_vorname_erkennung + "' AND Nachname = '" + result_nachname_erkennung + "'")
                verbindung.commit()
                rows = c.fetchall()[0]
                try:
                    if len(index) != 0:
                        #for x in index:
                            if index.count(rows[0]) == 1:
                                pass
                            else:
                                self.Gesicht_table.insert("", END, value=rows)
                                index.append(rows[0])
                    else:
                        self.Gesicht_table.insert("", END, value=rows)
                        index.append(rows[0])
                except Exception :
                    print(" ;(")
                    # pass

            else:
                y1, x2, y2, x1 = Faceloc
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                rows = ['x', 'nicht bekannt', 'nicht bekannt', 'nicht bekannt']
                if index.count(rows[0]) == 1:
                    pass
                else:
                    self.Gesicht_table.insert("", END, value=rows)
                    index.append(rows[0])

            verbindung.commit()
        c.close()
        verbindung.close()

# _____________________________________________

    def web(self):
        global vid
        vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        self.delay = 15
        self.web_close_btn.configure(state ="active")
        self.play_video_btn.configure(state = "disabled")
        self.web_button.configure(state="disabled")
        self.up()

# _____________________________________________

    def play_video(self):
        global vid
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Bild Browser ",
                                         filetypes=(("all video format", ".mp4"),
                                                    ("all video format", ".flv"),
                                                    ("all video format", ".avi"),
                                                    ("All files", "*.*")))
        vid = cv2.VideoCapture(fln)
        vid.set(5, 30)
        self.delay = 15
        self.play_video_btn.configure(state="disabled")
        self.web_button.configure(state="disabled")
        self.web_close_btn.configure(state="active")
        self.up()

# _____________________________________________

    def up(self):
        scan_this = True
        # Get a frame from the video source
        # Gesichtserkennung aktiverien
        if self.select.get() == 1:

            #vid.set(5, 60)
            ret, self.frame = vid.read()
            if ret:
                self.frame = imutils.resize(self.frame, width=700, height=500)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                if scan_this:
                    self.face_recognition()
                    scan_this = not scan_this
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.labimg.configure(image=self.photo)
                self.root.after(10, self.up)

# Gesichtserkennung ausschalten
        else:
            ret, self.frame = vid.read()
            if ret:
                self.frame = imutils.resize(self.frame, width=700,height=500)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.labimg.configure(image=self.photo)
                self.root.after(15, self.up)

# _____________________________________________

    def web_Video_close(self):

        vid.release()
        self.labimg.configure(image=web_img)
        self.labimg.image = web_img
        self.web_close_btn.configure(state="disabled")
        self.play_video_btn.configure(state="active")
        self.web_button.configure(state="active")

# ___________________________________________________

    def knowfaces(self):
        mylist = os.listdir(path)
        if len(mylist) != 0:
            for cls in mylist:
                name = path, '/', cls
                imgpath = ''.join(name)
                curimg = face_recognition.load_image_file(imgpath)
                images.append(curimg)
                classnames.append(os.path.splitext(cls)[0])

            return classnames
            return images
            self.findencodknown(images)
        else:
            pass

# ______________________________________________________________

    def findencodknown(self, images):

        for image in images:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]

            encodelist.append(encode)
        return encodelist

# ____________________   Gesichtimage   ____________________
# mit diese Funktion können wir eine Bild  walhen und die face_reg durchfüchen um die Gesicht Matrix zu erstellen
# und mit der Bekannte pesonen Matrix zu vergleichen

    def Gesichtimage(self):
        global image1_enc
        global image1_face
        self.result_Info_Bild_lbl.configure(image=id_image)
        self.result_Info_Bild_lbl.image = id_image
        self.res_ID_Label.config(text="")
        self.res_Vorname_Label.config(text="")
        self.res_Nachname_Label.config(text="")
        self.res_Geburstdatum_Label.config(text="")
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Bild Browser ",
                                         filetypes=(("JPG file", "*.jpg"), ("PNG file", "*.png"), ("All files", "*.*")))
        image1 = face_recognition.load_image_file(f'{fln}')
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image1_face = face_recognition.face_locations(image1)
        image1_enc = face_recognition.face_encodings(image1,image1_face)
        img = Image.open(fln)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        test_image.configure(image=img)
        test_image.image = img

# ___________________________________________________
# mit hilfe diese Funktion ist die präsentation von der Matrix-Vergleichung Egebnisse möglich
    def erkannte_Gesicht_Info(self,ev):
        self.result_Info_Bild_lbl.configure(image=id_image)
        self.result_Info_Bild_lbl.image = id_image
        cursor_row = self.Gesicht_table.focus()
        contents = self.Gesicht_table.item(cursor_row)
        rows = contents['values']
        self.res_ID_Label.config(text=f'{rows[0]}')
        self.res_Vorname_Label.config(text=rows[1])
        self.res_Nachname_Label.config(text=rows[2])
        self.res_Geburstdatum_Label.config(text=rows[3])
        if f'{rows[1]}'!= "nicht bekannt":
            name = 'Bilder/', rows[1], '.', rows[2], '.jpg'
            path = ''.join(name)
            image = Image.open(path)
            image.thumbnail((250, 250))
            image = ImageTk.PhotoImage(image)
            self.result_Info_Bild_lbl.configure(image=image)
            self.result_Info_Bild_lbl.image = image
        else:
            pass

# ___________________  Verbindung & Add ___________________

    def Add(self):

        if self.vorname_var.get() and self.Nachname_var.get() and blobData != 0:

            verbindung = sqlite3.connect("Tamplate.db")
            c = verbindung.cursor()
            c.execute(""" INSERT INTO  Tamplate (Vorname , Nachname , Geburstdatum, bild ) VALUES (?,?,?,?) """, (
                self.vorname_var.get(),
                self.Nachname_var.get(),
                kal.get_date(),
                sqlite3.Binary(blobData),
            ))
            verbindung.commit()
            self.fetch_all()
            c.close()
            verbindung.close()
            self.save()
            self.clear()
            self.knowfaces()
            self.message_Succes()
        else:
            self.message_error()

# _________________________________________________

    def update(self):
        if self.vorname_var.get() and self.Nachname_var.get() and blobData != 0:
            cursor_row = self.person_table.focus()
            contents = self.person_table.item(cursor_row)
            row = contents['values']
            verbindung = sqlite3.connect("Tamplate.db")
            c = verbindung.cursor()
            c.execute("""update Tamplate set Vorname = ? , Nachname = ?, Geburstdatum =? , bild =? where ID=? """, (
                self.vorname_var.get(),
                self.Nachname_var.get(),
                kal.get_date(),
                blobData,
                row[0]
            ))
            verbindung.commit()
            self.fetch_all()
            c.close()
            verbindung.close()
            name = 'Bilder/', row[1], '.', row[2], '.jpg'
            path = ''.join(name)
            os.remove(path)
            self.save()
            self.clear()
            self.Aktualisier()
            self.message_update()
        else:
            self.message_error()

# ------------------   Data Zeigen    -------------------

    def fetch_all(self):
        verbindung = sqlite3.connect("Tamplate.db")
        c = verbindung.cursor()
        c.execute("select * from Tamplate")
        rows = c.fetchall()
        # if len(rows)!=0:
        self.person_table.delete(*self.person_table.get_children())
        for row in rows:
            self.person_table.insert("", END, value=row)
        verbindung.commit()
        c.close()
        verbindung.close()

# ____________________     Delete       ___________________

    def delete(self):

        if Info_Vorname_Label and Info_Nachname_Label and Info_Geburstdatum_Label != 0:

            cursor_row = self.person_table.focus()
            contents = self.person_table.item(cursor_row)
            row = contents['values']
            verbindung = sqlite3.connect("Tamplate.db")
            c = verbindung.cursor()
            c.execute("""DELETE  FROM  Tamplate WHERE ID= ? AND Vorname = ? AND Nachname = ?AND Geburstdatum = ? """, (
                row[0],
                row[1],
                row[2],
                row[3]
            ))
            verbindung.commit()
            self.fetch_all()
            self.Aktualisier()
            name = 'Bilder/', row[1], '.', row[2], '.jpg'
            path = ''.join(name)
            os.remove(path)
            code_name = 'Tamplate code/',  row[1], '.', row[2], '.npy'
            pathcode = ''.join(code_name)
            os.remove(pathcode)
            self.Aktualisier()
            self.message_delet()
            c.close()
            verbindung.close()
        else:
            self.message_error()

# ____________________    Showimage     ___________________

    def Showimage(self):
        global blobData
        global image1_enc

        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Bild Browser ",
                                         filetypes=(("JPG file", "*.jpg"), ("PNG file", "*.png"), ("All files", "*.*")))
        code = face_recognition.load_image_file(f'{fln}')
        code = cv2.cvtColor(code, cv2.COLOR_BGR2RGB)
        image1_enc = face_recognition.face_encodings(code)

        img = Image.open(fln)
        with open(fln, 'rb') as file:
            blobData = file.read()
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        Bild_lbl.configure(image=img)
        Bild_lbl.image = img
        return image1_enc

# ____________________      clear       ___________________

    def clear(self):

        Vorname_eingabe.delete(0, END)
        Nachname_eingabe.delete(0, END)
        my_lab.configure(text='')
        Bild_lbl.configure(image=id_image)
        Bild_lbl.image = id_image

# _____________________  clear_image    ____________________

    def clear_image(self):
        img = Image.open("Programm Bilder/gesichtserkennung.jpg")
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        test_image.configure(image=img)
        test_image.image = img
        self.result_Info_Bild_lbl.configure(image=id_image)
        self.result_Info_Bild_lbl.image = id_image
        self.res_ID_Label.config(text="")
        self.res_Vorname_Label.config(text="")
        self.res_Nachname_Label.config(text="")
        self.res_Geburstdatum_Label.config(text="")
        self.Gesicht_table.delete(*self.Gesicht_table.get_children())
        index.clear()


# ____________________       Datum      ___________________

    def datum(self):
        global geb
        global kal
        geb = Tk()
        geb.geometry("200x250")
        geb.resizable(False, False)
        kal = Calendar(geb, selectmode="day")
        kal.pack(pady=20)
        button = Button(geb, text='Get Date', command=self.grab)
        button.pack()
        geb.mainloop()
# ____________________       Grab       ___________________

    def grab(self):
        global my_lab
        my_lab.config(text=kal.get_date(), font=('serif', 11))
        geb.destroy()

# ____________________    Message Error ___________________

    def message_error(self):
        messagebox.showwarning("Warning", " Bitte Alle Information eingeben")

# ____________________    Message Succes ___________________

    def message_Succes(self):
        messagebox.showinfo("Info", " die Template ist hergestelt")

# ____________________    Message Aktualisieren ____________

    def message_update(self):
        messagebox.showinfo("Info", " die Template ist aktualisiert")

# ____________________    Message Aktualisieren ____________

    def message_delet(self):
        messagebox.showinfo("Info", " die Template ist gelöscht !!")

# ____________________    Aktualisier   ___________________

    def Aktualisier(self):
        self.fetch_all()
        self.suchen_var.set('')
        self.suchen_type.set('')
        Info_ID_Label.config(text='')
        Info_Vorname_Label.config(text='')
        Info_Nachname_Label.config(text='')
        Info_Geburstdatum_Label.config(text='')
        Info_Bild_lbl.configure(image= id_image)
        Info_Bild_lbl.image = id_image

        mylist = os.listdir(path)
        if len(mylist) != 0:
            for cls in mylist:
                name = path, '/', cls
                imgpath = ''.join(name)
                curimg = face_recognition.load_image_file(imgpath)
                images.append(curimg)
                classnames.append(os.path.splitext(cls)[0])
            self.findencodknown(images)
        else:
            pass

# ____________________    Info zeigen   ___________________

    def Info(self, ev):
        global blob
        cursor_row = self.person_table.focus()
        contents = self.person_table.item(cursor_row)
        row = contents['values']
        Info_ID_Label.config(text=row[0])
        Info_Vorname_Label.config(text=row[1])
        Info_Nachname_Label.config(text=row[2])
        Info_Geburstdatum_Label.config(text=row[3])
        name = 'Bilder/', row[1], '.', row[2], '.jpg'
        path = ''.join(name)
        image = Image.open(path)
        image.thumbnail((250, 250))
        image = ImageTk.PhotoImage(image)
        Info_Bild_lbl.configure(image=image)
        Info_Bild_lbl.image = image

# ____________________       Exit       ___________________

    def exit(self):
        exit_frage = messagebox.askquestion("Exit", "Sind sie Sicher ? ")
        if exit_frage == 'yes':
            root.destroy()

# ________________________________________________________

    def message_error_suche(self):
        messagebox.showwarning("Warning", " Keine Treffer")

# ________________________________________________________

    def save(self):
        verbindung = sqlite3.connect("Tamplate.db")
        c = verbindung.cursor()
        c.execute("SELECT * FROM  Tamplate  WHERE  Vorname = ? AND Nachname = ?AND Geburstdatum = ? ", (
            self.vorname_var.get(),
            self.Nachname_var.get(),
            kal.get_date(),
        ))
        verbindung.commit()
        myresult = c.fetchone()[4]
        namebild = 'Bilder/', self.vorname_var.get(),'.', self.Nachname_var.get(), '.jpg'
        pathbild = ''.join(namebild)
        with open(pathbild, 'wb') as F:
            F.write(myresult)
            F.close
        code_name ='Tamplate code/', self.vorname_var.get(),'.', self.Nachname_var.get(),'.npy'
        pathcode = ''.join(code_name)
        code_file = np.save(pathcode, image1_enc)

# _______________________________________________________

    def suchen(self):
        verbindung = sqlite3.connect("Tamplate.db")
        c = verbindung.cursor()
        name = ''.join(self.suchen_var.get())
        print(self.suchen_type.get())
        print(self.suchen_var.get())
        c.execute("select * from Tamplate WHERE " + self.suchen_type.get() + " = ' " + self.suchen_var.get() + "' ")
        rows = c.fetchall()
        if len(rows) != 0:
            self.person_table.delete(*self.person_table.get_children())
            for row in rows:
                self.person_table.insert("", END, value=row)
            verbindung.commit()
        else:
            self.message_error_suche()
        c.close()
        verbindung.close()

# ________________________________________________________

root = Tk()
ob = template(root)
root.mainloop()