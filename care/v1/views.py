import traceback
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from account.firebase_auth import FirebaseAuthentication
from ..models import VaccinationCard, Photo, Veterinarian
from .serializers import VaccineCardSerializer, PhotoSerializer, VetSerializer
from core.models import Pet, Tutor


class VaccineCardViewset(viewsets.ModelViewSet):
    queryset = VaccinationCard.objects.all()
    serializer_class = VaccineCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    parser_classes = [MultiPartParser, JSONParser]

    @action(methods=["GET"], detail=True, url_path="vaccine-cards")
    def get_pet_vaccine_cards(self, request, *args, **kwargs):
        try:
            tutor = Tutor.objects.get(user=request.user)
            pet = Pet.objects.get(tutor=tutor)
            cards = VaccinationCard.objects.all(pet=pet)
            serializer = VaccineCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            tutor = Tutor.objects.get(user=request.user)
            pet = Pet.objects.get(tutor=tutor)
            cards = VaccinationCard.objects.all(pet=pet)
            serializer = VaccineCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            tutor = Tutor.objects.get(user=request.user)
            pet = Pet.objects.get(tutor=tutor)
            card, _ = VaccinationCard.objects.get_or_create(pet=pet)
            # pet.image = request.FILES.get("pet-vaccine")
            photo = Photo.objects.create(
                image=request.FILES.get("pet-vaccine"),
                vaccines=card
            )
            photo.save()
            serializer = PhotoSerializer(photo, context={'request': request})
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            traceback.print_exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            Photo.objects.get(pk=kwargs.get("pk")).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            traceback.print_exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VetViewset(viewsets.ModelViewSet):
    queryset = Veterinarian.objects.all()
    serializer_class = VetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self, ):
        tutor = self.get_tutor()
        return Veterinarian.objects.filter(tutor=tutor)

    def get_tutor(self,):
        request = self.get_serializer_context().get('request')
        return Tutor.objects.get(user=request.user)

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

            serializer = VetSerializer(
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
            vet = Veterinarian.objects.get(
                id=data.pop("id"),
            )
            # tutor = self.get_tutor()

            serializer = VetSerializer(
                data={
                    **data,
                },
                partial=True,
                instance=vet,
                context={'request': request}
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        except ValidationError as e:
            traceback.print_exception(e)
            return Response()
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
