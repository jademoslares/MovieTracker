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
                session.add(new_movie)
                session.commit()
            finally:
                session.close()
                return redirect('home')
    else:
        form = MovieForm()
        actors = actor_list()
        genres = genre_list()
    return render(request, 'movies/movie_form.html', {'form': form, 'actors': actors, 'genres': genres})

###########################################################
#################### ACTOR ################################
def actor_list():
    session: Session = SessionLocal()
    try:
        actors = session.query(Actor).all()
    finally:
        session.close()
    return actors

###########################################################
#################### GENRE ################################
def genre_list():
    session: Session = SessionLocal()
    try:
        genres = session.query(Genre).all()
    finally:
        session.close()
    return genres

def about(request):
    return render(request, 'about.html')