#!/usr/bin/env python3
"""
FluentControl Laboratory Automation Scripts
===========================================

This module provides automation scripts for FluentControl instruments:
- POST deck layout configuration
- POST session parameters for source to destination transfer

Author: Laboratory Automation Expert
Version: 1.0.0
"""

import json
import logging
import requests
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LabwareType(Enum):
    """Enumeration of supported labware types"""
    MICROPLATE_96 = "96-well microplate"
    MICROPLATE_384 = "384-well microplate"
    TUBE_RACK_24 = "24-tube rack"
    TUBE_RACK_48 = "48-tube rack"
    TUBE_RACK_96 = "96-tube rack"
    RESERVOIR = "reservoir"
    TIP_RACK_96 = "96-tip rack"
    TIP_RACK_384 = "384-tip rack"
    ADAPTER_PLATE = "adapter plate"
    CUSTOM = "custom"


class PositionStatus(Enum):
    """Enumeration of position statuses"""
    EMPTY = "empty"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    ERROR = "error"


@dataclass
class LabwarePosition:
    """Data class for labware position configuration"""
    position_id: str
    labware_type: LabwareType
    barcode: Optional[str] = None
    status: PositionStatus = PositionStatus.EMPTY
    description: Optional[str] = None
    custom_properties: Optional[Dict] = None


@dataclass
class TransferParameters:
    """Data class for transfer session parameters"""
    source_position: str
    destination_position: str
    volume_ul: float
    liquid_class: str
    tip_type: str
    aspiration_speed: Optional[float] = None
    dispense_speed: Optional[float] = None
    air_gap: Optional[float] = None
    touch_off: Optional[bool] = None
    mix_cycles: Optional[int] = None
    mix_volume: Optional[float] = None
    blow_out: Optional[bool] = None
    retract_distance: Optional[float] = None


class FluentControlClient:
    """Client for interacting with FluentControl instruments"""
    
    def __init__(self, base_url: str, username: str = None, password: str = None, 
                 api_key: str = None, timeout: int = 30):
        """
        Initialize FluentControl client
        
        Args:
            base_url: Base URL of the FluentControl instrument
            username: Username for authentication (if using basic auth)
            password: Password for authentication (if using basic auth)
            api_key: API key for authentication (if using API key auth)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure authentication
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
        elif username and password:
            self.session.auth = (username, password)
            self.session.headers.update({'Content-Type': 'application/json'})
        else:
            logger.warning("No authentication provided - some endpoints may fail")
            self.session.headers.update({'Content-Type': 'application/json'})
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                     params: Dict = None) -> requests.Response:
        """
        Make HTTP request to FluentControl instrument
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request payload
            params: Query parameters
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            if data:
                logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
            
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            logger.info(f"Request successful: {response.status_code}")
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise
    
    def get_instrument_status(self) -> Dict:
        """Get current instrument status"""
        response = self._make_request('GET', '/api/v1/status')
        return response.json()
    
    def get_deck_layout(self) -> Dict:
        """Get current deck layout configuration"""
        response = self._make_request('GET', '/api/v1/deck/layout')
        return response.json()
    
    def post_deck_layout(self, positions: List[LabwarePosition]) -> Dict:
        """
        POST deck layout configuration to the instrument
        
        Args:
            positions: List of labware positions to configure
            
        Returns:
            Response from the instrument
        """
        # Convert dataclass objects to dictionaries
        layout_data = {
            'positions': [asdict(pos) for pos in positions],
            'timestamp': time.time(),
            'version': '1.0'
        }
        
        logger.info(f"Posting deck layout with {len(positions)} positions")
        response = self._make_request('POST', '/api/v1/deck/layout', data=layout_data)
        return response.json()
    
    def post_transfer_session(self, transfers: List[TransferParameters]) -> Dict:
        """
        POST session parameters for source to destination transfer
        
        Args:
            transfers: List of transfer parameters
            
        Returns:
            Response from the instrument
        """
        # Convert dataclass objects to dictionaries
        session_data = {
            'transfers': [asdict(transfer) for transfer in transfers],
            'session_id': f"session_{int(time.time())}",
            'timestamp': time.time(),
            'status': 'pending'
        }
        
        logger.info(f"Posting transfer session with {len(transfers)} transfers")
        response = self._make_request('POST', '/api/v1/transfers/session', data=session_data)
        return response.json()
    
    def start_transfer_session(self, session_id: str) -> Dict:
        """Start a transfer session"""
        response = self._make_request('POST', f'/api/v1/transfers/session/{session_id}/start')
        return response.json()
    
    def get_transfer_status(self, session_id: str) -> Dict:
        """Get status of a transfer session"""
        response = self._make_request('GET', f'/api/v1/transfers/session/{session_id}/status')
        return response.json()
    
    def cancel_transfer_session(self, session_id: str) -> Dict:
        """Cancel a transfer session"""
        response = self._make_request('POST', f'/api/v1/transfers/session/{session_id}/cancel')
        return response.json()


def create_standard_96_well_layout() -> List[LabwarePosition]:
    """
    Create a standard 96-well microplate deck layout
    
    Returns:
        List of labware positions for a typical 96-well setup
    """
    positions = []
    
    # Define standard positions for 96-well setup
    layout_config = [
        ("A1", LabwareType.MICROPLATE_96, "Source_Plate_01"),
        ("A2", LabwareType.MICROPLATE_96, "Destination_Plate_01"),
        ("A3", LabwareType.TIP_RACK_96, "Tips_01"),
        ("A4", LabwareType.TIP_RACK_96, "Tips_02"),
        ("B1", LabwareType.RESERVOIR, "Wash_Buffer"),
        ("B2", LabwareType.RESERVOIR, "Reagent_01"),
        ("B3", LabwareType.TIP_RACK_96, "Tips_03"),
        ("B4", LabwareType.TIP_RACK_96, "Tips_04"),
    ]
    
    for pos_id, labware_type, description in layout_config:
        position = LabwarePosition(
            position_id=pos_id,
            labware_type=labware_type,
            description=description,
            status=PositionStatus.OCCUPIED
        )
        positions.append(position)
    
    return positions


def create_transfer_parameters(source_pos: str, dest_pos: str, 
                             volume_ul: float = 50.0) -> TransferParameters:
    """
    Create transfer parameters for a standard liquid transfer
    
    Args:
        source_pos: Source position ID
        dest_pos: Destination position ID
        volume_ul: Transfer volume in microliters
        
    Returns:
        TransferParameters object
    """
    return TransferParameters(
        source_position=source_pos,
        destination_position=dest_pos,
        volume_ul=volume_ul,
        liquid_class="Standard",
        tip_type="Standard_200uL",
        aspiration_speed=100.0,
        dispense_speed=100.0,
        air_gap=5.0,
        touch_off=True,
        mix_cycles=3,
        mix_volume=volume_ul * 0.5,
        blow_out=True,
        retract_distance=2.0
    )


def main():
    """Example usage of FluentControl automation scripts"""
    
    # Configuration - Update these values for your instrument
    INSTRUMENT_URL = os.getenv('FLUENT_CONTROL_URL', 'http://192.168.1.100')
    USERNAME = os.getenv('FLUENT_CONTROL_USERNAME')
    PASSWORD = os.getenv('FLUENT_CONTROL_PASSWORD')
    API_KEY = os.getenv('FLUENT_CONTROL_API_KEY')
    
    try:
        # Initialize client
        client = FluentControlClient(
            base_url=INSTRUMENT_URL,
            username=USERNAME,
            password=PASSWORD,
            api_key=API_KEY
        )
        
        # Check instrument status
        logger.info("Checking instrument status...")
        status = client.get_instrument_status()
        logger.info(f"Instrument status: {status}")
        
        # Example 1: POST deck layout
        logger.info("Setting up deck layout...")
        deck_positions = create_standard_96_well_layout()
        layout_response = client.post_deck_layout(deck_positions)
        logger.info(f"Deck layout response: {layout_response}")
        
        # Example 2: POST transfer session parameters
        logger.info("Creating transfer session...")
        transfers = [
            create_transfer_parameters("A1", "A2", volume_ul=50.0),
            create_transfer_parameters("A1", "A2", volume_ul=25.0),
            create_transfer_parameters("B1", "A2", volume_ul=100.0),
        ]
        
        session_response = client.post_transfer_session(transfers)
        session_id = session_response.get('session_id')
        logger.info(f"Transfer session created: {session_id}")
        
        # Start the transfer session
        if session_id:
            logger.info("Starting transfer session...")
            start_response = client.start_transfer_session(session_id)
            logger.info(f"Transfer session started: {start_response}")
            
            # Monitor transfer progress
            logger.info("Monitoring transfer progress...")
            for i in range(10):  # Monitor for up to 10 iterations
                status_response = client.get_transfer_status(session_id)
                logger.info(f"Transfer status: {status_response}")
                
                if status_response.get('status') in ['completed', 'failed', 'cancelled']:
                    break
                    
                time.sleep(5)  # Wait 5 seconds before next check
        
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        raise


if __name__ == "__main__":
    main() 