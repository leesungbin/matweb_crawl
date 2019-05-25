from django.db import models

class Stainless(models.Model):
    name=models.CharField(default='',max_length=256)
    num=models.CharField(default='',max_length=256)
    
    def __str__(self):
        return self.name

class Composition(models.Model):
    compound=models.CharField(default='',max_length=256)
    ratio=models.FloatField(default=0)
    stainless=models.ForeignKey(Stainless,on_delete=models.CASCADE)
    def __str__(self):
        return self.compound+' '+str(self.ratio)

class Tag(models.Model):
    name=models.CharField(default='',max_length=256)
    stainless=models.ForeignKey(Stainless,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class TensileStrength(models.Model):
    strength=models.FloatField(blank=True,null=True) #Tensile Strength, MPa
    crit=models.FloatField(default=20, blank=True,null=True) #criteria T, celsius
    cond=models.CharField(blank=True, null=True, max_length=256)
    stainless=models.ForeignKey(Stainless,on_delete=models.CASCADE)
    def __str__(self):
        return 'TS - '+str(self.strength)+' MPa at T='+str(self.crit)

class YieldStrength(models.Model):
    strength=models.FloatField(blank=True) #Yield Strength, MPa
    crit=models.FloatField(default=20, blank=True,null=True) #criteria strain ... etc
    cond=models.CharField(blank=True, null=True,max_length=256)
    stainless=models.ForeignKey(Stainless,on_delete=models.CASCADE)
    def __str__(self):
        return 'YS - '+str(self.strength)+' MPa at T='+str(self.crit)

class ThermodynamicProperty(models.Model):
    k=models.FloatField(default=0, blank=True, null=True) #thermal conductivity, W/mK
    crit=models.FloatField(default=20, blank=True, null=True) #criteria T,s celsius
    stainless=models.ForeignKey(Stainless,on_delete=models.CASCADE)
    def __str__(self):
        return 'k = '+str(self.k)+' at T='+str(self.crit)