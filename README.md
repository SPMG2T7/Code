# Code

### Pre-requisites files to have
1. .env file (Refer to Telegram Pinned)
2. search.env file (Refer to Telegram Pinned)
3. prepare_script.sql (Refer to Telegram Pinned)
4. requirements.txt

### To setup frontend
1. Navigate to src/Frontend/feature2/ondeh-ondeh/src
2. Run 'npm install'
3. Run 'npm run serve'
4. Click on the link generated once the command has been run successfully to open the index page

### To setup backend
1. Copy the respective .env file based on OS to the root directory of the repo (Refer to Telegram Pinned)
2. Start your WAMP/MAMP, execute the prepare_script.sql
3. Install the library needed for backend by running 'pip install -r requirements.txt'
4. Copy the .env file to /
5. Copy the search.env & .env file to /src/Backend
6. Go to src/Backend folder, run 'python app.py' to start the backend, if there are 'No Modules' error, just run 'pip install <module_name>' based on the error of module name shown
7. Go to src/Backend folder, run 'docker-compose up' to start the search container
8. If there is an error with MeiliSearch docker happening on first "docker-compose up", re-run the command "docker-compose up" again


!!! IMPORTANT !!!
1. If you encounter an error with the search function relating to "No index 'Role' found", try to run the docker-compose down command and then run the docker-compose up command again.
2. If you encounter an error called "MeilisearchCommunicationError", try to run docker compose up again. This issue arises when the docker MeiliSearch container starts slower than the flask app resulting in it referring to a non-existent container.