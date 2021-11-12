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

In addition to the Quotebank dataset, we will explore the data used in an article published in Our World in Data, available here: https://ourworldindata.org/causes-of-death. This dataset is extracted from other sources, mainly from Global Burden of Disease, a global study on the causes of death and disease, available here: http://ghdx.healthdata.org/gbd-results-tool, but also Amnesty International, which records data on e.g. executions, available here: https://www.amnesty.org/en/what-we-do/death-penalty/. The dataset used in Our World in Data contains estimations of the annual death tolls as well as their causes for each country from 1970 to 2017. Hence, we will use the overlapping years between the Quotebank dataset and the Our World in Data data: 2008-2017. The dataset from Our World in Data is already stored in a CSV file and needs minimal preprocessing. It includes death by cause for the world, individual countries, and different age groups, allowing us to work on all the research questions.

We also use data from the UN with annual population count, available here: https://population.un.org/wpp/Download/Standard/Population/. This data is combined with the Our World in Data data to get a more realistic understanding of the yearly relative death tolls.

For research question four, we also need data on the GDP of countries. We can use data from The World Bank, available here: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD.

## Methods

To estimate asymmetries between media coverage and actual death causes, we have two main challenges.

- **1. Quote categorization**: To extract accurate categorizations of quotes about a certain category of death, we will create an intelligent keyword extraction function. This means extracting quotes that contain keywords belonging to a certain death cause. The function will be optimized by analyzing the correctness of the classified quotes. Examples of preliminary keywords used for the death causes are:

  - Diarrheal: dierrhea, cholera, etec, rotavirus, shigellosis, typhoid

  - Lower respiratory infections: lower respiratory infections, pneumonia, bronchitis, tuberculosis

  - Intestinal infectious diseases: intestinal infectious diseases, cholera, typhoid fever, paratyphoid fever, salmonella

- **2. Under-represented vs. over-represented**: To answer our first research question, we will compare the ratios between the number of deaths and quotes for all the issues.

Once we have answers to these two strategies in place, we will develop our methods for the research questions 2-5. In combination with population data and GDP data, Our World in Data has all the information we need for these research questions. However, research question four considers countries' GDP, and the Quotebank dataset may be too restrictive. Understandably, people talk more about death causes that affect their country. Therefore, we would need speakers from a wide range of countries with different GDP levels to research question four. We are not confident that the Quotebank dataset contains enough quotes by people from countries with a low GDP.

## Proposed Project Timeline

- Week 45: As of now, the project pipeline is in place. We have performed initial analysis on the Our World of Data dataset, made the code skeleton to extract quotes belonging to specific death causes, and planned how to compare them to their actual death toll.

- Week 48: The goal is to have an initial analysis made on each death cause and to have preliminary results, e.g., results concerning the first of our research questions, and to have the structure in place to go further in our analysis.

- Week 49: More in-depth analysis made and research carried out concerning the rest of our research questions.

- Week 50: Finishing up the project – working on presenting and visualizing the results.

## Organization within the team

The current main tasks for each team member are the following:

**Andrea Perozziello**: Developing the code skeleton and the optimization quote classification.

**Oliver Welin Odeback**: Responsible for the data story and visualization of results.

**Jurriaan Schuring**: Data-preprocessing, working on extracting information of which country each quote origins from and connecting to the death causes in each country.

**Henrik Myhre**: Mainly responsible for data wrangling and analyses performed on the Our World in Data.
