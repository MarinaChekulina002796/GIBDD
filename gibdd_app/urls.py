from django.conf.urls import url
from django.conf.urls.static import static

from gibdd_app import views
# from gibdd_app.views import login, logout, rate, add_channel
from gibdd_app.views import main
    # , item, new, registration
from gibdd_application import settings

urlpatterns = [
                  url(r'^$', main, name='main'),
                  # url(r'^new$', new, name='new'),
                  # url(r'^item/(?P<id>\d+)$', item, name='item'),
                  # url(r'^add_channel/', add_channel, name='add_channel'),
                  # url(r'^registration/', registration, name='registration'),
                  # url(r'^login/', login, name='login'),
                  # url(r'^logout/', logout, name='logout'),
                  # url(r'^rate', rate, name='rate'),
                  # url(r'^subscribe/(?P<id>\d+)', views.SubscribeView.as_view(), name='subscribe'),
                  # url(r'^add_content', views.AddContent.as_view(), name='add_content'),
                  # # url(r'^subscribe/', subscribe, name='subscribe'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
