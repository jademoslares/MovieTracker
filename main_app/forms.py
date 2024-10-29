from django import forms
from .models import Movie, Actor, Genre
from sqlalchemy.orm import Session
from datetime import date
from utilities.sqlalchemy_setup import SessionLocal

class MovieForm(forms.Form):
    type = forms.CharField(max_length=10, required=True)
    title = forms.CharField(max_length=255, required=True)
    director = forms.CharField(max_length=255, required=True)
    country = forms.CharField(max_length=100, required=True)
    date_added = forms.DateField(required=True)
    release_year = forms.IntegerField(required=True)
    rating = forms.CharField(max_length=10,required=True)
    duration = forms.IntegerField(required=True)
    description = forms.CharField(max_length=255, required=False)

    actors = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    genres = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        session: Session = SessionLocal()
        try:
            actor_list = session.query(Actor).all()
            self.fields['actors'].choices = [(actor.actor_id, actor.actor_name) for actor in actor_list]

            genre_list = session.query(Genre).all()
            self.fields['genres'].choices = [(genre.genre_id, genre.genre_name) for genre in genre_list]
        finally:
            session.close()

    def clean_release_year(self):
        release_year = self.cleaned_data.get('release_year')
        if release_year and release_year > date.today().year:
            raise forms.ValidationError("Release year cannot be in the future.")
        elif release_year < 1888:
            raise forms.ValidationError("Release year cannot be before 1888.")
        return release_year

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        valid_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17','TV-MA','TV-14','TV-PG','TV-G']
        if rating not in valid_ratings:
            raise forms.ValidationError(f"Rating must be one of the following: {', '.join(valid_ratings)}.")
        return rating    
    

    

class ActorForm(forms.Form):
    actor_name = forms.CharField(max_length=255)

class GenreForm(forms.Form):
    genre_name = forms.CharField(max_length=255)