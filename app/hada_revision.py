from random import randrange
import stat
import time
from fastapi import FastAPI, HTTPException, Response, status

# hadi bach n9dro ndiro extraction l data li dakhal body
from fastapi.params import Body

# pydantic is a data validation and settings management library for Python
from pydantic import BaseModel

# optional bch t9dr tsta3ml type dyal data li rah ykon optional
from typing import Optional

# psycopg2 bch na9adro nahadro m3a database mn python
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import Engine
from . import models
from .database import session_local, engine, Base


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# doka 9lk kyn whd dependency lazam nakatboha hia l responssable to talk with data base
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# hadi bch exiger type dyal data li rah fl body
# hadik true default value hata lokn mata3tilhach value true
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


# dok rah ndiro la connection m3a database
while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Oussama.123@github",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("database was successfully connected")
        break
    except Exception as Error:
        print("connection to database failed")
        print(f"Error : {Error}")
        time.sleep(2)


""" my_post = [{"id": 1,"title" : "title 1", "content" : "content 1"},{"id" : 2,   "title" : "title 2", "content" : "content 2"}]
 """

""" @app.get("/")
def get_request():
    return {"message": "Hello, World!"} """

""" @app.get("/posts")
def get_post():
    return {"posts": my_post} """


# fi hadih lhala malgre path kif kif mais yafichi lawl
""" @app.get("/")
def get():
    return {"post": "there's your post"} """

# we know that just the type of post or put or patch which we can store in the body and we will see how to extract data from the body
# METHOD ONE body content stored inside a variable called var
""" @app.post("/createpost")
def create_post(var: dict = Body(...)):
    print(var)
    return {"message": f"title is {var["title"]} and content is {var["content"]}"} """

# METHOD TWO EXTRACT DATA FROM BODY WITH PYDANTIC MODEL
# hna remarqina bli ki drna extract l data li raha dakhal l body ki ndiro print liha matakhrajch dictinaries i mala fi haalat hna nsha9oha dictionaries nzido dict()
""" @app.post("/createpost")
def create_post0(post: Post):
    print(post.dict())
    print(post.title)
    return {"message": post} """


# rana nsayo nzido 3fays bch nt3almo
""" @app.post("/createpost1" , status_code= status.HTTP_201_CREATED)
def create_post1(post: Post):
   post_dict = post.dict()
   post_dict["id"] = randrange(0, 1000000)
   my_post.append(post_dict)
   return {"message": post_dict} """

# hna hadi function rah nasta3mloha bch n3awana njbdo data li rana nhwso 3lih
""" def find_post(id : int):
    for p in my_post:
        if p["id"] == id:
            return p """


# how to get a post bi an id
# hna rah ndirou l id dyal post li bghina njbdouh
# hna dok rak nzido response bch nthakmo f http code
""" @app.get("/posts/{id}")
def get_post_by_id(id : int , response : Response):
    post = find_post(id)
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}
    return {"post": post} """


# hadi nfsha li fo9ha mais rah nasta3mlo HTTPExeption fi plast status
""" @app.get("/posts/{id}")
def get_post_by_id(id : int ):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return {"post": post} """


# hadi function zyada how to get the latest post
# o hada latest mhbch ymchi psQ raho yassana int valeu mor /posts tsma kili rah ykhdm b tartib
""" @app.get("/posts/latest")
def get_latest_post():
    post = my_post[-1]
    return {"post": post} """


# hna i rah fa9at index t3 p , p howa item t3 list
# hadi function rah t3awana bch nasta3mlou delete
""" def fin_index_post(id : int):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i
    return None """


# dok hna ki drna status code 204 return lakhrani li drnah mawalach ymchi li hada lazm ndakhlo response
""" @app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = fin_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    else:
        my_post.pop(index)
        print(my_post)
        #return {"message": f"post with id {id} was deleted successfully"} 
        return Response(status_code=status.HTTP_204_NO_CONTENT) """


# bi nisba ll base model n9dro nst3mlo la class post n9dro nhalo wakhdokhra
""" @app.put("/posts/{id}")
def update_post(id : int , post: Post):
    index = fin_index_post(id)
    if index is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    else:
        post_dict = post.dict()
        post_dict["id"] = id #hdi psq id madiklarinahch f base model m3nah mkch id dakhal body
        my_post[index] = post_dict
        print(my_post)
        return {"message": f"post with id {id} was updated successfully"} """


# |||| now i will start another http requests with database using cursor ||||
# hadi kifh tmodifyi f data base ta3k bla matadkhol ll pg admin


# for get request
@app.get("/posts")
def get_posts():
    # posts = cursor.execute("""SELECT * FROM post""")
    # chikh 9lk bli ki tkhazan lwla fi variable marah ta3tik wallo lazm tzid l fetch
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there's no data in the database",
        )
    else:
        return posts


# for post request
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    # without connection.commit() the data will not be saved in the database
    connection.commit()  # Commit the transaction
    return new_post


# for get request by id
@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute(
        """SELECT * FROM post WHERE id = %s""", (id,)
    )  # 3lblna bli id lazm tkon str bch manakatboch str(id) drna (id,) moraha kama , meme result
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return post


# for delete request by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    connection.commit()


# for update request by id
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, (id,)),
    )
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    connection.commit()
    return updated_post


""" رسالة الخطأ "Depends" is not defined تظهر غالبًا في إطار استخدام مكتبة FastAPI، وتحديدًا عند محاولة استخدام التابع Depends بدون استيراده أولاً.

✅ الحل:
يجب أن تقوم باستيراد Depends من مكتبة fastapi كما يلي:


from fastapi import Depends
📌 مثال عملي:
إذا كنت تكتب كودًا لإنشاء مسار (endpoint) يستخدم Depends لحقن تبعية (dependency)، مثل الاعتماد على دالة تحقق من المستخدم:


from fastapi import FastAPI, Depends

app = FastAPI()

def verify_user():
    # تحقق وهمي مثلاً
    return "user verified"

@app.get("/items/")
def read_items(user=Depends(verify_user)):
    return {"message": f"{user}"}
إذا نسيت كتابة from fastapi import Depends، فسيظهر لك الخطأ "Depends" is not defined.

❗ ملاحظة:
تأكد أيضًا أنك تستورد أي تبعيات أخرى ضرورية، مثل FastAPI, HTTPException, status, إلخ، حسب استخدامك.

إذا أردت أن أراجع الكود الذي ظهرت فيه هذه الرسالة، أرسله لي وسأساعدك خطوة بخطوة إن شاء الله. """
