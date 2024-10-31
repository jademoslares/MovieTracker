from django.shortcuts import render, redirect
from sqlalchemy.orm import Session
from utilities.sqlalchemy_setup import SessionLocal
from .models import User,Movie,Actor,Genre,ShowActor,ShowGenre
from .forms import MovieForm, ActorForm, GenreForm

def home(request):
    session: Session = SessionLocal()
    try:
        movies = session.query(Movie).all()

    finally:
        session.close()

    return render(request, 'home.html', {'movies': movies})

###########################################################
#################### MOVIE ################################
def movie_detail(request, show_id):
    session: Session = SessionLocal()
    try:
        movie = session.query(Movie).filter_by(show_id=show_id).first()
        actors = session.query(Actor).join(ShowActor).filter(ShowActor.show_id == show_id).all()
        genres = session.query(Genre).join(ShowGenre).filter(ShowGenre.show_id == show_id).all()
        print(actors)
    finally:
        session.close()

    return render(request, 'movies/movie_detail.html', {'movie': movie, 'actors': actors, 'genres': genres})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            session = SessionLocal()
            try:
                # print(form.cleaned_data)
                # print("Selected Actor IDs:", selected_actor_ids)
                new_movie = Movie(
                    show_id = session.query(Movie).count() + 1,
                    type = "Movie",
                    title = form.cleaned_data['title'],
                    director = form.cleaned_data['director'],
                    country = form.cleaned_data['country'],
                    date_added = form.cleaned_data['date_added'],
                    release_year = form.cleaned_data['release_year'],
                    rating = form.cleaned_data['rating'],
                    duration = form.cleaned_data['duration'],
                    description = form.cleaned_data['description']
                )

                selected_actor_ids = form.cleaned_data.get('actors', [])
                for actor_id_str in selected_actor_ids:
                    actor_id = int(actor_id_str)

                    act = session.query(Actor).filter_by(actor_id=actor_id).first()
                    if act:
                        show_actor = ShowActor(show_id=new_movie.show_id, actor_id=act.actor_id)
                        session.add(show_actor)
                    else:
                        print(f"Actor with ID {actor_id} not found.")

                selected_genre_ids = form.cleaned_data.get('genres', [])
                for genre_id_str in selected_genre_ids:
                    genre_id = int(genre_id_str)

                    genre = session.query(Genre).filter_by(genre_id=genre_id).first()
                    if genre:
                        show_genre = ShowGenre(show_id=new_movie.show_id, genre_id=genre.genre_id)
                        session.add(show_genre)
                    else:
                        print(f"Genre with ID {genre_id} not found.")

                session.add(new_movie)
                session.commit()
                
                return redirect('home')
            except Exception as e:
                session.rollback()
                print(f"Error occurred: {e}")
            finally:
                session.close()
    else:
        form = MovieForm()
        

    return render(request, 'movies/movie_form.html', {'form': form, 'action': 'Create'})

def movie_update(request, show_id):
    session = SessionLocal()
    movie = session.query(Movie).filter_by(show_id=show_id).first()

    if not movie:
        return redirect('home')
    
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            try:
                # Update movie attributes
                movie.type = 'Movie'
                movie.title = form.cleaned_data['title']
                movie.director = form.cleaned_data['director']
                movie.country = form.cleaned_data['country']
                movie.date_added = form.cleaned_data['date_added']
                movie.release_year = form.cleaned_data['release_year']
                movie.rating = form.cleaned_data['rating']
                movie.duration = form.cleaned_data['duration']
                movie.description = form.cleaned_data['description']

                # Clear existing associations
                session.query(ShowActor).filter_by(show_id=movie.show_id).delete()
                session.query(ShowGenre).filter_by(show_id=movie.show_id).delete()

                # Handle selected actor IDs
                selected_actor_ids = form.cleaned_data.get('actors', [])
                for actor_id_str in selected_actor_ids:
                    actor_id = int(actor_id_str)
                    act = session.query(Actor).filter_by(actor_id=actor_id).first()
                    if act:
                        show_actor = ShowActor(show_id=movie.show_id, actor_id=act.actor_id)
                        session.add(show_actor)
                    else:
                        print(f"Actor with ID {actor_id} not found.")

                # Handle selected genre IDs
                selected_genre_ids = form.cleaned_data.get('genres', [])
                for genre_id_str in selected_genre_ids:
                    genre_id = int(genre_id_str)
                    genre = session.query(Genre).filter_by(genre_id=genre_id).first()
                    if genre:
                        show_genre = ShowGenre(show_id=movie.show_id, genre_id=genre.genre_id)
                        session.add(show_genre)
                    else:
                        print(f"Genre with ID {genre_id} not found.")

                session.commit()
                return redirect('home')
            except Exception as e:
                session.rollback()
                print(f"Error occurred: {e}")
            finally:
                session.close()
    else:
        # If GET request, populate the form with the existing movie data
        form = MovieForm(initial={
            'type': movie.type,
            'title': movie.title,
            'director': movie.director,
            'country': movie.country,
            'date_added': movie.date_added,
            'release_year': movie.release_year,
            'rating': movie.rating,
            'duration': movie.duration,
            'description': movie.description,
            'actors': [actor.actor_id for actor in movie.actors],
            'genres': [genre.genre_id for genre in movie.genres],
        })

    return render(request, 'movies/movie_form.html', {'form': form, 'action': 'Update'})


def movie_delete(request, show_id):
    session = SessionLocal()
    movie = session.query(Movie).filter_by(show_id=show_id).first()

    if movie:
        try:
            session.delete(movie)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            session.close()
    
    return redirect('home')

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