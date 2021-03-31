from django.urls import path
from .views import DataView, call, home, NotamListView, NotamSelectView, AirportView, cleanup, NotamCreateView, NotamUpdateView, NotamDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('call/', call, name='call'),
    path('upload/', DataView.as_view(), name='upload'),
    path('upload-airports/', AirportView.as_view(), name='upload_airports'),
    path('select/', NotamSelectView.as_view(), name='notam_select'),
    path('notams/', NotamListView.as_view(), name='notam_list'),
    path('create-notam/', NotamCreateView.as_view(), name='notam_create'),
    path('<int:pk>/update/', NotamUpdateView.as_view(), name='notam_update'),
    path('<int:pk>/delete/', NotamDeleteView.as_view(), name='notam_delete'),
    path('cleanup/', cleanup, name='cleanup'),
]