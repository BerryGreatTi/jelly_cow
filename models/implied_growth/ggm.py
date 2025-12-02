from typing import Dict, Type
from models.schemas import ModelMetadata

class GordonGrowthModel:
    """Gordon Growth Model (GGM)"""

    @classmethod
    def get_metadata(cls) -> ModelMetadata:
        """
        Returns the metadata for the model.
        """
        return ModelMetadata(
            name="Gordon Growth Model (GGM)",
            description="Calculates the implied growth based on the dividend growth model.",
            required_inputs={
                "r": "concept:cost_of_equity",
                "D1": "float",
                "P0": "float",
            },
            model_class=cls
        )

    def calculate(self, **inputs: float) -> float:
        """
        Calculates the implied growth (g) using the GGM formula.
        g = r - (D1 / P0)
        """
        r = inputs["r"]
        d1 = inputs["D1"]
        p0 = inputs["P0"]

        if p0 <= 0:
            raise ValueError("Current stock price (P0) must be greater than zero.")

        implied_growth = r - (d1 / p0)
        return implied_growth
