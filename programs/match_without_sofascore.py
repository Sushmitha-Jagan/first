from sys import argv
from collections import defaultdict
import re

def cronned_sources_per_match(file_path):
	cronned_sources = {}
	with open(file_path, 'r') as f:
		line = f.readline()
		while line:
                    try:
			data = re.split(r'\s{2,}', line.strip())
                        if not data:
                            continue
			if not cronned_sources.get(data[0]):
				cronned_sources[data[0]] = defaultdict()
			cronned_sources[data[0]]['title'] = data[-1]
			if not cronned_sources[data[0]].get('sources'):
				cronned_sources[data[0]]['sources'] = []
			cronned_sources[data[0]]['sources'].append(data[3])
                        cronned_sources[data[0]]['start_time'] = data[1]
			line = f.readline()
                        #print data
                        #break
                    except Exception as e:
                        print "Error occured while processing %s" %data
	return cronned_sources

def main():
	file_path = argv[1]
	if not file_path:
		print "No file provided"
		return

	sources_per_match = cronned_sources_per_match(file_path)
	print "These matches do not have sofascore as a source..."
	for match in sources_per_match:
		if 'sofascore' not in sources_per_match[match]['sources']:
			print "%s\t%s\t%s\t%s" %(match, sources_per_match[match]['title'], sources_per_match[match]['start_time'], '\\'.join(sources_per_match[match]['sources']))

if __name__ == '__main__':
	main()
