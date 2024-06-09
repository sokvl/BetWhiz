from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('Posts.urls')),
    path('games/', include('Matches.urls')),
    path('predict/', include('predictions.urls'))
]
