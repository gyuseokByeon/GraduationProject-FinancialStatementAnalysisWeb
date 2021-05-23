"""
config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('core.urls', namespace='core')),
    path("corps/", include('corps.urls', namespace='corps')),
    path("financials/", include('financial_statements.urls', namespace='financials')),
    path("incomes/", include('income_states.urls', namespace='incomes')),
    path("stocks/", include('stocks.urls', namespace='stocks')),
    path("users/", include('users.urls', namespace='users')),
    path("reviews/", include('reviews.urls', namespace='reviews')),
    path("discussions/", include('discussions.urls', namespace='discussions')),
    path("lists/", include('lists.urls', namespace='lists')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)