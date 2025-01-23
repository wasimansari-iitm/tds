from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Load the CSV file
data = pd.read_csv("q-fastapi.csv")  # Adjust the path as necessary

# Create FastAPI instance
app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None)):
    # Convert DataFrame to a list of dictionaries
    students = data.to_dict(orient='records')
    
    if class_:
        # Filter students based on the class query parameter
        students = [student for student in students if student['class'] in class_]
    
    return {"students": students}