from django.conf.urls import url
from django.conf.urls.static import static
from gibdd_app.views import login, logout, services, gibdd, participants, workers, statistics, contacts, \
    med_list, delete_med, med_detail, categ_list, categ_detail, CategoryCreate, CategoryUpdate, delete_categ, \
    MedicalCertificateUpdate, license_list, license_detail, LicenseCreate, LicenseUpdate, delete_license, delete_driver, \
    driver_detail, DriverCreate, driver_list, DriverUpdate, disq_list, disq_detail, LicenseDisqualificationCreate, \
    LicenseDisqualificationUpdate, delete_disq, update_license, add_license, add_lic_cat, add_med, add_accident, \
    add_witness, add_licen_accid, add_inspector, add_fine, add_car, add_registr, add_owner, add_steal, add_decree, \
    add_camera, med_search, mix_search, mix_list_reg_auto_fine, mix_list_licen_fine, mix_search_licen_fine, \
    mix_list_VIN_stealing, mix_search_VIN_stealing, mix_list_VIN_history, mix_search_VIN_history, mix_list_VIN_accident, \
    mix_search_VIN_accident
# med_search
from gibdd_app.views import main
from gibdd_application import settings
from gibdd_app.views import MedicalCertificateCreate

# LicenseCreate

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
                  url(r'^med/create/$', add_med, name='med_create'),
                  url(r'^med/(?P<pk>\d+)/update/$', MedicalCertificateUpdate.as_view(), name='med_update'),
                  url(r'^med/delete/(?P<pk>\d+)/$', delete_med, name='med_delete'),
                  url(r'^categ_list/$', categ_list, name='categ_list'),
                  url(r'^categ/detail/(?P<pk>\d+)/$', categ_detail, name='categ_detail'),
                  url(r'^categ/create/$', CategoryCreate.as_view(), name='categ_create'),
                  url(r'^categ/(?P<pk>\d+)/update/$', CategoryUpdate.as_view(), name='categ_update'),
                  url(r'^categ/delete/(?P<pk>\d+)/$', delete_categ, name='categ_delete'),
                  url(r'^license_list/$', license_list, name='license_list'),
                  url(r'^license/detail/(?P<pk>\d+)/$', license_detail, name='license_detail'),
                  url(r'^license/create/$', add_license, name='license_create'),
                  # url(r'^license/create/$', LicenseCreate.as_view, name='license_create'),
                  url(r'^license/(?P<pk>\d+)/update/$', update_license, name='license_update'),
                  url(r'^license/delete/(?P<pk>\d+)/$', delete_license, name='license_delete'),
                  url(r'^driver_list/$', driver_list, name='driver_list'),
                  url(r'^driver/detail/(?P<pk>\d+)/$', driver_detail, name='driver_detail'),
                  url(r'^driver/create/$', DriverCreate.as_view(), name='driver_create'),
                  url(r'^driver/(?P<pk>\d+)/update/$', DriverUpdate.as_view(), name='driver_update'),
                  url(r'^driver/delete/(?P<pk>\d+)/$', delete_driver, name='driver_delete'),
                  url(r'^disq_list/$', disq_list, name='disq_list'),
                  url(r'^disq/detail/(?P<pk>\d+)/$', disq_detail, name='disq_detail'),
                  url(r'^disq/create/$', LicenseDisqualificationCreate.as_view(), name='disq_create'),
                  url(r'^disq/(?P<pk>\d+)/update/$', LicenseDisqualificationUpdate.as_view(), name='disq_update'),
                  url(r'^disq/delete/(?P<pk>\d+)/$', delete_disq, name='disq_delete'),
                  url(r'^lic_cat/create/$', add_lic_cat, name='lic_cat_create'),
                  url(r'^accident/create/$', add_accident, name='accident_create'),
                  url(r'^witness/create/$', add_witness, name='witness_create'),
                  url(r'^licen_accid/create/$', add_licen_accid, name='licen_accid_create'),
                  url(r'^inspector/create/$', add_inspector, name='inspector_create'),
                  url(r'^fine/create/$', add_fine, name='fine_create'),
                  url(r'^car/create/$', add_car, name='car_create'),
                  url(r'^reg/create/$', add_registr, name='registr_create'),
                  url(r'^owner/create/$', add_owner, name='owner_create'),
                  url(r'^steal/create/$', add_steal, name='steal_create'),
                  url(r'^decree/create/$', add_decree, name='decree_create'),
                  url(r'^camera/create/$', add_camera, name='camera_create'),
                  url(r'^med_search/$', med_search, name="med_search"),
                  url(r'^mix_list_reg_auto_fine/$', mix_list_reg_auto_fine, name='mix_list_reg_auto_fine'),
                  url(r'^mix_list_licen_fine/$', mix_list_licen_fine, name='mix_list_licen_fine'),
                  url(r'^mix_search/$', mix_search, name="mix_search"),
                  url(r'^mix_search_licen_fine/$', mix_search_licen_fine, name="mix_search_licen_fine"),
                  url(r'^mix_list_VIN_stealing/$', mix_list_VIN_stealing, name='mix_list_VIN_stealing'),
                  url(r'^mix_search_VIN_stealing/$', mix_search_VIN_stealing, name="mix_search_VIN_stealing"),
                  url(r'^mix_list_VIN_history/$', mix_list_VIN_history, name='mix_list_VIN_history'),
                  url(r'^mix_search_VIN_history/$', mix_search_VIN_history, name="mix_search_VIN_history"),
                  url(r'^mix_list_VIN_accident/$', mix_list_VIN_accident, name='mix_list_VIN_accident'),
                  url(r'^mix_search_VIN_accident/$', mix_search_VIN_accident, name="mix_search_VIN_accident"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
