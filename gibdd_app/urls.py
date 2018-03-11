from django.conf.urls import url
from django.conf.urls.static import static
from gibdd_app.views import login, logout, services, gibdd, participants, workers, statistics, contacts, \
    med_list, delete_med, med_detail
from gibdd_app.views import main
from gibdd_application import settings
from gibdd_app.views import MedicalCertificateCreate, MedicalCertificateUpdate, LicenseCreate

urlpatterns = [
                  url(r'^$', main, name='main'),
                  url(r'^login/', login, name='login'),
                  url(r'^logout/', logout, name='logout'),
                  url(r'^gibdd/', gibdd, name='gibdd'),
                  url(r'^participants/', participants, name='participants'),
                  url(r'^services/', services, name='services'),
                  url(r'^workers/', workers, name='workers'),
                  url(r'^statistics/', statistics, name='statistics'),
                  url(r'^contacts/', contacts, name='contacts'),
                  url(r'^med_list/$', med_list, name='med_list'),
                  url(r'^med/detail/(?P<pk>\d+)/$', med_detail, name='med_detail'),
                  url(r'^med/create/$', MedicalCertificateCreate.as_view(), name='med_create'),
                  url(r'^med/(?P<pk>\d+)/update/$', MedicalCertificateUpdate.as_view(), name='med_update'),
                  url(r'^med/delete/(?P<pk>\d+)/$', delete_med, name='med_delete'),
                  url(r'^license/create/$', LicenseCreate.as_view(), name='license_create'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
