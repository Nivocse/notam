import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings 
from django.core.mail import send_mail 

from processing.models import Notam, Airport

# Create your views here.

def verbose_report(request):
    if request.method == "POST":
        subject = "verbose report"
        message = request.POST["message"].replace("<br>", "\n")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["botond@roff.hu"]
        send_mail(subject, message, email_from, recipient_list)
        return redirect(reverse_lazy("notam_list"))
    
    else:
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=24)
        notams = Notam.objects.filter(startdate__lt=end)
        airports = {airport.icao: airport.purpose for airport in Airport.objects.all()}
        base = {}
        for notam in sorted(notams, key=lambda x: x.airport):
            text = f"{base.get(notam.airport, '')}\n\t\t{notam.comment}".strip()
            if start < notam.startdate.replace(tzinfo=None) < end:
                text += f" FROM {str(notam.startdate)[8:16]}"
            if start < notam.enddate.replace(tzinfo=None) < end:
                text += f" TILL {str(notam.enddate)[8:16]}"
            if airports.get(notam.airport, "") == "BASE" and notam.comment.strip():
                base[notam.airport] = text
        dest = {}
        for notam in sorted(notams, key=lambda x: x.airport):
            text = f"{dest.get(notam.airport, '')}\n\t\t{notam.comment}".strip()
            if start < notam.startdate.replace(tzinfo=None) < end:
                text += f" FROM {str(notam.startdate)[8:16]}"
            if start < notam.enddate.replace(tzinfo=None) < end:
                text += f" TILL {str(notam.enddate)[8:16]}"
            if airports.get(notam.airport, "") == "DEST" and notam.comment.strip():
                dest[notam.airport] = text
        # data = {
        #     "BASE": base,
        #     "DEST": dest
            # "BASE": {notam.airport: notam.comment for notam in sorted(notams, key=lambda x: x.airport) if airports.get(notam.airport, "") == "BASE" and notam.comment.strip()},
            # "DEST": {notam.airport: notam.comment for notam in sorted(notams, key=lambda x: x.airport) if airports.get(notam.airport, "") == "DEST" and notam.comment.strip()}
        # }

        message = "BASE\n"
        for airport, notam in base.items():
            message += f"{airport}\t{notam}\n"
        message += "\nDEST\n"
        for airport, notam in dest.items():
            message += f"{airport}\t{notam}\n"


        context = {
            "message": message
        }
        return render(request, "report_preview.html", context=context)
    
