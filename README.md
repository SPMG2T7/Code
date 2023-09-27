# Code

### Pre-requisites files to have
1. .env file (Refer to Telegram Pinned)
2. search.env file (Refer to Telegram Pinned)
3. prepare_script.sql (Refer to Telegram Pinned)

### To setup backend
1. Copy the respective .env file based on OS to the root directory of the repo (Refer to Telegram Pinned)
2. Start your WAMP/MAMP, execute the prepare_script.sql
3. Install the library dotenv by running 'pip install python-dotenv'
4. Copy the .env file to /
5. Copy the search.env file to /src/Backend
6. Go to src/Backend folder, run 'docker-compose up' to start the search container
7. Go to src/Backend folder, run 'python app.py' to start the backend, if there are 'No Modules' error, just run 'pip install <module_name>' based on the error of module name shown


!!! IMPORTANT !!!
If testing backend functions and you are too lazy to use the docker portion, look for the keyword 'MeiliSearch' in app.py and comment those sections out before resuming with your code.
