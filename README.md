# Recognition and severity of issues asymmetries

## Abstract

In this project, we will compare the number of quotes about certain death causes with their actual death toll. The background for this research is our belief that there is a significant asymmetry between the issues with the highest death tolls and the most spoken about issues. We will combine the Quotebank dataset with data from Our World in Data, which has ranked the number of deaths by cause from 1970 to 2017. The death toll does not consider factors such as at what age people die, the fear created by e.g. a terrorist attack, and suffering without death. However, the death toll is still a decent indicator of the severity of most issues. The goal of this research is to learn what issues society cares most about and see if it correlates to the death tolls. Furthermore, the research will show which issues are neglected and hence might need more attention.

## Research questions

1) Is there a significant asymmetry between the issues that receive the most attention and the issues that cause most deaths?
2) Does the number of quotes about an issue increase/decrease proportionally to the number of deaths per year?
3) Does the average age of victims of an issue affect how much attention it receives?
4) Do issues receive more/less attention based on the average GDP of the countries they affect?
5) Do issues grouped into injuries, communicable diseases and non-communicable diseases receive different amounts of attention per death caused?


## Datasets

In addition to the Quotebank dataset, we will explore the data used in an article published in Our World in Data, available here: https://ourworldindata.org/causes-of-death. This dataset is in turn extracted from other sources, mainly from Global Burden of Disease, a global study on the causes of death and disease, available here: http://ghdx.healthdata.org/gbd-results-tool, but also Amnesty International, which records data on e.g. executions, available here: https://www.amnesty.org/en/what-we-do/death-penalty/). The dataset used in Our World in Data contains estimations of the annual deathtolls as well as their causes for each country from 1970 to 2017. This dataset has been pre-processed and analyzed. 

## Methods

To estimate asymmetries between media coverage and actual death causes, we have two main challenges. 

* **Quote Categorization**: To extract accurate categorizations of quotes about a certain category of death, we will create an intelligent keyword extraction function. This means that quotes containing certain keywords belonging to a certain topic. This function will be optimized by analyzing the correctness of the classified quotes. The preliminary keywords used for each death cause is the following:



* **Under-represented vs over-represented**: To answer our research question, we will compare the ratios between the number of deaths and the number of quotes they have between the different quotes. 

Once we have answers to these two strategies in place, we will move on to develop our methods for the research questions 2-5.

## Proposed Project Timeline

* Week 45: As of now, the project pipeline is in place. We have performed initial analysis on the Our World of Data dataset, made the code skeleton for the extraction of quotes belonging to a certain quote type, and how to compare them to their actual death toll. 

* Week 48: The goal is here to have initial analysis made on each death cause and to have preliminary results, e.g. results concerning the first of our research question, and to have the structure in place to go further in our analysis. 

* Week 49: More in-depth analysis made and research carried out concerning the rest of our research questions. 

* Week 50: Finishing up the project – working on presenting and visualizing the results.

## Organization within team

The current main tasks for each team member are the following:

**Andrea**: Developing the code skeleton and the optimization quote classification.

**Oliver Welin Odeback**: Responsible for the data story and visualization of results. 

**Jurriaan Schuring**: Data-preprocessing, working on extracting information of which country each quote origins from and connecting to the death causes in each country. 

**Henrik Myhre**: Mainly responsible for data wrangling and analyses performed on the Our World in Data. 

