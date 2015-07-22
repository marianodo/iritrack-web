#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import mktime
from datetime import *
import cookielib
import os
import urllib
import urllib2
import sys
from bottle import template, request, redirect
from server import app
from server.models import Driver
from server.models import LastUpdate
from server.services import Iritrack
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from server import engine
from server.services import dataFetch
Session = sessionmaker(bind=engine)
session = Session()
from bottle import Bottle, request, redirect


@app.route('/')
def index(db):
	
	return template('index.html')

