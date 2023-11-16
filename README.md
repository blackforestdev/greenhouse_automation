# Greenhouse Automation Project

## Overview
This project is designed to automate various greenhouse operations, providing a web interface to control and monitor environmental conditions.

## Features
- **Web Interface**: Control and monitor your greenhouse environment through a user-friendly web interface.
- **Real-Time Updates**: Using WebSocket for real-time communication between the client and server.
- **Environmental Monitoring**: Track temperature, humidity, and other environmental factors.
- **Motor Controls**: Manage greenhouse motors for functions like rolling up and down sidewalls.

## Prerequisites
Before installing the project, ensure you have the following installed:
- Python 3
- Node.js (for managing Bootstrap and other front-end dependencies)

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone [https://gitlab.com/dev8292144/greenhouse_automation/]
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. sudo apt-get update
sudo apt-get install nodejs npm
4. install the database: 
sudo apt-get install mariadb 
```configure the database by running setup_config.py```

## Usage
To run the application:

1. Start the server:
   ```bash
   python3 main.py
   ```

2. Access the web interface at [http://localhost:5000] (or your configured address).

## Contributing
Contributions to the project are welcome. Please follow standard coding conventions and add unit tests for new features.

## License
This project is licensed under the MIT License.


### Additional Notes:


