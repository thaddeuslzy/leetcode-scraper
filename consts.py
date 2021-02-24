# Leetcode API URL to get json of algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

# e.g https://leetcode.com/problems/two-sum
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

JSON_FILENAME_QNS = "leetcode_qns.json"

JSON_FILENAME_GRAPH = "leetcode_qns_graph.json"

''' Requirements
--Pre-Scrape--
ID - Number
Name - String 
Diff - Sting
Url - String
isPaid - Bool
Submissions - Number
Acc Submissions - Number

--Post-Scrape--
Topics - []
Upvote, Downvote
'''

''' Structure of a question dict
{
  "stat": {
    "question_id": 1865,
    "question__article__live": null,
    "question__article__slug": null,
    "question__article__has_video_solution": null,
    "question__title": "Checking Existence of Edge Length Limited Paths II",
    "question__title_slug": "checking-existence-of-edge-length-limited-paths-ii",
    "question__hide": false,
    "total_acs": 109,
    "total_submitted": 167,
    "frontend_question_id": 1724,
    "is_new_question": true
  },
  "status": null,
  "difficulty": {
      "level": 3
  },
  "paid_only": true,
  "is_favor": false,
  "frequency": 0,
  "progress": 0
},
'''