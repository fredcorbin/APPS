from django.http import HttpResponse
from django.shortcuts import render
from stock.models import Labo,Modele,Famille,Preferes
from django.db.models.functions import Lower
from django.db.models import Value,Subquery

from django.core import serializers

def index(request):
    return render(request,"stock/index.html")

def famille(request):
    pref=Preferes.objects.all()
    table = Famille.objects.using('in2p3').all().order_by(Lower('nom'))
    for t in table:
        t.pref=Preferes.objects.filter(familleId=t.id,modeleId=-1).count()


    return render(request,"stock/famille.html",
                  {'famille': table, 'preferes': pref } )

def modele(request):
    pref = Preferes.objects.all()
    tableF = Famille.objects.using('in2p3').all().order_by(Lower('nom'))
    for t in tableF:
        t.pref=Preferes.objects.filter(familleId=t.id,modeleId=-1).count()

    tableM = Modele.objects.using('in2p3').all()

    return render(request,"stock/modele.html", {'famille': tableF,'modele':tableM})

