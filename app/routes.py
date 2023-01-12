from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user 
from app.forms import SignUpForm, LoginForm, DateForm
from app.models import User, Data
import urllib.request, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

@app.route('/')
def index():
    return render_template('createpost.html')


@app.route('/signup', methods=["GET","POST"])
def signup():
    form = SignUpForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        #Before we add the user to the database, check to see if there is already a user with username or email
        existing_user = User.query.filter((User.email == email)|(User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.","success")
        return redirect(url_for('index'))
    return render_template('signup.html',form=form)


@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = DateForm()
    if form.validate_on_submit():
        dateinput = form.dateinput.data
        data = Data.query.filter((Data.date == (dateinput))).first()
        if data:
            data_list = Data.query.filter(Data.date<=dateinput).order_by(Data.date.desc()).limit(10).all()
            summationindexavg4 = sum([d.sumclose for d in data_list[0:4]])/4
            nasdaqindexavg10 = sum([d.nasclose for d in data_list[0:10]])/10
            if summationindexavg4 < data.sumclose:
                flash('It is time to BUY the NASDAQ Index')
            elif (summationindexavg4 > data.sumclose) and (data.nasclose < nasdaqindexavg10):
                flash('It is time to SELL the NASDAQ Index')
            elif (data.sumclose < summationindexavg4) and (data.nasclose > nasdaqindexavg10):
                flash('It is time to HOLD the NASDAQ Index')
            img = BytesIO()
            y = [d.nasclose for d in data_list[0:10]]
            x = [d.date for d in data_list[0:10]]
            y1 = [d.sumclose for d in data_list[0:4]]
            x1 = [d.date for d in data_list[0:4]]

            #plt.plot(x,y)
            fig,(ax1,ax2) = plt.subplots(1,2)
            ax1.set_title('NASDAQ Index Close vs Date')
            ax2.set_title('Summation Index Close vs Date')
            ax1.plot(x,y)
            ax2.plot(x1,y1)
            ax1.set_xticklabels(x, rotation = 50)
            ax2.set_xticklabels(x1, rotation = 50)
            plt.subplots_adjust(bottom=0.2)
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
            return render_template('plot.html', plot_url=plot_url)

        else:
            flash('Please enter a business day between Jan 15th 1986 and June 3rd 2020')

    return render_template('createpost.html',form=form)



@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Get username and password from form
        username = form.username.data
        password = form.password.data
        #Query the user table for a user with the same username as the form
        user = User.query.filter_by(username=username).first()
        #If the user exists and the password is correct for that user
        if user is not None and user.check_password(password):
            #Log the user in with the login_user function from flask_login
            login_user(user)
            #Flash a success message
            flash(f"Welcome back {user.username}!", "success")
            #Redirect back to homepage
            return redirect(url_for('create'))
        # If no user with username or password incorrect
        else:
            # flash a danger message
            flash('Incorrect username and/or password.  Please try again.', 'danger')
            # Redirect back to login page
            return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'primary')
    return redirect(url_for('index'))
