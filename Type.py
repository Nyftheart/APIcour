from fastapi import FastAPI, HTTPException, Depends, Query
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


@app.get("/api/books/by_category/")
async def get_books_by_category(category: str, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "SELECT * FROM livres WHERE categorie = %s"
    cursor.execute(query, (category,))
    livres = cursor.fetchall()
    if not livres:
        raise HTTPException(status_code=404, detail=f"Aucun livre trouvé pour la catégorie {category}")
    return livres

# Endpoint pour obtenir les livres par langue
@app.get("/api/books/by_language/")
async def get_books_by_language(language: str, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "SELECT * FROM livres WHERE langue = %s"
    cursor.execute(query, (language,))
    livres = cursor.fetchall()
    if not livres:
        raise HTTPException(status_code=404, detail=f"Aucun livre trouvé pour la langue {language}")
    return livres

# Endpoint pour obtenir les livres par fonctionnalité (features)
@app.get("/api/books/by_features/")
async def get_books_by_features(features: str = Query(...), db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    # Utilisation de LIKE pour trouver les livres ayant une certaine fonctionnalité
    query = "SELECT * FROM livres WHERE features LIKE %s"
    cursor.execute(query, (f"%{features}%",))
    livres = cursor.fetchall()
    if not livres:
        raise HTTPException(status_code=404, detail=f"Aucun livre trouvé avec la fonctionnalité {features}")
    return livres
