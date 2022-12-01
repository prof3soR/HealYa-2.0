import streamlit as st

def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")

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

from PIL import Image
img = Image.open('mind.png')
st.set_page_config(
    page_title="HealYa-login",
    page_icon=img
    )
import mysql.connector
mydb = mysql.connector.connect(
      host="bjcmnr2uzuxqqy10wqm4-mysql.services.clever-cloud.com",
      user="uivtvnwzwynrvnwz",
      password="FtCHQZ1jvztYvRVFQi1G",
      database="bjcmnr2uzuxqqy10wqm4"
    )
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.markdown("""

<style>


 .css-163ttbj {
        display: none;
    }

</style>

""", unsafe_allow_html=True)






def login(uid):
    mycursor = mydb.cursor()
    mycursor.execute("select password from accounts where user_id={};".format(uid))
    myresult = mycursor.fetchall()
    valid=myresult
    
    if len(valid)==0:
        st.write("Invalid login")
    else:
        if pas==valid[0][-1]:
            st.write("success")
            if 'user_id' not in st.session_state:
                st.session_state['user_id'] = uid
            switch_page("app")
            
            
        else:
            st.write("Wrong password!")
    mydb.close()


mycursor = mydb.cursor()
mycursor.execute("select User_id from accounts;")
myresult = mycursor.fetchall()
new_id=myresult[-1][0]+1

col1,col2=st.columns((0.7,2))
with col1:
    st.write("")
with col2:
    st.title('Welcome to HealYa')



tab1,tab2= st.tabs(['Sign-up','Login'])

with tab1:
    col1,col2,col3=st.columns((1,2,1))
    with col1:
        st.write("")
    with col2:                  
        st.subheader("Create your account here!!")
        st.subheader("Your User id is:"+' '+str(new_id))
        pas=st.text_input("Create Password",placeholder="Enter your password")
        pas_con=st.text_input("Confirm your Password",placeholder="Enter your password")
        
        if st.button("  Create account  "):
            if pas!=pas_con:
                st.write("Password did not match ")
            else:
                try:
                    sql= "INSERT INTO accounts(User_id,password) VALUES (%s,%s);"
                    val=(new_id,pas)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.write("Account created successfully!")
                except:
                    mydb.rollback()
                    st.write("Failed!")
    with col3:
        st.write("")
with tab2:
    col1,col2,col3=st.columns((1,2,1))
    with col1:
        st.write("")
    with col2:
        st.subheader("Already a member login here!!")
        uid=st.text_input("User Id",placeholder="Enter Your user id (Ex:1)")
        pas=st.text_input("Password",placeholder="Password")
        if st.button("Log in"):
            login(uid)
    with col3:
        st.write("")


mydb.close()
st.write("* Please remember your UserId and password since we do not collect any user data like phone number or email we cannot recover password if lost")
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1595113316349-9fa4eb24f884?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1772&q=80");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

