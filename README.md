# 2019 Cyber attack detection methods course - Sherlock project

## Installation
1. install python 3.7
2. run _pip install -r requirements.txt_ in src folder

## Usage
### exfil_detector
1. run _python exfil_detector.py_ for command line usage
2. run _python exfil_detector.py extract-exfil-data <dataset_dir_name> <target_dir>_ to transform the sample dataset into an exfiltration dataset that only contains the relevant info, split per user
3. run _python exfil_detector.py shell <exfil_data_dir>_ to open an ipyton shell with both networking and malicious activitiy data loaded into pandas iterator and dataframe, respectively (see source code for details)  
