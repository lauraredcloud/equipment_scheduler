from django import template
from datetime import datetime
import pytz
from django.utils import timezone

register = template.Library()

# Formatting for the calendar

# Height of calendar box
@register.filter
def calc_height(co,max_height):
	diff_delta = co.end_time-co.start_time # Timedelta of the length of the time block
	diff_minutes = (diff_delta.seconds) / 60 # Convert timedelta to number of minutes
	ratio = float(max_height) / 1440 # Come up with the ratio to convert minutes to pixels
	pix_height = diff_minutes * ratio
	return int(pix_height)

# Top px of calendar box
@register.filter
def calc_top(co,max_height):
	midnight = datetime(co.start_time.year,co.start_time.month,co.start_time.day,0,0) # Create datetime of midnight of current day
	midnight = midnight.replace(tzinfo=pytz.utc) # Make timezone aware
	diff_delta = co.start_time-midnight # Convert start time to a number of minutes since midnight
	diff_minutes = (diff_delta.seconds) / 60 # Convert timedelta to number of minutes
	ratio = float(max_height) / 1440 # Come up with the ratio to convert minutes to pixels
	pix_top = diff_minutes * ratio	
	return pix_top
	
# Border color, given a user color (darkens hexcolor)
def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

@register.filter
def make_border_color(hexstr):
	scalefactor = 0.75
	
	if scalefactor < 0 or len(hexstr) != 6:
		return hexstr

	r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

	r = clamp(r * scalefactor)
	g = clamp(g * scalefactor)
	b = clamp(b * scalefactor)

	return "#%02x%02x%02x" % (r, g, b)