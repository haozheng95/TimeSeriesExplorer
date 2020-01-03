"""TimeSeriesExplorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url

from TimeSeriesExplorer.views import upload_view, report_view, result_view

urlpatterns = [
    url(r'^upload/', upload_view),
    url(r'^eda-report/(?P<task_id>.+)/', report_view),
    url(r'^jsonp/result/(?P<task_id>.+)\.js', result_view),
]
