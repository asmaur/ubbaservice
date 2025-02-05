import re
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import Http404, get_object_or_404
from rest_framework.validators import ValidationError
from rest_framework import permissions
from account.firebase_auth import FirebaseAuthentication
# from oauth2_provider.contrib.rest_framework.authentication import (
#     OAuth2Authentication
# )
# from oauth2_provider.contrib.rest_framework.permissions import (
#     TokenHasReadWriteScope, TokenHasScope
# )
import traceback
from core.exceptions import (
    RegisteredTagException,
    NotTutorException,
    AlreadyTutorException
)
from core.error_messages import (
    TagErrorMessage,
    ContactErrorMessage,
    TutorErrorMessage,
    PetErrorMessage,
    UserErrorMessage,
)
from core.pagination import StandardResultsSetPagination
from core.models import (
    Pet,
    Petname,
    Tutor,
    # Serie,
    # Allotment,
    Tag,
    Contact
)
from .serializers import (
    PetSerializer,
    PetDetailSerializer,
    TutorSerializer,
    PetnameSerializer,
    ContactSerializer,
    TagSerializer
)
from account.models import (
    User
)
from ..permissions import UpdateOwnPet


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class PetPublic(viewsets.ViewSet):
    """Public view for pet by uuid

    Args:
        APIView (_type_): _description_
    """
    permission_classes = [ReadOnly]
    queryset = Pet.objects.all()

    def get_object(self, uuid):
        try:
            return Pet.objects.get(uuid=uuid)
        except Pet.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(uuid=kwargs.get("pk"))
            pet = Pet.objects.get(tag=tag)
            serializer = PetDetailSerializer(pet, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pet.DoesNotExist:
            return Response(
                PetErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tag.DoesNotExist:
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["GET"], detail=True, url_path="/tag-status/")
    def check_tag_status(self, request, pk=None, *args, **kwargs):
        """return tag status

        Args:
            request (_type_): _description_
        """
        try:
            tag = Tag.objects.get(uuid=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PetViewset(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # UpdateOwnPet
    ]
    authentication_classes = [FirebaseAuthentication]
    parser_classes = [MultiPartParser, JSONParser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, ):
        tutor = self.get_tutor()
        return Pet.objects.filter(tutor=tutor)

    def get_tutor(self,):
        request = self.get_serializer_context().get('request')
        return Tutor.objects.get(user=request.user)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            tag = Tag.objects.get(
                uuid=data.pop("tag"),
            )
            tutor = self.get_tutor()

            if tag.registered:
                raise RegisteredTagException

            serializer = PetSerializer(
                data={
                    "birth_date": data.pop("birth_date").split("T")[0],
                    **data,
                }
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save(tutor=tutor, tag=tag)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        except Tag.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tutor.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except RegisteredTagException:
            return Response(
                TagErrorMessage.get("already_registered"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as ex:
            traceback.print_exception(ex)
            return Response(
                TutorErrorMessage.get("validation_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(uuid=kwargs.get("pk"))
            pet = Pet.objects.get(tag=tag)
            serializer = PetDetailSerializer(pet, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pet.DoesNotExist:
            return Response(
                PetErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tag.DoesNotExist:
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            # page = self.paginate_queryset(queryset)
            # if page is not None:
            #     serializer = PetSerializer(
            #         page,
            #         many=True,
            #         context={'request': request}
            #     )
            #     return self.get_paginated_response(serializer.data)

            serializer = PetSerializer(
                queryset,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            tag = Tag.objects.get(
                uuid=data.pop("tag"),
            )
            pet = Pet.objects.get(tag=tag)
            tutor = self.get_tutor()

            if pet.tutor.id is not tutor.id:
                raise NotTutorException

            serializer = PetSerializer(
                data={
                    "birth_date": data.pop("birth_date").split("T")[0],
                    **data,
                },
                partial=True,
                instance=pet,
                context={'request': request}
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save(tutor=tutor, tag=tag)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        except Tag.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tutor.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )

        except ValidationError as e:
            traceback.print_exception(e)
            return Response(
                PetErrorMessage.get("validation_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    @action(methods=["PATCH"], detail=True)
    def lost(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            pet = get_object_or_404(Pet, pk=pk)
            pet.lost = data.get("lost")
            pet.save()
            return Response(
                PetSerializer(pet, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                PetErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["PATCH"], detail=True)
    def deceased(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            pet = get_object_or_404(Pet, pk=pk)
            pet.alive = data.get("alive")
            pet.save()
            return Response(
                PetSerializer(pet, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                PetErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["PATCH"], detail=True)
    def upload_image(self, request, pk=None, *args, **kwargs):
        try:
            pet = get_object_or_404(Pet, pk=pk)
            pet.image = request.FILES.get("pet-image")
            pet.save()
            return Response(
                PetSerializer(pet, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                PetErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["POST"], detail=False, url_path="/petname/")
    def check_petname(self, request, *args, **kwargs):
        try:
            data = request.data
            get_object_or_404(Petname, pet_name=data.get("petname"))
            return Response(
                {"detail": "message", "available": False},
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                {"detail": "message", "available": True},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            traceback.print_exception(ex)
            return Response("assafds")

    @action(methods=["PUT"], detail=True, url_path="/petname/")
    def set_petname(self, request, pk=None, *args, **kwargs):
        try:
            pet = Pet.objects.get(pk=pk)
            data = request.data
            if pet is None:
                raise Pet.DoesNotExist
            serializer = PetnameSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return Response(
                {"detail": "petname saved successfully"},
                status=status.HTTP_200_OK
            )
        except Pet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            traceback.print_exception(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["POST"], detail=False, url_path="/transfer/")
    def transfer(self, request, *args, **kwargs):
        try:
            data = request.data
            current_tutor = Tutor.objects.get(pk=data.get("current_tutor_id"))
            new_tutor = Tutor.objects.get(pk=data.get("new_tutor_id"))
            tag = Tag.objects.get(uuid=data.get("tag"))
            pet = Pet.objects.get(tag=tag)

            if pet.tutor.id != current_tutor.id:
                raise NotTutorException

            if pet.tutor.id == new_tutor.id:
                raise AlreadyTutorException

            pet.tutor = new_tutor
            pet.save()
            return Response(
                {
                    "detail": "Pet Transfer successfull"
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Tutor.DoesNotExist:
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tag.DoesNotExist:
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except NotTutorException:
            return Response(
                TutorErrorMessage.get("not_tutor_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except AlreadyTutorException:
            return Response(
                TutorErrorMessage.get("already_tutor_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["POST"], detail=False, url_path="/tag-status/")
    def check_tag_status(self, request, *args, **kwargs):
        """return tag status

        Args:
            request (_type_): _description_
        """
        try:
            data = request.data
            print(data)
            tag = Tag.objects.get(uuid=data.get("uuid"))
            # if tag.exported:
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response(
                TagErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TutorViewset(viewsets.ViewSet):
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    parser_classes = [MultiPartParser, JSONParser]

    def list(self, request, *args, **kwargs):
        return Response(TutorSerializer(self.queryset, many=True).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            tutor = Tutor.objects.get(pk=pk)
            serializer = TutorSerializer(tutor, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tutor.DoesNotExist:
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["GET"], detail=False, url_path="/tutor/")
    def get_tutor(self, request, *args, **kwargs):
        try:
            # user = User.objects.get(pk="5826a5ae-078a-4580-8e1d-9b1dbf7caf42") #ryry
            tutor = Tutor.objects.get(user=request.user)
            return Response(
                TutorSerializer(tutor).data,
                status=status.HTTP_200_OK
            )
        except Tutor.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["POST"], detail=False)
    def find_tutor(self, request, *args, **kwargs):
        try:
            data = request.data
            user = User.objects.get(email=data.get("email"))
            tutor = Tutor.objects.get(user=user)
            return Response(
                TutorSerializer(tutor, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                UserErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Tutor.DoesNotExist as e:
            traceback.print_exception(e)
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            tutor = Tutor.objects.get(pk=pk)
            serializer = TutorSerializer(
                data=data,
                instance=tutor,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Tutor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["PATCH"], detail=True, url_path="/tutor-image/")
    def update_image(self, request, pk=None, *args, **kwargs):
        try:
            tutor = get_object_or_404(Tutor, pk=pk)
            tutor.image = request.FILES.get("tutor-image")
            tutor.save()
            return Response(
                TutorSerializer(tutor, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PetNameViewset(viewsets.ViewSet):
    serializer_class = PetnameSerializer
    queryset = Pet.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]#OAuth2Authentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["petname"]
    search_fields = ["petname"]

    def update(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            petname = Petname.objects.get(pk=pk)
            serializer = PetnameSerializer(
                instance=petname,
                data=data,
                partial=True
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"detail": "message", "code": "288282"},
                    status=status.HTTP_200_OK
                )
        except Petname.DoesNotExist:
            return Response()


class ContactViewset(viewsets.ViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def get_tutor(self, request):
        # user = User.objects.get(pk="5826a5ae-078a-4580-8e1d-9b1dbf7caf42")
        return Tutor.objects.get(user=request.user)

    def list(self, request, *args, **kwargs):
        try:
            contacts = Contact.objects.filter(tutor=self.get_tutor(request))
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        serializer = None
        try:
            tutor = self.get_tutor(request)
            data = request.data
            phone = data.get("phone")
            whatsapp_number = re.sub(r"\D", "", phone)
            serializer = ContactSerializer(data={
                **data,
                "whatsapp": whatsapp_number,
            })
            if serializer.is_valid(raise_exception=True):
                serializer.save(tutor=tutor)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        except Tutor.DoesNotExist as ex:
            traceback.print_exception(ex)
            return Response(
                TutorErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as ex:
            traceback.print_exception(ex)
            return Response(
                ContactErrorMessage.get("validation_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None, *args, **kwargs):
        serializer = None
        try:
            data = request.data
            phone = data.get("phone")
            whatsapp_number = re.sub(r"\D", "", phone)
            contact = Contact.objects.get(pk=pk)
            serializer = ContactSerializer(
                {**data, "whatsapp": whatsapp_number},
                partial=True,
                instance=contact
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                ContactErrorMessage.get("validation_error"),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Contact.DoesNotExist:
            return Response(
                ContactErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            contact = Contact.objects.get(pk=pk)
            contact.delete()
            return Response(
                ContactErrorMessage.get("deleted"),
                status=status.HTTP_204_NO_CONTENT
            )
        except Contact.DoesNotExist:
            return Response(
                ContactErrorMessage.get("not_found"),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "at": traceback.format_exc(),
                    "error": "99991"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
