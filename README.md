# COMP3297 Group I - IceCube
## BackTrack

## Installation
Kindly refer to the Django tutorial provided on course Moodle  
Please use Python3.x for this project

## Things to take note
### Git related rules
* Please create a new branch of your own and work on your branch only
* Please __DO NOT PUSH__ to __others' branch__
* Only push to __master branch__ when you have tested your modification does not break the code
* Please write __MEANINGFUL__ commit messages
* You are free to pull others branch and merge it to yours to check integration of each other's work
* Please make it a habit to push to github constantly even small changes have been made. Do not push in a big chunck as it will be very hard to revert to previous commit

### Django related stuff
* Admin account
  - ID: admin
  - PW: admin
* *Migrations*
  - When you create a model or make modifications to model.py and run 
    ```
    python manage.py makemigrations <app_name>
    ```
    a new .py file will be created in the "migrations" directory, DO NOT touch those .py files unless you are aware of what you are doing
  - models.py is going to be modified as we progress in the project, it will start to get messy when you have your previous models and data in the db.sqlite3, and you modify the model (eg. deleting a column), running
    ```
    python manage.py migration
    ```
    might not always reflect the changes accordingly (due to whatsoever reason). So please take note of that and try to bring up the problem in the group so that we can discuss and resolve it together
  - Please __backup db.sqlite3__ to your local machine if you have your data in it and you wish to restore it in case something went wrong during the migration
 
* *Templates*
  - The path for the template file will be in *<project_directory>/templates/*
  - The "common" directory is for common templates that can use across different pages for example headers, footers, navbar, etc
  - Please create a new directory for each new page
  - Try to modularise the components, usually components that can be reuse should be in different template files
  - Place all .css file in the css directory
  - When working on css, please bear in mind of devices with different screens, make it responsive
  - Place all .js file in the js directory new stuff
