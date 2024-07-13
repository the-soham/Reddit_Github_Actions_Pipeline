# Interactions of Football/Soccer Club Fans on Reddit

## Description

In this project, I have tried to capture the interactions of football fans of all the 20 Football clubs of the English Premier Club. The data is scraped at a 24 hr interval using reddit's PRAW api and jupyter notebook that is orchestrated using Github Actions. The scraped data is then stored in Data Folder as a csv file. The fan interactions are then displayed on a public facing [dashboard](https://reddit-epl-interactions.streamlit.app/) created using streamlit.

If you have any questions or are looking to hire someone with data-skills then please feel free to reach out @ [sohambhagwat2@gmail.com](sohambhagwat2@gmail.com) or on [Linkedin](https://www.linkedin.com/in/soham-bhagwat/).

## Architecture Diagram

![architecture](https://github.com/the-soham/Reddit_Github_Actions_Pipeline/blob/main/Reddit_Datapipeline%20diag.svg)

## Workflow
* The python notebook is triggered using the github actions workflow with an interval of 24 hrs.
* The script scrpaes all the relevant data from the subreddits and appends/writes it to the csv file.
* The streamlit dashboard deployed on streamlit cloud reads the data stored in the csv file in the github repo and renders the dashboard.

## Dashboard Sample
![dashboard sample](https://github.com/the-soham/Reddit_Github_Actions_Pipeline/blob/main/dashboard_sample.png)
