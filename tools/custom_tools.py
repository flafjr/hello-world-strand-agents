"""
Custom Tools for Amazon Strand Agents
"""
import json
import requests
import logging
from typing import Dict, Any, List
from datetime import datetime
import os

logger = logging.getLogger(__name__)

def weather_tool(location: str) -> Dict[str, Any]:
    """
    Get weather information for a location
    
    Args:
        location: City name or location
        
    Returns:
        Weather information dictionary
    """
    try:
        # This is a placeholder - you would need to implement with a real weather API
        # For now, returning mock data
        return {
            "location": location,
            "temperature": "22°C",
            "condition": "Partly cloudy",
            "humidity": "65%",
            "wind": "10 km/h",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Weather tool error: {e}")
        return {"error": str(e)}

def file_reader_tool(file_path: str) -> Dict[str, Any]:
    """
    Read and return contents of a file
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents or error message
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return {
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "lines": len(content.split('\n'))
        }
    except Exception as e:
        logger.error(f"File reader tool error: {e}")
        return {"error": str(e)}

def json_validator_tool(json_string: str) -> Dict[str, Any]:
    """
    Validate and parse JSON string
    
    Args:
        json_string: JSON string to validate
        
    Returns:
        Validation results
    """
    try:
        parsed = json.loads(json_string)
        return {
            "valid": True,
            "parsed_data": parsed,
            "type": type(parsed).__name__,
            "message": "Valid JSON"
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": str(e),
            "message": "Invalid JSON"
        }
    except Exception as e:
        logger.error(f"JSON validator tool error: {e}")
        return {"error": str(e)}

def text_analyzer_tool(text: str) -> Dict[str, Any]:
    """
    Analyze text for basic statistics
    
    Args:
        text: Text to analyze
        
    Returns:
        Text analysis results
    """
    try:
        words = text.split()
        sentences = text.split('.')
        paragraphs = text.split('\n\n')
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "paragraph_count": len([p for p in paragraphs if p.strip()]),
            "average_words_per_sentence": round(len(words) / max(len([s for s in sentences if s.strip()]), 1), 2),
            "most_common_words": get_most_common_words(words, 5)
        }
    except Exception as e:
        logger.error(f"Text analyzer tool error: {e}")
        return {"error": str(e)}

def get_most_common_words(words: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Get most common words from a list
    """
    word_count = {}
    for word in words:
        clean_word = word.lower().strip('.,!?;:"()[]{}')
        if clean_word and len(clean_word) > 2:  # Ignore short words
            word_count[clean_word] = word_count.get(clean_word, 0) + 1
    
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [{"word": word, "count": count} for word, count in sorted_words[:top_n]]

def timestamp_tool() -> Dict[str, Any]:
    """
    Get current timestamp in various formats
    
    Returns:
        Timestamp information
    """
    now = datetime.now()
    return {
        "iso_format": now.isoformat(),
        "unix_timestamp": int(now.timestamp()),
        "human_readable": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date_only": now.strftime("%Y-%m-%d"),
        "time_only": now.strftime("%H:%M:%S")
    }

def unit_converter_tool(value: float, from_unit: str, to_unit: str, unit_type: str) -> Dict[str, Any]:
    """
    Convert between different units
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
        unit_type: Type of unit (length, weight, temperature, etc.)
        
    Returns:
        Conversion result
    """
    try:
        conversions = {
            "length": {
                "meter": 1.0,
                "kilometer": 1000.0,
                "centimeter": 0.01,
                "millimeter": 0.001,
                "inch": 0.0254,
                "foot": 0.3048,
                "yard": 0.9144,
                "mile": 1609.34
            },
            "weight": {
                "kilogram": 1.0,
                "gram": 0.001,
                "pound": 0.453592,
                "ounce": 0.0283495,
                "ton": 1000.0
            },
            "temperature": {
                # Special case - handled separately
            }
        }
        
        if unit_type == "temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            if unit_type not in conversions:
                return {"error": f"Unknown unit type: {unit_type}"}
            
            unit_map = conversions[unit_type]
            if from_unit not in unit_map or to_unit not in unit_map:
                return {"error": f"Unknown unit for {unit_type}"}
            
            # Convert to base unit, then to target unit
            base_value = value * unit_map[from_unit]
            result = base_value / unit_map[to_unit]
        
        return {
            "original_value": value,
            "original_unit": from_unit,
            "converted_value": round(result, 6),
            "converted_unit": to_unit,
            "unit_type": unit_type
        }
    except Exception as e:
        logger.error(f"Unit converter tool error: {e}")
        return {"error": str(e)}

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    # Convert to Celsius first
    if from_unit.lower() == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit.lower() == "kelvin":
        celsius = value - 273.15
    else:  # Celsius
        celsius = value
    
    # Convert from Celsius to target
    if to_unit.lower() == "fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit.lower() == "kelvin":
        return celsius + 273.15
    else:  # Celsius
        return celsius

# Tool registry for easy access
CUSTOM_TOOLS = {
    "weather": weather_tool,
    "file_reader": file_reader_tool,
    "json_validator": json_validator_tool,
    "text_analyzer": text_analyzer_tool,
    "timestamp": timestamp_tool,
    "unit_converter": unit_converter_tool
}