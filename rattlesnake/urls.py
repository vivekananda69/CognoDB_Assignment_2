from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),        # Existing app routes
    path('', include('app.graph.urls')),  # Graph explorer routes
]