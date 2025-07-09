# FluentControl Laboratory Automation Scripts

This repository contains comprehensive automation scripts for FluentControl laboratory instruments, enabling programmatic control of deck layouts and liquid transfer operations.

## Overview

The scripts provide a complete solution for:
- **POST deck layout configurations** to the instrument
- **POST session parameters** for source to destination transfers
- **Predefined transfer protocols** for common laboratory workflows
- **Real-time monitoring** of transfer operations

## Files Structure

```
fluent_control_automation.py    # Main automation client and core functions
fluent_control_config.py        # Configuration and predefined protocols
fluent_control_examples.py      # Practical usage examples
FLUENT_CONTROL_README.md        # This documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- `requests` library (already included in your project requirements)

### Setup

1. **Environment Variables**: Set up your FluentControl instrument credentials:

```bash
export FLUENT_CONTROL_URL="http://192.168.1.100"
export FLUENT_CONTROL_USERNAME="your_username"
export FLUENT_CONTROL_PASSWORD="your_password"
# OR use API key authentication:
export FLUENT_CONTROL_API_KEY="your_api_key"
```

2. **Verify Connection**: Test your connection to the instrument:

```python
from fluent_control_automation import FluentControlClient

client = FluentControlClient(
    base_url="http://192.168.1.100",
    username="your_username",
    password="your_password"
)

status = client.get_instrument_status()
print(f"Instrument status: {status}")
```

## Core Functionality

### 1. POST Deck Layout

Configure the instrument's deck layout with labware positions:

```python
from fluent_control_automation import FluentControlClient, LabwarePosition, LabwareType, PositionStatus

# Initialize client
client = FluentControlClient(base_url="http://192.168.1.100", username="user", password="pass")

# Create deck positions
positions = [
    LabwarePosition(
        position_id="A1",
        labware_type=LabwareType.MICROPLATE_96,
        description="Source Plate",
        status=PositionStatus.OCCUPIED
    ),
    LabwarePosition(
        position_id="A2",
        labware_type=LabwareType.MICROPLATE_96,
        description="Destination Plate",
        status=PositionStatus.OCCUPIED
    ),
    LabwarePosition(
        position_id="A3",
        labware_type=LabwareType.TIP_RACK_96,
        description="Tips",
        status=PositionStatus.OCCUPIED
    )
]

# POST deck layout to instrument
response = client.post_deck_layout(positions)
print(f"Deck layout posted: {response}")
```

### 2. POST Session Parameters for Transfer

Create transfer sessions with detailed parameters:

```python
from fluent_control_automation import TransferParameters

# Create transfer parameters
transfers = [
    TransferParameters(
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
]

# POST transfer session
session_response = client.post_transfer_session(transfers)
session_id = session_response.get('session_id')

# Start the transfer
client.start_transfer_session(session_id)

# Monitor progress
status = client.get_transfer_status(session_id)
print(f"Transfer status: {status}")
```

## Predefined Protocols

The configuration includes optimized protocols for common laboratory applications:

### Available Transfer Protocols

1. **Standard Water Transfer** (`standard_water`)
   - Optimized for aqueous solutions
   - Standard 200μL tips
   - Moderate speeds and mixing

2. **DMSO Transfer** (`dmso_transfer`)
   - Optimized for organic solvents
   - Low retention tips
   - Slower speeds, increased air gap

3. **Cell Culture Transfer** (`cell_culture`)
   - Gentle handling for sensitive samples
   - Filtered tips
   - Minimal mixing, no blow out

4. **Protein Transfer** (`protein_transfer`)
   - Optimized for protein solutions
   - Low retention tips
   - Moderate mixing cycles

### Using Predefined Protocols

```python
from fluent_control_config import get_transfer_protocol, get_deck_layout

# Get a predefined protocol
protocol = get_transfer_protocol("dmso_transfer")

# Get a standard deck layout
layout = get_deck_layout("96_well_standard")

# Use protocol parameters in your transfers
transfer = TransferParameters(
    source_position="A1",
    destination_position="A2",
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
```

## Practical Examples

### Example 1: Serial Dilution

```python
from fluent_control_examples import FluentControlExamples

examples = FluentControlExamples(
    instrument_url="http://192.168.1.100",
    username="user",
    password="pass"
)

# Run serial dilution protocol
examples.example_2_serial_dilution_protocol()
```

### Example 2: Cell Culture Transfer

```python
# Run cell culture transfer protocol
examples.example_3_cell_culture_transfer()
```

### Example 3: Complete Workflow

```python
# Run complete workflow (deck setup + transfer + monitoring)
session_id = examples.run_complete_workflow()
```

## API Reference

### FluentControlClient

Main client class for instrument communication.

#### Methods

- `get_instrument_status()` - Get current instrument status
- `get_deck_layout()` - Get current deck layout
- `post_deck_layout(positions)` - POST deck layout configuration
- `post_transfer_session(transfers)` - POST transfer session parameters
- `start_transfer_session(session_id)` - Start a transfer session
- `get_transfer_status(session_id)` - Get transfer session status
- `cancel_transfer_session(session_id)` - Cancel a transfer session

### Data Classes

#### LabwarePosition
- `position_id`: Position identifier (e.g., "A1")
- `labware_type`: Type of labware (LabwareType enum)
- `barcode`: Optional barcode
- `status`: Position status (PositionStatus enum)
- `description`: Human-readable description

#### TransferParameters
- `source_position`: Source position ID
- `destination_position`: Destination position ID
- `volume_ul`: Transfer volume in microliters
- `liquid_class`: Liquid class name
- `tip_type`: Tip type
- `aspiration_speed`: Aspiration speed (μL/s)
- `dispense_speed`: Dispense speed (μL/s)
- `air_gap`: Air gap volume (μL)
- `touch_off`: Enable touch off
- `mix_cycles`: Number of mix cycles
- `mix_volume`: Mix volume (μL)
- `blow_out`: Enable blow out
- `retract_distance`: Retract distance (mm)

## Error Handling

The scripts include comprehensive error handling:

```python
try:
    response = client.post_deck_layout(positions)
    print("Deck layout posted successfully")
except requests.RequestException as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Logging

All operations are logged with detailed information:

```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Logs will show:
# - Request details
# - Response status
# - Error information
# - Transfer progress
```

## Security Considerations

1. **Authentication**: Use API keys when possible for better security
2. **Network Security**: Ensure instrument is on secure network
3. **Credentials**: Store credentials in environment variables, not in code
4. **Validation**: Always validate responses from instrument

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Verify instrument IP address
   - Check network connectivity
   - Ensure instrument is powered on

2. **Authentication Failed**
   - Verify username/password or API key
   - Check authentication method (basic auth vs API key)
   - Ensure user has appropriate permissions

3. **Invalid Deck Layout**
   - Verify position IDs are valid
   - Check labware type compatibility
   - Ensure positions don't conflict

4. **Transfer Failed**
   - Check tip availability
   - Verify source/destination positions
   - Ensure sufficient volume in source

### Debug Mode

Enable debug logging for detailed troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To extend the functionality:

1. Add new transfer protocols to `fluent_control_config.py`
2. Create new example workflows in `fluent_control_examples.py`
3. Extend the client class for additional instrument features
4. Add validation for new labware types

## License

This software is provided as-is for laboratory automation purposes. Ensure compliance with your institution's safety and validation requirements before use in production environments. 