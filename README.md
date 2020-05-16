This web app is called DecDex, and it was created with a combination of Python and
HTML/CSS/Javascript using Python's frameworks Flask and Django. To run the app on your own, you should have
this directory downloaded called "decdex" in your IDE. In this directory are two folders called "static" and "templates",
which hold the style sheet and the HTML/JS templates for each route of the web app respectively. Along with
those folders is "application.py", which is the Python/Flask backend of the website. application.py tells DecDex
dynamically what exactly to load on each page when routes are reached by "GET" or "POST" requests. "helpers.py"
is just a few helping functions that appliction.py references, and "decdex.db" is the SQLite3 database that
stores three tables: user login information, user training logs, and user cues for each event in the decathlon.

To start running this app, change directorys into "decdex" in your IDE by executing "cd decdex" in your terminal.
If the decdex directory is in another folder in your IDE, make sure to execute "cd nameoffolder/decdex". From there,
you can simply type the argument "flask run" into your terminal to run Flask on the app and get a temporary host server.
The "flask run" argument should produce a line that says "Running on https:// ..." -- click on the link here in your
terminal to go to the login page of DecDex in a new tab in your browser. If this is your first time and you do not have an
account set up, click on either the "register" link in the top right or the link under the login button to go to the
register page. There, enter your full name and desired username / password. The app will make you re-enter your username /
password if either is under 6 characters in length, if your username is already taken, or if your password does not match
the password confirmation field. After registering, you should be logged in and redirected to the homepage.
The homepage has two main features: a decathlon calculator and a news feed. To use the calculator, simply type
in your distance/time in a decathlon event in the units of measurement specified on the left column of the table (eg.
"10.9" would work for the 100m, "1.8" for the high jump, "300" for the 1500m, etc.). The bottom row will add up all your
points and give you a decathlon score as you complete the table.

In the navigation bar, you can click on the events dropdown menu and select any of the 10 decathlon events to be taken
to a page where you can store cues (things to think about while competing in the event to help you do well) for the selected
event. To add a cue, simply type it into the text field and click the "Submit cue" button. You should recieve an alert from
your browser that your submission has been saved. Then, if at any point you want to edit or delete your list of cues, you
can simply edit it in the text field and click the same button that has now been changed to "Submit edits". If the text field
you leave is blank, the cue will be deleted and you can start from scratch. Each of the 10 pages in the events dropdown
selector works exactly the same way, however they all store cues independant from eachother, so changing the text field on
one of the 10 events will not affect any of the text fields on the other events' pages. Also on each page is a news feed
relating to each event that you can scroll through and interact with.

Also in the navigation bar is a dropdpown selector called "Training Logs". If you select "Add a New Log", you will
be taken to a page that has 5 fields to describe how your decathlon training session went. You can enter the date (most
easily done using the down arrow on the right side of the text field which will give you a visual calendar to select the
date from), rate how well the session went with three options ("poor", "average", "great"), enter what events you trained
for, and give summaries of what went well and what did not go so well. If you click the submit button at the bottom of the
page, you will be redirected to the "Previous Logs" section of the same "Training Logs" dropdown selector, where all of
your submitted training logs are displayed in table format. If you want to delete a log from your account, you can
simply click on it in the table and your browser will give you a confirmation warning, where you can either confirm or
deny the deletion.

Finally, there is an "About" page in the navigation bar that just gives a small amount of information about me and
the website. At any point, you can log out of your account using the "Log Out" link in the top right of the naviagtion bar
(this will obviously only appear if you are logged in). A few things to keep in mind during your use of DecDex: if you exit
out of your IDE or lose connection to the internet, the web app will not be able to run and you will have to restart the
app. Also, the link that flask gives you in your terminal is a one-time use link -- if you restart your IDE, you will
have to do "flask run" again, and it will give you a different link than you had before, so make sure to use the new one.

Thank you for using DecDex and enjoy!# DecDex
