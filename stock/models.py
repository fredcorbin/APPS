from django.db import models

class Labo(models.Model):
    nom= models.CharField(max_length=30)

    class Meta:
        managed=True
        db_table = "labo"



class Famille(models.Model):
    nom = models.CharField(max_length=50);
    labo= models.ForeignKey(Labo,on_delete=models.CASCADE)

    class Meta:
        managed=True
        db_table="famille"

class Modele(models.Model):
    nom = models.CharField(max_length=50);
    famille = models.ForeignKey(Famille,on_delete=models.CASCADE)
    labo= models.ForeignKey(Labo,on_delete=models.CASCADE)

    class Meta:
        managed=True
        db_table="modele"

class Preferes(models.Model):
    familleId = models.IntegerField(default=-1)
    modeleId = models.IntegerField(default=-1)

    class Meta:
        managed=True
        db_table="preferes"


