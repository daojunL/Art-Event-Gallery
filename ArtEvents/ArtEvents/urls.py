"""ArtEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from dashboard import views as dashViews
from music import views as musicViews
from theater import views as theaterViews
from exhibition import views as exhibitionViews
from payment import views as paymentViews
from django.conf import settings

urlpatterns = {
    url(r'^admin/', admin.site.urls),
    url(r'^$', dashViews.home),
    url(r'^music/$', musicViews.ShowEvents),
    url(r'^music/search/$', musicViews.QueryEvents),
    url(r'^contact/$', dashViews.get),
    url(r'^contact/subscribe/$', dashViews.subscribe),
    path(r'detail/', musicViews.detail),
    path(r'detail/payment/', paymentViews.payment),
    path(r'paybill/', paymentViews.write_pay_info),
    url(r'^theater/$', theaterViews.ShowEvents),
    url(r'^theater/search/$', theaterViews.QueryEvents),
    url(r'^exhibition/$', exhibitionViews.ShowEvents),
    url(r'^exhibition/search/$', exhibitionViews.QueryEvents),
    path(r'detailExp/', exhibitionViews.detail),
    url(r'cancel/$', paymentViews.get),
    url(r'^cancel/refund/$', paymentViews.cancel)
}

