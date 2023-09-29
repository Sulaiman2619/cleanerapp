# forms.py

from django import forms
from .models import Building, Room, Work

class WorkFilterForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label="All Buildings")
    floor = forms.ModelChoiceField(queryset=Room.objects.values('floor_num').distinct().order_by('floor_num'), empty_label="All Floors")
    work_name = forms.ModelChoiceField(queryset=Work.objects.values('work_name').distinct().order_by('work_name'), empty_label="All Work Names")
