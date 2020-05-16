In this first paragraph, I will go over the visual design (HTML/CSS choices) for the website as a whole, and in
the paragraphs after I will explain how all the visual elements work together with the backend code to create a
fully funcitonal website. For the overall look of the website, I wanted to go with something very clean looking. This
meant that I was only using a few CSS colors throughout, fonts are consistent, and everything is centered. The file
"styles.css" contains most of the general themes, and most of the alignment (margins, padding) is done in the individual
HTML templates. The navigation bar was implemented from Bootstrap, as well as the buttons throughout the website (Submit /
login buttons, the rating buttons on the "Add New Log" page). The twitter feeds were all embedded using Twitter's "publish"
feature, which allows you get twitter feeds of certain users in the form of an "a" element that works using a twitter JS
"script" source that I link to in the HTML templates. The file "layout.html" has the basic template of the navbar and the
footer that appears on each page, and each template extends that the layout's body using Django syntax.

For the backend details of the website, I will start with the register/login/logout features. Each of these routes
uses functions in "application.py" -- on the "POST" request of "register" which is activated by pressing the register button,
the function first checks if the username is already taken by querying to the "users" table in decdex.db and making sure
there are no entries for that inputted username. The HTML file also has a script for the onsubmit action, which makes sure
the user has inputted values for all the fields, the username/password are more than 6 characters in length, and the password
matches the confirmation, and the function returns false and gives an alert if any of the specifications aren't met. I put
this function in the html file rather than application.py so that the user is not taken to a whole new apology page on an
invalid register and the information already inputted in the page is not deleted. After a valid register, the function in
application.py puts the new users full name, username, and password hash into a table in decdex.db called users. It then logs
the user in by making the "session" the session of the users id, and then it redirects the logged in user to the homepage.

On the "POST" request of "login", the function in application.py queries the database for the inputted username. If there
is no entry for the username in the users table or if the user exists but the password hash does not match, the function
returns an apology page. In login.html, there is a JS function that makes sure the fields are not blank and returns
and false and gives an alert on the onsubmit action of the page. If the username and password match an entry in the database,
the user is loggin in by setting the "session" to the session of the user's id and the user is redirected to the homepage.
The logout feature works by simply clearing the session and redirecting to the login page.

The homepage's most complex feature is the calculator. The calculator works by utilizing anonymous that trigger on
the onchange action of any of the input fields. When a user inputs a number (the number must be a reasonable distance/time
for the given event), the inputted number is run through formulas that calcualate the point total, and the resulting number
is displayed in an "output" element in the right column of the table. If the user clears the inputted number, the script will
recognize that input as 0 and will display 0 in the output. If the user changes the input, since the function triggers on
the onchange action, the output will be immediately updated. The total points display at the bottom of the table works through
a function called "total", which simply adds all the numbers of the outputs of the table and displays it in another output
element. I get all of the inputs for the functions by using "document.getElementById()".

All of the pages in the "Events" dropdown selector in the navbar work exactly the same way. On the "POST" request of the
pages which are triggered by the submit button, application.py finds the inputted text through "request.form.get" and runs
it through a series of if statements. If the user has never submitted a cue for the event, the function inserts a row into
the "cues" table of decdex.db that specifies the user id, event name, and the inputted cue from the text field. It then
reloads the template with the saved cue by querying decdex.db for the cue saved for that event and displays it in the text
field using Django syntax. However, the function first checks if a user has already inputted a cue for the event by querying
decdex.db for any cues that have the user's id and the event name. If one exists, the page displays the saved cue and displays
a "Submit Edits" button instead of a "Submit Cue" button. If the user changes the text field and submits the edits, decdex.db
is updated with the new cue and the page is reloaded with that new cue. If the user deletes the cue by submitting a blank text
field, the whole row of the event is deleted in decdex.db and the page reloads with a blank field and a "Submit Cue" button.
On the "GET" request of the page, the function checks if a cue for the event has been saved and displays it, and displays a
blank text field otherwise. On any submission or edit, there is a JS function that displays an alert to let the user
know that their submission or edit has been recorded. These pages essentially store the users cue for an event and lets the
user edit it or delete it at any time.

The "Training Logs" dropdown selector in the navbar has two options, one to add a new training log and one to see the
previous logs. On the "POST" request of the add new log page which is triggered by hitting the "Submnit Log" button, a few
pieces of information are passed into the "logs" table of decdex.db. First, the date of the training session which is "date"
type of an input field so that it only accepts inputs in a date mm/dd/yyyy format. Second, the rating of the session -- this
works by using an onclick action of any of the buttons. When one button is clicked, the value of an invisible input field is
updated to be either "poor", "average", or "great", and this is the value passed on the "POST" request. A JS function
makes only one button selectable by changing the class of the other two buttons to a not-pressed class when one is clicked.
Finally, the events, what went well, and went went poorly are passed as text to decdex.db in their respective columns. There
is also JS function that returns false and an alert if any of the fields are left blank. On a successful submission, a
submission alert is displayed, all the information gets inserted into "logs" in decdex.db, and the user is redirected to the
previous logs page.

On the "GET" request of the previous logs page, application.py queries "logs" in decdex.db for any stored training logs.
It then uses Django to display each of the saved logs for the user in table format with the date, rating, events, and what
went well/poorly for each session. You will notice that hovering over any training session will turn the row a red color,
which was accomplished by using a :hover attribute in styles.css for the rows to signal to the user that clicking on a session
will delete it from their stored logs. The "POST" request of this page is triggered on the onclick action of any of the
rows -- this does a few things. First, clicking on a row triggeres a JS function that changes the value of an invisible input
field to the id of the session clicked on. Then, your browser will display a confirmation message of deleting the log, which
will return false if denied and true if accepted. If you accept, the "POST" request will continue and application.py takes the
id stored in the invisible input field using "request.form.get" and deletes from decdex.db the training session with this id
and the user id. It then reloads the page with the remaining training sessions in the table. Lastly, the about page simply displays some information about the website and uses a few "a" elements to link to Twitter
and a mailto: johnminicus@gmail.com page, which both open in new tabs using the "target=_blank" attribute.

This is the bulk of the backend details of the website, and I hope you have been able to gain a solid idea of what went
into the making of this DecDex web app.