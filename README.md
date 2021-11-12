# Recognition and severity of issues asymmetries

## Abstract

This project will compare the number of quotes about specific death causes with their actual death toll. The background for this research is our belief that there is a significant asymmetry between the issues with the highest death tolls and the most spoken about issues. We will combine the Quotebank dataset with data from Our World in Data, which has ranked the number of deaths by cause from 1970 to 2017. The death toll does not consider factors such as the fear created by e.g. a terrorist attack and suffering without death. However, we believe that the death toll is still a decent indicator of the severity of most issues. This research aims to learn what issues society cares most about and see if it correlates to the death tolls. Furthermore, the research will show which issues are neglected and hence might need more attention.

## Research questions

1. Is there a significant asymmetry between the issues that receive the most attention and the issues that cause most deaths?
2. Does the number of quotes about an issue increase/decrease proportionally to the number of deaths per year?
3. Does the average age of victims of an issue affect how much attention it receives?
4. Do issues receive more/less attention based on the average GDP of the countries they affect?
5. Do issues grouped into injuries, communicable diseases, and non-communicable diseases receive different amounts of attention per death caused?

## Datasets

In addition to the Quotebank dataset, we will explore the data used in an article published in Our World in Data, available here: https://ourworldindata.org/causes-of-death. These datasets are extracted from other sources, mainly from Global Burden of Disease, a global study on the causes of death and disease, available here: http://ghdx.healthdata.org/gbd-results-tool, but also Amnesty International, which records data on e.g., executions, available here: https://www.amnesty.org/en/what-we-do/death-penalty/. The datasets used in Our World in Data contain estimations of the annual death tolls and their causes for each country and age group from 1970 to 2017. Hence, we will use the overlapping years between the Quotebank dataset and the Our World in Data data: 2008-2017. The dataset from Our World in Data is already stored in a CSV file and needs minimal preprocessing. It includes death by cause for the world, individual countries, and different age groups, allowing us to work on all the research questions.

We also use data from the UN with annual population count, available here: https://population.un.org/wpp/Download/Standard/Population/. This data is combined with the Our World in Data data to understand the yearly relative death tolls better.

For research question four, we also need data on the GDP of countries and the country of origin for the speakers. We will get the GDP data from The World Bank, available here: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD, and the origin countries are retrieved from Wikidata using the speakers QIDs.

## Methods

To estimate asymmetries between media coverage and actual death causes, we have two main challenges.

- **1. Quote categorization**: To accurately categorize the quotes to causes of death, we compare keywords for each death cause with the quotes. The process will be optimized by analyzing a sample of the classified quotes, and then modifying the keywords we use. We are currently just comparing strings in Python, but we plan on using The Fuzz, available here: https://github.com/seatgeek/thefuzz, which will allow us to include misspelled words or other slight modifications. For Milestone 1, we are not using The Fuzz because reading and comparing the quotes take too long, but we will try to optimize this process in Milestone 2. Examples of the preliminary keywords we use to extract relevant quotes are:

  - Diarrheal: dierrhea, cholera, etec, rotavirus, shigellosis, typhoid

  - Lower respiratory infections: lower respiratory infections, pneumonia, bronchitis, tuberculosis

  - Intestinal infectious diseases: intestinal infectious diseases, cholera, typhoid fever, paratyphoid fever, salmonella

- **2. Under-represented vs. over-represented**: To answer our first research question, we will compare the ratios between deaths and quotes for all the issues.

Once we have answers to these two strategies, we will develop our methods for the research questions 2-5. Our World in Data has all the information we need for these research questions in combination with population data and GDP data. However, research question four considers countries' GDP, and the Quotebank dataset may be too restrictive. Understandably, people talk more about death causes that affect their country. Therefore, we would need speakers from various countries with different GDP levels to research question four. We are not confident that the Quotebank dataset contains enough quotes by people from countries with a low GDP.

## Proposed Project Timeline

- Week 45: As of now, the project pipeline is in place. We have performed initial analysis on most of the relevant Our World of Data datasets, made the code skeleton to extract quotes belonging to specific death causes, and planned how to compare them to their actual death toll.

- Week 48: The goal is to have an initial analysis made on each death cause and to have preliminary results, e.g., results concerning the first of our research questions, and to have the structure in place to go further in our analysis.

- Week 49: More in-depth analysis made and research carried out concerning the rest of our research questions.

- Week 50: Finishing up the project – working on presenting and visualizing the results.

## Organization within the team

The current main tasks for each team member are the following:

**Andrea Perozziello**: Developing the code skeleton and the optimization quote classification.

**Oliver Welin Odeback**: Responsible for the data story and visualization of results.

**Jurriaan Schuring**: Data-preprocessing, working on extracting information of which country each quote origins from and connecting to the death causes in each country.

**Henrik Myhre**: Mainly responsible for data wrangling and analyses performed on the Our World in Data.
