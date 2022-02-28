#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 15:39:13 2022

@author: gabrielmartinong
"""

from flask import Flask, request, jsonify
app = Flask(__name__)
server = app.server
app.title = 'Case Study 5'