# moneyandvotes
I wrote scripts in python to collect data from FEC API and analyze them statistically. 

In "data", there are several json files and csv files:

"2016" - "2004" contains data for the year's individual races. 

X = S >>> Senate, H >>> House, or B >>> Both house and senate.

X-YEAR-datasets-financial.json >>> fianancial data without votes information, data straight from OpenFEC API.
X-YEAR-datasets-2.json >>> financial dat and votes information. It also has a bunch of statistics are added. 
B-YEAR-datasets-2.json contains stats of each state and nationwide (NA).

In B-YEAR-datasets-2.json: 
"correlation_coef" >>> correlation coefficient between the funding (the campaign's spending / total spending by all candidates) and electoral performance (the candidate's vote / entire votes cast in the race). This is the main statistical figure in this project. Keep in mind that correlation does not necessarily mean causation. Candidates who raise a lot of money are naturally likely to recieve a lot of votes as well. 

"average_spending" >>> total spending by all candidates / number of candidates. 

"topspender_share" >>> the funding of the candidate who raised the most money / total funding by all candidates. Indicates campaign finance unequality

"Stats" has B-YEAR-datasets-2.json's data in .csv format (excel compatible).

"choroplethB" contains choropleth images of "correlation_coef," "average_spending," and "topspender_share." 

Bottom line conclusion >>> Very very high correlation between money and votes.

==========================================================

In bin, there are scripts that I used to collect and analyze these data:

hosuelister.py >>> collect and analyze data for HOUSE races.
candidate-lister.py >>> collect and analyze data for SENATE races.
bothlister >>> reads datasets-2 files and calculate statistics for Senate and House combined.

json2sql >>> reads json files and throw them into sql relational database. I used mysql.

housdistrict.py >>> inside each state, creates lists of districts according to how many districts there are in that state 


Data used in this project are collected from FEC under the condition of Non-Commercial use.

Visit votesandmoney.com

Main page: you can click the states in the map to see individual House and Senate races. This is Wisconsin Senate race in 2016.
![clicakble-map](https://user-images.githubusercontent.com/28686892/64263100-baa18380-cef4-11e9-9e6e-7940fdbb0abc.png)
Statistics pages: you can see the line graph of three statistics for each state and nationwide. 

![Screenshot_2019-10-05 money votes - Stats](https://user-images.githubusercontent.com/28686892/66262820-9cf26300-e7ad-11e9-8d26-be1f341a0d0f.png)
Choropleth: shows nation wide trend overtime (you can scroll the bar on the bottom to change the year from 2004 to 2016)

![Screenshot_2019-10-05 money votes - Stats(1)](https://user-images.githubusercontent.com/28686892/66262856-3c175a80-e7ae-11e9-8c3a-4a858fcf8076.png)



(Update)
The website is temporarily taken down because the GCP sql database was costing too much everyday.




