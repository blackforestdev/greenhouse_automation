1.) Address the issue with GPIO permissions as running the program with sudo is not viable in production. the current workaround is to run: sudo usermod -a -G gpio your_username
2.) Build database builder to generate the required database configuration for the application to function.
3.) modify main.py to run in a tmux session for remote admin.     