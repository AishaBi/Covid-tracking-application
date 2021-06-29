from flask import render_template, url_for, flash, redirect, request, Blueprint, Markup
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from flaskblog import db, bcrypt
from flaskblog.models import User
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,UpdateHomeForm,
                                   RequestResetForm, ResetPasswordForm, UpdateMHomeForm,UpdateGraphForm)
from flaskblog.users.utils import save_picture, send_reset_email
from sqlalchemy.sql.functions import func


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
            department=form.department.data,
            manager=form.manager.data,
            job_title=form.job_title.data,
            supervisor=form.supervisor.data,
            high_risk=form.high_risk.data,
            health=form.health.data,
            h_comment=form.h_comment.data,
            employment=form.employment.data,
            e_comment=form.e_comment.data,
            date_updated=form.date_updated.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
            return redirect(url_for('users.mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.mainpage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))
    # return redirect(url_for('main.home'))

@users.route("/mainpage")
def mainpage():
    return render_template('mainpage.html', title='Main')


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.job_title = form.job_title.data
        current_user.department = form.department.data
        current_user.supervisor = form.supervisor.data
        current_user.manager = form.manager.data
        current_user.high_risk = form.high_risk.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.job_title.data = current_user.job_title
        form.department.data = current_user.department
        form.supervisor.data = current_user.supervisor
        form.manager.data = current_user.manager
        form.high_risk.data = current_user.high_risk
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if current_user.manager.lower() == 'yes':
        return redirect(url_for('users.option'))
    # elif current_user.manager.lower() == 'no':
    #     return redirect(url_for('users.home'))

    form = UpdateHomeForm()
    if form.validate_on_submit():
        current_user.health = form.health.data
        current_user.h_comment = form.h_comment.data
        current_user.employment = form.employment.data
        current_user.e_comment = form.e_comment.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.home'))
        # return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.health.data = current_user.health
        form.h_comment.data = current_user.h_comment
        form.employment.data = current_user.employment
        form.e_comment.data = current_user.e_comment
    return render_template('home.html', title='Home', form=form)

@users.route("/m_home", methods=['GET', 'POST'])
@login_required
def option():
    form = UpdateMHomeForm()
    if form.validate_on_submit():
        option = form.option.data
        if option == 'Analytics':
            return redirect(url_for('users.analytics'))
        elif option == 'Graphs':
            return redirect(url_for('users.graphs'))
        elif option == 'Search':
            return redirect(url_for('users.search'))     
    return render_template('m_home.html', title='MHome', form=form)
        

@users.route("/m_home/analytics")
def analytics():
    case_total = User.query.filter_by(health='covid').count()
    employees_total = case_total + User.query.filter_by(health='covid-free').count()
    case_percent = ("%.0f%%" % (100 * case_total / employees_total))
    home_total = User.query.filter_by(employment='working from home').count()
    office_total = User.query.filter_by(employment='working in office').count()
    part_time_total = User.query.filter_by(employment='part-time in office').count()
    
    return render_template('analytics.html', title='Analytics', case_total=case_total, home_total=home_total, office_total=office_total, part_time_total=part_time_total, employees_total=employees_total, case_percent=case_percent)


@users.route("/m_home/graphs", methods=['GET', 'POST'])
def graphs():
    form = UpdateGraphForm()
    if form.validate_on_submit():
        option = form.option.data
        if option == 'Line graph':
            return redirect(url_for('users.line'))
        elif option == 'Bar chart':
            return redirect(url_for('users.bar'))
        elif option == 'Pie chart':
            return redirect(url_for('users.pie'))     
    return render_template('graphs.html', title='Graphs',form=form)

@users.route("/m_home/graphs/bar")
def bar():
    home_total = User.query.filter_by(employment='working from home').count()
    office_total = User.query.filter_by(employment='working in office').count()
    part_time_total = User.query.filter_by(employment='part-time in office').count()

    labels = ['Working from Home', 'Working in office', 'Part-time in office']
    values = [home_total,office_total,part_time_total]
    return render_template('bar.html', title='Bar Chart',max=5, labels=labels, values=values)

@users.route("/m_home/graphs/pie")
def pie():
    case_total = User.query.filter_by(health='covid').count()
    employees_total = User.query.filter_by(manager= 'yes').count() + User.query.filter_by(manager= 'no').count()
    covid_free_total = employees_total - case_total

    labels = ['Covid', 'Covid-free']
    values = [case_total,covid_free_total]
    colors = ["#F7464A","#46BFBD"]
    return render_template('pie.html', title='Pie Chart',max=5, set=zip(values,labels,colors))

@users.route("/m_home/graphs/line")
def line():

    # # https://flaskage.readthedocs.io/en/latest/database_queries.html

    total = 0
    september = total + (User.query.filter_by(health='covid').filter_by(date_updated = '2020-09-27 19:35:45.840362')).count()
    october = september + (User.query.filter_by(health='covid').filter_by(date_updated = '2020-10-27 19:35:45.840362')).count()
    november = october + (User.query.filter_by(health='covid').filter_by(date_updated = '2020-11-27 19:35:45.840362')).count()
    december = november + (User.query.filter_by(health='covid').filter_by(date_updated = '2020-12-27 19:35:45.840362')).count()
    january = december + (User.query.filter_by(health='covid').filter_by(date_updated = '2021-01-27 19:35:45.840362')).count()
    february = january + (User.query.filter_by(health='covid').filter_by(date_updated = '2021-02-27 19:35:45.840362')).count()
    march = february + (User.query.filter_by(health='covid').filter_by(date_updated = '2021-03-27 19:35:45.840362')).count()
    
    labels = ['Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
    values = [september, october,november,december,january, february, march]
    # labels = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed','Thu','Fri']
    # values = [saturday, sunday,monday,tuesday,wednesday,thursday,friday]
        
    return render_template('line.html', title='Monthly covid rates',max=25, labels=labels, values=values)



@users.route("/m_home/search")
def search():
    return render_template('search.html', title='Search')






@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
