from datetime import datetime
from django.db import models
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import HiddenInput
from django.forms import MultiWidget
from django.forms.widgets import SplitDateTimeWidget

class User(models.Model):
	user_name = models.CharField(max_length=200)
	user_color = models.CharField(max_length=6,default='CCCCFF')
	def __str__(self):
		return self.user_name

class ItemType(models.Model):
	type_name = models.CharField(max_length=200)
	def __str__(self):
		return self.type_name	

class Item(models.Model):
	item_type = models.ForeignKey(ItemType)
	item_name = models.CharField(max_length=200)
	item_desc = models.CharField(max_length=1000)
	def __str__(self):
		return self.item_name
    
class Checkout(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	
	def __str__(self):
		return self.user.user_name+" checked out "+self.item.item_name+" from "+str(self.start_time)+" to "+str(self.end_time)

class DateForm(forms.Form):
	date = forms.DateTimeField(widget=SelectDateWidget,initial=datetime.now)
				
class CheckoutForm(ModelForm):
	class Meta:
		model = Checkout
		exclude = {'item'}
		widgets = {
			'start_time': SplitDateTimeWidget(),
			'end_time': SplitDateTimeWidget(),
		}
		
	def checkConflicts(self,i,u,s,e):
		checkouts = Checkout.objects.filter(item=i)
		conflict = ""
		
		for c in checkouts:
			if (s >= c.start_time and s < c.end_time) or (e > c.start_time and e <= c.end_time) or (c.start_time > s and c.start_time < e) or (c.end_time > s and c.end_time < e):
				if u == c.user:
					conflict = "You already have the "+c.item.item_name+" reserved from "+c.start_time.strftime('%Y-%m-%d %H:%M')+" to "+c.end_time.strftime('%Y-%m-%d %H:%M')
				else:
					conflict = "Time conflict: "+c.user.user_name+" has the "+c.item.item_name+" reserved from "+c.start_time.strftime('%Y-%m-%d %H:%M')+" to "+c.end_time.strftime('%Y-%m-%d %H:%M')
			else:
				#print str(s)+" to "+str(e)+" for item "+str(i.id)+" is not between "+str(c.start_time)+" and "+str(c.end_time)
				continue
		
		return conflict
		
	# Validation
	def clean(self):
		cleaned_data = super(CheckoutForm, self).clean()
		start_time = cleaned_data.get("start_time")
		end_time = cleaned_data.get("end_time")
		user = cleaned_data.get("user")
		item = self.item
		#print "cleaning checkout form. item: "+str(item)+", start time "+str(start_time)+", end time "+str(end_time)

		if start_time and end_time:
			if start_time > end_time:
				raise forms.ValidationError("Start time must be before end time.")
			
			conflicts = self.checkConflicts(item,user,start_time,end_time)	
			if conflicts != "":
				raise forms.ValidationError(conflicts)