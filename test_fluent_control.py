#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for FluentControl Automation
========================================

This script tests the FluentControl automation functionality
without requiring an actual instrument connection.
"""

import unittest
import sys
import os
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import json

# Add current directory to path
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


class TestFluentControlAutomation(unittest.TestCase):
    """Test cases for FluentControl automation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = FluentControlClient(
            base_url="http://test.instrument.com",
            username="test_user",
            password="test_pass"
        )
    
    def test_labware_position_creation(self):
        """Test creating labware positions"""
        position = LabwarePosition(
            position_id="A1",
            labware_type=LabwareType.MICROPLATE_96,
            description="Test Plate",
            status=PositionStatus.OCCUPIED
        )
        
        self.assertEqual(position.position_id, "A1")
        self.assertEqual(position.labware_type, LabwareType.MICROPLATE_96)
        self.assertEqual(position.description, "Test Plate")
        self.assertEqual(position.status, PositionStatus.OCCUPIED)
    
    def test_transfer_parameters_creation(self):
        """Test creating transfer parameters"""
        transfer = TransferParameters(
            source_position="A1",
            destination_position="A2",
            volume_ul=50.0,
            liquid_class="Standard",
            tip_type="Standard_200uL",
            aspiration_speed=100.0,
            dispense_speed=100.0,
            air_gap=5.0,
            touch_off=True,
            mix_cycles=3,
            mix_volume=25.0,
            blow_out=True,
            retract_distance=2.0
        )
        
        self.assertEqual(transfer.source_position, "A1")
        self.assertEqual(transfer.destination_position, "A2")
        self.assertEqual(transfer.volume_ul, 50.0)
        self.assertEqual(transfer.liquid_class, "Standard")
        self.assertEqual(transfer.tip_type, "Standard_200uL")
    
    def test_standard_96_well_layout(self):
        """Test creating standard 96-well layout"""
        positions = create_standard_96_well_layout()
        
        self.assertIsInstance(positions, list)
        self.assertGreater(len(positions), 0)
        
        # Check that all positions have required attributes
        for position in positions:
            self.assertIsInstance(position, LabwarePosition)
            self.assertIsNotNone(position.position_id)
            self.assertIsNotNone(position.labware_type)
            self.assertIsNotNone(position.status)
    
    def test_config_protocols(self):
        """Test configuration protocols"""
        # Test getting available protocols
        protocols = list_available_protocols()
        self.assertIsInstance(protocols, list)
        self.assertGreater(len(protocols), 0)
        
        # Test getting specific protocol
        protocol = get_transfer_protocol("standard_water")
        self.assertIsNotNone(protocol)
        self.assertEqual(protocol.name, "Standard Water Transfer")
    
    def test_config_layouts(self):
        """Test configuration layouts"""
        # Test getting available layouts
        layouts = list_available_layouts()
        self.assertIsInstance(layouts, list)
        self.assertGreater(len(layouts), 0)
        
        # Test getting specific layout
        layout = get_deck_layout("96_well_standard")
        self.assertIsNotNone(layout)
        self.assertIn("positions", layout)
    
    def test_config_patterns(self):
        """Test configuration patterns"""
        # Test getting available patterns
        patterns = list_available_patterns()
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        
        # Test getting specific pattern
        pattern = get_transfer_pattern("serial_dilution")
        self.assertIsNotNone(pattern)
        self.assertIn("transfers", pattern)
    
    @patch('requests.Session')
    def test_client_initialization(self, mock_session):
        """Test client initialization"""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        client = FluentControlClient(
            base_url="http://test.com",
            username="user",
            password="pass"
        )
        
        self.assertEqual(client.base_url, "http://test.com")
        self.assertEqual(client.timeout, 30)
    
    @patch('requests.Session')
    def test_api_key_authentication(self, mock_session):
        """Test API key authentication"""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        client = FluentControlClient(
            base_url="http://test.com",
            api_key="test_api_key"
        )
        
        # Check that API key was set in headers
        mock_session_instance.headers.update.assert_called()
        call_args = mock_session_instance.headers.update.call_args[0][0]
        self.assertIn('Authorization', call_args)
        self.assertIn('Bearer test_api_key', call_args['Authorization'])
    
    def test_enum_values(self):
        """Test enum values are correct"""
        # Test LabwareType enum
        self.assertEqual(LabwareType.MICROPLATE_96.value, "96-well microplate")
        self.assertEqual(LabwareType.TIP_RACK_96.value, "96-tip rack")
        self.assertEqual(LabwareType.RESERVOIR.value, "reservoir")
        
        # Test PositionStatus enum
        self.assertEqual(PositionStatus.EMPTY.value, "empty")
        self.assertEqual(PositionStatus.OCCUPIED.value, "occupied")
        self.assertEqual(PositionStatus.ERROR.value, "error")


class TestFluentControlIntegration(unittest.TestCase):
    """Integration tests for FluentControl automation"""
    
    def test_complete_workflow_simulation(self):
        """Test complete workflow simulation"""
        # Create deck layout
        positions = create_standard_96_well_layout()
        self.assertGreater(len(positions), 0)
        
        # Create transfer parameters
        transfers = [
            TransferParameters(
                source_position="A1",
                destination_position="A2",
                volume_ul=50.0,
                liquid_class="Standard",
                tip_type="Standard_200uL"
            ),
            TransferParameters(
                source_position="A1",
                destination_position="A3",
                volume_ul=25.0,
                liquid_class="Standard",
                tip_type="Standard_200uL"
            )
        ]
        
        self.assertEqual(len(transfers), 2)
        
        # Test protocol integration
        protocol = get_transfer_protocol("standard_water")
        self.assertIsNotNone(protocol)
        
        # Test layout integration
        layout = get_deck_layout("96_well_standard")
        self.assertIsNotNone(layout)
        
        # Test pattern integration
        pattern = get_transfer_pattern("replicate_transfer")
        self.assertIsNotNone(pattern)
    
    def test_data_serialization(self):
        """Test data serialization for API calls"""
        # Test LabwarePosition serialization
        position = LabwarePosition(
            position_id="A1",
            labware_type=LabwareType.MICROPLATE_96,
            description="Test"
        )
        
        # Convert to dict (simulating API serialization)
        position_dict = {
            'position_id': position.position_id,
            'labware_type': position.labware_type.value,
            'description': position.description,
            'status': position.status.value
        }
        
        self.assertEqual(position_dict['position_id'], "A1")
        self.assertEqual(position_dict['labware_type'], "96-well microplate")
        
        # Test TransferParameters serialization
        transfer = TransferParameters(
            source_position="A1",
            destination_position="A2",
            volume_ul=50.0,
            liquid_class="Standard",
            tip_type="Standard_200uL"
        )
        
        transfer_dict = {
            'source_position': transfer.source_position,
            'destination_position': transfer.destination_position,
            'volume_ul': transfer.volume_ul,
            'liquid_class': transfer.liquid_class,
            'tip_type': transfer.tip_type
        }
        
        self.assertEqual(transfer_dict['source_position'], "A1")
        self.assertEqual(transfer_dict['destination_position'], "A2")
        self.assertEqual(transfer_dict['volume_ul'], 50.0)


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestFluentControlAutomation))
    test_suite.addTest(unittest.makeSuite(TestFluentControlIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running FluentControl Automation Tests")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n[SUCCESS] All tests passed!")
        print("\nThe FluentControl automation scripts are ready to use.")
        print("Next steps:")
        print("1. Configure your instrument URL and credentials")
        print("2. Test with a real instrument connection")
        print("3. Customize protocols for your specific needs")
    else:
        print("\n[FAILED] Some tests failed!")
        print("Please check the test output above for details.")
    
    sys.exit(0 if success else 1) 