# models/cost_of_equity/__init__.py

# 1. Define Concept Information
CONCEPT_CODE = "cost_of_equity"
CONCEPT_NAME = "Cost of Equity"

# 2. Import Model Classes
from .capm import CAPM
from .fama_french import FamaFrench3Factor

# 3. Dynamically build the metadata dictionary by calling get_metadata() from each class
MODELS_METADATA = {
    model_class.__name__: model_class.get_metadata()
    for model_class in [CAPM, FamaFrench3Factor]
}
