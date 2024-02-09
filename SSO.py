import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt

# Configuration de la connexion à la base de données
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


app = FastAPI()

# Configuration de sécurité
SECRET_KEY = "un-truc-bien-cache"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour récupérer les informations de l'utilisateur depuis la base de données
def get_user(email: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, nom, prenom, email, mdp FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    return user

# Fonction pour créer un jeton JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint pour générer un jeton JWT en mode SSO
@app.post("/token")
async def login(email: str, password: str):
    # Vérifier les informations d'identification de l'utilisateur
    user = get_user(email)
    if not user or user["mdp"] != password:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    # Créer le contenu du jeton
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
