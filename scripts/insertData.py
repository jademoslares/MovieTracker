##########################################################################################
######## TO RUN THIS SCRIPT TYPE IN THE TERMINAL: python3 -m scripts.insertData ###########
##########################################################################################
import pandas as pd
from utilities.sqlalchemy_setup import SessionLocal, text

csv_file_path = '../netflix_titles.csv'  # Adjust the path as necessary

netflix_data = pd.read_csv(csv_file_path)
netflix_data = netflix_data.fillna({"title": "N/A", "director": "N/A", "country": "N/A",  
                                     "rating": "N/A",
                                     "description": "N/A", "cast": "N/A", 
                                     "listed_in": "N/A"})
movies_data = netflix_data[netflix_data['type'] == 'Movie'].copy()
movies_data['show_id'] = movies_data['show_id'].str.replace("s", "", regex=False)
movies_data = movies_data.drop_duplicates(subset=['show_id'])



# output_csv_file_path = 'netflix_movies.csv'
# movies_data.to_csv(output_csv_file_path, index=False)
# print(f'Successfully saved movies data to {output_csv_file_path}')


def insert_data():
    with SessionLocal() as session:
        try:
            for index, row in movies_data.iterrows():
                # Insert movie data
                # print(f"{row['show_id']} / {len(movies_data)}")
                print(f"Processing movie {index + 1}")
                session.execute(text("""
                    INSERT INTO movies (show_id, type, title, director, country, date_added, release_year, rating, duration, description)
                    VALUES (:show_id, :type, :title, :director, :country, STR_TO_DATE(:date_added, '%M %d, %Y'), :release_year, :rating, :duration, :description)
                    ON DUPLICATE KEY UPDATE title = VALUES(title)
                """), {
                    "show_id": row["show_id"], "type": row["type"], "title": row["title"], "director": row["director"],
                    "country": row["country"], "date_added": row["date_added"], "release_year": row["release_year"],
                    "rating": row["rating"], "duration": int(row["duration"].split()[0]) if pd.notna(row["duration"]) else None,
                    "description": row["description"]
                })
                
                # Insert actors
                if pd.notna(row["cast"]):
                    actors = row["cast"].split(", ")
                    for actor in actors:
                        session.execute(text("""
                            INSERT INTO actors (actor_name) VALUES (:actor_name)
                            ON DUPLICATE KEY UPDATE actor_name = VALUES(actor_name)
                        """), {"actor_name": actor})

                        exists = session.execute(text("""
                            SELECT COUNT(*) FROM show_actors 
                            WHERE show_id = :show_id AND actor_id = (SELECT actor_id FROM actors WHERE actor_name = :actor_name LIMIT 1)
                            """), {"show_id": row["show_id"], "actor_name": actor}).scalar()

                        if exists == 0:
                            session.execute(text("""
                            INSERT INTO show_actors (show_id, actor_id)
                            VALUES (:show_id, (SELECT actor_id FROM actors WHERE actor_name = :actor_name LIMIT 1))
                            """), {"show_id": row["show_id"], "actor_name": actor})
                
                # Insert genres
                if pd.notna(row["listed_in"]):
                    genres = row["listed_in"].split(", ")
                    for genre in genres:
                        session.execute(text("""
                            INSERT INTO genres (genre_name) VALUES (:genre_name)
                            ON DUPLICATE KEY UPDATE genre_name = VALUES(genre_name)
                        """), {"genre_name": genre})
                        session.execute(text("""
                            INSERT INTO show_genres (show_id, genre_id)
                            VALUES (:show_id, (SELECT genre_id FROM genres WHERE genre_name = :genre_name LIMIT 1))
                        """), {"show_id": row["show_id"], "genre_name": genre})
                        
            session.commit()
            print("Data inserted successfully")
        
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")

try:
    print("Inserting data...")
    insert_data()
    print("Data insertion completed.")
except Exception as e:
    print(f"An error occurred during the insertion process: {e}")

def remove_duplicates(batch_size=1000):
    with SessionLocal() as session:
        try:
            while True:
                # Remove duplicate actors in batches
                result = session.execute(text(f"""
                    DELETE FROM actors
                    WHERE actor_id NOT IN (
                        SELECT actor_id FROM (
                            SELECT MIN(actor_id) as actor_id
                            FROM actors
                            GROUP BY actor_name
                        ) AS keep
                    )
                    LIMIT {batch_size};
                """))
                
                if result.rowcount == 0:
                    break

            while True:
                # Remove duplicate genres in batches
                result = session.execute(text(f"""
                    DELETE FROM genres
                    WHERE genre_id NOT IN (
                        SELECT genre_id FROM (
                            SELECT MIN(genre_id) as genre_id
                            FROM genres
                            GROUP BY genre_name
                        ) AS keep
                    )
                    LIMIT {batch_size};
                """))
                
                if result.rowcount == 0:  # Exit if no more duplicates
                    break


            session.commit()
            print("Duplicate genres and actors removed successfully")
        
        except Exception as e:
            session.rollback()
            print(f"An error occurred while removing duplicates: {e}")

        

try:
    print("Removing duplicates...")
    remove_duplicates()
    print("Duplicate removal completed.")
except Exception as e:
    print(f"An error occurred during the duplicate removal process: {e}")

def insert_admin():
    with SessionLocal() as session:
        try:
            session.execute(text("""
                                 INSERT INTO users (username, password, user_type)
                                 VALUES ('admin', 'pbkdf2_sha256$870000$dKtBnTffUBPt3cVYsKAG2E$wtj2Wy/5lLN5m48K7waHvgPhMsLzme8W0/lLIXgpyMM=', 'admin');
            """))
            session.commit()
            print("Admin user inserted successfully")
        except Exception as e:
            session.rollback()
            print(f"An error occurred while inserting the admin user: {e}")
        finally:
            session.close()

insert_admin()
print("Admin user insertion completed.")