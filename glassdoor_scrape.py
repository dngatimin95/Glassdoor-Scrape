"""Adapted from natmod's glassdoor-scrape repo (https://github.com/natmod/glassdoor-scrape) and
arapfaik's scraping-glassdoor-selenium repo (https://github.com/arapfaik/scraping-glassdoor-selenium)"""

import time
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords

def scrape_jobs():
    job_name, country, num_jobs = input("Please enter a job name, a location and the number of jobs seperated by comma:\n").split(',')

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(1120, 1000)

    location_id = {'san francisco':1147401, 'new york':1132348, 'boston':1154532, 'los angeles':1146821, 'singapore': 3235921, 'jakarta':2709872}

    job_name = job_name.strip().lower()
    country = country.strip().lower()
    num_jobs = int(num_jobs)
    if country in location_id:
        url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=' +\
            job_name + '&sc.keyword=' + job_name + '&locT=C&locId=' + str(location_id[country]) + '&jobType='

    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:
        time.sleep(4)
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_id("prefix__icon-close-1").click()
        except NoSuchElementException:
            pass

        job_posts = driver.find_elements_by_class_name("jl")
        for posts in job_posts:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            posts.click()
            time.sleep(1)
            collected = False

            while not collected:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1

            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1

            company_name = company_name[:-4]
            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location})

        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
    return pd.DataFrame(jobs)

def simplify_desc(txt):
    tokens = word_tokenize(txt)
    stopset = set(stopwords.words('english'))
    tokens = [x.lower() for x in tokens if not x in stopset]
    text = nltk.Text(tokens)
    return list(set(text))

def skill_search(jobs_df):
    words = []

    for description in jobs_df['Job Description']:
        words.append(simplify_desc(description))

    doc_frequency = Counter()
    [doc_frequency.update(word) for word in words]

    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'], 'C#':doc_frequency['c#'],
                    'Ruby':doc_frequency['ruby'], 'Julia':doc_frequency['julia'],
                    'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                    'Mathematica':doc_frequency['mathematica'], 'Php':doc_frequency['php'],
                    'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala'],
                    'Octave':doc_frequency['octave']})

    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                        'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                        'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3'],
                        'Spotfire': doc_frequency['spotfire'],'Stata':doc_frequency['stata'],
                        'Power BI': doc_frequency['power bi']})

    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
                'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
                'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})

    other_dict = Counter({'Azure':doc_frequency['azure'], 'AWS':doc_frequency['aws']})

    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'], 'MySQL':doc_frequency['mysql'],
                    'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                    'MongoDB':doc_frequency['mongodb']})

    edu_dict = Counter({'Bachelor':doc_frequency['bachelor'],'Master':doc_frequency['master'],\
                          'PhD': doc_frequency['phd'],'MBA':doc_frequency['mba']})

    education_dict = Counter({'Computer Science':doc_frequency['computer science'], 'MIS':doc_frequency['mis'],
                              'Statistics':doc_frequency['statistics'],
                              'Mathematics':doc_frequency['mathematics'],
                              'Physics':doc_frequency['physics'],
                              'Machine Learning':doc_frequency['machine learning'],
                              'Economics':doc_frequency['economics'],
                              'Software Engineer': doc_frequency['software engineer'],
                              'Information System':doc_frequency['information system'],
                              'Quantitative Finance':doc_frequency['quantitative finance']})

    skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict + other_dict

    skills_frame = pd.DataFrame(list(skills.items()), columns = ['Term', 'Number of Postings'])
    edu_frame = pd.DataFrame(list(edu_dict.items()), columns = ['Education Level', 'Number of Postings'])
    focus_frame = pd.DataFrame(list(education_dict.items()), columns = ['Major Focus', 'Number of Postings'])

    skills_frame['Number of Postings'] = (skills_frame['Number of Postings'])*100/len(jobs_df)

    skills_frame.sort_values(by='Number of Postings', ascending = False, inplace = True)
    edu_frame.sort_values(by='Number of Postings', ascending = False, inplace = True)
    focus_frame.sort_values(by='Number of Postings', ascending = False, inplace = True)
    return skills_frame, edu_frame, focus_frame

pd.set_option('display.max_columns', None)
jobs_df = scrape_jobs()
#df.to_csv('C:\Users\****\Desktop\Job descriptions.csv')

skill_df, edu_df, focus_df = skill_search(jobs_df)

skill_df.plot.bar(x='Term', y='Number of Postings',figsize=(10,6))
edu_df.plot.bar(x='Education Level', y='Number of Postings',figsize=(10,6))
focus_df.plot.bar(x='Major Focus', y='Number of Postings',figsize=(10,6))
plt.show()
