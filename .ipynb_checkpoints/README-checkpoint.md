# 'It's the economny, stupid!' - 

## 1. Project/Goals
##### Applying Machine Learning to economic and political data to examine the relationship between these two fields and generate predictions about future election outcomes 

## 2. Project Description
##### The title of this project is of course a reference to James Carville's line during the 1992 presidential election, an election which would see the sitting president, George H.W. Bush, lose to Bill Clinton, a loss usually attributed to the perception that Bush was responsible for an especially poorly performing economy. In at least this instance there's likely something to Carville pronouncement, given that just a year earlier Bush had held an approval rating of 90% following the first Gulf War. Still this is the kind of sentimental 'seems-right' reasoning I wanted to apply my Data Science skills to examining deliberately.

##### To do so, this project will focus on brining together data from US House of Representative elections with data from the Internal Revenue Service to address the question 'can we look at economic data and election outcomes and apply Machine Learning models to account for one or the other, and can we find a relationship in the historic data and then make better predictions about future elections based on current data.'

##### Specifically, the initial portion of this project will examine whether a good economy helps or hurts incumbent candidates be re-elected, and how much a bad economy helps or hurts their challengers. 

## 3. Project Structure


```
├── data
    ├── FEC
    |    ├──**.*.csv, formatted fec files
    |    ├── raw (contains raw Federal Elections Commission data)
    ├── formatted_house_totals
    |    ├──**.*.csv, formatted US House election data
    ├── house_fec_irs_joined
    |    ├──**.*.csv, formatted and joined FEC, House Election, and IRS data - ready for pre-processing and ML deployment
    ├── irs_data
        |   ├──**.*.csvc, formatted data from IRS.gov
        ├── docguides 
        |    ├──**/*.docx, tables containing column codes and descriptions for IRS data
        ├── raw
        |    ├──**.*.csv, unprocessed data from IRS.gov
        |(formatted IRS data)
    ├── logarithm_of_joined_data
    |    ├──**.*.csv, data from house_fec_irs_joined after np.log was applied
    ├── raw_elec_totals
    |    ├──**.*.xls/.xlsx, data from individual states recording election statistics
├── Notebooks
|    ├── (jupyter notebook files exploring the data should be housed here)
├── Presentation
|    ├──**.*.txt/pdf, script and slideshow files used when presenting this project publically
├── src
|    ├──**.*py, commonly used functions
|
|    ├──**.*.py files are housed in the base directory)(in the future, these should be moved to their own .py folder)
```
 

## 4. Methodology
#### To begin with, this project is guided by five principles with regards to handling data and data sources.

##### ++ Independence -  use primary sources as much as possible, rather than building a model out of other models and relying other analyists assumptions about significance. This meant at least initially avoiding the most common sources of economic data.

##### ++ Modularity -  datasets produced should be easily connected to new sources or swapped out in order to easily examine different relationships.

##### ++ Preservation -  a total avoidance of destructive processes while creating a library of formatted data to be used in the future - economic data is formatted and preserved seperately from election data, but the methods of joining them should be programatic so that any sources could be combined and fed into the model, or old data which had at first been dismissed as unimportant could be re-incorporated.

##### ++ Granularity -  data should be grouped by geographic bounds of an appropirate size, so that each boundary is significant, but they don't contain too much data. These boundaries also shouldn't change often and should be unlikely to change in the future. 

##### ++ Future-Proofing -  With the principles of modularity, preservation and granularity, the ability to easily add in future data follows easily.


#### ~~ Following from this:

##### The decision to use US house data fullfils these points as follows:

##### ++ Elections are frequent and regular - each seat is elected every two years
##### ++ There are 435 seats, each with multiple candidates - many datapoints are generated during these elections regarding party preference, and the value of incumbancy
##### ++ While congressional districts are large (each has around 750,000 constituents as of 2023), election data is reported by states at the County level as well, allowing us to avoid dealing with redistricting and changing boundaries over time


##### Using the IRS data on individual income tax filing fulfills the principle of using primary sources, and is also available broken down at the county level 

## 5. Running order
##### (This section will be re-written when the filestructure is cleaned up)
##### County data will be processed first, corresponding to the python files number '1, 2, 3' for OH, IL and WI

## Results - [Tableau Dashboard](https://public.tableau.com/app/profile/adrian1635/viz/Chess_17013176907810/Dashboard1)
##### Due to the complexity of chess as a game, neither Logical Regression nor Generalized Linear Models were able to be used to find correlations between move order and win conditions at this level. 
##### Instead, Tableau's visualizations and filtering were used to describe the datasets and produce recommendations.
##### A lack of correlation in this data is a result in and of itself (we were never going to 'solve' chess)

## Challenges 
##### The amount of data available on chess games is vast (60-70GB of data are produced by lichess just from game results, without analysis)
##### Knowing how to limit this while obtaining enough data the something can be meaningfully said is key.

## Future Goals
##### Add additional datasets, produce slices of datasets by rating to be processed using statistical models (an attempt to keep the dataset smaller but focused, so that models can be built more easily and accurately)
##### Structure API calls that will pull live data for those particular slices
##### Apply machine learning models to produce better results.
