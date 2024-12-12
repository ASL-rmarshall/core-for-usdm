import requests
import json
import yaml
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from scripts import LOCAL_RULES_PATH

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 502, 503, 504, 408],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

class JiraClient:

    def __init__(self, api_key):
        self.base_api_url = "https://jira.cdisc.org/rest/api/2"
        self.api_key = api_key

    def get_api_json(self, href):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }
        raw_data = http.get(self.base_api_url+href, headers=headers)
        if raw_data.status_code == 200:
            return json.loads(raw_data.text)
        else:
            raise Exception(f"Request to {self.base_api_url+href} returned unsuccessful {raw_data.status_code} response")

api_key = os.environ.get("CONFLUENCE_API_KEY")

jira_client = JiraClient(api_key=api_key)

jira_query = "/search?jql=project%20%3D%20CORERULES%20AND%20component%20in%20(\"USDM%20v3.0\"%2C\"USDM%20v4.0\")%20and%20status%20in%20(\"Unit%20Testing\"%2C%20\"Awaiting%20QC\"%2C%20\"QC%20in%20Progress\"%2C%20\"Ready%20to%20Publish\")%20ORDER%20BY%20key"

draft_rules = jira_client.get_api_json(jira_query)

draft_rule_ids = {rule["fields"]["summary"]: rule["fields"]["status"]["name"].replace(" ","_").upper() for rule in draft_rules["issues"]}

rules_dir = os.fsencode(LOCAL_RULES_PATH)
    
for rule_file in os.listdir(rules_dir):
    filename = os.fsdecode(rule_file)
    rule_id = filename.split(".")[0]
    file = os.path.join(os.fsdecode(rules_dir),filename)
    if rule_id in draft_rule_ids:
        custom_id = f"{rule_id}-{draft_rule_ids[rule_id]}"
        with open(file,"r") as f:
            rule_def = yaml.safe_load(f)
        if "Core" not in rule_def:
            rule_def["Core"] = {"Id": custom_id,
                                 "Status": "Draft",
                                 "Version": "1"}
        else:
            rule_def["Core"]["Id"] = custom_id        

        rule_yaml = yaml.dump(rule_def)

        with open(
            os.path.join(os.fsdecode(rules_dir), rule_id + ".yaml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(rule_yaml)

        #f = open(file,"a")
        #f.write(f"custom_id: \"DRAFT-{rule_id}\"")
        #f.close
    os.remove(file)