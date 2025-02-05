from rest_framework import serializers
from care.models import Veterinarian, Contact, VaccinationCard, Photo


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class VetSerializer(serializers.ModelSerializer):
    # contacts = ContactSerializer(many=True)

    class Meta:
        model = Veterinarian
        fields = [
            "id",
            "doctor_name",
            "hospital_name",
            "doctor_crm",
            "email",
            "phone",
            "instagram",
            "tiktok"
        ]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            "id",
            "image",
            "created_date"
        ]


class VaccineCardSerializer(serializers.ModelSerializer):
    cards = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = VaccinationCard
        fields = [
            "cards"
        ]
