import os
import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

load_dotenv()
app = FastAPI()


class Lead(BaseModel):
    name: str
    email: EmailStr | None = None
    budget: int


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.get("/")
def read_root():
    return {"message": "Leads API is running"}

@app.get("/leads")
def get_leads():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM leads")
        leads = cursor.fetchall()
    conn.close()
    return leads

@app.put("/leads/{lead_id}")
def update_lead(lead_id: int, lead: Lead):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE leads SET name = %s, email = %s, budget = %s WHERE id = %s",
            (lead.name, lead.email, lead.budget, lead_id),
        )
        conn.commit()
        updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"id": lead_id, **lead.model_dump()}

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM leads WHERE id = %s", (lead_id,))
        conn.commit()
        deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": f"Lead {lead_id} deleted"}


@app.post("/leads", status_code=201)
def create_lead(lead: Lead):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO leads (name, email, budget) VALUES (%s, %s, %s)",
            (lead.name, lead.email, lead.budget),
        )
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, **lead.model_dump()}


@app.get("/leads/{lead_id}")
def get_lead(lead_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM leads WHERE id = %s", (lead_id,))
        lead = cursor.fetchone()
    conn.close()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead