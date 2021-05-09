# twitter_dash


This is a web application created to remind the importance of data visualisation. This is a dashboard with Dynamic visualisations regarding the COVID-19 pandemic.

The file structure is as follows:

- templates: This file includes all the HTML files required for the web application.

- Static: This folder includes all the packages required for styling the HTML files.

- application.py: This is the main python file that contains all the commands required to run the app.

- hashtag.py: This python files consist of code for collecting hashtags from tweets and function to create the visualisation.

- live_tweets_graphs.py: This python file has the code to retrieve the live tweets from SQL and create visualisations.

- settings.py: This python file has the attributes required to call the SQL queries

- source.py: This python file has the code to retrieve the number of covid cases from the repository created by Johns Hopkins University, Github,2019, COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University, available at: https://github.com/CSSEGISandData/COVID-19, [Accessed 14 March 2021] 

- Procfile: It is the file used for running the code in the webserver

- requirements.txt: This is a file that contains all the requirements needed to run this application, this is used by the webserver while creating a virtual environment. 


The web application can be viewed in: https://twitter-analysis-dashboard.herokuapp.com/

