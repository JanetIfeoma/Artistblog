from flask import Blueprint,render_template, redirect, url_for, request,flash
from flask_login import login_required,current_user
from . import db
from.models import Post,User


display = Blueprint("display", __name__)

@display.route("/")
@display.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html",user=current_user, posts=posts)


@display.route("/about")
def about():
    return render_template("about.html",user=current_user)
    
@display.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)



@display.route("/new_post", methods=['GET','POST'] )
@login_required
def new_post():
    if request.method =="POST":
        text =request.form.get('text')
        if not text:
            flash('Post box cannot be empty', category='error')
        else:
            post =Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('display.home'))
    return render_template("new_post.html",user=current_user)



@display.route("/delete-post/<id>")
@login_required
def deletepost(id):
    post =Post.query.filter_by(id=id).first()

    if not post:
        flash('Post is non-existent', category='error')
    elif current_user.id == post.id:
        flash('You cannot delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted',category='success')    
    return redirect(url_for('display.home'))


@display.route("/edit/<id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST':
       text= request.form.get('text')
       if not text:
        flash('Only text can be entered', category='error')
       else:
        post = Post(text=text , author=current_user.id)
        db.session.add(post)
       db.session.commit()
       flash('Post has been Updated',category='success')
       return redirect(url_for('display.home'))
    return render_template('edit.html', user=current_user, post=posts)




@display.route("/posts/<username>")
@login_required
def posts(username):
    user =User.query.filter_by(username= username).first()

    if not user:
        flash('User not available', category='error')
        return redirect(url_for('display.home'))

    posts =Post.query.filter_by(author= user.id).all()
    return render_template('posts.html',user=current_user,username=username, posts=posts)


