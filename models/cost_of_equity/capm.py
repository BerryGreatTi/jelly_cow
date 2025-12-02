from typing import Dict, Type
from models.schemas import ModelMetadata

class CAPM:
    """Capital Asset Pricing Model (CAPM)"""

    @classmethod
    def get_metadata(cls) -> ModelMetadata:
        """
        Returns the metadata for the model.
        """
        return ModelMetadata(
            name="Capital Asset Pricing Model (CAPM)",
            description="Calculates the Cost of Equity using beta, risk-free rate, and expected market return.",
            required_inputs={
                "risk_free_rate": "float",
                "beta": "float",
                "market_return": "float",
            },
            model_class=cls
        )

    def calculate(self, **inputs: float) -> float:
        """
        Calculates the Cost of Equity using the CAPM formula.
        """
        rfr = inputs["risk_free_rate"]
        beta = inputs["beta"]
        mr = inputs["market_return"]
        
        cost_of_equity = rfr + beta * (mr - rfr)
        return cost_of_equity
