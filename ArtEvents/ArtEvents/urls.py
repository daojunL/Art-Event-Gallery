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
from exhibition import views as exViews
from django.conf import settings

urlpatterns = {
    url(r'^admin/', admin.site.urls),
    url(r'^$', dashViews.home),
    url(r'^music/$', musicViews.MusicPage),
    url(r'^music/search/$', musicViews.MusicQuery),
    url(r'^theater/$', theaterViews.TheaterPage),
    url(r'^theater/search/$', theaterViews.TheaterQuery),
    url(r'^exhibition/$', exViews.ExhibitionPage),
    url(r'^exhibition/search/$', exViews.ExhibtionQuery),
    url(r'^contact/$', dashViews.ContactPage),
    url(r'^contact/subscribe/$', dashViews.subscribe),
    #path(r'detail/', musicViews.MusicDetail),
    path(r'detail/payment/', musicViews.payment),  # 可以写在payment app下
    path(r'paybill/', musicViews.write_pay_info)
}


