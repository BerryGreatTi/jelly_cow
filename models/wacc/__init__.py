# models/wacc/__init__.py

# 1. Define Concept Information
CONCEPT_CODE = "wacc"
CONCEPT_NAME = "Weighted Average Cost of Capital"

# 2. Import Model Classes
from .wacc_model import WACC

# 3. Dynamically build the metadata dictionary by calling get_metadata() from each class
MODELS_METADATA = {
    model_class.__name__: model_class.get_metadata()
    for model_class in [WACC]
}
