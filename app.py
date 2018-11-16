from flask import Flask, jsonify
from flask_cors import CORS
import requests
from xml.etree import ElementTree as etree

JOBS =[]

# JOBS = [
#     {
#         'Submit_Time': '10/11/2018 - 9h22',
#         'Status': 'done',
#         'Progress': '100%',
#         'Source': "COLTTEST.mxf",
#         'Output': "C://output_folder",
#         'Priority': 5,
#         'End_Time': '10/11/2018 - 9h28'
#     },
#     {
#         'Submit_Time': '10/11/2018 - 9h32',
#         'Status': 'running',
#         'Progress': '50%',
#         'Source': "Quantico.mxf",
#         'Output': "C://output_folder",
#         'Priority': 5,
#         'End_Time': '10/11/2018 - 9h38'
#     },
#       {
#         'Submit_Time': '10/11/2018 - 9h42',
#         'Status': 'done',
#         'Progress': '100%',
#         'Source': "COLTEST2.mxf",
#         'Output': "C://output_folder",
#         'Priority': 5,
#         'End_Time': '10/11/2018 - 9h48'
#     }
# ]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# Jobs route
@app.route('/jobs', methods=['GET'])
def all_jobs():
    JOBS = request_data_from_jobs(request_current_jobs())
    return jsonify({
        'status': 'success',
        'jobs': JOBS
    })
    


# -----------------------------------------------------    

response = requests.get('http://10.0.0.106:8647/CambriaFC/v1/SystemInfo')
tree = etree.fromstring(response.content)

print('Number of cluster in the farm :', tree[1].attrib['HasCluster'], ' - number of CPU :', tree[1].attrib['CPUs'])

# -----------------------------------------------------   


def request_current_jobs():
    current_jobs = []
    response2 = requests.get('http://10.0.0.106:8647/CambriaFC/v1/Jobs/?Status=All&SortBy=SubmitTime&Orderby=Desc')
    tree2 = etree.fromstring(response2.content)


    for i in tree2.iter('Job'):
        # print(i.tag, i.attrib['ID'])
        current_jobs.append(i.attrib['ID'])
    
    return current_jobs

    
def request_data_from_jobs(current_jobs):
    DJOBS = []
    for j in current_jobs:
        getJobsInfos = requests.get('http://10.0.0.106:8647/CambriaFC/v1/Jobs/{}/?Content=Description'.format(j))
        # print('jobs => ', getJobsInfos.content)
        tree_jobs = etree.fromstring(getJobsInfos.content)
        job_dict = {}

        for job in tree_jobs.iter('JobDescInfo'):
            
            job_dict['Submit_Time'] = job.attrib['SubmissionTime']
            job_dict['Status'] = job.attrib['Status']
            job_dict['Progress'] = job.attrib['Priority']
            job_dict['Source'] = job.attrib['SourceFilename']
            job_dict['Output'] = job.attrib['OutputFilename']
            job_dict['Priority'] = job.attrib['Priority']
            job_dict['End_Time'] = job.attrib['EndTime']
            # DJOBS.append(job_dict)

        for x in tree_jobs.iter('Task'):
            # print(x.tag, x.attrib['Progress'])
            job_dict['Progress'] = x.attrib['Progress']
            DJOBS.append(job_dict)
            # print('job_id', job.tag, job.attrib['JobID'])
    
    # print(DJOBS)  
    return DJOBS

# JOBS = request_data_from_jobs(request_current_jobs())
# print(JOBS)




if __name__ == '__main__':
    app.run(port=5001)