import pickle
import streamlit as st
from PIL import Image, ImageOps
from classifier import image_classification
import matplotlib.pyplot as plt
import numpy as np

import streamlit_authenticator as stauth # pip install streamlit_authenticator
from pathlib import Path

# import sqlite3
# conn = sqlite3.connect('data.db', check_same_thread=False)
# cur = conn.cursor()

import pandas as pd


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


# loading the trained model
st.set_option('deprecation.showfileUploaderEncoding', False)
html_temp = """
    <div style ="background-image: url("https://www.jigsawstore.com.au/assets/full/RB15633-7.jpg?20200726170018"); background-repeat: no-repeat; background-attachment: fixed; background-size: 100% 100%;} body::before{content: ""; position: absolute; top: 0px; right: 0px; bottom: 0px; left: 0px; background-color: rgba(1,2,1,0.80);">
    <div style ="background-color:tomato;padding:13px"> 
    <h1 style ="font-family:verdana;color:white;text-align:center;">PREDICTION DE RACE DE CHIEN</h1> 
    </div> 
    """
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True)
# st.markdown('<style>body{background-image: url("https://www.jigsawstore.com.au/assets/full/RB15633-7.jpg?20200726170018"); background-repeat: no-repeat; background-attachment: fixed; background-size: 100% 100%;} body::before{content: ""; position: absolute; top: 0px; right: 0px; bottom: 0px; left: 0px; background-color: rgba(1,2,1,0.80);}</style>',unsafe_allow_html=True)
# st.markdown('<style>body{color: tomato; text-align: center;}</style>',unsafe_allow_html=True)
# st.markdown()


st.header("Téléchargez une image d'un chien pour identifier sa race :chien:")

st.write("")
st.write("")
st.write("")
st.write("")
st.subheader("Choisissez une image de chien... :chien:")

# AND in st.sidebar!
with st.sidebar:
      if st.button("À propos"):
          st.write("Visit [Github](https://github.com/catri-01) !!")
          st.text("By Chancy Maouene")

      elif st.button("Login"):
           st.subheader("Login Section")

           username = username = st.sidebar.text_input("User Name")
           password = st.sidebar.text_input("Password",type='password')
           if st.sidebar.checkbox("Login"):
                create_usertable()
                hashed_pswd = make_hashes(password)

                result = login_user(username,check_hashes(password,hashed_pswd))
                if result: 
                      st.success("Logged In as {}".format(username))

                    #   task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
                    #   if task == "Add Post":
                    #         st.subheader("Add Your Post")
                    
                    #   elif task == "Analytics":
                    #         st.subheader("Analytics")
                    #   elif task == "Profiles":
                    #         st.subheader("Profiles")
                    #         user_result = view_all_users()
                    #         clean_db =pd.DataFrame(user_result,columns=["Username","Password"])
                    #         st.dataframe(clean_db)

                else:
                      st.warning("Incorrect Username/Password")

    
      elif st.button("SignUp"):
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')

            if st.button("Signup"):
                  create_usertable()
                  add_userdata(new_user, make_hashes(new_password))
                  st.success("You have successfully created a valid Account")
                  st.info("Go to login Menu to login")


    #   if st.button("Connexion"):
    #       names = ["Peter Parker", "Rebecca Miller"]
    #       usernames = ["pparker", "rmiller"]
    #       passwords = ["XXX", "XXX"]

    #       hashed_passwords = stauth.Hasher(passwords).generate()

    #       file_path = Path(__file__).parent / "hashed_pw.pkl"
    #       with file_path.open("wb") as file:
    #         pickle.dump(hashed_passwords, file)

    #   if st.button("Connexion"):
    #       def form():
    #             st.write("This is a form")
    #             with st.form(key="Information form"):
    #                 name = st.text_input("Enter you name : ")
    #                 age = st.text_input("Enter age : ")
    #                 clg_name = st.text_input("Enter your college name: ")
    #                 date = st.date_input("Enter the data: ")
    #                 submission = st.form_submit_button(label="Submit")
    #                 if submission == True:
    #                     addData(name, age, clg_name, date)
                        
    #       def addData(a,b,c,d):
    #             cur.execute("""CREATE TABLE IF NOT EXISTS clg_form(NAME TEXT(50), AGE TEXT(50), CLGNAME TEXT(60),DATE TEXT(50));""")
    #             cur.execute("INSERT INTO clg_form VALUE (?, ?, ?, ?)", (a,b,c,d))
    #             conn.commit()
    #             conn.close()
    #             st.success("Successfully submitted")
    #       form()

# AND in st.sidebar!
# with st.sidebar:
#       if st.button("Connexion"):
#           st.write("")
#           st.text("")
            
uploaded_file = st.file_uploader("", type=["jpg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image téléchargée.', use_column_width=True)
    st.write("")
    with st.spinner('Identification...'):
        label = image_classification(image,"20230516-22551684277709-full-image-set-mobilenetv2-Adam.h5")

    btn = st.button("Voir les résultats!!")
    if btn :
      st.info(label)
      st.balloons()

