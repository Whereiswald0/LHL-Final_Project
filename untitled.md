# 'It's the economny, stupid!' - 

## Project/Goals
##### Applying Machine Learning to economic and political data to examine the relationship between these two fields and generate predictions about future election outcomes 

## Project Description
##### The title of this project is of course a reference to James Carville's line during the 1992 presidential election, an election which would see the sitting president, George H.W. Bush, lose to Bill Clinton, a loss usually attributed to the perception that Bush was responsible for an especially poorly performing economy. In at least this instance there's likely something to Carville pronouncement, given that just a year earlier Bush had held an approval rating of 90% following the first Gulf War. Still this is the kind of sentimental 'seems-right' reasoning I wanted to apply my Data Science skills to examining deliberately.

##### To do so, this project will focus on brining together data from US House of Representative elections with data from the Internal Revenue Service to address the question 'can we look at economic data and election outcomes and apply Machine Learning models to account for one or the other, and can we find a relationship in the historic data and then make better predictions about future elections based on current data.'

## Project Structure
#### |
#### Python .py files (in the future, these should be moved to their own .py folder)

## Methodology
##### Independence - I wanted to use primary sources as much as possible, rather than building a model out of other models and relying other analyists assumptions about significance. This meant at least initially avoiding the most common sources of economic data.

##### Modularity -  the datasets produced should be easily connected to new sources or swapped out in order to easily examine different relationships.

##### Preservation - a total avoidance of destructive processes while creating a library of formatted data to be used in the future - economic data was formatted and preserved seperately from election data, but the methods of joining them were programatic so that any sources could be combined and fed into the model, or old data which had at first been dismissed as unimportant could be re-incorporated.

##### Granularity - data should be grouped by geographic bounds of an appropirate size, so that each boundary is significant, but they don't contain too much data. These boundaries also shouldn't change often and should be unlikely to change in the future.. 

##### Future-Proofing - With the principles of modularity, preservation and granularity, the ability to easily add in future data follows easily.

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
