# LearnTime - Learn it! • Time it! • Track it!
#### Description:
LearnTime is a LearnTime Tracker. So what exactly can it do?

- it can be just an easy to use simple timer
- you can assign your timer to different subjects
- you can add/remove/edit subjects
- you can see the total time learned for each subject
- you can register or login
- you can save up to 4 preset timers

And all of that in an easy to use, intuitive design. That's what makes LearnTime so great.

---
my Usecases:
- LearnTime tracking: When learning for subjects in 90 minute Inervalls I can see an overview of how many minutes I've studied for each subject in total
- Practice Exam with breaks: When going through practice exams that should take i.e. 120 minutes and I want to practice but don't have 120 minutes in a row, I can create a new subject and call it practice exam 1 and then track the total time I've spend on that practice exam

---

## How to use LearnTime?


### Register:
To use LearnTime you need to be signed in. To create an account you can click register in the header/navbar at the top.
Additionally you will find a button `Get Started` in the About page that will also redirect you to the register page.

On that register page simply choose a username (it has to be unique, if you'll get an error message simply return to the register page and select a new username). Then make sure to choose any password and repeat it exactly as is on the 'Repeat Password' field. Then click `Register`. You should get redirected to the Homepage.

### Log In:
To Log In simply click on `Log In` in the Header and enter your username and password. If you don't see a Log In button in your Header/Navbar at the top, you are likely already signed in. Even if so you may still go to the `/login` page to log in.

### Log Out:
To Log Out simply click on `Log Out` in the Header/Navbar. If you don't see a Log Out button in your Header/Navbar at the top, you are likely already signed out.

### myAccount page:
Once Signed In you will see a `myAccount` Section at the top right of your Header/Navbar. Once you click on it you will see a welcome message with your username in bold text. There you will find two buttons. The first one is `Change Password` and I'll talk about the second one later.

### Change Password
To change your Password, go to the `/change_password` page by clicking the button in the myAccount page as per the paragraph atop. Then type in your old password followed by your new password and don't forget to retype it below. Then you must select the checkbox that says 'I understand and accept the fact that this can not be reverted!' to click that button and change your password.

**Note: You need to have your old password present in order to change it. If you cannot remember your password, you can always just create a new free account**

### Homepage (Timer Page):
On the Homepage `/` you can find the timer itself.
#### Setting length:
By default it show 90 Minutes. To change the timer duration you can use the `+` and `-` buttons you can find right and left of the timer number.

#### Controlling the Timer:
you can start the timer by clicking on the `Start` Button and stop it by clicking on the `Stop` button. Note that you can only click on the start button when the timer is not started already. Respectively you cannot click on the stop button if the timer is already stopped/not running. Selecting the start button will disable all other buttons except for the stop button on that page. To reenable click the stop button.

If the timer has ended you can stop the music/alarm sound by clicking the stop button.

When the timer is running and you're trying to leave the timer/home page there should appear a popup from your browser that will ask you to confirm that you want to close the page.

The timer minutes will also appear in the title of your tab, while running.

The reset button will **always** reset to 90 Minutes. If you commonly want to reset to a different length you can create Timer Presets.

### Timer Presets:
To create Timer presets go to the 'Timer Presets' `/presets` page. There you can create up to 4 timer presets.
Simply enter the length in Minutes and click the `Add Preset` Button. Note: If you already have 4 presets you will not see that Button, to add new presets you must first delete existing ones.

You will see a list of all of your Presets below. To **Delete** a timer presets click on the delete button next to it on the right and confirm the browser popup asking you to confirm your deletion.

To use the Timer Presets go to the timer page (aka. Homepage). There you will see the buttons below the select subject menu. Simply click on a button to set the timer to that length if the timer isn't running already. The Timer Presets will appear on the Homepage in increasing length from left to right.

### Manage Subjects
This is what makes LearnTime so special. You can create and manage subjects on the subjects page `/subjects`.

To create a new subject, enter a name and click the `Add Subject` button beneath. The subjects should appear in a list below.

To delete a subject click on the `Delete` button next to the subject name on the right and confirm in the popup.

To change the name of a subject click the `Edit` Button right next to the name. There you can change the name in the input field and click the `Save Changes` Button to save the changes.

### Use Subject Timers
In the Homepage / Timer page you will find a dropdown list beneath your timer display. Select on of the subjects you have created as by the pargraphs above and start a timer. Now when you click on `Stop` the time you have learned will be saved for that specific subjects.

Note: If no subject is selected, the time will not be saved to your statistics.

### See your Stats
To see your stats *(statistics)* go to the stats page `/stats`. There you will see an overview with the total time learned for each individual subject. If you want to see a history of all of your logged time you can find it via the second button in the myAccount page (the last timer will appear at the very bottom).

---
### Requirements / Setup:

You need python and pip.
then when in the folder execute
```
python3 -m venv venv
````
to create a virtual environment.

Then run the following for Mac/Linux
````
source venv/bin/activate
````
or this on Windows
````
venv\Scripts\activate
````

Then run

````
pip install -r requirements.txt
````

To install all the requiered packages.

Then run the following comands to set everything else up:

````
export FLASK_APP=app.py
export FLASK_ENV=development  # Optional, for development mode
````

then to run just type 
```
flask run
```
and LearnTime should run on `http://127.0.0.1:5000/`


---

## How it works.

This is a flask web application. The main app that handles everything in the backend is the `app.py` file. It uses Flask and to run the app use the command ```flask run```. The database used is a sqlite3 database managed by SQLAlchemy in the app.py file.
In the `/templates` folder you will find all of the HTML code of that website. These use jinja templates. The main layout is in the `layout.html` file. This includes the Header, Title and Footer of the page. All other templates extend the layout.html one.
The layout.html includes uses Bootstrap. A css file can be found in the `static` folder, where you can also find the two javascript files that were used. the `button-sounds.js` file handles all buttons with the class 'button-add-sfx' or 'button-pop-sfx'. It makes sure that sound is played when clicking the Buttons. It also handles the popup when clicking the delete Buttons which have the button-pop-sfx class. The `timer.js` file handles everything timer related on the homepage, like using localStorage to save the timer state and update the *disable* property of each button on the timer page and of course the file also updates the timer display in the page itself and in the title. The sounds used for the alarm and the buttons are in `static/sounds`. The helpers.py file includes the python decorator @login_required that is used in the app.py for the pages that require login. Furthermore the file contains the apologize function borrowed from CS50 finance to display error messages with meme cat photos, because - why not.

The Database schema of my db used:

``` SQL
sqlite> .schema
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE subjects (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, subject TEXT NOT NULL);
CREATE TABLE tracker (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, minutes NUMERIC NOT NULL);
CREATE TABLE presets (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, minutes INTEGER NOT NULL);
sqlite>
```

## I hope you like it.
