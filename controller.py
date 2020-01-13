from manage import User, LoggedUsers, LoggedUsersPost, db, app
from flask import Flask, request, jsonify, redirect, url_for, render_template
from datetime import datetime
# import datetime
# from jinja2 import Markup
# from flask_moment import Moment
import json


# USER class methods
@app.route('/signup')
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

    return redirect('/listusers')


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
    # return render_template('test.html',contacts=user_list)


@app.route("/loggedusers",methods=['GET','POST'])
def logged_users():
    input_data = request.get_json()
    print(input_data['user_id'])

    existing_user = User.query.get(input_data['user_id'])

    # last_name = input_data.get('last_name')
    # email=input_data.get('email')
    # mobile=input_data.get('mobile')
    # password=input_data.get('password')


    if not existing_user:
        print("User signup is needed to login")
        return "User signup is needed to login"
        # return redirect(url_for('user_signup'))

    print(existing_user.mobile)
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

    # return redirect('register.html')
    return "logged users"
    # return redirect(url_for('post'))

@app.route('/loggedusers/post')
def post():
    input_message = request.get_json()
    print(input_message)
    # if input_message == None:
    #     print("Input message is required to post.")

    login_existing = LoggedUsers.query.filter_by(user_id=input_message['user_id']).first()
    print(login_existing)
    if not login_existing:
        print("Login is needed to post")
        return "Login is needed to post"
        # moment = Moment(app)
        # print(moment)
        # return moment
        # return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

        
    existing_user = LoggedUsers.query.get(input_message['user_id'])
    print(existing_user)
    print(existing_user.user_name)
    print(existing_user.id)
    print(input_message['message'])

    # print(existing_user.user_name)
    # now = datetime.datetime.now()
    # print (now.strftime("%Y-%m-%d %H:%M:%S"))

    log_users_post = LoggedUsersPost(
        user_id = input_message['user_id'],
        user_name = existing_user.user_name,
        message = input_message['message'],
        time = datetime.utcnow()
    )    
    log_users_post.add()
    # print(time)

    # return json.dumps(log_users_post.__dict__ )
    return "posted"
    # return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

@app.route('/loggedusers/comment')
def comment():
    input_content = request.get_json()
    print(input_content)

    login_existing = LoggedUsers.query.filter_by(user_id=input_content['user_id']).first()
    print(login_existing)
    
    if not login_existing:
        print("Login is needed to comment")
        return "Login is needed to comment"
    
    existing_user = LoggedUsersPost.query.get(input_content['user_id'])
    print(existing_user)
    print(existing_user.user_id)
    print(existing_user.user_name)

    
    return "comment"

app.run(host='0.0.0.0',port=7000,debug=True)
