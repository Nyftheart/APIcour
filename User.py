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

# Endpoint pour créer un utilisateur
@app.post("/api/users/")
async def create_user(user_data: dict, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "INSERT INTO users (nom, prenom, email, mdp) VALUES (%(nom)s, %(prenom)s, %(email)s, %(mdp)s)"
    cursor.execute(query, user_data)
    db.commit()
    return JSONResponse(content={"message": "Utilisateur créé avec succès"}, status_code=201)

# Endpoint pour obtenir la liste des utilisateurs
@app.get("/api/users/")
async def get_users(db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    return users

# Endpoint pour obtenir les détails d'un utilisateur
@app.get("/api/users/{user_id}")
async def get_user(user_id: int, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# Endpoint pour mettre à jour les détails d'un utilisateur
@app.put("/api/users/{user_id}")
async def update_user(user_id: int, updated_user_data: dict, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "UPDATE users SET nom = %(nom)s, prenom = %(prenom)s, email = %(email)s, mdp = %(mdp)s WHERE id = %(id)s"
    updated_user_data["id"] = user_id
    cursor.execute(query, updated_user_data)
    db.commit()
    return JSONResponse(content={"message": "Utilisateur mis à jour avec succès"})

# Endpoint pour supprimer un utilisateur
@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    db.commit()
    return JSONResponse(content={"message": "Utilisateur supprimé avec succès"})

