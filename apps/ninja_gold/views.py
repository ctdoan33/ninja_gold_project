# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
import random
from datetime import datetime
def index(request):
    if "gold" not in request.session:
        request.session["gold"]=0
    if "log" not in request.session:
        request.session["log"]=[]
    return render(request, "ninja_gold/index.html")
def process_money(request, location):
    if location == "farm":
        delta=random.randint(10, 20)
    if location == "cave":
        delta=random.randint(5, 10)
    if location == "house":
        delta=random.randint(2, 5)
    if location == "casino":
        delta=random.randint(-50,50)
        if request.session["gold"] <= -delta:
            new = {"entry" : "Entered a casino and lost all your gold... Ouch... "+datetime.strftime(datetime.today(), "(%Y/%m/%d %I:%M %p)"), "color" : "red"}
        elif delta >= 0:
            new = {"entry" : "Entered a casino and earned "+str(delta)+" golds! "+datetime.strftime(datetime.today(), "(%Y/%m/%d %I:%M %p)"), "color" : "green"}
        else:
            new = {"entry" : "Entered a casino and lost "+str(-delta)+" golds... Ouch... "+datetime.strftime(datetime.today(), "(%Y/%m/%d %I:%M %p)"), "color" : "red"}
    else:
        new = {"entry" : "Earned "+str(delta)+" golds from the "+location+"! "+datetime.strftime(datetime.today(), "(%Y/%m/%d %I:%M %p)"), "color" : "green"}
    request.session["gold"]+=delta
    if request.session["gold"]<0:
        request.session["gold"]=0
    request.session["log"].insert(0, new)
    return redirect("/")
def reset(request):
    request.session.clear()
    return redirect("/")