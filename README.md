# CORE Utility Programs for USDM

## Set-up

1. Clone or copy this repository
2. Create a virtual environment:
    `python -m venv venv`
3. Activate virtual environment
4. Install required packages:
    `pip install -r requirements.txt`

## usdm2xl.py

This program uses the CORE USDM data service to convert a specified USDM JSON file into an Excel file (in the format expected for CORE validation):

`python usdm2xl.py -dp path/to/usdm/json/file`

The output file will have the same name as the JSON file, but with a timestamp suffix.

## run_usdm_validation.py

This is an example implementation of the `validate_usdm` method to demonstrate how running CORE validation of a USDM JSON file can be integrated into a Python program.  The JSON file name input is hard-coded in this example, but could be replaced with variable containing the file name.

`python run_usdm_validation.py`

## publish_local_rules.py

Currently (as of 2024-12-12) no USDM rules have been published, so there are no USDM rules available via the CDISC Library.  USDM rules therefore have to be run as local rules - i.e., rules stored locally in YAML format.

To download YAML rule specifications from the CORE Rules Editor:
1. Log into the CORE rules editor.
2. Filter rules to show only USDM rules with a rule id starting with DDF:
    1. Clear the filter on the Creator column
    2. Type `DDF` in the Rule Ids column search box
    3. Type `USDM` in the Standards column search box
3. Click on the Export... button (downwards pointing arrow) and select "Export rules YAML (as filtered)"
4. Wait for the rules to be exported - they're exported as a zip file called Rules.zip (or with a suffix if you've downloaded them before) in your browser's usual download folder.
5. Unzip the rule definitions into the resources/local_rules folder
 
Once the rule definitions have been downloaded, run this program (publish_local_rules.py) to:
- Remove any rule specifications where the status for the corresponding CORERULES JIRA ticket is not "Unit Testing", "Awaiting QC", "QC in Progress", or "Ready to Publish".
- Add a dummy CORE-id, which is required to run validation for local rules.

`python publish_local_rules.py`

### Prerequisites
  
Note that the following are required to run this program:
- A [CDISC JIRA](https://jira.cdisc.org/) account with at least read access to the [CORERULES project](https://jira.cdisc.org/projects/CORERULES).
- A JIRA personal access token (PAT) (see "Creating PATs in the application" instructions [here](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)) that has been saved in an environment variable called `CONFLUENCE_API_KEY`.

# Source

Most of the content of this repository is a static copy from the [cdisc-rules-engine](https://github.com/cdisc-org/cdisc-rules-engine) repository (see version.py for copied version) as a temporary fix until an updated version of the cdisc-rules-engine is available via PyPI. 