# Template for ECS639U Group Coursework

This template should be used as the starting point for your group coursework in the module ECS639U Web Programming (at Queen Mary University of London). Use Git (github.qmul.ac.uk) to collaborate on the coursework with your group members. Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>

## Contribution

| Student ID | Name           | Assigned Task                                   | Final Deliverable                               |
| ---------- | -------------- | ----------------------------------------------- | ----------------------------------------------- |
| 210554416  | HongKai Yu     | Create statics image path and organise views.py | Create statics image path and organise views.py |
| 220519250  | Demoy Witter   | Testing/ Create test cases                      | Testing/ Create test cases                      |
| 220364926  | Quoc Viet Phan | Front/Backend, database                         | Front/Backend, database                         |
| ---------- | ----------     | Login/signup html template                      | Login/signup html template                      |

## User list

| UserName | Password |
| -------- | -------- |
| alan.schwartz@qmul.ac.uk | blueberry42 |
| raymond.hanna@qmul.ac.uk | summer2023 |
| jamal.wiley@qmul.ac.uk | applejuice1 |
| fatima.yates@qmul.ac.uk | piano12345 |
| josh.melton@qmul.ac.uk | sunshine88 |
| hasnain.cervantes@qmul.ac.uk | chocolate56 |
| frederic.zuniga@qmul.ac.uk | greenhouse9 |
| hussain.hansen@qmul.ac.uk | happyday7 |
| kieron.tanner@qmul.ac.uk | tiger2024 |
| dominic.chase@qmul.ac.uk | guitar77 |
| bill.valentine@qmul.ac.uk | watermelon3 |
| jorge.nolan@qmul.ac.uk | rainbow2010 |
| josiah.reynolds@qmul.ac.uk | soccerball4 |
| kadie.rasmussen@qmul.ac.uk | winter2022 |
| sophia.kaufman@qmul.ac.uk | butterfly56 |
| zara.francis@qmul.ac.uk | mountain33 |
| ashton.casey@qmul.ac.uk | snowflake21 |
| elif.osborn@qmul.ac.uk | puzzle8game |
| leah.fuller@qmul.ac.uk | balloon45 |
| ilyas.rubio@qmul.ac.uk | lovelyday1 |
| zuzanna.horne@qmul.ac.uk | blueSky9 |
| laurence.wilkins@qmul.ac.uk | carrot202 |
| macy.barrett@qmul.ac.uk | rainyDay7 |
| zachariah.newman@qmul.ac.uk | starfish8 |
| georgie.matthams@qmul.ac.uk | bookworm2 |
| jed.mcbride@qmul.ac.uk | cookie22 |
| kamran.romero@qmul.ac.uk | mountain4 |
| kian.carlson@qmul.ac.uk | treehouse3 |
| gladys.swanson@qmul.ac.uk | soccerball3 |
| sylvie.gibbons@qmul.ac.uk | jellyfish6 |
| jane.doe@qmul.ac.uk | fillerpassword |

## Super User

| UserName | Password |
| -------- | -------- |
| admin | JohmDoe2024Gr17 |

## URL for Deploy

https://group17-hobbies-app.apps.a.comp-teach.qmul.ac.uk/

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip and add the files to your own private repo.

3. Install Pyhton dependencies (main folder):

   ```console
   $ pip install -r requirements.txt
   ```

4. Create a development database:

   ```console
   $ python manage.py migrate
   ```

5. Install JavaScript dependencies (from 'frontend' folder):

   ```console
   $ npm install
   ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

   ```console
   $ python manage.py runserver
   ```

7. and the Vue server from the 'frontend' sub-folder:

   ```console
   $ npm run dev
   ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

   ```console
   $ npm run build
   ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
