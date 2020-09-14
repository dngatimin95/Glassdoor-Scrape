# Glassdoor-Scrape

*This repo is targeted only for those seeking a career in data science, software engineer or data/business analyst. Hopefully, it can be expanded further for other careers.*

During my junior/senior year of college, I was browsing Glassdoor and LinkedIn for internship/full-time oppurtunities and was overwhelmed with the amount of information each job description had. There were alot of things people needed that might suit one particular job, but not for another. Thus, I was curious and wondered what skills were highly sought after so that I could polish my skills in a certain area and possibly learn something new while I had time, so that I would be a little more hireable. I also wanted to practice my scraping skills and try out Selenium (instead of using BeautifulSoup).

## So what does this repo do?
This repo initially requires the user to input a career of the user's choice, along with a location and the number of jobs one wants to know about. (E.g. data analyst, new york, 100) It then scrapes the Glassdoor website for the number of jobs, and stores important information into a dataframe which can then be exported into a csv or excel file. It collects information such as the job title, salary estimate, job description, rating, company name and exact location. After scraping and storing into a database, it looks into the job description and tallies certain keywords by tokenizing the job description. It counts how often each important keywords are mentioned such as how much the word "Bachelor's" appears compared to "Masters" or how often programming langauages such as "Python" or "SQL" appears in job descriptions. It is then stored into a different dataframe and plotted out using matplotlib to show users what the most important skills are.

## How do I run it?
Besides having to install certain libraries or packages, just downloading the repo and running it on python would be sufficient. Line 20 shows the comment #options.add_argument('headless'). Uncommenting this would hide the window that pops up when Selenium tries to scrape the website. I excluded it as seeing the website being scraped was pretty cool.

*Credit to natmod's glassdoor-scrape repo and arapfaik's scraping-glassdoor-selenium repo for walking me through how to use Selenium step by step*
