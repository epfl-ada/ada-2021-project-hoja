# Recognition and severity of issues asymmetries

## Abstract

This project compares the number of quotes about specific death causes with their actual death toll.  We combined the Quotebank dataset with data from Our World in Data, which has ranked the number of deaths by cause from 1970 to 2017. The death toll does not consider factors such as the fear created by e.g. a terrorist attack and suffering without death. However, we believe that the death toll is still a decent indicator of the severity of most issues. In this project we show the difference between the attention death causes receive and the number of actual deaths. Furthermore, we show how the number of deaths influences the attention a certain topic gets. Finally, we try to shed light on the inbalances and try to reason on why they occur. For the full story, see: https://peroza.github.io/ada-2021-project-hoja-pages/

## Research questions

1. Is there a significant asymmetry between the issues that receive the most attention and the issues that cause most deaths?
2. Does the number of quotes about an issue increase/decrease proportionally to the number of deaths per year?
~~3. Does the average age of victims of an issue affect how much attention it receives?~~
~~4. Do issues receive more/less attention based on the average GDP of the countries they affect?~~
5. Do issues grouped into injuries, communicable diseases, and non-communicable diseases receive different amounts of attention per death caused?

## Datasets

In addition to the Quotebank dataset, we will explore the data used in an article published in Our World in Data, available here: https://ourworldindata.org/causes-of-death. These datasets are extracted from other sources, mainly from Global Burden of Disease, a global study on the causes of death and disease, available here: http://ghdx.healthdata.org/gbd-results-tool, but also Amnesty International, which records data on e.g., executions, available here: https://www.amnesty.org/en/what-we-do/death-penalty/. The datasets used in Our World in Data contain estimations of the annual death tolls and their causes for each country and age group from 1970 to 2017. Hence, we will use the overlapping years between the Quotebank dataset and the Our World in Data data: 2008-2017. The dataset from Our World in Data is already stored in a CSV file and needs minimal preprocessing. It includes death by cause for the world, individual countries, and different age groups, allowing us to work on all the research questions.



## Methods

**1. Quote categorization**: In order to identify when a certain quote mentions a particular death cause, we first created manually a list of keywords related to the topics of the Our World in Data. Next, we expanded these keywords by looking for aliases on Wikidata and finding synonyms using Wordnet. For some words we hardcoded exceptions to prevent Wikidata or Wordnet (Princeton University "About WordNet." https://wordnet.princeton.edu/. Princeton University. 2010.) from finding too many words, sometimes unrelated or giving high chances of finding a wrong quote. For example, one of the aliases of war on Wikidata is conflict. Conflict will however give many quotes which are not about war, so we chose to not take it from Wikidata.

After identification of quotes in the dataset and grouping them in the topics, we saw that some topics had quotes which we’re obviously not about the topic we wanted. For example, the topic poisoning contained quotes about water being poisoned with lead, but also about the political debate being poisoned. To filter out the latter type of quotes, we used [Sentence Transformers](https://www.sbert.net/) to vectorize the quotes of and then we clustered them with [HBDSCAN](https://hdbscan.readthedocs.io/en/latest/index.html). Finally, we took those clusters for which at least two of the top most important words are also in keywords.  This was done for those topics as defined in TOPICS_FOR_CLUSTERING in CONSTS.py.

We chose to use sentence transformers and HBDSCAN as opposed to a LDA method and k-means clustering because sentence transformers should be able to distinguish between different semantic uses of the same word, which is harder with LDA. The HBDSCAN allowed to automatically get the right number of clusters, without having to set it ourselves. The clustering method was taken from: https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6


**2. Deaths and death causes**: To get the number of deaths for each cause and type of cause, we analyzed the data from Our World in Data. The combination of this data with the found quotes per death cause allowed us to answer our research questions.

**3. Linking quotes to country**: To see where the quotes come from, we found the country of the url on which the quote can be found by wikidata if the URL had a wikidata page. The country of the speaker was found by first looking up the speaker in the speaker_attributes.parquet dataset, from which we could get the Q-identifier of the country of the speaker. From there we could find the country once again via wikidata. This information allows us to shed some perspective on possible biases in our dataset.



## Project Timeline (Milestone 2)

- Week 45: As of now, the project pipeline is in place. We have performed initial analysis on most of the relevant Our World of Data datasets, made the code skeleton to extract quotes belonging to specific death causes, and planned how to compare them to their actual death toll.

- Week 48: The goal is to have an initial analysis made on each death cause and to have preliminary results, e.g., results concerning the first of our research questions, and to have the structure in place to go further in our analysis.

- Week 49: More in-depth analysis made and research carried out concerning the rest of our research questions (2-5). The feasibility of research question four will be examined, and we may have to drop this due to lack of diversity based on the GDP of the origin countries of speakers. To do research question 3, we will also have to add more datasets from Our World in Data that includes age groups.

- Week 50: Finishing up the project – working on presenting and visualizing the results.

## Organization within the team

The main tasks done by each team member are the following:

**Andrea Perozziello**: Developing the code skeleton, structuring code and development of webpage.

**Oliver Welin Odeback**: Responsible for the data story, visualization of results and development of webpage.

**Jurriaan Schuring**: Optimization of quote classification and adding country of url and speaker to the quote data.

**Henrik Myhre**: Mainly responsible for data wrangling and analyses performed on the Our World in Data.
