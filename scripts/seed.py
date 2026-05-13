import psycopg
import time

def seed_basic_data():
    db_config = {
        "dbname": "book_library",
        "user": "postgres",
        "password": "FrozenLu1827.",
        "host": "localhost"
    }

    while True:
        try:
            conn = psycopg.connect(**db_config)
            cursor = conn.cursor()
            print("Connected to the database successfully!")
            
            categories_data = [
                ('Fiction', 1), 
                ('Science Fiction', 2), 
                ('History', 3), 
                ('Technology', 4), 
                ('Biography', 5)
            ]
            
            print("Duke insertuar kategoritë...")

            cursor.executemany(
                'INSERT INTO "Categories" (name, categories_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;', 
                categories_data
            )

            authors_data = [
                ('Ismail Kadare', 'Albania', 1), 
                ('George Orwell', 'UK', 2), 
                ('Isaac Asimov', 'USA', 3), 
                ('Fjodor Dostojevski', 'Russia', 4), 
                ('Agatha Christie', 'UK', 5), 
                ('Robert Kurvitz', 'Estonia', 6),
                ('J.K. Rowling', 'UK', 7), 
                ('Yuval Noah Harari', 'Israel', 8), 
                ('Neil Gaiman', 'UK', 9)
            ]
            
            print("Duke insertuar autorët...")
           
            cursor.executemany(
                'INSERT INTO "Authors" (full_name, country, authors_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;', 
                authors_data
            )

           
            conn.commit()
            print("Sukses: Te dhenat u ruajten me 'commit'!")
            
        
            cursor.close()
            conn.close()
            break

        except Exception as error:
            print("Database connection failed")
            print("Error details:", error)
            time.sleep(5)

if __name__ == "__main__":
    seed_basic_data()