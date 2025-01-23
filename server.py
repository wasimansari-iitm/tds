from fastapi import FastAPI, HTTPException
from typing import Dict, List, Union, Optional
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the CSV file into a DataFrame
students_df = pd.read_csv('cleaned_q-fastapi.csv')

# Convert DataFrame to a list of dictionaries for API usage
items: List[Dict[str, Union[int, str]]] = students_df.to_dict(orient='records')

# Create a GET endpoint that returns all students' data, optionally filtered by class
@app.get("/api")
async def get_all_students(class_: Optional[List[str]] = None) -> Dict[str, List[Dict[str, Union[int, str]]]]:
    print(f"Requested classes: {class_}")  # Debug statement
    if class_:
        filtered_items = [item for item in items if item["class"] in class_]
        return {"students": filtered_items}
    return {"students": items}

# Create a GET endpoint that returns a specific item by student ID
@app.get("/students_df/{student_id}")
async def get_student(student_id: int) -> Dict[str, Union[int, str]]:
    if item := next((i for i in items if i["studentId"] == student_id), None):
        return item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
