# models/implied_growth/__init__.py

# 1. Define Concept Information
CONCEPT_CODE = "implied_growth"
CONCEPT_NAME = "Implied Growth"

# 2. Import Model Classes
from .ggm import GordonGrowthModel

# 3. Dynamically build the metadata dictionary by calling get_metadata() from each class
MODELS_METADATA = {
    model_class.__name__: model_class.get_metadata()
    for model_class in [GordonGrowthModel]
}
