from fastapi import FastAPI, HTTPException, UploadFile, Form
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELOS BASE
class Usuario(BaseModel):
    id: str
    email: str
    password: str
    nombre: str

class Paciente(BaseModel):
    id: str
    nombre: str
    fecha_nacimiento: str
    doctor_id: str

class Examen(BaseModel):
    id: str
    paciente_id: str
    tipo: str
    fecha: str
    filename: str

# BASE DE DATOS TEMPORAL (memoria)
usuarios = []
pacientes = []
examenes = []

@app.post("/registro")
def registro(email: str = Form(...), password: str = Form(...), nombre: str = Form(...)):
    for u in usuarios:
        if u.email == email:
            raise HTTPException(status_code=400, detail="Ya existe ese email")
    nuevo = Usuario(id=str(uuid4()), email=email, password=password, nombre=nombre)
    usuarios.append(nuevo)
    return {"mensaje": "Usuario creado", "id": nuevo.id}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    for u in usuarios:
        if u.email == email and u.password == password:
            return {"mensaje": "Login exitoso", "id": u.id, "nombre": u.nombre}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/paciente")
def crear_paciente(nombre: str = Form(...), fecha_nacimiento: str = Form(...), doctor_id: str = Form(...)):
    nuevo = Paciente(id=str(uuid4()), nombre=nombre, fecha_nacimiento=fecha_nacimiento, doctor_id=doctor_id)
    pacientes.append(nuevo)
    return {"mensaje": "Paciente creado", "id": nuevo.id}

@app.get("/pacientes/{doctor_id}")
def listar_pacientes(doctor_id: str):
    return [p for p in pacientes if p.doctor_id == doctor_id]

@app.post("/examen")
def subir_examen(paciente_id: str = Form(...), tipo: str = Form(...), fecha: str = Form(...), file: UploadFile = None):
    nuevo = Examen(
        id=str(uuid4()),
        paciente_id=paciente_id,
        tipo=tipo,
        fecha=fecha,
        filename=file.filename if file else "no_file.nii.gz"
    )
    examenes.append(nuevo)
    return {"mensaje": "Examen registrado", "id": nuevo.id}

@app.get("/examenes/{paciente_id}")
def examenes_paciente(paciente_id: str):
    return [e for e in examenes if e.paciente_id == paciente_id]
