import streamlit as st
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@st.cache_resource
def init_connection():
    uri = st.secrets["mongo"]['uri']
    print(uri)
    return MongoClient(uri,server_api=ServerApi('1'))

client = init_connection()
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

mydb = client['user']
userQA = mydb['userQA']
@st.cache_data(ttl=60)
def get_data():
    userInfo = mydb['userInfo'].find()
    users = [x['ID'] for x in list(userInfo)]  # make hashable for st.cache_data
    return users

users = get_data()

st.header('QA数据采集')
if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = True
    st.session_state.collect = False

if "original" not in st.session_state:
    st.session_state.original = True

def click_collect():
    st.session_state.collect = True

def click_reset():
    st.session_state.original = False

def submit_collect():
    st.session_state.submit = True

@st.cache_data
def load_data(url):
    uuid_shelter = pd.read_csv(url)
    return uuid_shelter

# uuid_shelter = ['1234567', '2345678']
# uuid_shelter = load_data()

# 建立用户id输入框
def reset_user():
    st.write("🎈请输入您的:orange[**ID**]")

    col1, col2 = st.columns([3,1])

    with col1:
        uuid = st.text_input("🎈请输入您的:orange[**ID**]",
                            placeholder="ID:",
                            key="uuid",
                            label_visibility="collapsed").strip()
    with col2:
        st.button('确认', on_click=click_collect,type="primary",use_container_width=True)
    return uuid


# st.write(" ")
uuid = reset_user()
# st.write(uuid)
# if st.session_state.userInfo.find({"ID":uuid}) is None:
#     print("true123")

# 用户id不存在时的情况
def unaviable_id():
    st.write(':orange[ID不存在, 请重新输入!]')
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = True

def unaviable_chapter():
    st.write(':orange[请选择对应章节!]')
    # st.session_state.visibility = "collapsed"
    # st.session_state.disabled = True


# 用户id存在时的情况
def in_uid(uuid):
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.original = False
    st.session_state.submit = False
    st.subheader("_{}, 下面开始开始采集_".format(uuid))
    option = st.selectbox(
    ':orange[请选择对应章节:]',
    ('None', 'chapter1', 'chapter2', 'chapter3', 'chapter4', 'chapter5'))
    

# st.write('You selected:', option)

    prompt = st.text_area("请输入prompt👇",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="prompt:",
                max_chars=4096,
                )
    response = st.text_area("请输入response👇",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="response:",
                max_chars=4096,
                )
    col3, col4 = st.columns(2)
    with col3:
        mit = st.form_submit_button('提交', on_click=submit_collect, type="primary", use_container_width=True)
        print(mit)
    with col4:
        re = st.form_submit_button('重置', use_container_width=True)
        print(re)
    return prompt, response, mit, re, option

def submit(uuid):
        # st.write(uuid, prompt, response)
    col3, col4 = st.columns(2)

    with col3:
        st.button('提交', type="primary", use_container_width=True, on_click=in_uid(uuid))

    with col4:
        st.button('重置', use_container_width=True)

def sucess_submit():
    st.write(':red[提交成功！]')

prompt = ""
response = ""
fileName = "c.txt"
if st.session_state.collect:
    if uuid not in users:
    # if uuid not in uuid_shelter:
        unaviable_id()
    else:
        
        with st.form(uuid,clear_on_submit=True):
            prompt, response, mit, re, option = in_uid(uuid)
            if mit:
                if option == 'None':
                    unaviable_chapter()
                else:
                    print('begin collect')
                    # with open(fileName,'w',encoding='utf-8')as file:
                    print(option+'QA')
                    chapter_coll = mydb[option+'QA']
                    u_QA = {'ID':uuid, 'prompt':prompt, 'response':response}
                    cha_QA = {'prompt':prompt, 'response':response}
                    userQA.insert_one(u_QA)
                    result = chapter_coll.insert_one(cha_QA)
                        # file.write(uuid)
                        # file.write(response)
                    sucess_submit()
                


# st.write(uuid, prompt, response)
