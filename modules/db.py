# /modules/db.py

import mysql.connector
import logging
from config import DB_CONFIG
from datetime import datetime

logger = logging.getLogger('my_application.db')

class Database:
    def __init__(self):
        """Initialize database connection."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Database connection established.")
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to the database: {err}")
            raise

    def __enter__(self):
        """Support context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database resources on context manager exit."""
        self.close()

    def close(self):
        """Close database connection and cursor."""
        try:
            if self.cursor:
                self.cursor.close()
                logger.info("Database cursor closed.")
            if self.connection:
                self.connection.close()
                logger.info("Database connection closed.")
        except mysql.connector.Error as err:
            logger.error(f"Error closing database resources: {err}")

    def update_time_settings(self, roll_up_time, roll_down_time):
        """Update the roll up and roll down times in the database."""
        try:
            query = """
            INSERT INTO time_settings (id, roll_up_time, roll_down_time) 
            VALUES (1, %s, %s) 
            ON DUPLICATE KEY UPDATE roll_up_time = VALUES(roll_up_time), roll_down_time = VALUES(roll_down_time)
            """
            values = (roll_up_time, roll_down_time)
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info("Time settings updated successfully.")
        except mysql.connector.Error as err:
            logger.error(f"Error updating time settings: {err}")

    def get_latest_time_settings(self):
        """Retrieve the latest roll up and roll down times."""
        try:
            query = "SELECT roll_up_time, roll_down_time FROM time_settings ORDER BY id DESC LIMIT 1"
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving latest time settings: {err}")
            return None

    def get_time_setting(self, setting_name):
        """Retrieve a specific time setting (roll_up_time or roll_down_time)."""
        try:
            sql = f"SELECT {setting_name} FROM time_settings ORDER BY id DESC LIMIT 1"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result[setting_name] if result else None
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving {setting_name}: {err}")
            return None

    def get_motor_statuses(self):
        """Retrieve the statuses of all motors."""
        try:
            query = "SELECT motor_id, status FROM motor_statuses"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving motor statuses: {err}")
            return []

    def update_motor_status(self, motor_id, status):
        """Update the status of a motor."""
        try:
            query = "UPDATE motor_statuses SET status = %s WHERE motor_id = %s"
            values = (status, motor_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info(f"Motor status for motor_id={motor_id} updated successfully to {status}.")
        except mysql.connector.Error as err:
            logger.error(f"Error updating motor status for motor_id={motor_id}: {err}")

    def save_api_token(self, token, expiry_time):
        """Save the API token and its expiry time."""
        try:
            query = "REPLACE INTO api_tokens (token, expiry_time) VALUES (%s, %s)"
            values = (token, expiry_time)
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info("API token saved successfully.")
        except mysql.connector.Error as err:
            logger.error(f"Error saving API token: {err}")

    def get_api_token(self):
        """Retrieve the API token and its expiry time."""
        try:
            query = "SELECT token, expiry_time FROM api_tokens LIMIT 1"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result if result else (None, None)
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving API token: {err}")
            return None, None

    def save_sensor_data(self, timestamp, temperature, humidity, vpd):
        """Save sensor data (temperature, humidity, VPD) to the database."""
        try:
            query = """
            INSERT INTO sensor_data (timestamp, temperature, humidity, vpd) 
            VALUES (%s, %s, %s, %s)
            """
            values = (timestamp, temperature, humidity, vpd)
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info("Sensor data saved successfully.")
        except mysql.connector.Error as err:
            logger.error(f"Error saving sensor data (Temperature: {temperature}, Humidity: {humidity}, VPD: {vpd}): {err}")
        except Exception as e:
            logger.error(f"Unexpected error in save_sensor_data (Temperature: {temperature}, Humidity: {humidity}, VPD: {vpd}): {e}")

# Additional methods here
