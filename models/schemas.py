from pydantic import BaseModel, Field
from typing import Dict, Type

class ModelMetadata(BaseModel):
    name: str = Field(..., description="The user-friendly name of the model")
    description: str = Field(..., description="A brief description of the model's functionality")
    required_inputs: Dict[str, str] = Field(
        ..., description="The input variables and their types/concepts required for the calculation"
    )
    model_class: Type = Field(..., exclude=True, description="The actual class containing the calculation logic")
