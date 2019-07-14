#__Author__ : Indu Sharma
#__Purpose__ : Load the Logs summary & allure csv reports to the elasticsearch 

import errno
import argparse
import json
import ijson
import itertools
import subprocess
import re
import os
import sys

def parse_allure_tests_log(logdir):
	fields_to_extract = ['status', 'newFailed', 'description', 'time.start', 'time.duration', 'statusMessage', 'flaky', 'fullName','statusTrace']

	def iter_items(parser):
    		for prefix, event, value in parser:
    			if prefix:
        			yield prefix, value
			if prefix == 'newFailed':
				return
	complete_list = []
	for fh in os.listdir(logdir):
		if fh.endswith( ".json" ):	
			with open(os.path.join(logdir,fh)) as infile:
    				items = iter_items(ijson.parse(infile))
    				ori_dict = dict(itertools.islice(items, 30))
				out_dict = { key: ori_dict[key].split(':')[0] if isinstance(ori_dict[key], basestring) else ori_dict[key] for key in fields_to_extract if ori_dict['status']!='passed'}
				complete_list.append(out_dict)

	with open(aggregate_test_log_filename, 'w') as fp:	
		json.dump(complete_list, fp)

def load_to_es(index, mappings, data_file, file_format):
	cmd = 'elasticsearch_loader  --index-settings-file  '+ mappings +' --index  '+index+ ' --es-host '+es_host+   '    --progress '+  file_format +'  '+  data_file
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   	out, error = res.communicate()
	print (out, error)
	if error:
		print ("Already I`ndex Mapping Exists for ES index or there is error in index mapping :{}\nInserting datafile - {} without mapping".format(index, data_file))
                cmd = 'elasticsearch_loader   --index  '+index+ ' --es-host '+es_host+'   --progress  '+file_format +'  '+  data_file
		res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
		print (res)


if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description='Load testNG tests from Allure reports to ELK Stack',
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  	parser.add_argument('-d', '--allure_reports_path', help='Absoulute Directory of Allure Reports. Ex: /var/lib/jenkins/workspace/<Jenkins Job>/')
	parser.add_argument('-e', '--es_host', help='Elasticsearch Host details, IP:PORT')
	parser.add_argument('--index_log', help='Elasticsearch Index for storing allure tests log reports', default='ztap-log-1')
	parser.add_argument('--index_csv', help='Elasticsearch Index for storing allure tests csv reports', default='ztap-run-1')
  	args = parser.parse_args()
  	allure_report_dir = args.allure_reports_path
	es_host = args.es_host
  	index_log=args.index_log
	index_csv=args.index_csv
	if allure_report_dir is  None or es_host is None:
		parser.print_help()
		sys.exit()
	elif not os.path.exists(allure_report_dir):
		parser.error("Directory doesn't exist")
		parser.print_help()
		sys.exit()
	baseDir = allure_report_dir+'/allure-report/data/'
	try:
		os.mkdir('targets/')
	except OSError as e:
		pass
	aggregate_test_log_filename = 'targets/test_log.json'
	tests_suite_csv_filename = baseDir+'suites.csv'
	mapping_paths = 'samples/mappings/'
	parse_allure_tests_log(baseDir+'/test-cases/')
	#Disabling loading data to ES to avoid accidental damage of the dashboards
	#load_to_es(index_log, mapping_paths+'mappings_log.json', aggregate_test_log_filename, 'json')
	#load_to_es(index_csv, mapping_paths+'mappings.json', tests_suite_csv_filename,'csv')
