from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Album, Banknote

admin.site.site_header = _("Collector Admin Panel")
admin.site.site_title = _("Collector Admin Panel")
admin.site.index_title = _("Welcome to Collector Admin Panel")


class BanknoteResource(resources.ModelResource):
    class Meta:
        model = Banknote


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class BanknoteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BanknoteResource
    list_display = [
        "country",
        "denomination",
        "currency",
        "year",
        "pick_number",
        "grading",
        "serial_number",
    ]
    list_filter = [
        "country",
        "currency",
        "year",
        "commemorative",
        "polymer",
        "overprint",
        "specimen",
        "notgeld",
        "grading",
        "album",
    ]
    fields = [
        "country",
        "denomination",
        "currency",
        "pick_number",
        "issued_date",
        "year",
        "serial_number",
        "description_front",
        "description_back",
        "size",
        "observations",
        ("image_front", "image_front_tag"),
        ("image_back", "image_back_tag"),
        "grading",
        ("commemorative", "polymer", "overprint", "specimen", "notgeld"),
        "owner",
        "album",
    ]
    search_fields = [
        "country",
        "currency",
        "description_front",
        "description_back",
    ]

    actions = [
        # "set_commemorative",
        # "set_polymer",
        # "set_overprint",
        # "set_specimen",
        # "set_notgeld",
        # "add_to_album",
        # "remove_from_album",
    ]
    readonly_fields = [
        "image_front_tag",
        "image_back_tag",
    ]
    list_fields = [
        "object_link",
    ]
    list_select_related = True
    filter_horizontal = ["album"]

    def image_front_tag(self, obj):
        return format_html(f'<img src="{obj.image_front.url}" width="200" />')

    image_front_tag.short_description = _("Current image")

    def image_back_tag(self, obj):
        return format_html(f'<img src="{obj.image_back.url}" width="200" />')

    image_back_tag.short_description = _("Current image")

    def set_commemorative(self, request, queryset):
        queryset.update(commemorative=True)
        self.message_user(request, _("The banknotes have been marked as commemorative"))

    set_commemorative.short_description = _("Mark selected banknotes as commemorative")

    def set_polymer(self, request, queryset):
        queryset.update(polymer=True)
        self.message_user(request, _("The banknotes have been marked as polymer"))

    set_polymer.short_description = _("Mark selected banknotes as polymer")

    def set_overprint(self, request, queryset):
        queryset.update(overprint=True)
        self.message_user(request, _("The banknotes have been marked as overprint"))

    set_overprint.short_description = _("Mark selected banknotes as overprint")

    def set_specimen(self, request, queryset):
        queryset.update(specimen=True)
        self.message_user(request, _("The banknotes have been marked as specimen"))

    set_specimen.short_description = _("Mark selected banknotes as specimen")

    def set_notgeld(self, request, queryset):
        queryset.update(notgeld=True)
        self.message_user(request, "The banknotes have been marked as notgeld")

    set_notgeld.short_description = _("Mark selected banknotes as notgeld")

    # def add_to_album(self, request, queryset):
    #     if "apply" in request.POST:
    #         form = AddRemoveAlbumForm(request.POST)
    #         if form.is_valid():
    #             album = form.cleaned_data["album"]
    #             count = 0
    #             for banknote in queryset:
    #                 added = banknote.album.add(album)
    #                 count += 1
    #             messages.success(request, f"{count} banknotes were added to {album}")
    #             return
    #     else:
    #         form = AddRemoveAlbumForm()

    #     return render(
    #         request,
    #         "admin/add_to_album.html",
    #         context={
    #             "banknotes": queryset,
    #             "form": form,
    #         },
    #     )

    # add_to_album.short_description = _("Add banknotes to album...")

    # def remove_from_album(self, request, queryset):
    #     if "apply" in request.POST:
    #         form = AddRemoveAlbumForm(request.POST)
    #         if form.is_valid():
    #             album = form.cleaned_data["album"]
    #             count = 0
    #             for banknote in queryset:
    #                 removed = banknote.album.remove(album)
    #                 count += 1
    #             messages.success(
    #                 request,
    #                 _("{0} banknotes were removed from {1}").format(count, album),
    #             )
    #             return
    #     else:
    #         form = AddRemoveAlbumForm()

    #     return render(
    #         request,
    #         "admin/remove_from_album.html",
    #         context={
    #             "banknotes": queryset,
    #             "form": form,
    #         },
    #     )

    # remove_from_album.short_description = _("Remove banknotes from album...")


admin.site.register(Album, AlbumAdmin)
admin.site.register(Banknote, BanknoteAdmin)
