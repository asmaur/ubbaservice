from rest_framework import serializers
from care.models import Veterinarian, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class VetSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Veterinarian
        fields = [
            "doctor_name",
            "hospital_name",
            "doctor_crm",
            "contacts"
        ]
