from django.urls import path
from rest_framework.routers import SimpleRouter
from core.v1 import views

app_name = "core"

router = SimpleRouter()

router.register('pets', views.PetViewset)
router.register('tutors', views.TutorViewset)
router.register('contacts', views.ContactViewset)
router.register('p', views.PetPublic, basename="p")

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
    ),
    path(
        "pets/upload-image/<str:pk>/", views.PetViewset.as_view(
            {"patch": "upload_image"}
        )
    ),
    path(
        "pets/pet-lost/<str:pk>/", views.PetViewset.as_view(
            {"patch": "lost"}
        )
    ),
    path(
        "pets/pet-alive/<str:pk>/", views.PetViewset.as_view(
            {"patch": "deceased"}
        )
    ),
    path(
        "tutors/find-tutor/", views.TutorViewset.as_view(
            {"post": "find_tutor"}
        )
    ),
    path(
        "tutors/tutor-image/<str:pk>/", views.TutorViewset.as_view(
            {"patch": "update_image"}
        )
    ),
    path(
        "tutors/tutor/", views.TutorViewset.as_view(
            {"get": "get_tutor"}
        )
    ),
    path(
        "p/tag-status/<str:pk>/", views.PetPublic.as_view(
            {"get": "check_tag_status"}
        )
    ),
    # path("pets/public/<str:pk>/", views.PetPublicDetail.as_view()),
    # path("pets/public/@<str:petname>", views.PetProfileDetail.as_view())
]

urlpatterns += router.urls
