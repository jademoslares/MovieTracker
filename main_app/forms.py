from django import forms
from .models import Movie, Actor, Genre, User
from sqlalchemy.orm import Session
from datetime import date
from utilities.sqlalchemy_setup import SessionLocal,asc
from django.core.cache import cache

class MovieForm(forms.Form):
    type = forms.CharField(max_length=10,required=False)
    title = forms.CharField(max_length=255, required=True)
    director = forms.CharField(max_length=255, required=True)
    country = forms.CharField(max_length=255, required=True)
    date_added = forms.DateField(required=False)
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
            # actor_list = session.query(Actor).order_by(asc(Actor.actor_name)).all()
            # self.fields['actors'].choices = [(actor.actor_id, actor.actor_name) for actor in actor_list]

            # genre_list = session.query(Genre).order_by(asc(Genre.genre_name)).all()
            # self.fields['genres'].choices = [(genre.genre_id, genre.genre_name) for genre in genre_list]

            actor_choices = cache.get('actor_choices')
            if not actor_choices:
                actor_list = session.query(Actor).order_by(asc(Actor.actor_name)).all()
                actor_choices = [(actor.actor_id, actor.actor_name) for actor in actor_list]
                cache.set('actor_choices', actor_choices, timeout=60 * 30)
            self.fields['actors'].choices = actor_choices

            genre_choices = cache.get('genre_choices')
            if not genre_choices:
                genre_list = session.query(Genre).order_by(asc(Genre.genre_name)).all()
                genre_choices = [(genre.genre_id, genre.genre_name) for genre in genre_list]
                cache.set('genre_choices', genre_choices, timeout=60 * 30)
            self.fields['genres'].choices = genre_choices
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


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, current_username=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_username = current_username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        session = SessionLocal()
        check_user = session.query(User).filter_by(username=username).first()
        session.close()
        if check_user and username != self.current_username:
            raise forms.ValidationError("Username already exists.")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)