# Script to Load Allure Reports(suites.csv & tests cases json logs) to ELK stack 

This file describes how to run the script from any environments, and load/view the Kibana dashboards for ZTAP automated tests reports analysis. 

### The code here does two things:

1. Loads the allure tests reports(suites.csv) to ELK stack, by default to the `ztap-run-1` index.

2. Loads the allure tests logs(json) to ELK stack, by default to the `ztap-log-1` index.


## Running on MacOS or CentOS or Windows/WSL

### Prerequisites

1. Elasticsearch 7.x and Kibana 7.x is installed & setup is up and running.
2. Ensure you have the right git credentials
3. Optional: Most developers need a python virtualenv. you may set this up like so:
    1. `pip install --user virtualenv`
    2. `virtualenv myenv`
    3. `source myenv/bin/activate`
4. Optional: Download/copy allure-report directory from the server where ZTAP tests were run to /Users/isharma (for example)
Note: allure-report directory on Jenkins server would be located in the directory: `/var/lib/jenkins/workspace/<Jenkins Job>/` 


### Execute

 
1. `git clone git@bitbucket.org:zaloni/ztap-ansible.git`
2.  Load Kibana dashbord and visualization and elasticsearch indices:
	A. Login to Kibana UI, go to Management -> Saved Objects 
	B. Import dashboards via json - export.json, present in cloned repository path: ztap-ansible/allureToElk/samples/dashboards 
3. `cd ztap-ansible/allureToElk`
4. Install elastic_loader and other reqs: `pip install -r requirements.txt`
5. Check out the appropriate branch, eg: `git checkout release/5.1.0`
6. `python load_allure_reports_to_elk.py -d /Users/isharma --es_host 192.168.2.65:9200` You can change the value `/Users/isharma` to the directory your allure-report folder is available and you can change the value `192.168.2.65:9200` to your elasticsearch IP:PORT 
7. Run `python load_allure_reports_to_elk.py -h` for more options.
8. To see the dashboard: On Kibana UI, search for dashboard : `[ZTAP/ZDP] Automation Overview` 

## Running on Jenkins

TBD: This script will be mainly used to run from the jenkins server. Once tested via Jenkins, this section will be updated. 


## Authors

- Indu Sharma
