from django.conf.urls import url
from django.conf.urls.static import static

from gibdd_app import views
from gibdd_app.views import login, logout, services, gibdd, participants, workers, statistics, contacts
# , rate, add_channel
from gibdd_app.views import main
# , item, new, registration
from gibdd_application import settings
from gibdd_app.views import MedicalCertificateCreate,MedicalCertificateUpdate,MedicalCertificateDelete

urlpatterns = [
                  url(r'^$', main, name='main'),
                  # url(r'^new$', new, name='new'),
                  # url(r'^item/(?P<id>\d+)$', item, name='item'),
                  # url(r'^add_channel/', add_channel, name='add_channel'),
                  # url(r'^registration/', registration, name='registration'),

                  url(r'^login/', login, name='login'),
                  url(r'^logout/', logout, name='logout'),
                  url(r'^gibdd/', gibdd, name='gibdd'),
                  url(r'^participants/', participants, name='participants'),
                  url(r'^services/', services, name='services'),
                  url(r'^workers/', workers, name='workers'),
                  url(r'^statistics/', statistics, name='statistics'),
                  url(r'^contacts/', contacts, name='contacts'),
                  url(r'^med/create/$', MedicalCertificateCreate.as_view(), name='med_create'),
                  url(r'^med/(?P<pk>\d+)/update/$', MedicalCertificateUpdate.as_view(), name='med_update'),
                  url(r'^med/(?P<pk>\d+)/delete/$', MedicalCertificateDelete.as_view(), name='med_delete'),
                  # url(r'^rate', rate, name='rate'),
                  # url(r'^subscribe/(?P<id>\d+)', views.SubscribeView.as_view(), name='subscribe'),
                  # url(r'^add_content', views.AddContent.as_view(), name='add_content'),
                  # # url(r'^subscribe/', subscribe, name='subscribe'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
