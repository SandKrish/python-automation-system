import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

class StabilityProfile(BaseModel):
    """Generic model for structural or stability profile data."""
    depth: float = Field(..., alias="Depth")
    primary_value: float = Field(..., alias="Primary Value")
    secondary_value: float = Field(..., alias="Secondary Value")
    index_factor: float = Field(..., alias="Index Factor")

class SafetyEnvelope(BaseModel):
    """Generic model for safety or threshold envelope data."""
    depth: float = Field(..., alias="Depth")
    actual_value: float = Field(..., alias="Actual Value")
    threshold_min: float = Field(..., alias="Threshold Min")
    threshold_max: float = Field(..., alias="Threshold Max")

class ExcelProcessor:
    """
    Robust generic processor for engineering profile and envelope data.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = {
            "stability_profile": StabilityProfile,
            "safety_envelope": SafetyEnvelope
        }
        self._setup_logging()

    def _setup_logging(self):
        log_cfg = self.config.get("logging", {})
        logging.basicConfig(
            level=log_cfg.get("level", "INFO"),
            format=log_cfg.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    def read_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        logger.info(f"Ingesting Data Workbook: {file_path}")
        try:
            return pd.read_excel(file_path, sheet_name=None)
        except Exception as e:
            logger.error(f"Failed to read Excel file {file_path}: {e}")
            raise

    def validate_data(self, data_frames: Dict[str, pd.DataFrame]) -> Dict[str, List[BaseModel]]:
        validated_results = {}
        for sheet_name, df in data_frames.items():
            model_key = sheet_name.lower().replace(" ", "_")
            model = self.models.get(model_key)

            if not model:
                logger.warning(f"No schema mapping found for: {sheet_name}")
                continue

            records = df.to_dict(orient="records")
            valid_records = []
            for i, record in enumerate(records):
                try:
                    valid_records.append(model(**record))
                except ValidationError as e:
                    logger.error(f"Validation Error in {sheet_name} at index {i}: {e}")

            validated_results[sheet_name] = valid_records
        return validated_results

    def process_and_save(self, validated_data: Dict[str, List[BaseModel]], output_filename: str):
        output_path = Path(self.config["paths"]["output_dir"]) / output_filename
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, records in validated_data.items():
                df = pd.DataFrame([r.model_dump() for r in records])
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                worksheet = writer.sheets[sheet_name]
                for col in worksheet.columns:
                    max_length = max([len(str(cell.value)) for cell in col] + [10])
                    worksheet.column_dimensions[col[0].column_letter].width = max_length + 2
        logger.info(f"Processed report generated at: {output_path}")
