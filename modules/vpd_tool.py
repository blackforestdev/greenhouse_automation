# modules/vpd_tool.py

import math

def calculate_vpd(temperature_celsius, relative_humidity):
    """
    Calculate the Vapor Pressure Deficit (VPD).

    Vapor Pressure Deficit is the difference between the amount of moisture 
    in the air and how much moisture the air can hold when it is saturated. 
    A higher VPD increases the potential for moisture to evaporate from 
    plants, driving transpiration.

    Parameters:
    - temperature_celsius (float): The temperature in degrees Celsius.
    - relative_humidity (float): The relative humidity in percentage (0-100).

    Returns:
    - float: The VPD in kilopascals (kPa).

    Formula:
    - SVP (Saturation Vapor Pressure) = 0.6108 * e^((17.27 * T) / (T + 237.3))
    - AVP (Actual Vapor Pressure) = (RH / 100) * SVP
    - VPD = SVP - AVP
    """

    # Ensure the temperature and humidity values are within reasonable ranges
    if not (0 <= relative_humidity <= 100):
        raise ValueError("Relative humidity must be between 0 and 100 percent.")

    # Calculate saturation vapor pressure (SVP) using the Tetens formula
    svp = 0.6108 * math.exp((17.27 * temperature_celsius) / (temperature_celsius + 237.3))

    # Calculate actual vapor pressure (AVP)
    avp = (relative_humidity / 100) * svp

    # Calculate VPD
    vpd = svp - avp

    return vpd
