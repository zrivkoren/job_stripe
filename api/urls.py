from django.urls import include, re_path, path
from api.views import test_payment, get_item_page, get_checkout_session, success, cancel

urlpatterns = [
    re_path(r'^test-payment/$', test_payment),
    re_path(r'^item/(?P<id>\d+)/$', get_item_page),
    re_path(r'^buy/(?P<id>\d+)/$', get_checkout_session),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),

]
