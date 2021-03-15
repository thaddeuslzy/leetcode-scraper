import sys
import json
import time
import requests

from argparse import ArgumentParser

from utils.logger import create_logger
from driver_instance import DriverInstance
from consts import (
  ALGORITHMS_ENDPOINT_URL,
  ALGORITHMS_BASE_URL,
  JSON_FILENAME_QNS,
  JSON_FILENAME_GRAPH,
)

def parse_args():
  """Parse command-line arguments.
  Returns:
    Namespace: contains the parsed arguments.
  """
  parser = ArgumentParser(description='Automate Leetcode Scraping.')
  parser.add_argument(
    '-m',
    '--mode',
    type=int,
    default=1,
    choices=[1,2],
    help='Mode to run the script in: 1-Get Leetcode problems. 2-Get Graph JSON of problems(requires 1. to be run at least once)',
  )
  parser.add_argument(
    '-hd',
    '--headless',
    action='store_true',
    help='Disable headless mode of webdriver.',
  )
  parser.add_argument(
    '-d',
    '--debug',
    action='store_true',
    help='Debug mode. Enables verbose logging.',
  )
  return parser.parse_args()

def main():
  """Fill the application described by the command line arguments.
  Example commands:
  'python3 run.py -hd -d' to run in debug mode with headless mode disabled
  'python3 run.py -m 2' to run in graph generation mode
  """
  LOGGER = create_logger('LOGGER')

  args = parse_args()
  is_debug = args.debug
  is_headless = not (args.headless)
  mode = args.mode

  if mode==1:
    LOGGER.info('Running Leetcode scraping task...')
    genProblemsJSON(LOGGER, is_headless, is_debug)
  elif mode==2:
    LOGGER.info('Running Graph generating task...')
    genGraphJSON()
  LOGGER.info('Done')

  return 0

# not the best abstraction, will revisit again
def genProblemsJSON(LOGGER, is_headless, is_debug):
  problem_list = requests.get(ALGORITHMS_ENDPOINT_URL).content # Fetch JSON from API
  problem_list = json.loads(problem_list)
  problem_list = problem_list["stat_status_pairs"]

  driver_instance = DriverInstance(LOGGER, is_headless, is_debug)
  problems = {}

  for problem in problem_list:
    if not problem["paid_only"]: # Only get free questions
      p = {}
      p["id"] = problem["stat"]["frontend_question_id"]
      p["name"] = problem["stat"]["question__title"]
      p["difficulty"] = problem["difficulty"]["level"]
      p["is_paid"] = problem["paid_only"]
      p["url"] = ALGORITHMS_BASE_URL + problem["stat"]["question__title_slug"]
      p["submissions"] = problem["stat"]["total_submitted"]
      p["accepted_subsmissions"] = problem["stat"]["total_acs"]
      p["group"] = 2
      problems[p["id"]] = p

  try: 
    for key in problems.keys():
      driver_instance.load_site(problems[key]["url"])
      problems[key]["topics"] = driver_instance.get_topics()
      problems[key]["upvotes"], problems[key]["downvotes"] = driver_instance.get_stats()
    driver_instance.close_window()
    with open(JSON_FILENAME_QNS, 'w') as outfile:
      json.dump(problems, outfile)

  finally:
    if driver_instance:
        if driver_instance.driver:
            driver_instance.driver.quit()
            LOGGER.info('Quit driver')

def genGraphJSON():
  with open(JSON_FILENAME_QNS) as json_file:
    problems = json.load(json_file)
    topics = set()
    nodes = []
    links = []

    # Problem Nodes & Links
    for node in problems.values():
      topics = topics.union(set(node["topics"])) # add topics to Topic set
      nodes.append(node)
      if len(node["topics"]) == 0:
        links.append({"source": "Uncategorized", "target": node["id"], "value": 1})
      else:
        for topic in node["topics"]: # generate links
          links.append({"source": topic, "target": node["id"], "value": 1})

    # Topic Nodes & Links
    nodes.append({"id": "Topics", "name": "Topics", "group": 0})
    topics.add("Uncategorized")
    for topic in topics:
      nodes.append({"id": topic, "name": topic, "group": 1})
      links.append({"source": "Topics", "target": topic})

    res = { "nodes":nodes, "links":links }

    with open(JSON_FILENAME_GRAPH, 'w') as outfile:
      json.dump(res, outfile)
    
if __name__ == '__main__':
  sys.exit(main())
