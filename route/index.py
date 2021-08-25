# coding:utf-8

from flask import Blueprint, render_template,request

here_index = Blueprint('here_index',__name__)

@here_index.route('/')
def index():
    return render_template('index.html')