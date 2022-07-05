import os
import psycopg2
import re
from datetime import datetime
from flask import Flask, json, render_template, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
# import uuid
import jwt
import datetime


app = Flask(__name__)

app.config['SECRET_KEY']='CnGL4xvdKlWPcQP51ZnovHr-fA0'
app.config['JSON_SORT_KEYS'] = False
# cloudinary = new Cloudinary(ObjectUtils.asMap("cloud_name", "di4wu7js0", "api_key", "252375724828993",
#                 "api_secret", "CnGL4xvdKlWPcQP51ZnovHr-fA0", "secure", true));

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='fooddb',
                            user='postgres',
                            password='password')
    return conn

  # 404
  #  400
  #  403

whitelistIP="http://localhost:4200"

def home():
    date = datetime.now()
    return str(date)

@app.route('/api/v1/product/highlight')
def productHighlight():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT  product.id_product,product.image_url,product.calories,product.description,product.discount_point,product.duration,product.highlight,product.name,product.price,product.status,product.id_category,category.id_category,category.image_url,category.name,category.status FROM product JOIN category on product.id_category=category.id_category where highlight>0 order by highlight asc;')
    opt = cur.fetchall()
    container={}
    products={}
    keydata={}
    Results=[]
    for entry in opt:
      Result={}
      categorydetails={}
      Result['idProduct']=entry[0]
      Result['name']=entry[7]
      Result['calories']=entry[2]
      Result['description']=entry[3]
      Result['price']=entry[8]
      Result['duration']=entry[5]
      Result['discountPoint']=entry[4]
      Result['highlight']=entry[6]
      if entry[9] == 1:
       Result['status']=str(entry[9]).replace("1", "ACTIVE")
      elif entry[9] == 0:
       Result['status']=str(entry[9]).replace("0", "INACTIVE")
      else:
       Result['status']="UNKNOWN"
      Result['imageUrl']=entry[1]
      categorydetails['idCategory']=entry[11]
      categorydetails['name']=entry[13]
      categorydetails['imageUrl']=entry[12]
      if entry[14] == 1:
       categorydetails['status']=str(entry[14]).replace("1", "ACTIVE")
      elif entry[14] == 0:
       categorydetails['status']=str(entry[14]).replace("0", "INACTIVE")
      else:
       categorydetails['status']="UNKNOWN"
      Result['category']=categorydetails
      Results.append(Result)
    products['products']=Results
    #keydata['data']=products
    container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container['statusCode']=200
    container['status']='OK'
    container['message']='Products highlight'
    container['data']=products
    # test1=container
    # print (container)
    resreturn=app.response_class(
    response=json.dumps(container),
    mimetype='application/json'
    )    
    resreturn.headers.add('Access-Control-Allow-Origin', whitelistIP)
    return resreturn
    #return jsonify(container)
    cur.close()
    conn.close()

@app.route('/api/v1/category/list')
def categoryList():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT  category.id_category,category.image_url,category.name,category.status FROM category  order by category.id_category asc;')
    opt = cur.fetchall()
    container={}
    products={}
    keydata={}
    Results=[]
    for entry in opt:
      categorylistdetails={}
      categorylistdetails['idCategory']=entry[0]
      categorylistdetails['name']=entry[2]
      categorylistdetails['imageUrl']=entry[1]
      if entry[3] == 1:
       categorylistdetails['status']=str(entry[3]).replace("1", "ACTIVE")
      elif entry[3] == 0:
       categorylistdetails['status']=str(entry[3]).replace("0", "INACTIVE")
      else:
       categorylistdetails['status']="UNKNOWN"
      Results.append(categorylistdetails)
    products['products']=Results
    container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container['statusCode']=200
    container['status']='OK'
    container['message']='Products list'
    container['data']=products
    resreturn=app.response_class(
    response=json.dumps(container),
    mimetype='application/json'
    )    
    resreturn.headers.add('Access-Control-Allow-Origin', whitelistIP)
    return resreturn
    cur.close()
    conn.close()

@app.route('/api/v1/product/category/<foodcategory>')
def productCategorybyName(foodcategory):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT  product.id_product,product.image_url,product.calories,product.description,product.discount_point,product.duration,product.highlight,product.name,product.price,product.status,product.id_category,category.id_category,category.image_url,category.name,category.status FROM product JOIN category on product.id_category=category.id_category where category.name=%s;",[foodcategory])
    opt = cur.fetchall()
    container={}
    products={}
    keydata={}
    Results=[]
    for entry in opt:
      Result={}
      categorydetails={}
      Result['idProduct']=entry[0]
      Result['name']=entry[7]
      Result['calories']=entry[2]
      Result['description']=entry[3]
      Result['price']=entry[8]
      Result['duration']=entry[5]
      Result['discountPoint']=entry[4]
      Result['highlight']=entry[6]
      if entry[9] == 1:
       Result['status']=str(entry[9]).replace("1", "ACTIVE")
      elif entry[9] == 0:
       Result['status']=str(entry[9]).replace("0", "INACTIVE")
      else:
       Result['status']="UNKNOWN"
      Result['imageUrl']=entry[1]
      categorydetails['idCategory']=entry[11]
      categorydetails['name']=entry[13]
      categorydetails['imageUrl']=entry[12]
      if entry[14] == 1:
       categorydetails['status']=str(entry[14]).replace("1", "ACTIVE")
      elif entry[14] == 0:
       categorydetails['status']=str(entry[14]).replace("0", "INACTIVE")
      else:
       categorydetails['status']="UNKNOWN"
      Result['category']=categorydetails
      Results.append(Result)
    products['products']=Results
    #keydata['data']=products
    container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container['statusCode']=200
    container['status']='OK'
    container['message']='Products category with name'
    container['data']=products
    resreturn=app.response_class(
    response=json.dumps(container),
    mimetype='application/json'
    )    
    resreturn.headers.add('Access-Control-Allow-Origin', whitelistIP)
    return resreturn
    #return jsonify(container)
    cur.close()
    conn.close()

@app.route('/api/v1/user/is-valid-username/<usrname>')
def verifyCustomerName(usrname):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username from user_app where username=%s;",[usrname])
    opt = cur.fetchone()
    container={}
    products={}
    keydata={}
    Result={}
    if opt == None:
        container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        container['statusCode']='400'
        container['status']='BAD_REQUEST'
        container['message']='The user called does not exist'
    else:
        Result['username']=opt[0]
        # for entry in opt:
        #   Result={}
        #   Result['username']=entry[0]
        products['User']=Result
        container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        container['statusCode']=200
        container['status']='OK'
        container['message']='get username'
        container['data']=products
    resreturn=app.response_class(
    response=json.dumps(container),
    mimetype='application/json'
    )    
    resreturn.headers.add('Access-Control-Allow-Origin', whitelistIP)
    return resreturn
    cur.close()
    conn.close()


@app.route('/api/v1/user/is-valid-email/<email>')
def verifyCustomereMail(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT email from user_app where email=%s;",[email])
    opt = cur.fetchone()
    container={}
    products={}
    keydata={}
    Result={}
    print (opt)
    if opt == None:
        container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        container['statusCode']='400'
        container['status']='BAD_REQUEST'
        container['message']='The User with mail does not exist'
    else:
        Result['email']=opt[0]
        # for entry in opt:
        #   print (entry[0])
        #   Result['email']=entry[0]
        products['User']=Result
        container['timeStamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        container['statusCode']=200
        container['status']='OK'
        container['message']='Get user by email'
        container['data']=products
    resreturn=app.response_class(
    response=json.dumps(container),
    mimetype='application/json'
    )    
    resreturn.headers.add('Access-Control-Allow-Origin', whitelistIP)
    return resreturn
    cur.close()
    conn.close()

    
@app.route('/api/v1/login', methods=['POST'])                          
def login():
    conn = get_db_connection()
    cur = conn.cursor()
    content_type = request.headers.get('Content-Type')
    # if (content_type == 'multipart/form-data'):
    if 1 == 1:
        formData = dict(request.form)
        userEmail = formData["username"]
        userpassword = formData["password"]
        print(userpassword)
        print(content_type)
        cur.execute("""SELECT username,password FROM user_app WHERE username=%s;""",[userEmail])
        opt = cur.fetchone()
        print ()
        is_correct_password= check_password_hash(opt[1],userpassword)
        print(is_correct_password)


    #     rv = cur.fetchall()
    #     for entry in rv:
    #         Result={}
    #         Result['userId']=entry[0]
    #         Result['userName']=entry[4]
    #         Result['userEmail']=entry[3]
    #         Result['userPassword']=entry[5]
    #         Result['userPhoneNumber']=entry[6]
    #         Result['userAge']=entry[2]
    #         Result['imgSrc']=entry[1]
    #         response=Result
    #     return jsonify(response)
        return jsonify(opt)
    else:
        return 'Request not valid!'
    #return resreturn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='443')
