# Designing an ETL process, conducting exploratory analysis and presenting findings to learn more about data analytics as a career
A project for learning more about the career I aspire to.


**What is the goal of this project?**

I'm interested in becoming a data analyst in Australia, but wanted to answer some important questions first, particularly the following:
1. Which skills are most in-demand?
2. What are analysts paid on average?
3. Will I need to go back to university to stand a chance?


**How am I answering these questions?**

1. ETL process to gather information
  * Creating a scraper from scratch to collect job data from multiple sites that do not prohibit scraping or automation in their terms of use.
  * Extracting additional details from scraped information (e.g. salaries in the job listing body text) and cleaning the data.
  * Loading it into a Google Sheets database (for easy use with Tableau later).

2. Exploring the data
  * Connecting the data to Tableau Public.
  * Answering the primary questions with various dashboards.


**Summary of Results**

At time of writing (14/10/21) from a sample of nearly 550 job listings, the following insights hold true:
* SQL is the most in-demand skill, with just over 61% of all listings requiring or preferring applicants who know it.
* Of the 18% of listings containing a salary, the average is AU $120,998.48 per annum FTE.
* Only 32% of listings mention the need or preference for a degree or other tertiary qualification.


**Disclaimer**

Please do not run the scraper on sites that haven't consented to automation being used. This includes the majority of big sites like LinkedIn or Seek. Always check the terms of use before configuring a scraper for it.
In addition, please do not lower the scraping speed below the thershold I have set. This is a courtesy measure. Running too fast could be seen as an attack by the site owners.


**Usage notes**

This project is largely here for display purposes, and as such three things will need to be done for personal use: 
  1. You'll need to create your own blank Google sheet.
  2. The 'open by key' methods in database_interaction.py will need to be substituted for your own G Sheet's key.
  3. You'll need to set up your own service account credentials. Don't forget to give edit permissions to the service account.
