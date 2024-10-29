from django import forms
from .models import Movie, Actor, Genre
from sqlalchemy.orm import Session
from utilities.sqlalchemy_setup import SessionLocal

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

    

class ActorForm(forms.Form):
    actor_name = forms.CharField(max_length=255)

class GenreForm(forms.Form):
    genre_name = forms.CharField(max_length=255)