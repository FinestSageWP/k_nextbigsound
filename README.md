# KPOP Next Big Sound

#### Description: A web application utilizing the Python-based web framework Flask, that tracks and ranks social metrics and statistics of KPOP artists. The data used in this were personally compiled by me since year 2020 and 2021 by web-scraping and utilizing API from nextbigsound.com and guyso.me. This web application is essentially helpful for people in the KPOP community to help them keep track of their idol's engagement and performance in the different social platforms. This web app utilizes Bootstrap 4.5.3, PostgreSQL as database and JavaScript with JQuery. It has built-in support feature for logging in/out and signing up as well as changing passwords.

## Files

### `project/static`
##### Static folder holds the pictures, icons, fonts and stylesheets which I produced for my web application.
#### `style.css`
##### Here lies the custom styles which I incorporated in my web app. The style which I used is minimalist and minimally change the built in Bootstrap css.

### `project/templates`
#### `login.html`
##### This renders the login page when the web app prompts for login.

#### `apology.html`
##### Adapted from CS50 Finance. This renders the apology page when there are errors reported from the web app, specifying the code and the type of error.

#### `change_pass.html`
##### Idea from CS50 Finance. This renders the page where users can change their passwords.

#### `index.html`
##### This renders the landing page showing the summary of the charts and their ranked tabulation which is sortable by utilizing SQLite3 and JQuery.

#### `smi.html`
##### This renders the breakdown of the Social Metrics Chart every month of 2021 which is sortable as well by utilizing SQLite3 and JQuery.

#### `cmb.html`
##### This renders the breakdown of the Combined Chart every month of 2021 which is sortable as well by utilizing PostgreSQL and JQuery.

#### `search.html`
##### Allows the user to search for the specific data that they want by specifying the artist, chart type and the month they are looking for.

#### `searched.html`
##### The rendering page of `search.html` via `POST` method whic shows te data the user prompted.

#### `layout.html`
##### Serves as the template of the HTML files using the Jinja2 syntax.

#### `register.html`
##### Allows the user to sign up for a new account and access data by logging in.

## `project`

#### `application.py`
##### Python program which handles most of the functions using Flask. This receives input and gives output based on the user's prompt

#### `helpers.py`
##### An aiding program to the `application.py` which contains helping functions for convenient coding.

#### `nbs.db`
##### SQlite3 database that stores data of Next Big Sound web app and returns valus when queried nby user

#### `accounts.db`
##### PostgreSQL database that stores data of accounts that signs in the web app

#### `requirements.txt`
##### Written here are the required libraries/frameworks for the web app.








