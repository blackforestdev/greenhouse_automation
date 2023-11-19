1.) Address the issue with GPIO permissions as running the program with sudo is not viable in production. the current workaround is to run: sudo usermod -a -G gpio your_username
2.) Build database builder to generate the required database configuration for the application to function.
3.) modify main.py to run in a tmux session for remote admin. 
4.) update the code for setup_config.py to configre the database 
5.) Update the code for medules/db.py for better error handling per save_sensor_data method 
6.) Add/build out phsical computing elelments in config.py for motor control.  