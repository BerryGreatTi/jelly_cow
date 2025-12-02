import importlib
from typing import Any, Dict

def run_calculation(model_name: str, inputs: Dict[str, Any]) -> float:
    """
    Executes a calculation for a specified financial model, serving as a core execution engine
    for the financial model agent's complex analysis workflows.

    This function is crucial for the successful operation of agents like the `financial_model_agent`
    as it directly performs the quantitative calculations necessary to derive insights and
    inform recommendations. The successful execution of this function contributes directly
    to the agent's ability to fulfill user requests involving theoretical financial models.

    The `inputs` parameter, a dictionary, must contain all the values corresponding to the
    `required_inputs` specified in the model's metadata (retrieved via `get_model_details` tool).
    For example, if `get_model_details('CAPM')` indicates `risk_free_rate`, `beta`, and
    `market_return` are required, then the `inputs` dictionary for `run_calculation`
    must be structured like `{'risk_free_rate': 0.02, 'beta': 1.2, 'market_return': 0.08}`.

    :param model_name: The class name of the model to execute (e.g., 'CAPM').
    :param inputs: A dictionary of input values required for the model's calculation.
                   These values must match the `required_inputs` defined in the model's metadata.
    :return: The calculated result from the specified financial model.
    """
    # The concept folder to which the model belongs must be found.
    all_concepts = _find_all_concepts()
    
    model_metadata = None
    for concept in all_concepts:
        try:
            module = importlib.import_module(f"models.{concept}")
            metadata_dict = getattr(module, "MODELS_METADATA", {})
            if model_name in metadata_dict:
                model_metadata = metadata_dict[model_name]
                break
        except (ImportError, AttributeError):
            continue

    if not model_metadata:
        raise ValueError(f"Model '{model_name}' could not be found.")

    # Check if all required inputs have been provided.
    required_inputs = model_metadata.required_inputs.keys()
    missing_inputs = [req for req in required_inputs if req not in inputs]
    if missing_inputs:
        raise ValueError(f"Missing required inputs for calculation: {', '.join(missing_inputs)}")

    # Get the model class, instantiate it, and run the calculation.
    model_class = model_metadata.model_class
    model_instance = model_class()
    
    try:
        result = model_instance.calculate(**inputs)
        return result
    except Exception as e:
        raise RuntimeError(f"An error occurred during the calculation of the '{model_metadata.name}' model: {e}")

def _find_all_concepts():
    """Helper function to find all concept directories."""
    import pkgutil
    import models
    return [name for _, name, is_pkg in pkgutil.iter_modules(models.__path__) if is_pkg]

