from typing import Dict, Type
from models.schemas import ModelMetadata

class WACC:
    """Weighted Average Cost of Capital (WACC)"""

    @classmethod
    def get_metadata(cls) -> ModelMetadata:
        """
        Returns the metadata for the model.
        """
        return ModelMetadata(
            name="Weighted Average Cost of Capital (WACC)",
            description="Calculates the weighted average cost of capital based on equity, debt, and their respective costs.",
            required_inputs={
                "market_cap": "float",
                "total_debt": "float",
                "cost_of_equity": "float",
                "cost_of_debt": "float",
                "tax_rate": "float",
            },
            model_class=cls
        )

    def calculate(self, **inputs: float) -> float:
        """
        Calculates the WACC.
        """
        e = inputs["market_cap"]
        d = inputs["total_debt"]
        re = inputs["cost_of_equity"]
        rd = inputs["cost_of_debt"]
        t = inputs["tax_rate"]
        
        v = e + d
        if v == 0:
            return 0.0
            
        wacc = (e / v * re) + (d / v * rd * (1 - t))
        return wacc
