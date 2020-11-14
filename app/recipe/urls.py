from django.urls import  path, include
from rest_framework.routers import  DefaultRouter

from recipe import  views 
# the default router is a feature of rest framework which automatically 
# generate urls for our viewset. 
router = DefaultRouter()
# i gonna give it a name of tags
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls))
]
