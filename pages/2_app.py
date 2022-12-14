###HEALYA CHATBOT PROGRAM 
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')
from nltk.stem import WordNetLemmatizer
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#nltk.download('popular')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
f=open('chatbot data.txt','r',errors='ignore')
raw=f.read()
raw=raw.lower()
sent_tokens=nltk.sent_tokenize(raw)
word_tokens=nltk.word_tokenize(raw)
Lemmer=nltk.stem.WordNetLemmatizer()
def LenTokens(tokens):
  return [Lemmer.lemmatize(token) for token in tokens]
remove_punct_dict=dict((ord(punct),None) for punct in string.punctuation)
def LemNormalize(text):
  return LenTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
def response(user_response):
  robo_response=''
  sent_tokens.append(user_response)
  TfidVec=TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
  tfidf=TfidVec.fit_transform(sent_tokens)
  vals=cosine_similarity(tfidf[-1],tfidf)
  idx=vals.argsort()[0][-2]
  flat=vals.flatten()
  flat.sort()
  req_tfidf=flat[-2]
  if req_tfidf==0:
    robo_response=robo_response+"Sorry! HealYa bot couldn't comprehend your conffesion our team will get back to you with personal solution in less than an hour kindly check your solutions sections! Thank you"
    return robo_response
  else:
     robo_response=robo_response+sent_tokens[idx]
     return robo_response

###USER INTERFACE PROGRAM 
import streamlit as st
from PIL import Image
from datetime import datetime
img = Image.open('mind.png')
st.set_page_config(
    page_title="HealYa Account",
    page_icon=img
    )
def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")
user_id=st.session_state['user_id']

st.write("Welcome! It's great to have you here today!",user_id)

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""

<style>


 .css-1vencpc {
        display: none;
    }
 .css-163ttbj {
        display: none;
    }

</style>

""", unsafe_allow_html=True)

import mysql.connector
mydb = mysql.connector.connect(
      host="bjcmnr2uzuxqqy10wqm4-mysql.services.clever-cloud.com",
      user="uivtvnwzwynrvnwz",
      password="FtCHQZ1jvztYvRVFQi1G",
      database="bjcmnr2uzuxqqy10wqm4"
    )


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")
col1, col2,col3 = st.columns([1,2,1])

with col1:
    st.image('mind.png',width=100)

with col2:
    st.write("Thank you for joining HealYa",anchor=None)
with col3:
    if st.button("Log out!"):
        switch_page("account")
def fetch_confessions(user_id):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("select con from confession where user_id={};".format(user_id))
        con = mycursor.fetchall()
        if len(con)==0:
            st.write("No confession records found!")
        else:
           for i in range(len(con)):
               st.write("confession - ",i+1,": ",con[i][0])
               
    except:
        mydb.rollback()
        st.write("There is a problem in database connection!")
    mydb.close()
def fetch_solutions(user_id):
    mycursor = mydb.cursor()
    mycursor.execute("select sol from solution where user_id={};".format(user_id))
    sol = mycursor.fetchall()
    if len(sol)==0:
        st.write("No confession records found!")
        st.subheader("Please check back again after an hour if have subbmited a new confession just now")
    else:
        for i in sol[0]:
            st.write(i)




def insert(confession):
    mycursor = mydb.cursor()
    mycursor.execute("select cid from confession;")
    myresult = mycursor.fetchall()
    new_id=myresult[-1][0]+1
    now = datetime.now()
    sql = "INSERT INTO confession(cid,user_id,con,DndT) VALUES (%s,%s,%s,%s);"
    val=(new_id,user_id,confession,now)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        st.write("SUCCESS!")
    except:
        mydb.rollback()
        st.write("Failed!")
    mydb.close()
    
tab1,tab2,tab3= st.tabs(['Take test','Confessions','Solutions'])
with tab1:
    st.write("This is HealYa's confession page")
    st.write("This is a safe and secure place for to take a mental heath status test and talk about it and help us help you get the best mental health care you deserve!")
    st.subheader("Take the test below to know you mental health status")
    st.write("Please answer the question keeping past two weeks of activity of your life to patiently answer the qustions so that we can give you a better assesment")
    st.write("On scale of 1 to 5 please select what you felt based on the question...")
    Q1= st.radio("Being so restless that it is hard to sit still",(1,2,3,4,5),horizontal=True)
    Q2= st.radio("Becoming easily annoyed or irritable",(1,2,3,4,5),horizontal=True)
    Q3= st.radio("Feeling bad about yourself - or that you are a failure or have let yourself or your family down",(1,2,3,4,5),horizontal=True)
    Q4= st.radio("Thoughts that you would be better off dead, or of hurting yourself and Little interest or pleasure in doing things ",(1,2,3,4,5),horizontal=True)
    Q5= st.radio("I find it difficult to get a hold of my thoughts",(1,2,3,4,5),horizontal=True)
    Q6= st.radio("Felt guilty or unable to stop blaming yourself or others for the event(s) or any problems the event(s) may have caused?",(1,2,3,4,5),horizontal=True)
    Q7= st.radio("Tried hard not to think about the event(s) or went out of your way to avoid situations that reminded you of the event(s)?",(1,2,3,4,5),horizontal=True)
    Q8= st.radio("Felt numb or detached from people, activities, or your surroundings?",(1,2,3,4,5),horizontal=True)
    Q9= st.radio("Can't stop overthinking and ruining even good things happening",(1,2,3,4,5),horizontal=True)
    Q10= st.radio("Others don't believe me when I tell them the things I see or hear",(1,2,3,4,5),horizontal=True)
                    

    def get_score(x):
        if x<=10:
            st.write("You have a Excellent state of mental health")
        elif x<=15:
            st.write("You have a Good state of mental health")
        elif x<=30:
            st.write("Your Mental health state is Average please let us help you!")
        elif x<=40:
            st.write("Your Mental health state is Below Average please let us help you!")
        else:
            st.write("You have a bad state of mental health please let us help you!")

    score=0
    score=Q1+Q2+Q3+Q4+Q5+Q6+Q7+Q8+Q9+Q10
                
    if st.button("Get score",type="primary"):
        get_score(score)

with tab2:
    tab1,tab2=st.tabs(["new confession","show old confessions"])
    with tab1:
        st.text("We want you to know that we care about you and your well-being, and we want to help you get through whatever is bothering you right now. If there's anything we can do, just let us know.")
        st.text("You don't have to tell us what's wrong; we just need to know how much it's affecting your life and how much of an impact it has on your moods.")
        st.text("You can tell us anything about yourself or any personal life at all, and we will not reveal anything about you.We want to help!")
        confession=st.text_area("Confession box",placeholder="You can confess your feeling here (completely anonymous)",height=1)
        if st.button("submit"):
            st.header("This is a HealYa bot generated quick solution ")
            st.write(response(confession))
            st.suheader("The solution generated by the HealYa bot may or may not be acurate so please wait for the real solution which you can check in the solution section of the application")
            insert(confession)
    with tab2:
        if st.button("Get confession "):
            fetch_confessions(user_id)
        
with tab3:
    st.header("Solutions")
    if st.button("Get solutons"):
        fetch_solutions(user_id)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1573055418049-c8e0b7e3403b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8ODh8fGhhcHB5JTIwcGVyc29ufGVufDB8MHwwfHdoaXRlfA%3D%3D&auto=format&fit=crop&w=800&q=60");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#add_bg_from_url() 

        
