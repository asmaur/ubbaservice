from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from random import randint


class Serie(models.Model):
    serie = models.CharField(_("Serie: KMSX0001"), max_length=50)
    active = models.BooleanField(_("Status"), default=True)
    created_at = models.DateField(
        _("Created at "),
        auto_now=False,
        auto_now_add=False
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.serie


class Allotment(models.Model):
    quantity = models.IntegerField(
        _(""),
        validators=[MinValueValidator(1), MaxValueValidator(100000)]
    )
    created_at = models.DateField(_(""), auto_now=False, auto_now_add=False)
    active = models.BooleanField(_("Status"), default=True)
    lot_number = models.CharField(_("Lot Num: A100001"), max_length=50)
    description = models.TextField(
        _(""),
        blank=True,
        null=True
    )
    serie = models.ForeignKey(
        "core.Serie",
        related_name="series",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Allotment'
        verbose_name_plural = 'Allotments'

    def __str__(self):
        return self.lot_number


def generate_tag_id():
    return uuid.uuid4().hex[:15].upper()


def rup_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def rup_generate():
    while True:
        cpf = [randint(0, 9) for _ in range(9)]
        if cpf != cpf[::-1]:
            break

    #  Gera os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        cpf.append(digit)

    #  Retorna o CPF como string
    result = ''.join(map(str, cpf))
    return result


class Address(models.Model):
    country = models.CharField(
        _("Country"),
        max_length=50,
        blank=True,
        null=True
    )
    state = models.CharField(
        _("State"),
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        _("City"),
        max_length=50,
        blank=True,
        null=True
    )
    neighbor = models.CharField(
        _("Neighbor"),
        max_length=50,
        blank=True,
        null=True
    )
    street = models.CharField(
        _("Street"),
        max_length=50,
        blank=True,
        null=True
    )
    number = models.CharField(
        _("Number"),
        max_length=50,
        blank=True,
        null=True
    )
    complement = models.CharField(
        _("Complemento"),
        max_length=50,
        blank=True,
        null=True
    )
    zip_code = models.CharField(
        _("Zip"),
        max_length=50,
        blank=True,
        null=True
    )

    tutor = models.ForeignKey(
        "core.Tutor",
        related_name="addresses",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    veterinarian = models.ForeignKey(
        "care.Veterinarian",
        related_name="addresses",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.CharField(
        _("uuid"),
        max_length=50,
        default=generate_tag_id,
        unique=True,
        editable=True
    )
    registered = models.BooleanField(_("Scanned"), default=False)
    exported = models.BooleanField(_("Exported"), default=False)
    active = models.BooleanField(_("Active"), default=True)
    url = models.URLField(_("tag url"), max_length=200)
    created_at = models.DateField(
        _("Created at"),
        auto_now=False,
        auto_now_add=False
    )
    allotment = models.ForeignKey(
        "core.Allotment",
        verbose_name=_("Allotment"),
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return f"{self.uuid.__str__()}"


class Tutor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Complete Name"),
        max_length=50,
        blank=True,
    )
    email = models.EmailField(
        _("Email"),
        max_length=254,
        unique=True
    )
    user = models.OneToOneField(
        "account.User",
        verbose_name=_(""),
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        _(""),
        upload_to="tutor_storage",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True
    )

    phone = models.CharField(
        _("Phone number"),
        max_length=50,
        blank=True,
        null=True
    )
    # whatsapp = models.CharField(
    #     _("whatsapp number"),
    #     max_length=200,
    #     blank=True,
    #     null=True
    # )
    instagram = models.CharField(
        _("instagram"), max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutors'

    def __str__(self):
        return self.user.name


class Contact(models.Model):
    name = models.CharField(
        _("name"),
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        _("email"),
        max_length=254,
        blank=True,
        null=True
    )

    phone = models.CharField(_("Phone number"), max_length=50)
    social = models.BooleanField(_("is whatsapp?"), default=True)
    emergency = models.BooleanField(_("is emergency number?"), default=False)
    whatsapp = models.CharField(
        _("whatsapp number"),
        max_length=200,
        blank=True,
        null=True
    )
    instagram = models.CharField(
        _("instagram"), max_length=200,
        blank=True,
        null=True
    )
    twitter = models.CharField(
        _("twitter"), max_length=200,
        blank=True,
        null=True
    )
    facebook = models.CharField(
        _("facebook"),
        max_length=200,
        blank=True,
        null=True
    )
    tiktok = models.CharField(
        _("tiktok"),
        max_length=200,
        blank=True,
        null=True
    )
    youtube = models.CharField(
        _("youtube"),
        max_length=200,
        blank=True,
        null=True
    )
    snapchat = models.CharField(
        _("snapchat"),
        max_length=200,
        blank=True,
        null=True
    )
    wechat = models.CharField(
        _("wechat"),
        max_length=200,
        blank=True,
        null=True
    )
    telegram = models.CharField(
        _("telegram"),
        max_length=200,
        blank=True,
        null=True
    )
    threads = models.CharField(
        _("threads"),
        max_length=200,
        blank=True,
        null=True
    )
    mine = models.BooleanField(_("is this number yours?"), default=True)
    tutor = models.ForeignKey(
        "core.Tutor",
        related_name="contacts",
        on_delete=models.CASCADE
    )
    # address = models.ForeignKey(
    #     "core.Address",
    #     verbose_name=_(""),
    #     on_delete=models.CASCADE,
    #     related_name="contacts",
    #     blank=True,
    #     null=True
    # )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        ordering = ("name",)

    def __str__(self):
        return self.name


class Petname(models.Model):
    # @frida
    petname = models.CharField(max_length=20, unique=True, db_index=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Petname'
        verbose_name_plural = 'Petnames'

    def __str__(self):
        return self.pet_name


class Pet(models.Model):
    # genre
    MALE = 'Male'
    FEMALE = 'Female'
    # pet type
    DOG = 'Dog'
    CAT = 'Cat'
    BIRD = "Bird"
    REPTILE = "Reptile"
    OTHER = "Other"

    GENRE_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, "Other")
    )

    # pet type
    PET_TYPE_CHOICES = (
        (DOG, 'Dog'),
        (CAT, 'Cat'),
        (BIRD, "Bird"),
        (REPTILE, "Reptile"),
        (OTHER, "Other")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.OneToOneField(
        "core.Tag",
        verbose_name=_("UUID"),
        on_delete=models.CASCADE
    )
    # ru = models.CharField(
    #     _("Registro Univ"),
    #     max_length=15,
    #     unique=True,
    #     default=rup_generate,
    #     validators=[rup_validate]
    # )
    petname = models.OneToOneField(
        "core.Petname",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    nickname = models.CharField(
        _("apelido"),
        max_length=50,
        blank=True,
        null=True
    )
    pet_type = models.CharField(
        max_length=20,
        choices=PET_TYPE_CHOICES,
        default=DOG
    )
    rg_link = models.CharField(
        _("RG Pet Link"),
        max_length=250,
        blank=True,
        null=True
    )
    rg_numero = models.CharField(
        _("RG Pet Link"),
        max_length=50,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=50)
    race = models.CharField(max_length=50)
    birth_date = models.DateField()
    castration = models.BooleanField(_("Castraded"), default=False)
    registered = models.BooleanField(_("Registered"), default=True)
    alive = models.BooleanField(_("Alive"), default=True)
    lost = models.BooleanField(_("Lost pet"), default=False)
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default=MALE
    )
    observation = models.TextField(_("Observation"), blank=True, null=True)
    medical_condition = models.TextField(
        _("Medical Condition"),
        blank=True,
        null=True
    )
    image = models.ImageField(
        _(""),
        upload_to="storage",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True
    )
    tutor = models.ForeignKey(
        "core.Tutor",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    # veterinarian = models.ForeignKey(
    #     "care.Veterinarian",
    #     verbose_name=_("Vet"),
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )

    joined_date = models.DateTimeField(
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
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ("joined_date",)

    def __str__(self):
        return self.name

    @property
    def age(self):
        return int(timezone.now().year - self.birth_date.year)


class PetLost(models.Model):
    pet = models.ForeignKey(
        "core.Pet",
        verbose_name=_(""),
        on_delete=models.CASCADE
    )
    lost_date = models.DateField(
        _(""),
        blank=True,
        null=True,
        auto_now=False,
        auto_now_add=False
    )


class PetDeath(models.Model):
    pet = models.OneToOneField(
        "core.Pet",
        verbose_name=_(""),
        on_delete=models.CASCADE
    )
    death_date = models.DateField(
        _(""),
        blank=True,
        null=True,
        auto_now=False,
        auto_now_add=False
    )
    death_reason = models.CharField(
        _(""),
        max_length=255,
        blank=True,
        null=True
    )
