import io, csv
import requests
import datetime
from . import util


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator



from .models import Runway, Notam, Airport
from .forms import RunwayForm, AirportForm, NotamSelectForm, NotamForm
from notam.settings import API_KEY


def home(request):
  return render(request, 'home.html')

@method_decorator(staff_member_required, name='dispatch')
class DataView(FormView):
  template_name = "runways_upload.html"
  form_class = RunwayForm
  success_url = "/upload/"

  def form_valid(self, form):
    form.process_csv()
    return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class AirportView(FormView):
  template_name = "airports_upload.html"
  form_class = AirportForm
  success_url = "/"

  def form_valid(self, form):
    form.process_csv()
    return super().form_valid(form)



@method_decorator(staff_member_required, name='dispatch')
class NotamSelectView(FormView):
  template_name = "notam_select.html"
  form_class = NotamSelectForm
  success_url = reverse_lazy("notam_select")




API_ADDRESS = f"https://applications.icao.int/dataservices/api/notams-list?api_key={API_KEY}&format=json&locations="

@staff_member_required
def call(request):
  if request.method == "GET":
    locations = [airport.icao for airport in Airport.objects.filter(purpose__in=["BASE", "DEST"])]
  elif request.method == "POST":
    if request.POST["locations"] == "0":
      locations = [airport.icao for airport in Airport.objects.filter(purpose="BASE")]
    elif request.POST["locations"] == "1":
      locations = [airport.icao for airport in Airport.objects.filter(purpose__in=["BASE", "DEST"])]
    elif request.POST["locations"] == "2":
      locations = request.POST["remark"].split()
  
  response = requests.get(f"{API_ADDRESS}{','.join(locations)}")
  notamdata = response.json()

  notam_ids = [notam.notam_id for notam in Notam.objects.all()]
  
  notams = [Notam(
    notam_id = f"{data['location'][0:2]} {data['id']}",
    airport = data["location"],
    qcode = data["Qcode"],
    message = data["message"] if len(data["message"]) < 511 else data["message"][:511],
    startdate = datetime.datetime(
      int(data["startdate"][0:4]),
      int(data["startdate"][5:7]),
      int(data["startdate"][8:10]),
      int(data["startdate"][11:13]),
      int(data["startdate"][14:16])),
    enddate = datetime.datetime(
      int(data["enddate"][0:4]),
      int(data["enddate"][5:7]),
      int(data["enddate"][8:10]),
      int(data["enddate"][11:13]),
      int(data["enddate"][14:16])),
    comment = util.comment(data["message"], data["Qcode"])
  ) for data in notamdata if f"{data['location'][0:2]} {data['id']}" not in notam_ids and data["Qcode"] in 
                          ["MRLC", "FAAH", "STAH", "FALC", 
                          "ATCA", "SPAH", "ACAH", "AECA",
                          "PIAU", "ICCT", "ICAS", "ISAS",
                          "IGAS", "ILAS", "IUAS", "FIAU"]]

  Notam.objects.bulk_create(notams)

  return redirect(reverse_lazy("notam_list"))


@method_decorator(login_required, name='dispatch')
class NotamListView(ListView):
  model = Notam
  context_object_name = 'notams'
  template_name = 'notams.html'

@staff_member_required
def cleanup(request):
  now = datetime.datetime.now()
  Notam.objects.filter(enddate__lt=now).delete()

  return redirect(reverse_lazy("notam_list"))


@method_decorator(staff_member_required, name='dispatch')
class NotamCreateView(CreateView):
  model = Notam
  form_class = NotamForm
  success_url = reverse_lazy("notam_list")
  template_name = "notam_create.html"


@method_decorator(staff_member_required, name='dispatch')
class NotamUpdateView(UpdateView):
  model = Notam
  form_class = NotamForm
  template_name = "notam_update.html"
  success_url = reverse_lazy("notam_list")


@method_decorator(staff_member_required, name='dispatch')
class NotamDeleteView(DeleteView):
  model = Notam
  success_url = reverse_lazy("notam_list")