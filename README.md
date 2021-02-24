# leetcode-scraper
Scrapes information on algorithm questions from LeetCode and outputs data to a JSON file. Project built on Selenium. 

## Getting Started
1. Create a virtual environment `python3 -m venv env`
2. Activate virtual environment `source env/bin/activate`
3. Install requirements `python3 -m pip install requirements.txt`
5. Run Project. There are 2 modes to run this project in
   1. Scrape Leetcode and generate a JSON - `python3 run.py`
   2. Convert JSON from 1. into graph representation - `python3 run.py -m 2`
   3. For more info on args formatting - `python3 run.py -h`
6. To deactivate venv, enter `deactivate`

### TODO
1. Get Related Questions for mapping
2. ... (Feel free to add on features!)