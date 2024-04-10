import os
import hashlib
import asyncio
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def encrypt(s):
    return hashlib.sha256(f"racism_{s}_isbad".encode(), usedforsecurity=True).hexdigest()

def authenticationStatus(success, message):
    return {
        "success": success,
        "message": message
    }

def authenticate(username, password):
    data, count = supabase.table("users").select("*").eq("username", username).execute()

    if len(data[1]) == 0:
        return authenticationStatus(False, "User doesn't exist")

    encrypted_password = encrypt(password)
    single_data = data[1][0]

    if single_data["password"] != encrypted_password:
        return authenticationStatus(False, "Invalid password")

    del single_data["password"]; # Remove password from sent data

    return authenticationStatus(True, single_data)


def createAccount(username, password): 
    same_username_count = len(supabase.table("users").select("*").eq("username", username).execute().data)
    already_exists = same_username_count > 0

    if already_exists:
        return authenticationStatus(False, "User already exists")

    encrypted_password = encrypt(password)

    data, count = supabase.table("users").insert({
        "username": username, 
        "password": encrypted_password 
    }).execute()

    single_data = data[1][0]
    del single_data["password"]; # Remove password from sent data

    return authenticationStatus(True, single_data)

    # data, count = supabase.table("countries").insert({"id": 5, "name": "Denmark"}).execute()

def saveArticle(username, password, id, title):
    authentication = authenticate(username, password)
    
    if not authentication["success"]:
        return authenticationStatus(False, "Authentication error, please log in again")
    
    _id = authentication["message"]["id"]
    saved_articles = authentication["message"]["saved_articles"]
    saved_articles.append({
        "id": id,
        "title": title
    })

    data, count = supabase.table("users").update({ 
        "saved_articles": saved_articles
    }).eq("id", _id).execute();

    return authenticationStatus(True, data[1][0])

def unsaveArticle(username, password, index):
    authentication = authenticate(username, password)

    if not authentication["success"]:
        return authenticationStatus(False, "Authentication error, please log in again")
    
    _id = authentication["message"]["id"]
    saved_articles = authentication["message"]["saved_articles"]
    del saved_articles[index]

    data, count = supabase.table("users").update({ 
        "saved_articles": saved_articles
    }).eq("id", _id).execute();

    return authenticationStatus(True, data[1][0])

def deleteAccount(username, password):
    authentication = authenticate(username, password)

    if not authentication["success"]:
        return authenticationStatus(False, "Authentication error");
    
    _id = authentication["message"]["id"]
    data, count = supabase.table("users").delete().eq("id", _id).execute()

    return authenticationStatus(True, "Successfully deleted")

# print(saveArticle("saddam_hussein_555", "password1234567890", "generic", "generic"))
# print(saveArticle("saddam_hussein_555", "password1234567890", "generic2", "generic2"))
