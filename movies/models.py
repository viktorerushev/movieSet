from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor and director"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default="")
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Release date", default=2022)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="genres")
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="enter the amount in dollars")
    fees_in_usa = models.PositiveIntegerField("Fees in USA", default=0, help_text="enter the amount in dollars")
    fees_in_world = models.PositiveIntegerField("Fees in World", default=0, help_text="enter the amount in dollars")
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Met:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Shot from movie"
        verbose_name_plural = "Shots from movie"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Message", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


