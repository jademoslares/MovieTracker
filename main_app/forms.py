from django import forms


class MovieForm(forms):
    show_id = forms.CharField(max_length=10)
    type = forms.CharField(max_length=10)
    title = forms.CharField(max_length=255)
    director = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=100, required=False)
    date_added = forms.DateField(required=False)
    release_year = forms.IntegerField()
    rating = forms.CharField(max_length=10)
    duration = forms.IntegerField()
    description = forms.CharField(max_length=255, required=False)

class ActorForm(forms):
    actor_name = forms.CharField(max_length=255)

class GenreForm(forms):
    genre_name = forms.CharField(max_length=255)