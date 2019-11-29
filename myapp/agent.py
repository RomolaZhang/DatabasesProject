# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify
from database import conn
import datetime
from decimal import *

agent = Blueprint('agent', __name__)

@agent.route("/agentHome")
def agentHome():
    email = session['email']
    return render_template('agentHome.html')