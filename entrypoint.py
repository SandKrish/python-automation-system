import argparse
import yaml
import logging
import sys
from pathlib import Path
from src.core.processor import ExcelProcessor
from src.core.visualizer import Visualizer

def load_config(config_path: str):
    """Loads configuration from a YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def setup_basic_logging():
    """Sets up a basic logger for the entrypoint before config is loaded."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def main():
    """Main execution flow for the automation pipeline."""
    setup_basic_logging()
    logger = logging.getLogger("entrypoint")

    parser = argparse.ArgumentParser(description="Professional Python Excel Automation System")
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.yaml", 
        help="Path to the configuration file"
    )
    parser.add_argument(
        "--input", 
        type=str, 
        required=True, 
        help="Path to the input Excel file"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="processed_report.xlsx", 
        help="Name of the output Excel file"
    )
    
    args = parser.parse_args()

    # 1. Load Configuration
    if not Path(args.config).exists():
        logger.error(f"Config file not found: {args.config}")
        sys.exit(1)
    
    config = load_config(args.config)
    logger.info("Configuration loaded successfully.")

    # 2. Initialize Components
    processor = ExcelProcessor(config)
    visualizer = Visualizer(config)

    # 3. Execute Pipeline
    try:
        # Step A: Ingest
        raw_data = processor.read_excel(args.input)
        
        # Step B: Validate & Transform
        validated_data = processor.validate_data(raw_data)
        
        # Step C: Save Processed Excel
        processor.process_and_save(validated_data, args.output)
        
        # Step D: Generate Visualizations
        logger.info("Generating data visualizations...")
        visualizer.generate_plots(validated_data)
        
        # Step E: Generate Architecture Diagram
        logger.info("Generating system architecture diagram...")
        visualizer.generate_architecture_diagram()

        logger.info("Pipeline execution completed successfully!")

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
