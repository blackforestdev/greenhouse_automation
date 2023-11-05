# /modules/db.py

import mysql.connector
import logging
from config import DB_CONFIG

logger = logging.getLogger('my_application.db')

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)  # Use dictionary cursor to return results as dictionaries
            logger.info("Database connection established.")
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to the database: {err}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
                logger.info("Database cursor closed.")
            if self.connection:
                self.connection.close()
                logger.info("Database connection closed.")
        except mysql.connector.Error as err:
            logger.error(f"Error closing database resources: {err}")

    def save_time_settings(self, roll_up_time, roll_down_time):
        """Save the roll up and roll down times."""
        try:
            query = "INSERT INTO time_settings (roll_up_time, roll_down_time) VALUES (%s, %s)"
            values = (roll_up_time, roll_down_time)
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info("Time settings saved successfully.")
        except mysql.connector.Error as err:
            logger.error(f"Error saving time settings: {err}")

    def get_latest_time_settings(self):
        """Retrieve the latest roll up and roll down times."""
        try:
            query = "SELECT roll_up_time, roll_down_time FROM time_settings ORDER BY id DESC LIMIT 1"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                logger.info("Latest time settings retrieved successfully.")
            return result
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving latest time settings: {err}")
            return None
        
    def get_roll_up_time(self):
        try:
            sql = "SELECT roll_up_time FROM time_settings ORDER BY id DESC LIMIT 1"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result:
                logger.info("Roll up time retrieved successfully.")
            return result[0] if result else None
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving roll up time: {err}")
            return None

    def get_roll_down_time(self):
        try:
            sql = "SELECT roll_down_time FROM time_settings ORDER BY id DESC LIMIT 1"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result:
                logger.info("Roll down time retrieved successfully.")
            return result[0] if result else None
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving roll down time: {err}")
            return None

    # Motor status related methods
    def get_motor_statuses(self):
        """Retrieve the statuses of all motors."""
        try:
            query = "SELECT motor_id, status FROM motor_statuses"
            self.cursor.execute(query)
            motor_statuses = self.cursor.fetchall()
            if motor_statuses:
                logger.info("Motor statuses retrieved successfully: %s", motor_statuses)
            else:
                logger.info("Motor statuses query returned no results.")
            return motor_statuses
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving motor statuses: {err}")
            raise

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
            raise

# You may continue with other methods you already have for time settings...
# Be sure to keep your existing time settings methods here as well.

