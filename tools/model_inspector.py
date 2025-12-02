import pkgutil
import importlib
from typing import List, Dict, Any, Optional

import models

def list_available_concepts() -> List[str]:
    """
    Returns a list of all available financial concept codes.
    (e.g., ['cost_of_equity', 'intrinsic_value'])
    """
    concept_paths = [name for _, name, is_pkg in pkgutil.iter_modules(models.__path__) if is_pkg]
    return concept_paths

def get_concept_details(concept_code: str) -> Dict[str, Any]:
    """
    Returns detailed information for a specific concept.
    """
    try:
        module = importlib.import_module(f"models.{concept_code}")
        return {
            "concept_code": getattr(module, "CONCEPT_CODE", "N/A"),
            "concept_name": getattr(module, "CONCEPT_NAME", "N/A"),
            "models": list(getattr(module, "MODELS_METADATA", {}).keys())
        }
    except ImportError:
        raise ValueError(f"Concept '{concept_code}' could not be found.")

def list_available_models(concept_code: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Returns all available models, grouped by concept.
    If a specific concept_code is provided, returns models for that concept only.
    """
    all_concepts = list_available_concepts()
    concepts_to_inspect = [concept_code] if concept_code else all_concepts
    
    result = {}
    for concept in concepts_to_inspect:
        try:
            details = get_concept_details(concept)
            result[concept] = details["models"]
        except ValueError:
            continue
    return result

def get_model_details(model_name: str) -> Dict[str, Any]:
    """
    Returns detailed metadata for a specific model name.
    """
    all_concepts = list_available_concepts()
    for concept in all_concepts:
        try:
            module = importlib.import_module(f"models.{concept}")
            metadata_dict = getattr(module, "MODELS_METADATA", {})
            if model_name in metadata_dict:
                # Convert the Pydantic model to a dict and return it.
                return metadata_dict[model_name].model_dump(exclude={'model_class'})
        except (ImportError, AttributeError):
            continue
            
    raise ValueError(f"Model '{model_name}' could not be found.")
