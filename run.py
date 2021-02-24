import sys
import json
import pickle
import time
import requests

from argparse import ArgumentParser

from utils.logger import create_logger
from driver_instance import DriverInstance
from consts import (
  ALGORITHMS_ENDPOINT_URL,
  ALGORITHMS_BASE_URL,
)

def main():
  LOGGER = create_logger('LOGGER')
  rcode = 0

  # TODO: Implement args parser
    # args = parse_args()
    # app_id = args.app_id if args.app_id else None
  is_headless = True
  debug = False

  problem_list = requests.get(ALGORITHMS_ENDPOINT_URL).content # Fetch JSON from API
  problem_list = json.loads(problem_list)
  problem_list = problem_list["stat_status_pairs"]

  driver_instance = DriverInstance(LOGGER, is_headless, debug)
  problems_dict = {}

  for problem in problem_list[:10]: # TODO: Remove limit of 10 qns when doing FREAL
    if not problem["paid_only"]: # Only free ones
      p = {}
      p["q_id"] = problem["stat"]["frontend_question_id"]
      p["name"] = problem["stat"]["question__title"]
      p["difficulty"] = problem["difficulty"]["level"]
      p["is_paid"] = problem["paid_only"]
      p["url"] = ALGORITHMS_BASE_URL + problem["stat"]["question__title_slug"]
      p["submissions"] = problem["stat"]["total_submitted"]
      p["accepted_subsmissions"] = problem["stat"]["total_acs"]
      # driver_instance.load_site(p["url"])
      # p["categories"] = driver_instance.get_categories()
      problems_dict[p["q_id"]] = p

  try: 
    for key in problems_dict.keys():
      driver_instance.load_site(problems_dict[key]["url"])
      problems_dict[key]["categories"] = driver_instance.get_categories()
      problems_dict[key]["upvotes"], problems_dict[key]["downvotes"] = driver_instance.get_stats()
    driver_instance.close_window()
    with open('leetcode_qns.json', 'w') as outfile:
      json.dump(problems_dict, outfile)

  except SystemExit:
    if driver_instance and driver_instance.logger:
      LOGGER.error('SystemExit raised.')
    rcode = 1
  except DriverInstanceException as err:
    if driver_instance and driver_instance.logger:
      LOGGER.error('Custom DriverInstanceException raised.')
    capture_exception(err)
    rcode = 2
  finally:
    if driver_instance:
        if driver_instance.driver:
            driver_instance.driver.quit()
            LOGGER.info('Quit driver')
  return rcode

if __name__ == '__main__':
  sys.exit(main())
