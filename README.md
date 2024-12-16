# Data Analysis Repo
Here is a place for a data analysis projects.
I am looking for insights and creating business value thanks to visualisation and Machine Learning tools.

## 🖥️ Notebook Pricing Analysis

### 📄 Source  
The data is scraped directly from a web shop's page. A **scraping script** is included as part of the project to ensure reproducibility and allow users to update the dataset when needed.

### 🔍 Relevant Features  
This project demonstrates the complete processing of data, including:  
- 🛒 **Scraping Data**: Extracting information from the web shop to build a dataset.  
- 🧹 **Data Cleaning**: Preparing raw data for analysis by removing inconsistencies and outliers.  
- 🔍 **Data Enrichment**: Adding contextual information to enhance the dataset.  
- 🤖 **Machine Learning Integration**: Using the processed data as input for predictive modeling and analytics.

Number of Instances: ~1000, values are varying based on shop product availability
Number of Input Attributes: ~60

### 🎯 Purpose  
The primary goal of this project is to:  
- Empower users with **in-depth insights** for selecting the most suitable PC hardware.  
- Support informed decision-making by offering analytics and predictions based on real market data.  

## Bank Marketing data
### 📄Source:
  
   Created by: Paulo Cortez (Univ. Minho) and Sérgio Moro (ISCTE-IUL) @ 2012
   
### 🔍Relevant Information:

   The data is related with direct marketing campaigns of a Portuguese banking institution. 
   The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, 
   in order to access if the product (bank term deposit) would be (or not) subscribed. 
   
  There are two datasets: 
    1) bank-full.csv with all examples, ordered by date (from May 2008 to November 2010).
    2) bank.csv - undersampled dataset. In this file there is similar count of positive and negative samples, what is very helpful in creating ML model.
     The smaller dataset is useful to test more computationally demanding machine learning algorithms (e.g. SVM).

  Number of Instances: 45211 for bank-full.csv
  
  Number of Attributes: 16 + output attribute.
