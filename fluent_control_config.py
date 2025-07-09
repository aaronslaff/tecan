#!/usr/bin/env python3
"""
FluentControl Configuration
==========================

Configuration file for FluentControl automation scripts.
Contains common labware types, transfer parameters, and instrument settings.
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class LiquidClass(Enum):
    """Standard liquid classes for FluentControl"""
    WATER = "Water"
    DMSO = "DMSO"
    ETHANOL = "Ethanol"
    STANDARD = "Standard"
    HIGH_VISCOSITY = "HighViscosity"
    LOW_VOLUME = "LowVolume"
    CELL_CULTURE = "CellCulture"
    PROTEIN = "Protein"


class TipType(Enum):
    """Standard tip types for FluentControl"""
    STANDARD_10UL = "Standard_10uL"
    STANDARD_50UL = "Standard_50uL"
    STANDARD_200UL = "Standard_200uL"
    STANDARD_1000UL = "Standard_1000uL"
    FILTERED_200UL = "Filtered_200uL"
    FILTERED_1000UL = "Filtered_1000uL"
    LOW_RETENTION_200UL = "LowRetention_200uL"


@dataclass
class TransferProtocol:
    """Predefined transfer protocols"""
    name: str
    liquid_class: LiquidClass
    tip_type: TipType
    aspiration_speed: float
    dispense_speed: float
    air_gap: float
    touch_off: bool
    mix_cycles: int
    mix_volume: float
    blow_out: bool
    retract_distance: float
    description: str


# Predefined transfer protocols
TRANSFER_PROTOCOLS = {
    "standard_water": TransferProtocol(
        name="Standard Water Transfer",
        liquid_class=LiquidClass.WATER,
        tip_type=TipType.STANDARD_200UL,
        aspiration_speed=100.0,
        dispense_speed=100.0,
        air_gap=5.0,
        touch_off=True,
        mix_cycles=3,
        mix_volume=25.0,
        blow_out=True,
        retract_distance=2.0,
        description="Standard protocol for aqueous solutions"
    ),
    
    "dmso_transfer": TransferProtocol(
        name="DMSO Transfer",
        liquid_class=LiquidClass.DMSO,
        tip_type=TipType.LOW_RETENTION_200UL,
        aspiration_speed=50.0,
        dispense_speed=50.0,
        air_gap=10.0,
        touch_off=True,
        mix_cycles=5,
        mix_volume=30.0,
        blow_out=True,
        retract_distance=3.0,
        description="Protocol optimized for DMSO and organic solvents"
    ),
    
    "cell_culture": TransferProtocol(
        name="Cell Culture Transfer",
        liquid_class=LiquidClass.CELL_CULTURE,
        tip_type=TipType.FILTERED_200UL,
        aspiration_speed=30.0,
        dispense_speed=30.0,
        air_gap=3.0,
        touch_off=False,
        mix_cycles=2,
        mix_volume=20.0,
        blow_out=False,
        retract_distance=1.0,
        description="Gentle protocol for cell culture media"
    ),
    
    "protein_transfer": TransferProtocol(
        name="Protein Transfer",
        liquid_class=LiquidClass.PROTEIN,
        tip_type=TipType.LOW_RETENTION_200UL,
        aspiration_speed=40.0,
        dispense_speed=40.0,
        air_gap=5.0,
        touch_off=True,
        mix_cycles=4,
        mix_volume=25.0,
        blow_out=True,
        retract_distance=2.0,
        description="Protocol for protein solutions and biological samples"
    )
}


# Standard deck layouts
STANDARD_DECK_LAYOUTS = {
    "96_well_standard": {
        "description": "Standard 96-well microplate layout",
        "positions": [
            {"id": "A1", "type": "96-well microplate", "description": "Source Plate"},
            {"id": "A2", "type": "96-well microplate", "description": "Destination Plate"},
            {"id": "A3", "type": "96-tip rack", "description": "Tips 1"},
            {"id": "A4", "type": "96-tip rack", "description": "Tips 2"},
            {"id": "B1", "type": "reservoir", "description": "Wash Buffer"},
            {"id": "B2", "type": "reservoir", "description": "Reagent 1"},
            {"id": "B3", "type": "96-tip rack", "description": "Tips 3"},
            {"id": "B4", "type": "96-tip rack", "description": "Tips 4"},
        ]
    },
    
    "384_well_standard": {
        "description": "Standard 384-well microplate layout",
        "positions": [
            {"id": "A1", "type": "384-well microplate", "description": "Source Plate"},
            {"id": "A2", "type": "384-well microplate", "description": "Destination Plate"},
            {"id": "A3", "type": "384-tip rack", "description": "Tips 1"},
            {"id": "A4", "type": "384-tip rack", "description": "Tips 2"},
            {"id": "B1", "type": "reservoir", "description": "Wash Buffer"},
            {"id": "B2", "type": "reservoir", "description": "Reagent 1"},
            {"id": "B3", "type": "384-tip rack", "description": "Tips 3"},
            {"id": "B4", "type": "384-tip rack", "description": "Tips 4"},
        ]
    },
    
    "tube_rack_layout": {
        "description": "Tube rack layout for sample processing",
        "positions": [
            {"id": "A1", "type": "24-tube rack", "description": "Sample Tubes"},
            {"id": "A2", "type": "96-well microplate", "description": "Destination Plate"},
            {"id": "A3", "type": "96-tip rack", "description": "Tips 1"},
            {"id": "A4", "type": "96-tip rack", "description": "Tips 2"},
            {"id": "B1", "type": "reservoir", "description": "Lysis Buffer"},
            {"id": "B2", "type": "reservoir", "description": "Wash Buffer"},
            {"id": "B3", "type": "96-tip rack", "description": "Tips 3"},
            {"id": "B4", "type": "96-tip rack", "description": "Tips 4"},
        ]
    }
}


# Common transfer patterns
TRANSFER_PATTERNS = {
    "serial_dilution": {
        "description": "Serial dilution pattern",
        "transfers": [
            {"source": "A1", "destination": "A2", "volume": 100.0},
            {"source": "A2", "destination": "A3", "volume": 50.0},
            {"source": "A3", "destination": "A4", "volume": 50.0},
            {"source": "A4", "destination": "A5", "volume": 50.0},
        ]
    },
    
    "replicate_transfer": {
        "description": "Replicate transfer pattern",
        "transfers": [
            {"source": "A1", "destination": "A2", "volume": 50.0},
            {"source": "A1", "destination": "A3", "volume": 50.0},
            {"source": "A1", "destination": "A4", "volume": 50.0},
            {"source": "A1", "destination": "A5", "volume": 50.0},
        ]
    },
    
    "multi_source_transfer": {
        "description": "Multiple source to single destination",
        "transfers": [
            {"source": "A1", "destination": "B1", "volume": 25.0},
            {"source": "A2", "destination": "B1", "volume": 25.0},
            {"source": "A3", "destination": "B1", "volume": 25.0},
            {"source": "A4", "destination": "B1", "volume": 25.0},
        ]
    }
}


def get_transfer_protocol(protocol_name: str) -> TransferProtocol:
    """Get a transfer protocol by name"""
    return TRANSFER_PROTOCOLS.get(protocol_name)


def get_deck_layout(layout_name: str) -> Dict:
    """Get a deck layout by name"""
    return STANDARD_DECK_LAYOUTS.get(layout_name)


def get_transfer_pattern(pattern_name: str) -> Dict:
    """Get a transfer pattern by name"""
    return TRANSFER_PATTERNS.get(pattern_name)


def list_available_protocols() -> List[str]:
    """List all available transfer protocols"""
    return list(TRANSFER_PROTOCOLS.keys())


def list_available_layouts() -> List[str]:
    """List all available deck layouts"""
    return list(STANDARD_DECK_LAYOUTS.keys())


def list_available_patterns() -> List[str]:
    """List all available transfer patterns"""
    return list(TRANSFER_PATTERNS.keys()) 