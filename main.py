import os
import psycopg
from psycopg.rows import dict_row
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
    return psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)


@app.get("/")
def read_root():
    return {"message": "Leads API is running"}


@app.get("/leads")
def get_leads():
    with get_connection() as conn:
        leads = conn.execute("SELECT * FROM leads ORDER BY id").fetchall()
    return leads


@app.get("/leads/{lead_id}")
def get_lead(lead_id: int):
    with get_connection() as conn:
        lead = conn.execute(
            "SELECT * FROM leads WHERE id = %s", (lead_id,)
        ).fetchone()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.post("/leads", status_code=201)
def create_lead(lead: Lead):
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO leads (name, email, budget) VALUES (%s, %s, %s) RETURNING id",
            (lead.name, lead.email, lead.budget),
        ).fetchone()
    return {"id": row["id"], **lead.model_dump()}


@app.put("/leads/{lead_id}")
def update_lead(lead_id: int, lead: Lead):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE leads SET name = %s, email = %s, budget = %s WHERE id = %s",
            (lead.name, lead.email, lead.budget, lead_id),
        )
        updated = cursor.rowcount
    if updated == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"id": lead_id, **lead.model_dump()}


@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM leads WHERE id = %s", (lead_id,))
        deleted = cursor.rowcount
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": f"Lead {lead_id} deleted"}