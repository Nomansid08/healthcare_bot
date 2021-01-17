import time
import datetime as dt
import pyodbc
from tkinter import *
import os
import numpy
import pandas
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from PIL import Image, ImageTk


training_dataset = pandas.read_csv('Training.csv')
test_dataset = pandas.read_csv('Testing.csv')

X = training_dataset.iloc[:, 0:132].values
Y = training_dataset['prognosis'].values

le = LabelEncoder()
y = le.fit_transform(Y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

cols = training_dataset.columns
cols = cols[:-2]

reduce_dimension = training_dataset.groupby(training_dataset['prognosis']).max()

importances = classifier.feature_importances_
indices = numpy.argsort(importances)[::-1]
features = cols

def print_disease(node):
    node = node[0]
    value = node.nonzero()
    disease = le.inverse_transform(value[0])
    return disease


def traverse(node, depth):
    global val, ans
    global tree_, feature_name, symptoms_present
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]
        yield name + " ?"
        ans = ans.lower()
        if ans == 'yes':
            val = 1
        else:
            val = 0
        if val <= threshold:
            yield from traverse(tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            yield from traverse(tree_.children_right[node], depth + 1)
    else:
        present_disease = print_disease(tree_.value[node])
        strData = "You may have :" + str(present_disease)

        healthcare_bot_gui.ref_obj.entry2.insert(END, str(strData) + '\n')

        red_cols = reduce_dimension.columns
        symptoms_given = red_cols[reduce_dimension.loc[present_disease].values[0].nonzero()]

        strData = "symptoms present:  " + str(list(symptoms_present))
        healthcare_bot_gui.ref_obj.entry2.insert(END, str(strData) + '\n')

        strData = "symptoms given: " + str(list(symptoms_given))
        healthcare_bot_gui.ref_obj.entry2.insert(END, str(strData) + '\n')
        yield strData


def tree_to_code(tree, feature_names):
    global tree_, feature_name, symptoms_present
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    symptoms_present = []
    traverse(0, 1)


def execute_bot():
    tree_to_code(classifier, cols)


logged = False
global rowss

def onFrameConfigure(c):
    c.configure(scrollregion=c.bbox("all"))


class heathcare_bot_gui():

    iter_obj = None
    ref_obj = None

    def __init__(self):
        heathcare_bot_gui.ref_obj = self
        self.iter_obj = None

    def customer(self):
        global r3
        r3 = Tk()
        r3.title('Diagnosis')
        r3.geometry('1536x864')
        c = Canvas(r3, background = "#FFFFFF")

        Label(r3, text=f"{dt.datetime.now():%d-%b-%Y    %a}", fg="green").place(x=1100, y=120)

        l1 = Label(r3, text="HealthCare Bot", fg="red", font=("Times New Roman", 26)).place(x=250, y=60)

        Label(r3, text="Answer question by clicking yes/no", font=("Helvetica", 16)).place(x=200, y=250)

        self.entry1 = Text(r3, borderwidth=2, relief="solid")
        self.entry1.config(fg="black")
        self.entry1.place(x=200, y=300, height=100, width=1050)

        Label(r3, text="Result of Diagnosis", font=("Helvetica", 16)).place(x=200, y=450)


        self.entry2 = Text(r3, borderwidth=2, relief="solid")
        self.entry2.config(fg="black")
        self.entry2.place(x=200, y=500, height=150, width=1050)

        Button(r3, text="Start", height=1, width=10, bg="green", fg="black",command=self.click_start).place(x=200, y=700)
        Button(r3, text="Yes", height=1, width=10, bg="green", fg="black",command=self.click_yes).place(x=400,y=700)
        Button(r3, text="No", height=1, width=10, bg="red", fg="black",command=self.click_no).place(x=500, y=700)
        Button(r3, text="Clear", height=1, width=10, fg="black",command=self.click_clear).place(x=700, y=700)

        c.pack(fill=BOTH, expand=1)

        r3.mainloop()

    def click_no(self):
        global val, ans
        ans = 'no'
        str1 = heathcare_bot_gui.iter_obj.__next__()
        self.entry1.delete(0.0, END)
        self.entry1.insert(END, str1 + "\n")

    def click_yes(self):
        global val, ans
        ans = 'yes'
        self.entry2.delete(0.0, END)
        str1 = heathcare_bot_gui.iter_obj.__next__()

    def click_clear(self):
        self.entry2.delete(0.0, END)
        self.entry1.delete(0.0, END)

    def click_start(self):
        execute_bot()
        self.entry2.delete(0.0, END)
        self.entry1.delete(0.0, END)
        self.entry2.insert(END, "Please Click on Yes or No for the above symptoms in Question")
        healthcare_bot_gui.iter_obj = traverse(0, 1)
        str1 = healthcare_bot_gui.iter_obj.__next__()
        self.entry1.insert(END, str1 + "\n")

def insert():
    file = open(username.get(), "w")
    file.write(username.get() + "\n")
    file.write(password.get())
    file.close()
    Label(r2, text="You have been successfully registered", font=("Helvetica", 16), fg="yellow").place(x=200, y=350)
    Button(r2, text="Login Here", height=2, width=20 , command=login).place(x=200, y=400)
    Button(r2, text="Home", height=2, width=20 , command=r2.destroy).place(x=400, y=400)


def click_login():
    username1 = username.get()
    password1 = password.get()
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verification = file1.read().splitlines()
        if password1 in verification:
            Label(root, text="Welcome %s" % (username.get()), font=("Helvetica", 16)).place(x=500, y=50)
            r1.destroy()
            logged = True
            logged_in = heathcare_bot_gui()
            logged_in.customer()
        else:
            Label(r1, text="Invalid Username or Password", fg="red").place(x=200, y=80)
            username.delete(0, "end")
            password.delete(0, "end")
            username.insert(0, "Username*")
            username.config(fg="grey")
            password.insert(0, "password*")
            password.config(fg="grey")
    else:
        Label(r1, text="Invalid Username or Password", fg="red").place(x=200, y=80)
        username.delete(0, "end")
        password.delete(0, "end")
        username.insert(0, "Username*")
        username.config(fg="grey")
        password.insert(0, "password*")
        password.config(fg="grey")

def login():
    global r1
    r1 = Toplevel(root)
    r1.title("Login")
    r1.geometry("700x400")
    Label(r1, text="Login", font=("Helvetica", 16)).place(x=250, y=30)

    global username                                                       # login username
    username = Entry(r1)
    username.insert(0, "Username*")
    username.bind("<FocusIn>", username_click)
    username.bind("<FocusOut>", username_out)
    username.config(fg="grey")
    username.place(x=200, y=100, height=30, width=300)

    global password                                                        # login password
    password = Entry(r1)
    password.insert(0, "Password*")
    password.bind("<FocusIn>", password_click)
    password.bind("<FocusOut>", password_out)
    password.config(fg="grey")
    password.place(x=200, y=150, height=30, width=300)

    Button(r1, text="LOG IN", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=click_login).place(x=200, y=200, width=300, height=30)
    Label(r1, text="Don't have an account").place(x=200, y=300)
    Button(r1, text="Register", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=register).place(x=200, y=330, width=300, height=30)

def register():
    global r2
    r2 = Toplevel(root)
    r2.title("REGISTER")
    r2.geometry("700x700")
    Label(r2, text="Register", font=("Helvetica",16)).place(x=250, y=30)

    global name                                                       # name of user
    name = Entry(r2)
    name.insert(0, "Name")
    name.bind("<FocusIn>", name_click)
    name.bind("<FocusOut>", name_out)
    name.config(fg="grey")
    name.place(x=200, y=100, height=30, width=300)

    global address                                                          # login password
    address = Entry(r2)
    address.insert(0, "Address*")
    address.bind("<FocusIn>", address_click)
    address.bind("<FocusOut>", address_out)
    address.config(fg="grey")
    address.place(x=200, y=150, height=30, width=300)

    global phno                                                                 # phone number of user
    phno = Entry(r2)
    phno.insert(0, "Phone no.")
    phno.bind("<FocusIn>", phno_click)
    phno.bind("<FocusOut>", phno_out)
    phno.config(fg="grey")
    phno.place(x=200, y=200, height=30, width=300)

    global username
    username = Entry(r2)
    username.insert(0, "Username*")
    username.bind("<FocusIn>", username_click)
    username.bind("<FocusOut>", username_out)
    username.config(fg="grey")
    username.place(x=200, y=250, height=30, width=300)

    global password
    password = Entry(r2)
    password.insert(0, "Password*")
    password.bind("<FocusIn>", password_click)
    password.bind("<FocusOut>", password_out)
    password.config(fg="grey")
    password.place(x=200, y=300, height=30, width=300)

    Button(r2, text="Register", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=insert).place(x=200, y=350, width=300, height=30)


def address_click(event):
    if address.cget("fg") == "grey":
        address.delete(0, "end")
        address.insert(0, "")
        address.config(fg="black")


def phno_click(event):
    if phno.cget("fg") == "grey":
        phno.delete(0, "end")
        phno.insert(0, "")
        phno.config(fg="black")


def username_click(event):
    if username.cget("fg") == "grey":
        username.delete(0, "end")
        username.insert(0, "")
        username.config(fg="black")


def password_click(event):
    if password.cget("fg") == "grey":
        password.delete(0, "end")
        password.insert(0, "")
        password.config(fg="black")


def name_click(event):
    if name.cget("fg") == "grey":
        name.delete(0, "end")
        name.insert(0, "")
        name.config(fg="black")

# username


def username_out(event):
    if username.get() == "":
        username.insert(0, "Username*")
        username.config(fg="grey")


# password


def password_out(event):
    if password.get() == "":
        password.insert(0, "Password*")
        password.config(fg="grey")



def name_out(event):
    if name.get() == "":
        name.insert(0, "Name*")
        name.config(fg="grey")



def address_out(event):
    if address.get() == "":
        address.insert(0, "Address*")
        address.config(fg="grey")


def phno_out(event):
    if phno.get() == "":
        phno.insert(0, "Phone no.*")
        phno.config(fg="grey")



def update_timeText1():

    current = time.strftime("[%H:%M:%S]")
    timeText.configure(text=current)
    # Call the update_timeText() function after 1 second
    root.after(1000, update_timeText1)

root = Tk()
root.title("HEALTHCARE PORTAL")
root.geometry("1536x864")

c = Canvas(root, borderwidth=0, background="#ffffff")
f1 = Frame(c, background="#ffffff", height=2000, width=1536)
vsb = Scrollbar(root, orient="vertical", command=c.yview)
c.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
c.pack(fill="both", expand=True)
c.create_window((0, 0), window=f1, anchor="nw")
f1.bind("<Configure>", onFrameConfigure(c))

c.bind("<Left>", lambda event: c.xview_scroll(-1, "units"))
c.bind("<Right>", lambda event: c.xview_scroll( 1, "units"))
c.bind("<Up>", lambda event: c.yview_scroll(-1, "units"))
c.bind("<Down>", lambda event: c.yview_scroll( 1, "units"))
c.focus_set()
c.bind("<1>", lambda event: c.focus_set())

timeText = Label(f1, fg="green")
timeText.place(x=1200, y=120)

update_timeText1()

Label(f1, text=f"{dt.datetime.now():%d-%b-%Y    %a}", fg="green").place(x=1100, y=120)


log = Button(f1, text="Login", height=2, width=20, fg="red", command=login).place(y=50, x=1000)

reg = Button(f1, text="Register", height=2, width=20, command=register).place(y=50, x=1200)

logo_img = Image.open("healthcare_bot_icon.jpg")
logo_img = logo_img.resize((200,150),Image.ANTIALIAS)
logo_img = ImageTk.PhotoImage(logo_img)
lbl_logo = Label(f1, image=logo_img).place(x=20, y=10)

l1 = Label(f1, text="HealthCare Bot", fg="red", font=("Times New Roman",26)).place(x=250,y=60)

l2 = Label(f1, text='''
HealthCare Bot, a collaborative healthcare platform to help hospitals to provide healthcare support online 24 x 7, it answers deep as 
well as general questions. By asking the questions in series it helps patients by guiding what exactly he/she is looking for.
''', fg="grey", font=("Times New Roman",20)).place(x=20,y=640)

logo_img1 = Image.open("healthcare3.jpg")
logo_img1 = logo_img1.resize((1480,400),Image.ANTIALIAS)
logo_img1 = ImageTk.PhotoImage(logo_img1)
logo_img2 = Image.open("healthcare1.png")
logo_img2 = logo_img2.resize((1480,400),Image.ANTIALIAS)
logo_img2 = ImageTk.PhotoImage(logo_img2)
logo_img3 = Image.open("healthcare2.png")
logo_img3 = logo_img3.resize((1480,400),Image.ANTIALIAS)
logo_img3 = ImageTk.PhotoImage(logo_img3)
logo_img4 = Image.open("healthcare6.png")
logo_img4 = logo_img4.resize((1480,400),Image.ANTIALIAS)
logo_img4 = ImageTk.PhotoImage(logo_img4)
logo_img5 = Image.open("healthcare7.jpg")
logo_img5 = logo_img5.resize((1480,400),Image.ANTIALIAS)
logo_img5 = ImageTk.PhotoImage(logo_img5)
logo_img8 = Image.open("healthcare11.jpg")
logo_img8 = logo_img8.resize((1480,400),Image.ANTIALIAS)
logo_img8 = ImageTk.PhotoImage(logo_img8)
logo_img9 = Image.open("healthcare12.jpg")
logo_img9 = logo_img9.resize((1480,400),Image.ANTIALIAS)
logo_img9 = ImageTk.PhotoImage(logo_img9)
logo_img11 = Image.open("healthcare13.jpg")
logo_img11 = logo_img11.resize((1480,400),Image.ANTIALIAS)
logo_img11 = ImageTk.PhotoImage(logo_img11)

label_image = Label(f1,font="bold")
label_image.place(x=20,y=180)
x = 1


def move():
    global x
    if x==9:
        x=0
    elif x==1:
        label_image.config(image=logo_img1)
    elif x==2:
        label_image.config(image=logo_img2)
    elif x == 3:
        label_image.config(image=logo_img3)
    elif x == 4:
        label_image.config(image=logo_img4)
    elif x == 5:
        label_image.config(image=logo_img5)
    elif x == 6:
        label_image.config(image=logo_img8)
    elif x == 7:
        label_image.config(image=logo_img9)
    elif x==8:
        label_image.config(image=logo_img11)
    x += 1
    label_image.after(2000,move)
move()


l3 = Label(f1, text="PLATFORM", fg="red", font=("Times New Roman",26)).place(x=650,y=900)

doc_img = Image.open("doctor1.jpg")
doc_img = doc_img.resize((600,300),Image.ANTIALIAS)
doc_img = ImageTk.PhotoImage(doc_img)
Label(f1, image=doc_img).place(x=820, y=1050)


l4 = Label(f1, text="Healthcare Providers", fg="red", font=("Times New Roman",18)).place(x=300,y=1070)


l5 = Label(f1, text="-  Online Consultation", fg="gray", font=("Times New Roman",16)).place(x=350,y=1170)
l6 = Label(f1, text="-  Remote Monitoring", fg="gray", font=("Times New Roman",16)).place(x=350,y=1220)
l7 = Label(f1, text="-  Grow Your Business", fg="gray", font=("Times New Roman",16)).place(x=350,y=1270)


indi_img = Image.open("doctor2.jpg")
indi_img = indi_img.resize((600,300),Image.ANTIALIAS)
indi_img = ImageTk.PhotoImage(indi_img)
Label(f1, image=indi_img).place(x=180, y=1500)

l8 = Label(f1, text="INDIVIDUALS", fg="red", font=("Times New Roman",18)).place(x=950,y=1500)

l9 = Label(f1, text="-  Personalized Healthcare At Your Fingertip", fg="gray", font=("Times New Roman",16)).place(x=1000,y=1600)
l10 = Label(f1, text="-  Manage Health Anytime Anywhere", fg="gray", font=("Times New Roman",16)).place(x=1000,y=1650)
l11 = Label(f1, text="-  Quick Treatment To Disease By Specialist", fg="gray", font=("Times New Roman",16)).place(x=1000,y=1700)

root.mainloop()