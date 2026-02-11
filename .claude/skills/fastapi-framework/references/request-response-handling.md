# FastAPI Request/Response Handling Guide

## Request Models with Pydantic

### Basic Request Model
```python
from pydantic import BaseModel, Field
from typing import Optional

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str
    tags: list[str] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "category": "electronics",
                "tags": ["electronics", "new"]
            }
        }
```

### Advanced Request Validation
```python
from pydantic import BaseModel, validator, root_validator
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.medium
    due_date: Optional[datetime] = None
    assignee_ids: list[int] = []

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v

    @validator('due_date')
    def due_date_must_be_future(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

    @root_validator(pre=True)
    def validate_assignees_exist(cls, values):
        assignee_ids = values.get('assignee_ids', [])
        # Validate that assignees exist in the system
        if assignee_ids:
            invalid_ids = [aid for aid in assignee_ids if aid < 1]
            if invalid_ids:
                raise ValueError(f'Invalid assignee IDs: {invalid_ids}')
        return values
```

## Response Models

### Basic Response Model
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables reading from ORM objects
```

### Response with Computed Fields
```python
from pydantic import BaseModel, computed_field

class ProductResponse(BaseModel):
    id: int
    name: str
    base_price: float
    tax_rate: float = 0.1
    created_at: datetime

    @computed_field
    @property
    def total_price(self) -> float:
        return round(self.base_price * (1 + self.tax_rate), 2)

    @computed_field
    @property
    def price_category(self) -> str:
        if self.total_price < 20:
            return "budget"
        elif self.total_price < 100:
            return "standard"
        else:
            return "premium"
```

## Request Parameter Types

### Path Parameters
```python
from fastapi import Path

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1)
):
    return {"item_id": item_id}

@app.get("/items/{item_id}/details/{detail_type}")
async def get_item_detail(
    item_id: int = Path(..., ge=1),
    detail_type: str = Path(...)
):
    return {"item_id": item_id, "detail_type": detail_type}
```

### Query Parameters with Validation
```python
from fastapi import Query
from typing import List, Optional

@app.get("/items/")
async def get_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    skip: int = Query(0, ge=0, le=1000),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", regex=r"^[a-zA-Z_]+$"),
    tags: List[str] = Query([])
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "tags": tags
    }
```

### Cookie and Header Parameters
```python
from fastapi import Cookie, Header

@app.get("/items/")
async def get_items_with_context(
    user_id: Optional[str] = Cookie(None),
    x_request_id: Optional[str] = Header(None)
):
    return {
        "user_id": user_id,
        "request_id": x_request_id
    }
```

## File Upload Handling

### Single File Upload
```python
from fastapi import File, UploadFile
import shutil
from pathlib import Path

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {allowed_types}"
        )

    # Validate file size (max 5MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 5MB"
        )

    # Save file securely
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / f"{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file_size,
        "location": str(file_path)
    }
```

### Multiple File Upload
```python
@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        # Process each file similar to single upload
        results.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(await file.read())
        })
        await file.seek(0)  # Reset file pointer

    return {"uploaded_files": results}
```

## Response Customization

### Custom Response Classes
```python
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse

@app.get("/custom-response")
async def custom_response():
    content = {"message": "Custom response", "timestamp": datetime.now().isoformat()}
    return JSONResponse(
        content=content,
        status_code=201,
        headers={"X-Custom-Header": "value"}
    )

@app.get("/redirect")
async def redirect_example():
    return RedirectResponse(url="/items/")

@app.get("/stream-data")
async def stream_large_data():
    def generate_data():
        for i in range(1000):
            yield f"data: {i}\n\n"
            time.sleep(0.1)

    return StreamingResponse(generate_data(), media_type="text/plain")
```

### Response Model Exclusion
```python
from pydantic import Field

class UserResponse(BaseModel):
    id: int
    username: str
    email: str = Field(exclude=True)  # Exclude from response
    is_active: bool = True
    created_at: datetime

    class Config:
        # Dynamically exclude fields based on context
        fields = {
            'email': {'write_only': True}
        }

@app.get("/users/{user_id}", response_model=UserResponse, response_model_exclude={'email'})
async def get_user(user_id: int):
    # Return user data without email
    pass
```

## Form Data Handling

### Regular Form Data
```python
from fastapi import Form

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Authenticate user
    return {"username": username}

@app.post("/contact")
async def contact_form(
    name: str = Form(..., min_length=2),
    email: str = Form(...),
    message: str = Form(..., max_length=1000)
):
    return {"name": name, "email": email, "message": message}
```

### Mixed Request Bodies and Form Data
```python
@app.post("/mixed")
async def mixed_request(
    item: ItemCreate,  # From request body
    file: UploadFile = File(...),  # From form data
    metadata: str = Form(...)  # From form data
):
    return {
        "item": item,
        "file_name": file.filename,
        "metadata": metadata
    }
```

## Request/Response Best Practices

### 1. Always Use Response Models
- Ensures consistent API responses
- Provides automatic validation
- Generates better documentation

### 2. Validate Request Data
- Use Pydantic validators
- Implement custom validation logic
- Provide clear error messages

### 3. Handle Large Requests Efficiently
- Stream large file uploads
- Use background tasks for processing
- Implement proper error handling

### 4. Use Type Hints Consistently
- Improves IDE support
- Enables automatic documentation
- Catches errors at development time

### 5. Implement Proper Error Responses
- Use appropriate HTTP status codes
- Provide meaningful error messages
- Follow consistent error format