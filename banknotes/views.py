from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.generic.detail import DetailView

from .forms import AlbumForm, BanknoteForm
from .models import Album, Banknote

User = settings.AUTH_USER_MODEL


class banknote_detail_view(DetailView):
    model = Banknote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_album"] = Album.objects.all().filter(owner=self.request.user)
        context["obj_banknote"] = Banknote.objects.all().filter(owner=self.request.user)
        context["list_countries"] = (
            Banknote.objects.order_by("country")
            .distinct("country")
            .filter(owner=self.request.user)
        )
        return context


class album_detail_view(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_album"] = Album.objects.all().filter(owner=self.request.user)
        context["obj_banknote"] = Banknote.objects.all().filter(owner=self.request.user)
        context["list_countries"] = (
            Banknote.objects.order_by("country")
            .distinct("country")
            .filter(owner=self.request.user)
        )
        return context


def album_all_detail_view(request, username):
    obj_banknote = Banknote.objects.all().filter(owner=request.user)
    obj_album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )

    # Pagination
    paginator = Paginator(obj_banknote, 30)
    page = request.GET.get("page")

    try:
        obj_banknote = paginator.page(page)
    except PageNotAnInteger:
        obj_banknote = paginator.page(1)
    except EmptyPage:
        obj_banknote = paginator.page(paginator.num_pages)

    return render(
        request,
        "banknote/album_all_banknotes.html",
        {
            "obj_banknote": obj_banknote,
            "obj_album": obj_album,
            "list_countries": list_countries,
        },
    )


def album_all_view(request, username):
    obj_album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )

    # Pagination
    paginator = Paginator(obj_album, 30)
    page = request.GET.get("page")

    try:
        obj_album = paginator.page(page)
    except PageNotAnInteger:
        obj_album = paginator.page(1)
    except EmptyPage:
        obj_album = paginator.page(paginator.num_pages)

    return render(
        request,
        "banknote/album_index.html",
        {
            "obj_album": obj_album,
            "list_countries": list_countries,
        },
    )


def album_country_view(request, username, url_country):
    obj_banknote = Banknote.objects.filter(owner=request.user).filter(
        country=url_country
    )
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )
    obj_album = Album.objects.all().filter(owner=request.user)

    # Pagination
    paginator = Paginator(obj_banknote, 30)
    page = request.GET.get("page")

    try:
        obj_banknote = paginator.page(page)
    except PageNotAnInteger:
        obj_banknote = paginator.page(1)
    except EmptyPage:
        obj_banknote = paginator.page(paginator.num_pages)

    return render(
        request,
        "banknote/country.html",
        {
            "obj_banknote": obj_banknote,
            "list_countries": list_countries,
            "obj_album": obj_album,
            "country": url_country,
        },
    )


def create_banknote(request, username):
    album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )
    if request.method == "POST":
        form = BanknoteForm(request.POST, user=request.user)
        if form.is_valid():
            banknote = form.save(commit=False)
            banknote.owner = request.user
            banknote.save()
            form.save_m2m()
            return redirect(
                "banknote_detail_view",
                username=slugify(request.user.username),
                pk=banknote.pk,
                slug=slugify(banknote.slug),
            )
    else:
        form = BanknoteForm(user=request.user)
    return render(
        request,
        "banknote/banknote_edit.html",
        {
            "form": form,
            "obj_album": album,
            "list_countries": list_countries,
        },
    )


def edit_banknote(request, username, pk, slug):
    banknote = get_object_or_404(Banknote.objects.filter(owner=request.user), pk=pk)
    album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )

    if request.method == "POST":
        form = BanknoteForm(
            request.POST, request.FILES, user=request.user, instance=banknote
        )
        if form.is_valid():
            banknote = form.save(commit=False)
            banknote.owner = request.user
            banknote.save()
            form.save_m2m()
            return redirect(
                "banknote_detail_view",
                username=slugify(request.user),
                pk=banknote.pk,
                slug=slugify(banknote.slug),
            )
    else:
        form = BanknoteForm(instance=banknote, user=request.user)
    return render(
        request,
        "banknote/banknote_edit.html",
        {
            "form": form,
            "banknote": banknote,
            "obj_album": album,
            "list_countries": list_countries,
        },
    )


def create_album(request, username):
    album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect(
                "album_detail_view",
                username=slugify(request.user),
                pk=album.pk,
                slug=slugify(album.name),
            )
    else:
        form = AlbumForm()
    return render(
        request,
        "banknote/album_edit.html",
        {
            "form": form,
            "obj_album": album,
            "list_countries": list_countries,
        },
    )


def edit_album(request, username, pk, slug):
    album = get_object_or_404(Album.objects.filter(owner=request.user), pk=pk)
    obj_album = Album.objects.all().filter(owner=request.user)
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )

    if request.method == "POST":
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect(
                "album_detail_view",
                username=slugify(request.user),
                pk=album.pk,
                slug=slugify(album.name),
            )
    else:
        form = AlbumForm(instance=album)
    return render(
        request,
        "banknote/album_edit.html",
        {
            "form": form,
            "obj_album": obj_album,
            "list_countries": list_countries,
            "album": album,
        },
    )


def pie_chart(request):
    num_banknotes_per_country = (
        Banknote.objects.values("country")
        .filter(owner=request.user)
        .order_by("country")
        .annotate(contador=Count("country"))
    )
    return render(
        request,
        "banknote/pie_chart.html",
        {
            "num_banknotes_per_country": num_banknotes_per_country,
        },
    )


def banknote_statistics_views(request, username):
    obj_banknote = Banknote.objects.all().filter(owner=request.user).order_by("country")
    obj_album = Album.objects.all().filter(owner=request.user)
    num_banknotes = Banknote.objects.all().filter(owner=request.user).count()
    num_albums = Album.objects.all().filter(owner=request.user).count()
    list_countries = (
        Banknote.objects.order_by("country")
        .distinct("country")
        .filter(owner=request.user)
    )
    num_countries = (
        Banknote.objects.all().filter(owner=request.user).distinct("country").count()
    )
    num_banknotes_per_country = (
        Banknote.objects.filter(owner=request.user)
        .values("country")
        .order_by("country")
        .annotate(contador=Count("country"))
    )

    return render(
        request,
        "banknote/dashboard.html",
        {
            "num_banknotes": num_banknotes,
            "num_albums": num_albums,
            "obj_banknote": obj_banknote,
            "obj_album": obj_album,
            "num_banknotes_per_country": num_banknotes_per_country,
            "num_countries": num_countries,
            "list_countries": list_countries,
        },
    )
