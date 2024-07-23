from django.urls import path
from rest_framework.routers import SimpleRouter
from core.v1 import views

app_name = "core"

router = SimpleRouter()

router.register('pets', views.PetViewset)
router.register('tutors', views.TutorViewset)
router.register('tutors-contact', views.ContactViewset)

urlpatterns = [
    path(
        "pets/petname/", views.PetNameViewset.as_view(
            {"post": "check_petname"}
        )
    ),
    path("pets/transfer/", views.PetViewset.as_view({"post": "transfer"})),
    path(
        "pets/<str:pk>/petname/", views.PetViewset.as_view(
            {"put": "set_petname"}
        )
    ),
    path(
        "pets/tag-status/", views.PetViewset.as_view(
            {"post": "check_tag_status"}
        )
    )
    # path("pets/public/", views.PetPublicDetail.as_view()),
    # path("pets/public/@<str:petname>", views.PetProfileDetail.as_view())
]

urlpatterns += router.urls
