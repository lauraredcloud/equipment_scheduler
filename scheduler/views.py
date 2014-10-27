from datetime import datetime
import dateutil.parser
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from scheduler.models import ItemType, Item, User, Checkout, DateForm, CheckoutForm

def index(request):
    item_type_list = ItemType.objects.all().order_by('type_name')
    context = {'item_type_list': item_type_list}
    return render(request,'scheduler/index.html',context)
     
def detail(request, item_id):
    try:
        # Get constants for this detail view: which item this is, the user set.
        item = Item.objects.get(pk=item_id)
        users = User.objects.all().order_by('user_name')
        
        # Get the date (from the preset form, or default to today)
        # This is overly complex, fix (probably by not using SplitDateTime in the Checkouts model and not using two forms)
        date_form = DateForm()
        date = datetime.now()        
        if request.method == "POST": 
        	if request.POST.get("co_submit"): # Other form was submit
        		if request.POST.get("start_time_0") and request.POST.get("start_time_1"): #Hacky fallback: create datetime from the POST values of the split field
        			date = dateutil.parser.parse(request.POST.get("start_time_0")+" "+request.POST.get("start_time_1"))
        			date_form = DateForm(initial={'date':date})
        		else: # Fallback -- this should never happen
        			date_form = DateForm()
        			date = datetime.now()
        	else: # This form was submit
				date_form = DateForm(request.POST)
				if date_form.is_valid():
					date = date_form.cleaned_data['date']
				else: # Date form not valid fallback
					date = datetime.now()
        
        # Get the checkouts list -- filtered by date
        max_start = datetime(date.year,date.month,date.day,23,59) # Last minute of current day
        min_end = datetime(date.year,date.month,date.day,00,00) # First minute of current day
        checkouts = Checkout.objects.filter(item=item_id,start_time__lte=max_start,end_time__gte=min_end).order_by('start_time')
        all_checkouts = Checkout.objects.filter(item=item_id).order_by('start_time') # for testing
        
        # Checkout form
        c = Checkout(item=item,start_time=date,end_time=date) # Instantiate the item with pre-filled values
        
        if request.method == "POST" and not date_form.is_valid(): # Only validate/process this form if we don't have the data from the previous form
        	co_form = CheckoutForm(request.POST,instance=c)
        else:
        	co_form = CheckoutForm(instance=c)
        co_form.item = item
        
    	if request.method == "POST" and co_form.is_valid():
    		co_form.save()
		
    except Item.DoesNotExist:
        raise Http404
    return render(request, 'scheduler/detail.html', {
    	'item': item, 
    	'users': users, 
    	'date': date,
    	'checkouts': checkouts, 
    	'all_checkouts': all_checkouts,
    	'date_form': date_form,
    	'reserve_form': co_form
    })