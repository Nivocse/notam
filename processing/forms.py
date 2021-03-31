import io, csv

from django import forms
from .models import Runway, Airport, Notam


class RunwayForm(forms.Form):
  file_upload = forms.FileField()


  def data_validation(self):
    file = self.cleaned_data["file_upload"]

    if not file.name.endswith(".csv"):
      raise forms.ValidationError("File type not supported!")
    return file


  def process_csv(self):
    csv_file = io.TextIOWrapper(self.cleaned_data["file_upload"].file)
    reader = csv.DictReader(csv_file)
  
    runways = [Runway(
        airport = row["Aerodrome / Heliport - ICAO Code"],
        designator = row["RWY direction - Designator"],
        category = row["Category"]
      ) for row in reader]
    
    Runway.objects.bulk_create(runways)
  

class AirportForm(forms.Form):
  file_upload = forms.FileField()


  def data_validation(self):
    file = self.cleaned_data["file_upload"]

    if not file.name.endswith(".csv"):
      raise forms.ValidationError("File type not supported!")
    return file


  def process_csv(self):
    csv_file = io.TextIOWrapper(self.cleaned_data["file_upload"].file)
    reader = csv.DictReader(csv_file)
  
    airports = [Airport(
        icao = row["ICAO"],
        purpose = row["Type"]
      ) for row in reader if row["Type"] in ["BASE", "DEST"]]
    
    Airport.objects.bulk_create(airports)
  

class NotamSelectForm(forms.Form):
  choices = enumerate(["BASE", "BASE+DEST", "SPECIFIC"])
  locations = forms.TypedChoiceField(choices=choices)
  remark = forms.CharField(required=False)


class NotamForm(forms.ModelForm):
  class Meta:
    model = Notam
    fields = "__all__"