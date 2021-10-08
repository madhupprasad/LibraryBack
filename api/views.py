from datetime import timedelta
from collections import Counter, defaultdict
from flask import Blueprint, json, jsonify, request
from libgen_api import LibgenSearch
from .db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,
)


main = Blueprint('main', __name__)


@main.route('/python/addBook' , methods=['POST'])
def addBook():
    data = request.get_json()
    res = db.users.update_one(
        {"username" : data['userName']},
        { "$addToSet": {"data"  : data["item"]}}
    )
    if res.modified_count == 1:
        return jsonify({"msg":"Added"}), 200
    else:
        return jsonify({"msg":"It's already available in ur list"}), 200


@main.route('/python/removeBook' , methods=['POST'])
def removeBook():
    data = request.get_json()
    res = db.users.update_one(
        {"username" : data['userName']},
        { "$pull": {"data"  : { "ID" : data["item"]["ID"]}}}
    )
    current_books = db.users.find_one({"username":data['userName']},{"_id":1, "username":1, "password" : 1, "data": 1})
    return jsonify({"msg":"Removed" , "data":current_books["data"]}), 200


@main.route('/python/getUserBooks' , methods=['POST'])
def getBooks():
    userName = request.get_json()
    try:
        retValue = db.users.find_one({"username":userName},{"_id":1, "username":1, "password" : 1, "data": 1})
    except:
        return jsonify([]), 200

    if retValue:
        return jsonify(retValue["data"]), 200

@main.route('/python/search/bookname', methods=['GET'])
def bybook():
    name = request.args.get('bookname')
    if name:
        s = LibgenSearch()
        books = s.search_title(name)
        return jsonify({"books":books})
    
@main.route('/python/search/authorname', methods=['GET'])
def byauthor():
    name = request.args.get('authorname')
    if name:
        s = LibgenSearch()
        books = s.search_author(name)
        return jsonify({"books":books})


@main.route('/python/getlink', methods=['POST'])
def getDlink():
    args = request.get_json()
    if args:
        s = LibgenSearch()
        links = s.resolve_download_links(args)
        return jsonify({"links" : links})


@main.route('/python/login', methods=['POST'])
def login():
    creds = request.get_json()
    retValue = db.users.find_one({"username":creds['username']},{"_id":1, "username":1, "password" : 1})
    if retValue:
        if retValue["password"] == creds["password"]:
            access_token = create_access_token(identity=creds['username'])
            return jsonify(access_token=access_token)
        else:
            return jsonify({"msg" : "Password Incorrect"}), 401

    return jsonify({"msg" : "Username Not found"}), 401


@main.route('/python/signup', methods=['POST'])
def signup():
    creds = request.get_json()
    creds["data"] = []
    try:
        db.users.insert_one(creds)
    except:
        return jsonify({"msg" : "Looks like there is another " + creds['username']}), 409
    
    access_token = create_access_token(identity=creds['username'])
    return jsonify(access_token=access_token)

@main.route("/python/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(current_user)

@main.route("/python/getAllLikedBooks", methods=["GET"])
def getAllLikedBooks():
    retValue = list(db.users.find({},{"_id":1, "username":1, "password" : 1, "data" : 1}))
    t = []
    id_dict = {}
    d = {}
    for doc in retValue:
        for books in doc["data"]:
            curr_id = books['ID']
            if curr_id in id_dict:
                id_dict[curr_id]+=1
                d[curr_id]["count"]=id_dict[curr_id]
            else:
                id_dict[curr_id] = 1
                d[books['ID']] =  { "title" : books['Title'], "count" : id_dict[curr_id] }

    ret = list(d.values())

    ret.sort(key=lambda e : e['count'], reverse=True)

    return jsonify(ret), 200

@main.route("/python/postBlog", methods=["POST"])
def postBlog():
    data = request.get_json()
    db.blog.insert_one(data)
    arr= []
    ret = list(db.blog.find({},{"_id":0, "username":1, "title" : 1, "content" : 1, "rating" : 1}))
    for doc in ret:
        arr.append(doc)
    return jsonify(arr), 200

@main.route("/python/getBlog", methods=["GET"])
def getBlog():
    data = request.get_json()
    arr = []
    if not data:
        ret = list(db.blog.find({},{"_id":0, "username":1, "title" : 1, "content" : 1, "rating" : 1}))
    else: 
        ret = list(db.blog.find({"username" : data["username"]},{"_id":0, "username":1, "title" : 1, "content" : 1, "rating" : 1}))

    for doc in ret:
        arr.append(doc)

    return jsonify(arr) , 200