from flask import render_template, request, Blueprint
# from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
# def mainpage():
# 	return render_template('mainpage.html')

# @main.route("/home")
# def home():
#     page = request.args.get('page', 1, type=int)
#     return render_template('home.html', title='Home')


@main.route("/info")
def info():
    return render_template('info.html', title='Info')



# @main.route("/mainpage")
# def mainpage():
#     return render_template('mainpage.html', title='Covid-19 Tracker')