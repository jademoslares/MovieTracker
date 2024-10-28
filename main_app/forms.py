from django import forms

class MovieForm(forms.Form):
    type = forms.CharField(max_length=10, required=True)
    title = forms.CharField(max_length=255)
    director = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=100, required=False)
    date_added = forms.DateField(required=False)
    release_year = forms.IntegerField()
    rating = forms.CharField(max_length=10)
    duration = forms.IntegerField()
    description = forms.CharField(max_length=255, required=False)

    # genre = forms.ChoiceField(choices=[], required=True)
    # actor = forms.ChoiceField(choices=[], required=True)
    

class ActorForm(forms.Form):
    actor_name = forms.CharField(max_length=255)

class GenreForm(forms.Form):
    genre_name = forms.CharField(max_length=255)