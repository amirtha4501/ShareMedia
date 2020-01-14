from manage import User, LoggedUsers, LoggedUsersPost, LoggedUsersComment, LoggedUsersLike, db, app
from flask import Flask, request, jsonify, redirect, url_for, render_template
from datetime import datetime
import json


# USER class methods
@app.route('/signup')
def user_signup():
    input_data = request.get_json()

    first_name = input_data.get('first_name')
    last_name = input_data.get('last_name')
    email=input_data.get('email')
    mobile=input_data.get('mobile')
    password=input_data.get('password')
    gender = input_data.get('gender')
    user_name = first_name + " " + last_name

    name_already_existing = User.query.filter_by(user_name=user_name).first()
    email_already_existing = User.query.filter_by(email=email).first()
    mobile_already_existing = User.query.filter_by(mobile=mobile).first()
    password_already_existing = User.query.filter_by(password=password).first()
    
    if name_already_existing:
        print("user name is already present")
        return "user name is already present"

    elif email_already_existing:
        print("email is already present")
        return "email name is already present"

    elif mobile_already_existing:
        print("mobile is already present")
        return "mobile is already present"

    elif password_already_existing:
        print("password is already present")
        return "password is already present"

    admin = User(
        user_name = user_name,
        email = email,
        mobile = mobile,
        password = password,
        gender = gender
    )
    admin.add()
    return redirect('/listusers')


@app.route("/listusers")
def list_users():
    users = User.query.all()
    user_list = []

    for user in users:
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
    # return redirect(url_for('post'))


@app.route('/loggedusers/post')
def post():
    input_message = request.get_json()
    login_existing = LoggedUsers.query.filter_by(user_id=input_message['user_id']).first()

    if not login_existing:
        print("Login is needed to post")
        return "Login is needed to post"
        
    existing_user = LoggedUsers.query.get(input_message['user_id'])

    log_users_post = LoggedUsersPost(
        user_id = input_message['user_id'],
        user_name = existing_user.user_name,
        message = input_message['message'],
        time = datetime.utcnow()
    )    
    log_users_post.add()
    return "posted"


@app.route('/loggedusers/post/comment')
def comment():
    input_content = request.get_json()
    login_existing = LoggedUsers.query.filter_by(user_id=input_content['user_id']).first()
    
    if not login_existing:
        print("Login is needed to comment")
        return "Login is needed to comment"
    
    posted_existing_user = LoggedUsersPost.query.get(input_content['post_id'])

    if not posted_existing_user:
        print("No such posts to comment.")
        return "No such posts to comment."

    comment_existing = LoggedUsersComment.query.filter_by(post_id=input_content['post_id']).count()

    log_users_comment = LoggedUsersComment(
    user_id = input_content['user_id'],
    post_id = input_content['post_id'],
    user_name = login_existing.user_name,
    comment = input_content['comment'],
    comment_count = comment_existing + 1,
    comment_time = datetime.utcnow()
    )    
    log_users_comment.add() 
    return "comment"


@app.route('/loggedusers/post/like')
def likes():
    input_content = request.get_json()
    login_existing = LoggedUsers.query.filter_by(user_id=input_content['user_id']).first()
    
    if not login_existing:
        print("Login is needed to like")
        return "Login is needed to like"
    
    posted_existing_user = LoggedUsersPost.query.get(input_content['post_id'])
    
    if not posted_existing_user:
        print("No such posts to like.")
        return "No such posts to like."

    like_existing_count = LoggedUsersLike.query.filter_by(post_id=input_content['post_id']).count()
    # liked_existing_pid = LoggedUsersLike.query.get(input_content['post_id'])
    # print(liked_existing_pid)

    log_users_like = LoggedUsersLike(
    user_id = input_content['user_id'],
    post_id = input_content['post_id'],
    user_name = login_existing.user_name,
    like_count = like_existing_count + 1,
    like_time = datetime.utcnow()
    )    
    log_users_like.add()
    return "Liked" 


app.run(host='0.0.0.0',port=7000,debug=True)
