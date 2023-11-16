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
3. cd [your_project_directory]
npm install

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
- Make sure to replace `[your_project_directory]` with the actual path where your project is located.
- If you have specific Node.js and npm versions that are required, it's good to mention those versions in the `Prerequisites` section.
- If your project uses a `package.json` file (which it should, if you're using npm), include instructions on how to use it, especially if there are scripts set up for building or running the project.
- Consider adding a section on how to set up and run any databases (like MariaDB) that are required for the project.

These updates will provide clear instructions to developers on how to set up and run your project, including the installation of Node.js, which is crucial for managing front-end dependencies.


