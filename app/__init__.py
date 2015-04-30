# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask_misaka import Misaka
from flask_restless import APIManager

# App initialization
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

# Jinja2 Setup
app.jinja_env.trim_blocks = True

# Logging with Rotating File Setup
handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')
)
app.logger.addHandler(handler)

# Database Setup
db = SQLAlchemy(app)

# Markdown Processor Setup
Misaka(app)

# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.session_protection = 'strong'


class MyAdminIndexView(AdminIndexView):
    """
    Administration Setup
    """
    @expose('/')
    def index(self):
        if current_user.is_authenticated():
            if current_user.is_superuser():
                return super(MyAdminIndexView, self).index()
        return redirect(url_for('MainView:index'))

admin = Admin(app, 'We Rate Movies', index_view=MyAdminIndexView())

manager = APIManager(app, flask_sqlalchemy_db=db)

from app import views
from app import models
from app import api

# Blueprint Registering
from app.modules import blog
app.register_blueprint(blog.blueprint)

from app.views.context import *


