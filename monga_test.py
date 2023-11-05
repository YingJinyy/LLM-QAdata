from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit.secret import Url
url = Url()
# Create a new client and connect to the server
client = MongoClient(url, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


#进入user数据库
mydb = client['user']
#print(mydb)


#查找所有人的信息
def get_all_userInfo():
    mycol = mydb['userInfo']    #进入数据库里的对应表
    for x in mycol.find():
        print(x)


#查找所有人的QA
def get_all_userQA():
    mycol = mydb['userQA']
    for x in mycol.find():
        print(x)

#查找特定人的信息
def get_userInfo(username='11111'):
    mycol = mydb['userInfo']
    for x in mycol.find({'name':username}):
        print(x)

#查找特定姓名的QA
def get_userQA(username):
    mycol = mydb['userQA']
    result = mycol.find({'name':username},{'_id':0})
    for x in result:
        print(x)

def get_chapter_QA(chapter_num):
    chaptername = 'chapter'+str(chapter_num)+'QA'
    mycol = mydb[chaptername]
    for x in mycol.find():
        print(x)


if __name__ == '__main__':
    print("获取所有人的信息：")
    get_all_userInfo()
    print("\n获取1111的信息：")
    get_userInfo('1111')

    print("\n获取所有人的QA：")
    get_all_userQA()
    print("\n获取1111的QA：")
    get_userQA('1111')

    print("\n获取第一章节的QA")
    get_chapter_QA(1)



