#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , time
import models as Models

@Models.app.route('/')
def main():
    flash("you not supose to be here")
    return render_template('test.html')

def setup():
    raise Exception("not implemented")

if __name__ == '__main__':
    Models.app.secret_key = 'super secret key'
    Models.app.run(host='0.0.0.0', port= 8081 , debug = True)
