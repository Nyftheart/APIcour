from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import mysql.connector

app = FastAPI()


# Configurer la connexion à la base de données
# Paramètres de connexion à la base de données
host = "db"
user = "id21680564_nyftheart"
password = "alexououA1.k"
database = "id21680564_evedata"

# Fonction pour obtenir une connexion à la base de données
def get_db():
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

# Endpoint pour créer un livre
@app.post("/api/books/")
async def create_book(book: dict, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "INSERT INTO livres (nom, categorie, langue, description, note, prix, features) VALUES (%(nom)s, %(categorie)s, %(langue)s, %(description)s, %(note)s, %(prix)s, %(features)s)"
    cursor.execute(query, book)
    db.commit()
    return JSONResponse(content={"message": "Livre créé avec succès"}, status_code=201)

# Endpoint pour obtenir la liste des livres
@app.get("/api/books/")
async def get_books(db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM livres"
    cursor.execute(query)
    livres = cursor.fetchall()
    return livres

# Endpoint pour obtenir les détails d'un livre
@app.get("/api/books/{livre_id}")
async def get_book(livre_id: int, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM livres WHERE id = %s"
    cursor.execute(query, (livre_id,))
    livre = cursor.fetchone()
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return livre

# Endpoint pour mettre à jour les détails d'un livre
@app.put("/api/books/{livre_id}")
async def update_book(livre_id: int, updated_book: dict, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "UPDATE livres SET nom = %(nom)s, categorie = %(categorie)s, langue = %(langue)s, description = %(description)s, note = %(note)s, prix = %(prix)s, features = %(features)s WHERE id = %(id)s"
    updated_book["id"] = livre_id
    cursor.execute(query, updated_book)
    db.commit()
    return JSONResponse(content={"message": "Livre mis à jour avec succès"})

# Endpoint pour supprimer un livre
@app.delete("/api/books/{livre_id}")
async def delete_book(livre_id: int, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "DELETE FROM livres WHERE id = %s"
    cursor.execute(query, (livre_id,))
    db.commit()
    return JSONResponse(content={"message": "Livre supprimé avec succès"})
