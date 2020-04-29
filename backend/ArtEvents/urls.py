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
from django.conf import settings

urlpatterns = {
    url(r'^admin/', admin.site.urls),
    url(r'^$', dashViews.home),
    url(r'^music/$', musicViews.ShowEvents),
    url(r'^music/search/$', musicViews.QueryEvents),
    url(r'^contact/$', dashViews.get),
    url(r'^contact/subscribe/$', dashViews.post),
    path(r'detail/', musicViews.detail)
    # path('event/<int:post_pk>', musicViews.detail) /detail?eid=
}

