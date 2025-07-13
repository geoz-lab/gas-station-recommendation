"""
Fuel calculation service for Gas Station Recommendation App
"""

from typing import Tuple, Optional
from models.schema import UserPreferences

def calculate_gas_needed(input_type: str, value: float, tank_size: Optional[float] = None) -> float:
    """
    Calculate how much gas is needed based on user input
    
    Args:
        input_type: 'gallon' or 'percent'
        value: amount in gallon or percentage
        tank_size: total tank capacity if using percent
    
    Returns:
        float: gallons needed
    
    Raises:
        ValueError: If invalid input or missing tank size
    """
    if input_type == 'gallon':
        if value <= 0:
            raise ValueError("Gallons must be positive")
        return value
    elif input_type == 'percent' and tank_size:
        if value < 0 or value > 100:
            raise ValueError("Percentage must be between 0 and 100")
        return (value / 100.0) * tank_size
    else:
        raise ValueError("Invalid input type or missing tank size for percentage calculation")

def calculate_remaining_fuel(tank_size: float, current_level: float, fuel_to_add: float) -> float:
    """
    Calculate remaining fuel after adding gas
    
    Args:
        tank_size: Total tank capacity
        current_level: Current fuel level
        fuel_to_add: Amount of fuel to add
    
    Returns:
        float: Remaining fuel capacity
    """
    new_level = current_level + fuel_to_add
    if new_level > tank_size:
        return 0.0  # Tank will be full
    return tank_size - new_level

def calculate_range(mpg: float, fuel_amount: float) -> float:
    """
    Calculate how far the car can travel with given fuel
    
    Args:
        mpg: Miles per gallon
        fuel_amount: Amount of fuel in gallons
    
    Returns:
        float: Range in miles
    """
    return mpg * fuel_amount

def validate_fuel_input(input_type: str, value: float, tank_size: Optional[float] = None) -> Tuple[bool, str]:
    """
    Validate fuel input from user
    
    Args:
        input_type: 'gallon' or 'percent'
        value: User input value
        tank_size: Tank size for percentage validation
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        if input_type == 'gallon':
            if value <= 0:
                return False, "Gallons must be positive"
            if tank_size and value > tank_size:
                return False, f"Cannot add more than tank size ({tank_size} gallons)"
        elif input_type == 'percent':
            if value < 0 or value > 100:
                return False, "Percentage must be between 0 and 100"
            if not tank_size:
                return False, "Tank size required for percentage calculation"
        else:
            return False, "Invalid input type. Use 'gallon' or 'percent'"
        
        return True, ""
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def suggest_fuel_amount(current_level: float, tank_size: float, target_percentage: float = 80) -> float:
    """
    Suggest fuel amount to reach target percentage
    
    Args:
        current_level: Current fuel level in gallons
        tank_size: Total tank capacity
        target_percentage: Target fuel level percentage (default 80%)
    
    Returns:
        float: Suggested fuel amount to add
    """
    target_level = (target_percentage / 100.0) * tank_size
    needed = target_level - current_level
    
    if needed <= 0:
        return 0.0
    
    return round(needed, 1)

def format_fuel_display(gallons: float) -> str:
    """
    Format fuel amount for display
    
    Args:
        gallons: Fuel amount in gallons
    
    Returns:
        str: Formatted fuel amount
    """
    if gallons < 1:
        return f"{gallons * 128:.0f} oz"  # Convert to ounces
    elif gallons < 10:
        return f"{gallons:.1f} gallons"
    else:
        return f"{gallons:.0f} gallons" 