from django.urls import path, include

urlpatterns = [
    path('api/', include('vadmin.api')),
    path('article_api/', include('vadmin.article_api'))
]