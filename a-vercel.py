from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Load the CSV file
data = pd.read_csv("q-vercel-python.csv")  # Ensure this path is correct

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
async def get_marks(name: Optional[List[str]] = Query(None)):
    # Convert DataFrame to a dictionary for easy lookup
    marks_dict = pd.Series(data.marks.values, index=data.name).to_dict()
    
    if name:
        # Get marks for requested names
        marks = [marks_dict.get(n, 0) for n in name]  # Default to 0 if not found
    else:
        marks = []

    return {"marks": marks}
