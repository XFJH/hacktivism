from django.db import models
from django.core.validators import validate_email

# Create your models here. 
class Notifier(models.Model):
    name= models.CharField( max_length=30, unique=True )
    touch_way= models.CharField(max_length=30, default='')
    e_mail= models.EmailField(null=True);

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'defacements_notifier'
    
class Defacements(models.Model):
    notifier= models.ForeignKey(Notifier)
    notifier_words = models.CharField(max_length=100, null=True)
    full_path= models.URLField( )
    time= models.DateTimeField()
    h_deface= models.BooleanField(default=False)
    m_deface= models.BooleanField(default=False)
    s_deface= models.BooleanField(default=False)
    r_deface= models.BooleanField(default=False)
    
    def __unicode__(self):
        return str([self.notifier, self.notifier_words, self.full_path, self.time, \
                self.h_deface, self.m_deface, self.s_deface, self.r_deface])
    class Meta:
        db_table = 'defacements_defacements'
        #unique_together = ('time', 'full_path')
        ordering=['-time']
        
    
    

class Attacker(models.Model):
    name= models.CharField(max_length=30, unique=True)
    touch_way= models.CharField(max_length=200, default='')
    e_mail= models.EmailField(null=True)
    team= models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'defacements_attacker'


class Victim(models.Model):
    # domain_name means the host
    domain_name= models.URLField()
    ip= models.IPAddressField()
    # victim geo analytics
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    os= models.CharField(max_length=30)
    server= models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.address
    class Meta:
        db_table = 'defacements_victim'