from django.shortcuts import render, redirect
from sqlalchemy.orm import Session
from utilities.sqlalchemy_setup import SessionLocal
from .models import User,Movie,Actor,Genre
from .forms import MovieForm, ActorForm, GenreForm

def home(request):
    session: Session = SessionLocal()
    try:
        movies = session.query(Movie).all()

        # final = [result.to_dict() for result in results]
    finally:
        session.close()

    return render(request, 'home.html', {'results': movies})

###########################################################
#################### MOVIE ################################
def movie_detail(request, show_id):
    session: Session = SessionLocal()
    try:
        movie = session.query(Movie).filter_by(show_id == show_id).first()
    finally:
        session.close()

    return render(request, 'movies/movie_detail.html', {'movie': movie})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            session: Session = SessionLocal()
            try:
                new_movie = Movie(**form.cleaned_data)
                new_movie.show_id = 1
                session.add(new_movie)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error occurred: {e}")
            finally:
                session.close()
                return redirect('home')
    else:
        form = MovieForm()
        # actors = actor_list()
        # genres = genre_list()

        # form.fields['actor'].choices = [(actor.actor_id, actor.actor_name) for actor in actors] if actors else []
        # form.fields['genre'].choices = [(genre.genre_id, genre.genre_name) for genre in genres] if genres else []
    return render(request, 'movies/movie_form.html', {'form': form})

def movie_update(request, show_id):
    pass

def movie_delete(request, show_id):
    pass

###########################################################
#################### ACTOR ################################
def actor_list():
    session: Session = SessionLocal()
    try:
        actors = session.query(Actor).all()
        final = [result.to_dict() for result in actors]
    finally:
        session.close()
    return actors

def actor_create(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            session: Session = SessionLocal()
            try:
                new_actor = Actor(**form.cleaned_data)
                session.add(new_actor)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error occurred: {e}")
            finally:
                session.close()
                return redirect('home')
    else:
        form = ActorForm()
    return render(request, 'actors/actor_form.html', {'form': form})

###########################################################
#################### GENRE ################################
def genre_list():
    session: Session = SessionLocal()
    try:
        genres = session.query(Genre).all()
        final = [result.to_dict() for result in genres]
    finally:
        session.close()
    return genres

def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            session: Session = SessionLocal()
            try:
                new_genre = Genre(**form.cleaned_data)
                session.add(new_genre)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error occurred: {e}")
            finally:
                session.close()
                return redirect('home')
    else:
        form = GenreForm()
    return render(request, 'genres/genre_form.html', {'form': form})

def about(request):
    return render(request, 'about.html')