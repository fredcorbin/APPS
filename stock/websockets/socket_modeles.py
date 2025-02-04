import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import WebsocketConsumer
from django.db.models.functions import Lower
from django.db.models import Q
from stock.models import Famille,Preferes,Modele

class webSocket_modeles(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('connect_modèles')

    def disconnect(self,close_code):
        print('disconnect')
        pass

    def receive(self,text_data):
        tmp= text_data.split('')
        cmd=tmp[0]
        print('RECEIVE:',text_data)
        if cmd=="INIT_FAMILLES": self.init_familles(text_data)
        if cmd=="INIT_MODELES" : self.init_modeles(text_data)
        if cmd=="AJOUT_MODELE" : self.ajoute_modele(text_data)
        if cmd=="MODIF_MODELE" : self.modifie_modele(text_data)
        if cmd=="SUPPRIME_MODELE": self.supprime_modele(text_data);

    def init_familles(self,data):
        cmd = data.split('')[0]
        print('init_familles')
        tmp=list(Preferes.objects.using('local').values_list('familleId',flat=True).filter(modeleId=-1))
        tmp=Famille.objects.using('in2p3').filter(pk__in=tmp).order_by(Lower('nom')).values('id','nom')
        data=json.dumps(list(tmp), cls=DjangoJSONEncoder)
        self.send(json.dumps({"cmd":cmd, "ok": True, "values": data } ))
        print('ok init_familles')

    def init_modeles(self,data):
        params = data.split('')
        print('init_modeles: ',data)
        ok=1
        try:
            data= self.dataModeles(params[1], params[2]=="true")
            self.send(json.dumps({"cmd":params[0],"ok":ok,"values":data}))
        except Exception as e: print(e)

    def ajoute_modele(self,data):
        params = data.split('')
        familleId = params[1]
        nom = params[2]
        pref = params[3]
        ok=0
        tmp=list(Modele.objects.using('in2p3').filter(famille_id=familleId).filter(nom=nom))

        if len(tmp)==0: ok=1
        if ok==1:
            nouveau= Modele(nom=nom,famille_id=familleId)
            nouveau.save(using='in2p3')
            modeleId=nouveau.id
            nouveau = Preferes(familleId=familleId,modeleId=modeleId)
            nouveau.save()

        data= self.dataModeles(familleId,pref)
        print("AJOUTE MODELE: ",familleId,nom,data)
        self.send(json.dumps({"cmd":params[0],"ok":ok,"values":data} ))
        return

    def modifie_modele(self,data):
        params = data.split('')
        familleId= params[1]
        modeleId = params[2]
        nom= params[3]
        pref = params[4]
        pref2=params[5]
        ok=0
        print('modifie_modele:',familleId,modeleId,nom,pref,pref2)
        tmp=list(Modele.objects.using('in2p3').filter(~Q(id=modeleId)).filter(nom=nom))
        print(len(tmp))
        if len(tmp)==0:
            ok=1
            elem =  Modele.objects.using('in2p3').filter(id=modeleId)[0]
            elem.nom=nom
            elem.save(using='in2p3')
        if ok==1:
            print('pref2=',pref2)
            tmp = Preferes.objects.filter(familleId=familleId).filter(modeleId=modeleId)
            print(len(tmp))
            print(tmp)
            if len(tmp)==0:
                if pref2=='true':
                    elem=Preferes(familleId=familleId,modeleId=modeleId)
                    elem.save()
            else:
                if pref2=='false':
                    tmp[0].delete()


        data = self.dataModeles(familleId, pref)
        print(data)
        self.send(json.dumps({"cmd":params[0],"ok":ok,"values":data} ))
        return

    def supprime_modele(self,data):
        params = data.split('')
        familleId= params[1]
        modeleId = params[2]
        pref=params[3]
        ok=0
        print('supprime_modele:',familleId,modeleId,pref)
        modele = Modele.objects.using('in2p3').filter(id=modeleId)
        if modele:
            ok=1
            modele[0].delete(using='in2p3')
            p = Preferes.objects.filter(familleId=familleId).filter(modeleId=modeleId)
            if p: p[0].delete()
        data = self.dataModeles(familleId, pref)
        print("SUPPRIME MODELE: ", modeleId)
        self.send(json.dumps({"cmd":params[0],"ok":ok,"values":data} ))
        return

    def dataModeles(self,familleId,pref):
        if isinstance(pref,str):  dopref= pref=="true"
        else: dopref=pref
        IdElem= Modele.objects.using('in2p3').filter(famille_id=familleId)
        IdElem=list(IdElem.filter(id__gt=-1).values_list('id',flat=True))
        prefs = Preferes.objects.filter(familleId=familleId).filter(modeleId__gt=-1).values_list('modeleId',flat=True)
        prefs=list(prefs)
        if dopref:   tmp = Modele.objects.using('in2p3').filter(pk__in=prefs)
        else: tmp = Modele.objects.using('in2p3').filter(pk__in=IdElem)
        tmp=list(tmp.order_by(Lower('nom')).values('id', 'nom'))
        for t in tmp:
            x=0
            id=t['id']
            if id in prefs: x=1
            t['pref']=x
        return json.dumps(tmp, cls=DjangoJSONEncoder)




