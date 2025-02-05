from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

app_name = "care"

router = SimpleRouter()

router.register('vaccines', views.VaccineCardViewset)
router.register('vets', views.VetViewset)

urlpatterns = [
    path(
        "vaccines/vaccine-card/", views.VaccineCardViewset.as_view(
            {"get": "get_pet_vaccine_cards"}
        )
    ),
]

urlpatterns += router.urls
