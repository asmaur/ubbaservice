from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator


class Veterinarian(models.Model):
    doctor_name = models.CharField(_("Dr. Name"), max_length=50)
    hospital_name = models.CharField(_("Clinic name"), max_length=50)
    doctor_crm = models.CharField(_("Dr. CRM"), max_length=15)
    # pet = models.ForeignKey(
    #     "core.Pet",
    #     verbose_name=_("Pet"),
    #     related_name="vets",
    #     on_delete=models.CASCADE
    # )
    email = models.EmailField(
        _("email"),
        max_length=254,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _("Phone"),
        max_length=50,
        blank=True,
        null=True
    )
    instagram = models.URLField(
        _("Instagram"), max_length=200,
        blank=True,
        null=True
    )
    tiktok = models.URLField(
        _("Tiktok"),
        max_length=200,
        blank=True,
        null=True
    )
    image = models.ImageField(
        _(""),
        upload_to="vets_storage",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True
    )
    tutor = models.ForeignKey(
        "core.Tutor",
        related_name="vets",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'vet'
        verbose_name_plural = 'vets'
        ordering = ("doctor_name",)

    def __str__(self):
        return self.doctor_name


class Contact(models.Model):
    name = models.CharField(_("name"), max_length=50, blank=True, null=True)
    email = models.EmailField(
        _("email"),
        max_length=254,
        blank=True,
        null=True
    )
    phone = models.CharField(_("Phone"), max_length=50)
    social = models.BooleanField(_("Social"), default=True)
    mine = models.BooleanField(_("Is mine?"), default=True)
    emergency = models.BooleanField(_("Emergency"), default=True)
    instagram = models.URLField(
        _("Instagram"), max_length=200,
        blank=True,
        null=True
    )
    twitter = models.URLField(
        _("Twitter"),
        max_length=200,
        blank=True,
        null=True
    )
    facebook = models.URLField(
        _("Facebook"),
        max_length=200,
        blank=True,
        null=True
    )
    tiktok = models.URLField(
        _("Tiktok"),
        max_length=200,
        blank=True,
        null=True
    )
    # address = models.ForeignKey(
    #     "core.Address",
    #     verbose_name=_("Address"),
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True
    # )
    veterinarian = models.ForeignKey(
        "care.Veterinarian",
        verbose_name=_("Vet"),
        related_name="contacts",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ("name",)

    def __str__(self):
        return self.name


class Vaccine(models.Model):
    name = models.CharField(_(""), max_length=50)
    lot = models.CharField(_(""), max_length=50)
    veterinary = models.ForeignKey(
        "care.Veterinarian",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    pet = models.ForeignKey(
        "core.Pet",
        on_delete=models.CASCADE
    )
    injection_date = models.DateField(
        _(""),
        auto_now=False,
        auto_now_add=False
    )
    created_date = models.DateTimeField(
        _(""),
        auto_now=False,
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        _(""),
        auto_now=True,
        auto_now_add=False
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Vaccine'
        verbose_name_plural = 'Vaccines'

    def __str__(self):
        return self.name


class Vaccination(models.Model):
    # vaccine/profilaxia/medication
    name = models.CharField(_(""), max_length=50)
    lot = models.CharField(_(""), max_length=50)
    dose = models.CharField(_("Dose"), max_length=15)
    hospital_name = models.CharField(_("Clinic name"), max_length=50)
    doctor_crmv = models.CharField(_("Dr. CRMV"), max_length=15)
    neighborhood = models.CharField(_("Neighborhood"), max_length=50)
    municipality = models.CharField(_("Municipality"), max_length=50)
    state = models.CharField(_("state"), max_length=50)
    country = models.CharField(_("country"), max_length=50, default="Brasil")
    strategy = models.CharField(_("strategy"), max_length=15)
    doctor_name = models.CharField(_("Dr. Name"), max_length=50)
    pet = models.ForeignKey(
        "core.Pet",
        on_delete=models.CASCADE
    )
    injection_date = models.DateField(
        _(""),
        auto_now=False,
        auto_now_add=False
    )
    created_date = models.DateTimeField(
        _(""),
        auto_now=False,
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Weigh(models.Model):
    pet = models.ForeignKey(
        "core.Pet",
        verbose_name=_(""),
        on_delete=models.CASCADE
    )
    weight = models.FloatField(_(""))
    unit = models.CharField(_(""), max_length=5)
    created_date = models.DateTimeField(
        _(""),
        auto_now=False,
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        _(""),
        auto_now=True,
        auto_now_add=False
    )


class Medecine(models.Model):
    name = models.CharField(max_length=55)
    unit = models.CharField(max_length=15)
    instruction = models.TextField()
    caution = models.TextField()
    pet = models.ForeignKey(
        "core.Pet",
        related_name="medecines",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Treatment(models.Model):
    pet = models.ForeignKey(
        "core.Pet",
        verbose_name=_(""),
        related_name="treatments",
        on_delete=models.CASCADE
    )
    veterinary = models.ForeignKey(
        "care.Veterinarian",
        verbose_name=_(""),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    reason_visit = models.TextField(_("Reason for visit/ Diagnosis"))
    diagnosis = models.TextField(_("Assesment/ Diagnosis"))
    treatment = models.TextField(_("Treatment/ Recommendation"))
    initial_date = models.DateField(_(""), auto_now=False, auto_now_add=False)
    final_date = models.DateField(_(""), auto_now=False, auto_now_add=False)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Treatment'
        verbose_name_plural = 'Treatments'

    def __str__(self):
        return self.name


class Health(models.Model):
    pet = models.ForeignKey("core.Pet", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Health'
        verbose_name_plural = 'Healths'

    def __str__(self):
        return self.__class__.__name__


class Behavior(models.Model):
    name = models.CharField(_(""), max_length=50)
    health = models.ForeignKey(
        "care.Health",
        verbose_name=_(""),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(_(""), max_length=55)
    health = models.ForeignKey(
        "care.Health",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Mood(models.Model):
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    health = models.ForeignKey("care.Health", on_delete=models.CASCADE)


class Allergy(models.Model):
    name = models.CharField(_(""), max_length=50)
    description = models.CharField(_(""), max_length=255)
    pet = models.ForeignKey(
        "core.Pet",
        related_name="allergies",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=55)
    color = models.CharField(max_length=10, blank=True, null=True)
    icon = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        "care.Category",
        related_name="subcategories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=55)
    icon = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    is_default = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category.name} --> {self.name}"


class Record(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
        indexes = [
            models.Index(fields=["content_type", "object_id"])
        ]


class VaccinationCard(models.Model):
    pet = models.OneToOneField(
        "core.Pet",
        related_name="vaccines",
        on_delete=models.CASCADE
    )
    # image = models.ForeignKey(
    #     "care.Photo",
    #     verbose_name=_(""),
    #     on_delete=models.CASCADE
    # )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Photo(models.Model):
    image = models.ImageField(
        _("vaccine card"),
        upload_to="vaccine_cards"
    )
    vaccines = models.ForeignKey(
        "care.VaccinationCard",
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="cards"
    )
    created_date = models.DateTimeField(auto_now_add=True)
