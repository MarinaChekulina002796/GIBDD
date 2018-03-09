from django.conf.urls import url
from django.conf.urls.static import static

from gibdd_app import views
from gibdd_app.views import login, logout, services, gibdd, participants, workers, statistics, contacts, \
    medical_cert_all, add_med, update_med
# , rate, add_channel
from gibdd_app.views import main
# , item, new, registration
from gibdd_application import settings
# from gibdd_app.views import MedicalCertificateCreate,MedicalCertificateUpdate,MedicalCertificateDelete, LicenseCreate,
#     CategoryCreate

urlpatterns = [
                  url(r'^$', main, name='main'),
                  # url(r'^new$', new, name='new'),
                  # url(r'^item/(?P<id>\d+)$', item, name='item'),
                  # url(r'^add_channel/', add_channel, name='add_channel'),
                  # url(r'^registration/', registration, name='registration'),

                  url(r'^login/', login, name='login'),
                  url(r'^logout/', logout, name='logout'),
                  url(r'^gibdd/', gibdd, name='gibdd'),
                  url(r'^med_all/$', medical_cert_all, name='med_all'),
                  url(r'^participants/', participants, name='participants'),
                  url(r'^services/', services, name='services'),
                  url(r'^workers/', workers, name='workers'),
                  url(r'^statistics/', statistics, name='statistics'),
                  url(r'^contacts/', contacts, name='contacts'),
                  url(r'^med_create/$', add_med, name='med_create'),
                  url(r'^med_update/(?P<pk>\d+)/$', update_med, name='med_update'),
                  # url(r'^med/create/$', MedicalCertificateCreate.as_view(), name='med_create'),
                  # url(r'^med/(?P<pk>\d+)/update/$', MedicalCertificateUpdate.as_view(), name='med_update'),
                  # url(r'^med/(?P<pk>\d+)/delete/$', MedicalCertificateDelete.as_view(), name='med_delete'),
                  # url(r'^license/create/$', LicenseCreate.as_view(), name='license_create'),
                  # url(r'^category/create/$', CategoryCreate.as_view(), name='category_create'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
