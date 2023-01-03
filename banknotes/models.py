from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

CONDITION_CHOICES = (
    ("UNC", _("Uncirculated")),
    ("AU", _("About Uncirculated")),
    ("XF", _("Extremely Fine")),
    ("VF", _("Very Fine")),
    ("F", _("Fine")),
    ("VG", _("Very Good")),
    ("G", _("Good")),
    ("PR", _("Poor")),
)


class Album(models.Model):
    """
    Banknote album model.
    """

    name = models.CharField(
        max_length=50, unique=True, help_text=_("Album name"), verbose_name=_("name")
    )
    description = models.CharField(
        max_length=200, help_text=_("Album description"), verbose_name=_("description")
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_("Album owner"),
        verbose_name=_("owner"),
    )

    def get_absolute_url(self):
        return reverse(
            "album_detail_view",
            args=[
                str(self.id),
                str(slugify(self.name)),
            ],
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("album")
        ordering = ("name",)


class Banknote(models.Model):
    """
    Banknote model.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_("Banknote owner"),
        verbose_name=_("owner"),
    )
    country = models.CharField(
        _("country"), max_length=100, help_text=_("Banknote country (e.g. Venezuela)")
    )
    denomination = models.CharField(
        _("denomination"),
        max_length=30,
        help_text=_("Banknote denomination (e.g. 100)"),
    )
    currency = models.CharField(
        _("currency"), max_length=25, help_text=_("Banknote currency (e.g. Bolívares)")
    )
    pick_number = models.CharField(
        _("pick number"),
        max_length=7,
        help_text=_("Pick number code (e.g. 59a)"),
        blank=True,
    )
    issued_date = models.CharField(
        _("issued date"),
        max_length=30,
        help_text=_(
            "Issued date of the banknote, ND stands for No Date in the banknote (e.g. ND(1980))"
        ),
        blank=True,
    )
    year = models.IntegerField(
        _("year"), help_text=_("Enter 4 digits year (e.g. 1980)")
    )
    description_front = models.CharField(
        max_length=200,
        help_text=_(
            "Banknote front description (e.g. Mausoleo de Bolívar. Simón Bolívar.)"
        ),
        blank=True,
        verbose_name=_("front description"),
    )
    description_back = models.CharField(
        max_length=200,
        help_text=_("Banknote back description (e.g. Expedición de Los Cayos.)"),
        blank=True,
        verbose_name=_("back description"),
    )
    serial_number = models.CharField(
        _("serial number"),
        max_length=20,
        help_text=_("Banknote serial (e.g. A09084450)"),
        blank=True,
    )
    size = models.CharField(
        _("size"),
        max_length=10,
        blank=True,
        help_text=_("Banknote dimensions (e.g. 157x69mm)"),
    )
    observations = models.TextField(
        _("observations"),
        help_text=_("Enter your observations about the banknote (e.g. two pinholes)"),
        blank=True,
    )
    image_front = models.ImageField(
        blank=True,
        upload_to="banknotes",
        help_text=_("Select an image for the banknote front"),
        verbose_name=_("front image"),
    )
    image_back = models.ImageField(
        blank=True,
        upload_to="banknotes",
        help_text=_("Select an image for the banknote back"),
        verbose_name=_("back image"),
    )
    commemorative = models.BooleanField(_("commemorative"), blank=True)
    polymer = models.BooleanField(_("polymer"), blank=True)
    overprint = models.BooleanField(_("overprint"), blank=True)
    specimen = models.BooleanField(_("specimen"), blank=True)
    notgeld = models.BooleanField(blank=True)
    grading = models.CharField(
        _("grading"),
        max_length=3,
        choices=CONDITION_CHOICES,
        help_text=_("Grading based on the IBNS Grading Standards"),
        blank=True,
    )
    slug = models.SlugField(max_length=100, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    album = models.ManyToManyField(
        help_text=_("Select the album(s) to add the banknote to"),
        related_name="my_album",
        to="Album",
        blank=True,
        verbose_name=_("album"),
    )

    class Meta:
        verbose_name = _("banknote")
        ordering = ("country", "pick_number", "serial_number")

    def __str__(self):
        return f"{self.country} {self.denomination} {self.currency} {self.year} P-{self.pick_number}"

    def get_absolute_url(self):
        return reverse(
            "banknote_detail_view",
            args=[
                str(self.id),
                str(slugify(self.slug)),
            ],
        )

    def save(self, *args, **kwargs):
        value = f"{self.country} {self.denomination} {self.currency} {self.year}"
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
