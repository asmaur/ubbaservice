from rest_framework.serializers import ModelSerializer
from core.models import (
    Pet,
    Tutor,
    Contact,
    Petname,
    Tag
)
from care.v1.serializers import VetSerializer


class PetnameSerializer(ModelSerializer):
    class Meta:
        model = Petname
        fields = "__all__"


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ContactPublicSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "name",
            "email",
            "phone",
            "social",
            "emergency",
        )


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "social",
            "mine",
            "emergency",
            "instagram",
            "tiktok",
            "whatsapp"
            # "tutor",
        )


class TutorPublicSerializer(ModelSerializer):
    contacts = ContactPublicSerializer(many=True)

    class Meta:
        model = Tutor
        fields = (
            "id",
            "name",
            "contacts"
        )


class TutorSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        fields = "__all__"


class PetNameSerializer(ModelSerializer):
    class Meta:
        model = Petname
        fields = ("pet_name",)


class PetPublicSerializer(ModelSerializer):
    tutor = TutorPublicSerializer()
    petname = PetNameSerializer()
    tag = TagSerializer()
    vet = VetSerializer()

    class Meta:
        model = Pet
        fields = (
                "tag",
                "name",
                "race",
                "birth_date",
                "castration",
                "genre",
                "lost",
                "image",
                "petname",
                "tutor"
        )


class PetSerializer(ModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = (
            "id",
            "tag",
            "name",
            "nickname",
            "image",
            "registered",
            "alive",
            "lost",
            "pet_type",
            "race",
            "birth_date",
            "castration",
            "genre",
            "observation",
            "medical_condition",
        )

    def create(self, validated_data):
        # validated_data.pop("uuid")
        return Pet.objects.create(**validated_data)


class PetMiniSerializer(ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = Pet
        fields = (
            # "id",
            "tag",
            "name",
            "registered",
            "race",
            "lost",
            "image",
            "birth_date",
            "castration",
            "genre",
        )


class PetDetailSerializer(ModelSerializer):
    tag = TagSerializer()
    tutor = TutorPublicSerializer()
    petname = PetnameSerializer()
    veterinarian = VetSerializer()

    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "nickname",
            "race",
            "birth_date",
            "castration",
            "registered",
            "alive",
            "lost",
            "pet_type",
            "genre",
            "image",
            "observation",
            "medical_condition",
            "tag",
            "petname",
            "tutor",
            "veterinarian"
        )
