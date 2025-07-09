#!/usr/bin/env python3
"""
FluentControl Automation Examples
================================

Practical examples demonstrating how to use FluentControl automation scripts
for common laboratory workflows.

This script provides ready-to-use examples for:
1. Setting up deck layouts
2. Creating transfer sessions
3. Running automated protocols
"""

import os
import sys
import time
import logging
from typing import List, Dict

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fluent_control_automation import (
    FluentControlClient, 
    LabwarePosition, 
    LabwareType, 
    PositionStatus,
    TransferParameters,
    create_standard_96_well_layout
)
from fluent_control_config import (
    get_transfer_protocol,
    get_deck_layout,
    get_transfer_pattern,
    list_available_protocols,
    list_available_layouts,
    list_available_patterns
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FluentControlExamples:
    """Collection of practical FluentControl automation examples"""
    
    def __init__(self, instrument_url: str, username: str = None, 
                 password: str = None, api_key: str = None):
        """
        Initialize FluentControl examples
        
        Args:
            instrument_url: URL of the FluentControl instrument
            username: Username for authentication
            password: Password for authentication
            api_key: API key for authentication
        """
        self.client = FluentControlClient(
            base_url=instrument_url,
            username=username,
            password=password,
            api_key=api_key
        )
    
    def example_1_basic_deck_setup(self):
        """
        Example 1: Basic deck layout setup for 96-well microplate work
        
        This example demonstrates:
        - Setting up a standard 96-well deck layout
        - Configuring labware positions
        - POST deck layout to instrument
        """
        logger.info("=== Example 1: Basic Deck Setup ===")
        
        try:
            # Create standard 96-well layout
            deck_positions = create_standard_96_well_layout()
            
            # POST deck layout to instrument
            response = self.client.post_deck_layout(deck_positions)
            logger.info(f"Deck layout posted successfully: {response}")
            
            # Verify layout was applied
            current_layout = self.client.get_deck_layout()
            logger.info(f"Current deck layout: {current_layout}")
            
            return response
            
        except Exception as e:
            logger.error(f"Deck setup failed: {e}")
            raise
    
    def example_2_serial_dilution_protocol(self):
        """
        Example 2: Serial dilution protocol
        
        This example demonstrates:
        - Creating transfer parameters for serial dilution
        - Using predefined transfer protocols
        - POST session parameters for complex transfer patterns
        """
        logger.info("=== Example 2: Serial Dilution Protocol ===")
        
        try:
            # Get predefined transfer protocol
            protocol = get_transfer_protocol("standard_water")
            
            # Create serial dilution transfers
            transfers = []
            source_well = "A1"
            base_volume = 100.0
            
            for i in range(1, 6):  # 5 serial dilutions
                dest_well = f"A{i+1}"
                transfer_volume = base_volume / (2 ** i)  # Serial dilution
                
                transfer = TransferParameters(
                    source_position=source_well if i == 1 else f"A{i}",
                    destination_position=dest_well,
                    volume_ul=transfer_volume,
                    liquid_class=protocol.liquid_class.value,
                    tip_type=protocol.tip_type.value,
                    aspiration_speed=protocol.aspiration_speed,
                    dispense_speed=protocol.dispense_speed,
                    air_gap=protocol.air_gap,
                    touch_off=protocol.touch_off,
                    mix_cycles=protocol.mix_cycles,
                    mix_volume=protocol.mix_volume,
                    blow_out=protocol.blow_out,
                    retract_distance=protocol.retract_distance
                )
                transfers.append(transfer)
            
            # POST transfer session
            session_response = self.client.post_transfer_session(transfers)
            logger.info(f"Serial dilution session created: {session_response}")
            
            return session_response
            
        except Exception as e:
            logger.error(f"Serial dilution protocol failed: {e}")
            raise
    
    def example_3_cell_culture_transfer(self):
        """
        Example 3: Cell culture media transfer
        
        This example demonstrates:
        - Using cell culture optimized transfer parameters
        - Gentle handling protocols for sensitive samples
        - Multiple source to destination transfers
        """
        logger.info("=== Example 3: Cell Culture Transfer ===")
        
        try:
            # Get cell culture protocol
            protocol = get_transfer_protocol("cell_culture")
            
            # Create cell culture transfers
            transfers = []
            
            # Transfer from multiple source wells to destination
            source_wells = ["A1", "A2", "A3", "A4"]
            dest_wells = ["B1", "B2", "B3", "B4"]
            
            for src, dest in zip(source_wells, dest_wells):
                transfer = TransferParameters(
                    source_position=src,
                    destination_position=dest,
                    volume_ul=50.0,
                    liquid_class=protocol.liquid_class.value,
                    tip_type=protocol.tip_type.value,
                    aspiration_speed=protocol.aspiration_speed,
                    dispense_speed=protocol.dispense_speed,
                    air_gap=protocol.air_gap,
                    touch_off=protocol.touch_off,
                    mix_cycles=protocol.mix_cycles,
                    mix_volume=protocol.mix_volume,
                    blow_out=protocol.blow_out,
                    retract_distance=protocol.retract_distance
                )
                transfers.append(transfer)
            
            # POST transfer session
            session_response = self.client.post_transfer_session(transfers)
            logger.info(f"Cell culture transfer session created: {session_response}")
            
            return session_response
            
        except Exception as e:
            logger.error(f"Cell culture transfer failed: {e}")
            raise
    
    def example_4_dmso_compound_transfer(self):
        """
        Example 4: DMSO compound transfer
        
        This example demonstrates:
        - Using DMSO-optimized transfer parameters
        - Low retention tips for organic solvents
        - Precise volume control for compound handling
        """
        logger.info("=== Example 4: DMSO Compound Transfer ===")
        
        try:
            # Get DMSO protocol
            protocol = get_transfer_protocol("dmso_transfer")
            
            # Create DMSO compound transfers
            transfers = []
            
            # Transfer compounds from source plate to assay plate
            for row in ['A', 'B', 'C', 'D']:
                for col in range(1, 13):  # 12 columns
                    source_well = f"{row}{col}"
                    dest_well = f"{row}{col}"
                    
                    transfer = TransferParameters(
                        source_position=source_well,
                        destination_position=dest_well,
                        volume_ul=10.0,  # Small volume for compounds
                        liquid_class=protocol.liquid_class.value,
                        tip_type=protocol.tip_type.value,
                        aspiration_speed=protocol.aspiration_speed,
                        dispense_speed=protocol.dispense_speed,
                        air_gap=protocol.air_gap,
                        touch_off=protocol.touch_off,
                        mix_cycles=protocol.mix_cycles,
                        mix_volume=protocol.mix_volume,
                        blow_out=protocol.blow_out,
                        retract_distance=protocol.retract_distance
                    )
                    transfers.append(transfer)
            
            # POST transfer session
            session_response = self.client.post_transfer_session(transfers)
            logger.info(f"DMSO compound transfer session created: {session_response}")
            
            return session_response
            
        except Exception as e:
            logger.error(f"DMSO compound transfer failed: {e}")
            raise
    
    def example_5_custom_deck_layout(self):
        """
        Example 5: Custom deck layout for specific experiment
        
        This example demonstrates:
        - Creating custom deck layouts
        - Mixed labware types
        - Custom position descriptions
        """
        logger.info("=== Example 5: Custom Deck Layout ===")
        
        try:
            # Create custom deck layout for specific experiment
            custom_positions = [
                LabwarePosition(
                    position_id="A1",
                    labware_type=LabwareType.MICROPLATE_96,
                    description="Compound Source Plate",
                    status=PositionStatus.OCCUPIED
                ),
                LabwarePosition(
                    position_id="A2",
                    labware_type=LabwareType.MICROPLATE_96,
                    description="Assay Destination Plate",
                    status=PositionStatus.OCCUPIED
                ),
                LabwarePosition(
                    position_id="A3",
                    labware_type=LabwareType.TIP_RACK_96,
                    description="Low Retention Tips",
                    status=PositionStatus.OCCUPIED
                ),
                LabwarePosition(
                    position_id="B1",
                    labware_type=LabwareType.RESERVOIR,
                    description="DMSO Control",
                    status=PositionStatus.OCCUPIED
                ),
                LabwarePosition(
                    position_id="B2",
                    labware_type=LabwareType.RESERVOIR,
                    description="Positive Control",
                    status=PositionStatus.OCCUPIED
                ),
                LabwarePosition(
                    position_id="B3",
                    labware_type=LabwareType.TIP_RACK_96,
                    description="Backup Tips",
                    status=PositionStatus.OCCUPIED
                ),
            ]
            
            # POST custom deck layout
            response = self.client.post_deck_layout(custom_positions)
            logger.info(f"Custom deck layout posted: {response}")
            
            return response
            
        except Exception as e:
            logger.error(f"Custom deck layout failed: {e}")
            raise
    
    def run_complete_workflow(self):
        """
        Run a complete workflow example
        
        This demonstrates a full workflow:
        1. Setup deck layout
        2. Create transfer session
        3. Start transfer
        4. Monitor progress
        """
        logger.info("=== Complete Workflow Example ===")
        
        try:
            # Step 1: Setup deck layout
            logger.info("Step 1: Setting up deck layout...")
            self.example_1_basic_deck_setup()
            
            # Step 2: Create transfer session
            logger.info("Step 2: Creating transfer session...")
            session_response = self.example_2_serial_dilution_protocol()
            session_id = session_response.get('session_id')
            
            if not session_id:
                raise ValueError("No session ID received from instrument")
            
            # Step 3: Start transfer
            logger.info("Step 3: Starting transfer session...")
            start_response = self.client.start_transfer_session(session_id)
            logger.info(f"Transfer started: {start_response}")
            
            # Step 4: Monitor progress
            logger.info("Step 4: Monitoring transfer progress...")
            max_attempts = 20
            for attempt in range(max_attempts):
                status_response = self.client.get_transfer_status(session_id)
                status = status_response.get('status', 'unknown')
                progress = status_response.get('progress', 0)
                
                logger.info(f"Transfer status: {status}, Progress: {progress}%")
                
                if status in ['completed', 'failed', 'cancelled']:
                    logger.info(f"Transfer finished with status: {status}")
                    break
                
                time.sleep(10)  # Wait 10 seconds between checks
            
            logger.info("Complete workflow finished successfully!")
            return session_id
            
        except Exception as e:
            logger.error(f"Complete workflow failed: {e}")
            raise


def main():
    """Main function to run examples"""
    
    # Configuration - Update these for your instrument
    INSTRUMENT_URL = os.getenv('FLUENT_CONTROL_URL', 'http://192.168.1.100')
    USERNAME = os.getenv('FLUENT_CONTROL_USERNAME')
    PASSWORD = os.getenv('FLUENT_CONTROL_PASSWORD')
    API_KEY = os.getenv('FLUENT_CONTROL_API_KEY')
    
    # Check if we have at least one authentication method
    if not any([USERNAME, API_KEY]):
        logger.error("No authentication provided. Please set FLUENT_CONTROL_USERNAME/PASSWORD or FLUENT_CONTROL_API_KEY")
        return
    
    try:
        # Initialize examples
        examples = FluentControlExamples(
            instrument_url=INSTRUMENT_URL,
            username=USERNAME,
            password=PASSWORD,
            api_key=API_KEY
        )
        
        # Check instrument status first
        logger.info("Checking instrument status...")
        status = examples.client.get_instrument_status()
        logger.info(f"Instrument status: {status}")
        
        # Run individual examples
        logger.info("\n" + "="*50)
        logger.info("Running FluentControl Automation Examples")
        logger.info("="*50)
        
        # Example 1: Basic deck setup
        examples.example_1_basic_deck_setup()
        
        # Example 2: Serial dilution
        examples.example_2_serial_dilution_protocol()
        
        # Example 3: Cell culture transfer
        examples.example_3_cell_culture_transfer()
        
        # Example 4: DMSO compound transfer
        examples.example_4_dmso_compound_transfer()
        
        # Example 5: Custom deck layout
        examples.example_5_custom_deck_layout()
        
        # Run complete workflow
        logger.info("\n" + "="*50)
        logger.info("Running Complete Workflow")
        logger.info("="*50)
        examples.run_complete_workflow()
        
        logger.info("\nAll examples completed successfully!")
        
    except Exception as e:
        logger.error(f"Examples failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 