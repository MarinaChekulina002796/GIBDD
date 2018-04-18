from django.conf.urls import url
from django.conf.urls.static import static
from gibdd_app.views import *
from gibdd_app.views import main
from gibdd_application import settings

urlpatterns = [
                  url(r'^$', main, name='main'),
                  url(r'^login/', login, name='login'),
                  url(r'^forbidden/', forbidden, name='forbidden'),
                  url(r'^logout/', logout, name='logout'),
                  url(r'^gibdd/', gibdd, name='gibdd'),
                  url(r'^participants/', participants, name='participants'),
                  url(r'^services/', services, name='services'),
                  url(r'^workers/', workers, name='workers'),
                  url(r'^statistics/', statistics, name='statistics'),
                  url(r'^stat_chart_1/', chart_view, name='stat_chart_1'),
                  url(r'^contacts/', contacts, name='contacts'),
                  url(r'^med_list/$', med_list, name='med_list'),
                  url(r'^med/detail/(?P<pk>\d+)/$', med_detail, name='med_detail'),
                  url(r'^med/create/$', add_med, name='med_create'),
                  url(r'^med/(?P<pk>\d+)/update/$', update_med, name='med_update'),
                  url(r'^med/delete/(?P<pk>\d+)/$', delete_med, name='med_delete'),
                  url(r'^categ_list/$', categ_list, name='categ_list'),
                  url(r'^categ/detail/(?P<pk>\d+)/$', categ_detail, name='categ_detail'),
                  url(r'^categ/create/$', add_category, name='categ_create'),
                  url(r'^categ/(?P<pk>\d+)/update/$', update_categ, name='categ_update'),
                  url(r'^categ/delete/(?P<pk>\d+)/$', delete_categ, name='categ_delete'),
                  url(r'^license_list/$', license_list, name='license_list'),
                  url(r'^license/detail/(?P<pk>\d+)/$', license_detail, name='license_detail'),
                  url(r'^license/create/$', add_license, name='license_create'),
                  url(r'^license/(?P<pk>\d+)/update/$', update_license, name='license_update'),
                  url(r'^license/delete/(?P<pk>\d+)/$', delete_license, name='license_delete'),
                  url(r'^driver_list/$', driver_list, name='driver_list'),
                  url(r'^driver/detail/(?P<pk>\d+)/$', driver_detail, name='driver_detail'),
                  url(r'^driver/create/$', add_driver, name='driver_create'),
                  url(r'^driver/(?P<pk>\d+)/update/$', update_driver, name='driver_update'),
                  url(r'^driver/delete/(?P<pk>\d+)/$', delete_driver, name='driver_delete'),
                  url(r'^disq_list/$', disq_list, name='disq_list'),
                  url(r'^disq/detail/(?P<pk>\d+)/$', disq_detail, name='disq_detail'),
                  url(r'^disq/create/$', add_disq, name='disq_create'),
                  url(r'^disq/(?P<pk>\d+)/update/$', update_disq, name='disq_update'),
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
                  url(r'^autoschool/create/$', add_autoschool, name='autoschool_create'),
                  url(r'^history/create/$', add_history, name='history_create'),
                  url(r'^diagnostic_card/create/$', add_diagnostic_card, name='diagnostic_card_create'),
                  url(r'^insurance/create/$', add_insurance, name='insurance_create'),
                  url(r'^insurance_license/create/$', add_insurance_license, name='insurance_license_create'),
                  url(r'^accident_car/create/$', add_accident_car, name='accident_car_create'),
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
                  url(r'^search_accidents_by_date/$', search_accidents_by_date, name="search_accidents_by_date"),
                  url(r'^accident_list/$', accident_list, name='accident_list'),
                  url(r'^accident/detail/(?P<pk>\d+)/$', accident_detail, name='accident_detail'),
                  url(r'^accident/(?P<pk>\d+)/update/$', update_accident, name='accident_update'),
                  url(r'^accident/delete/(?P<pk>\d+)/$', delete_accident, name='accident_delete'),
                  url(r'^car_reg_plan/$', car_reg_plan, name='car_reg_plan'),
                  url(r'^reg_accident/$', reg_accident, name='reg_accident'),
                  url(r'^europrotocol_instuction/$', europrotocol, name='europrotocol'),
                  url(r'^change_dr_license/$', change_dr_license, name='change_dr_license'),
                  url(r'^med003/$', med003, name='med003'),
                  url(r'^car_list/$', car_list, name='car_list'),
                  url(r'^car/detail/(?P<pk>\d+)/$', car_detail, name='car_detail'),
                  url(r'^car/(?P<pk>\d+)/update/$', update_car, name='car_update'),
                  url(r'^car/delete/(?P<pk>\d+)/$', delete_car, name='car_delete'),
                  url(r'^lic_cat_list/$', lic_cat_list, name='lic_cat_list'),
                  url(r'^lic_cat/detail/(?P<pk>\d+)/$', lic_cat_detail, name='lic_cat_detail'),
                  url(r'^lic_cat/(?P<pk>\d+)/update/$', update_lic_cat, name='lic_cat_update'),
                  url(r'^lic_cat/delete/(?P<pk>\d+)/$', delete_lic_cat, name='lic_cat_delete'),
                  url(r'^witness_list/$', witness_list, name='witness_list'),
                  url(r'^witness/detail/(?P<pk>\d+)/$', witness_detail, name='witness_detail'),
                  url(r'^witness/(?P<pk>\d+)/update/$', update_witness, name='witness_update'),
                  url(r'^witness/delete/(?P<pk>\d+)/$', delete_witness, name='witness_delete'),
                  url(r'^licen_accid_list/$', licen_accid_list, name='licen_accid_list'),
                  url(r'^licen_accid/detail/(?P<pk>\d+)/$', licen_accid_detail, name='licen_accid_detail'),
                  url(r'^licen_accid/(?P<pk>\d+)/update/$', update_licen_accid, name='licen_accid_update'),
                  url(r'^licen_accid/delete/(?P<pk>\d+)/$', delete_licen_accid, name='licen_accid_delete'),
                  url(r'^inspector_list/$', inspector_list, name='inspector_list'),
                  url(r'^inspector/detail/(?P<pk>\d+)/$', inspector_detail, name='inspector_detail'),
                  url(r'^inspector/(?P<pk>\d+)/update/$', update_inspector, name='inspector_update'),
                  url(r'^inspector/delete/(?P<pk>\d+)/$', delete_inspector, name='inspector_delete'),
                  url(r'^fine_list/$', fine_list, name='fine_list'),
                  url(r'^fine/detail/(?P<pk>\d+)/$', fine_detail, name='fine_detail'),
                  url(r'^fine/(?P<pk>\d+)/update/$', update_fine, name='fine_update'),
                  url(r'^fine/delete/(?P<pk>\d+)/$', delete_fine, name='fine_delete'),
                  url(r'^registr_list/$', registr_list, name='registr_list'),
                  url(r'^registr/detail/(?P<pk>\d+)/$', registr_detail, name='registr_detail'),
                  url(r'^registr/(?P<pk>\d+)/update/$', update_registr, name='registr_update'),
                  url(r'^registr/delete/(?P<pk>\d+)/$', delete_registr, name='registr_delete'),
                  url(r'^owner_list/$', owner_list, name='owner_list'),
                  url(r'^owner/detail/(?P<pk>\d+)/$', owner_detail, name='owner_detail'),
                  url(r'^owner/(?P<pk>\d+)/update/$', update_owner, name='owner_update'),
                  url(r'^owner/delete/(?P<pk>\d+)/$', delete_owner, name='owner_delete'),
                  url(r'^steal_list/$', steal_list, name='steal_list'),
                  url(r'^steal/detail/(?P<pk>\d+)/$', steal_detail, name='steal_detail'),
                  url(r'^steal/(?P<pk>\d+)/update/$', update_steal, name='steal_update'),
                  url(r'^steal/delete/(?P<pk>\d+)/$', delete_steal, name='steal_delete'),
                  url(r'^decree_list/$', decree_list, name='decree_list'),
                  url(r'^decree/detail/(?P<pk>\d+)/$', decree_detail, name='decree_detail'),
                  url(r'^decree/(?P<pk>\d+)/update/$', update_decree, name='decree_update'),
                  url(r'^decree/delete/(?P<pk>\d+)/$', delete_decree, name='decree_delete'),
                  url(r'^camera_list/$', camera_list, name='camera_list'),
                  url(r'^camera/detail/(?P<pk>\d+)/$', camera_detail, name='camera_detail'),
                  url(r'^camera/(?P<pk>\d+)/update/$', update_camera, name='camera_update'),
                  url(r'^camera/delete/(?P<pk>\d+)/$', delete_camera, name='camera_delete'),
                  url(r'^autoschool_list/$', autoschool_list, name='autoschool_list'),
                  url(r'^autoschool/detail/(?P<pk>\d+)/$', autoschool_detail, name='autoschool_detail'),
                  url(r'^autoschool/(?P<pk>\d+)/update/$', update_autoschool, name='autoschool_update'),
                  url(r'^autoschool/delete/(?P<pk>\d+)/$', delete_autoschool, name='autoschool_delete'),
                  url(r'^history_list/$', history_list, name='history_list'),
                  url(r'^history/detail/(?P<pk>\d+)/$', history_detail, name='history_detail'),
                  url(r'^history/(?P<pk>\d+)/update/$', update_history, name='history_update'),
                  url(r'^history/delete/(?P<pk>\d+)/$', delete_history, name='history_delete'),
                  url(r'^diagnostic_card_list/$', diagnostic_card_list, name='diagnostic_card_list'),
                  url(r'^diagnostic_card/detail/(?P<pk>\d+)/$', diagnostic_card_detail, name='diagnostic_card_detail'),
                  url(r'^diagnostic_card/(?P<pk>\d+)/update/$', update_diagnostic_card, name='diagnostic_card_update'),
                  url(r'^diagnostic_card/delete/(?P<pk>\d+)/$', delete_diagnostic_card, name='diagnostic_card_delete'),
                  url(r'^insurance_list/$', insurance_list, name='insurance_list'),
                  url(r'^insurance/detail/(?P<pk>\d+)/$', insurance_detail, name='insurance_detail'),
                  url(r'^insurance/(?P<pk>\d+)/update/$', update_insurance, name='insurance_update'),
                  url(r'^insurance/delete/(?P<pk>\d+)/$', delete_insurance, name='insurance_delete'),
                  url(r'^insurance_license_list/$', insurance_license_list, name='insurance_license_list'),
                  url(r'^insurance_license/detail/(?P<pk>\d+)/$', insurance_license_detail,
                      name='insurance_license_detail'),
                  url(r'^insurance_license/(?P<pk>\d+)/update/$', update_insurance_license,
                      name='insurance_license_update'),
                  url(r'^insurance_license/delete/(?P<pk>\d+)/$', delete_insurance_license,
                      name='insurance_license_delete'),
                  url(r'^accident_car_list/$', accident_car_list, name='accident_car_list'),
                  url(r'^accident_car/detail/(?P<pk>\d+)/$', accident_car_detail, name='accident_car_detail'),
                  url(r'^accident_car/(?P<pk>\d+)/update/$', update_accident_car, name='accident_car_update'),
                  url(r'^accident_car/delete/(?P<pk>\d+)/$', delete_accident_car, name='accident_car_delete'),

                  url(r'^europrotocol/create/$', add_europrotocol, name='europrotocol_create'),
                  url(r'^europrotocol/$', europrotocol_list, name='europrotocol_list'),
                  url(r'^europrotocol/detail/(?P<pk>\d+)/$', europrotocol_detail, name='europrotocol_detail'),
                  url(r'^europrotocol/(?P<pk>\d+)/update/$', update_europrotocol, name='europrotocol_update'),
                  url(r'^europrotocol/delete/(?P<pk>\d+)/$', delete_europrotocol, name='europrotocol_delete'),

                  url(r'^autostudent/create/$', add_autostudent, name='autostudent_create'),
                  url(r'^autostudent/$', autostudent_list, name='autostudent_list'),
                  url(r'^autostudent/detail/(?P<pk>\d+)/$', autostudent_detail, name='autostudent_detail'),
                  url(r'^autostudent/(?P<pk>\d+)/update/$', update_autostudent, name='autostudent_update'),
                  url(r'^autostudent/delete/(?P<pk>\d+)/$', delete_autostudent, name='autostudent_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
