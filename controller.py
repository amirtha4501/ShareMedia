from manage import User, LoggedUsers, db, app
from flask import Flask, request, jsonify, redirect, url_for
import json


# USER class methods
@app.route("/signup",methods=['GET','POST'])
def user_signup():
    input_data = request.get_json()
    get_data = request.json
    print(input_data)
    print(get_data)

    first_name = input_data.get('first_name')
    last_name = input_data.get('last_name')
    email=input_data.get('email')
    mobile=input_data.get('mobile')
    password=input_data.get('password')
    # dob = input_data.get('dob'),
    gender = input_data.get('gender')
    user_name = first_name + " " + last_name

    admin = User(
        user_name = user_name,
        # email=input_data.get('email'),
        # mobile=input_data.get('mobile'),
        # password=input_data.get('password'),
        # # dob = input_data.get('dob'),
        # gender = input_data.get('gender')
        email = email,
        mobile = mobile,
        password = password,
        # dob = dob,
        gender = gender
    )
    admin.add()

    return "Signed Up"


@app.route("/listusers")
def list_users():
    users = User.query.all()
    user_list = []

    for user in users:
        print(user.id,user.user_name,user.email)
        dic_user = {
            "User_id" : user.id,
            "User_name" : user.user_name,
            "Email" : user.email
        }
        user_list.append(dic_user)    
    return jsonify(user_list)   


@app.route("/loggedusers",methods=['GET','POST'])
def logged_users():
    input_data = request.get_json()
    print(input_data['user_id'])

    existing_user = User.query.get(input_data['user_id'])
    # print(existing_user.mobile)

    # last_name = input_data.get('last_name')
    # email=input_data.get('email')
    # mobile=input_data.get('mobile')
    # password=input_data.get('password')


    if not existing_user:
        print("User signup is needed to login")
        return "User signup is needed to login"
        # return redirect(url_for('user_signup'))

    already_existing = LoggedUsers.query.filter_by(user_id=input_data['user_id']).first()
    
    if already_existing:
        print("You're already logged in")
        return "You're already logged in"


    log_users = LoggedUsers(
        user_id = input_data['user_id'],
        user_name = existing_user.user_name,
        user_email = existing_user.email
    )
    log_users.add()

    return "logged users"


app.run(host='0.0.0.0',port=7000,debug=True)
