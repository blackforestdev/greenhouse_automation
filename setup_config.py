import os
import random
import string
import mysql.connector
from pathlib import Path

def generate_random_secret_key(length=32):
    """Generate a random secret key."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def setup_mariadb(username, password, database_name):
    """Setup MariaDB credentials and create database."""
    root_password = input("Enter your MariaDB root password: ")

    try:
        # Connect to MariaDB as root
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=root_password
        )

        cursor = connection.cursor()

        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        # Create user and grant privileges
        cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {database_name}.* TO '{username}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")

        # Close the connection
        cursor.close()
        connection.close()

        print("MariaDB setup completed successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def main():
    # Prompt the user for database credentials
    username = input("Enter your desired MariaDB username: ")
    password = input("Enter your desired MariaDB password: ")
    database_name = input("Enter your desired MariaDB database name: ")

    # Generate a random secret key
    secret_key = generate_random_secret_key()

    # Load the current content of config.py
    config_path = Path(__file__).parent / 'config.py'
    with config_path.open('r') as f:
        config_content = f.read()

    # Replace placeholders with actual values
    config_content = config_content.replace('your_username', username)
    config_content = config_content.replace('your_password', password)
    config_content = config_content.replace('your_database_name', database_name)
    config_content = config_content.replace('your_secret_key_here', secret_key)

    # Write the updated content back to config.py
    with config_path.open('w') as f:
        f.write(config_content)

    # Prompt user for MariaDB setup
    setup_db_choice = input("Do you want to set up the MariaDB database now? (yes/no): ").lower()
    if setup_db_choice == 'yes':
        setup_mariadb(username, password, database_name)

    print("Configurations updated successfully!")

if __name__ == "__main__":
    main()
