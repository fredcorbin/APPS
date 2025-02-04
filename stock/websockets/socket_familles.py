import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import WebsocketConsumer
from django.db.models.functions import Lower
from stock.models import Famille,Preferes,Modele

class webSocket_familles(WebsocketConsumer):
    def connect(self):
        print('connect_familles')
        self.accept()

    def disconnect(self,close_code):
        print('disconnect')
        pass

    def receive(self,text_data):
        tmp= text_data.split('')
        print("RECEIVE ",text_data)
        cmd=tmp[0]
        print('RECEIVE:',cmd)
        if cmd=="INIT_FAMILLES": self.initFamilles(text_data)
        if cmd=="ADDFAMILLE": self.ajouteFamille(text_data)
        if cmd=="MODIFFAMILLE": self.modifFamille(text_data)
        if cmd == "SUPPRIMEFAMILLE": self.supprimeFamille(text_data)
        if cmd == "TEST": self.test(text_data)

    def initFamilles(self,data):
        cmd = data.split('')[0]
        data=self.dataFamilles(False)
        self.send(json.dumps({"cmd":cmd, "ok": True, "values": data } ))

    def ajouteFamille(self,data):
        values= data.split('')
        try:
            ok = not Famille.objects.using("in2p3").filter(nom=values[1])
            id=-1
            pos=-1
            if ok:
                pos=self.getPos(values[1],'nom',Famille.objects.using("in2p3").all())
                nouveau = Famille(nom=values[1],labo_id=1,pref=False)
                nouveau.save(using="in2p3")
                id=nouveau.id
                if values[2]=='true':
                    nouveau = Preferes(familleId=id,modeleId=-1)
                    nouveau.save()
            data = self.dataFamilles(False)
            self.send(json.dumps({"cmd":values[0], "ok": ok,"nom": values[1],  "id":id, "pos":pos, "values":data } ))
        except Exception as e: print(e)

    def modifFamille(self,data):
        values= data.split('')
        ok=False
        famille= Famille.objects.using("in2p3").filter(id=values[3])
        if famille:
            ok=True
            elem=famille[0]
            elem.nom=values[1]
            elem.save(using="in2p3")
            pref = Preferes.objects.filter(familleId=values[3],modeleId=-1)
            if pref:
                if values[2]=='false':
                    pref.delete()
            else:
                if values[2]=='true':
                    pref=Preferes()
                    pref.familleId=values[3]
                    pref.modeleId=-1
                    pref.save()
        self.send(json.dumps({"cmd":values[0], "ok": ok,"nom": values[1],  "id":values[3], "pref":values[2] } ))

    def supprimeFamille(self,data):
        values= data.split('')
        print('supprimeFamille: ',values)
        idfamille=values[3]
        ok=False
        famille= Famille.objects.using("in2p3").filter(id=idfamille)
        if famille:
            prefs= Preferes.objects.filter(familleId=idfamille).all()
            for pref in prefs:   pref.delete()
            ok=True
            elem=famille[0]
            elem.delete(using='in2p3')
        data = self.dataFamilles(False)
        self.send(json.dumps({"cmd":values[0], "ok": ok,"nom": values[1],  "id":values[2], "values": data } ))

    def getPos(self,value,key,dict):
        pos = 0
        for t in dict.values(key):
            if t[key] <= value: pos = pos + 1
            # print(value,t['nom'], pos)
        return pos

    def test(self,data):
        print("TEST:",data)
        values= data.split('')
        nom=values[1]
        pos=self.getPos(nom,'nom',Famille.objects.using("in2p3").all())
        print(pos,nom)

    def dataFamilles(self,dopref):
        prefs = Preferes.objects.filter(modeleId=-1).values_list('familleId', flat=True)
        prefs = list(prefs)

        if dopref: tmp = Famille.objects.using('in2p3').filter(pk__in=prefs)
        else:tmp = Famille.objects.using('in2p3')
        tmp = list(tmp.order_by(Lower('nom')).values('id', 'nom'))
        for t in tmp:
            x = 0
            id = t['id']
            if id in prefs: x = 1
            t['pref'] = x
        return json.dumps(tmp, cls=DjangoJSONEncoder)
