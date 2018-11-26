from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from xml.etree import ElementTree as etree
from presets import presets_list

JOBS =[]

print(presets_list['preset1']) # import du preset1 depuis le fichier des presets

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

# # Jobs route
# @app.route('/jobs', methods=['GET'])
# def all_jobs():
#     JOBS = request_data_from_jobs(request_current_jobs())
#     return jsonify({
#         'status': 'success',
#         'jobs': JOBS
#     })
    

# Jobs route GET and POST
@app.route('/jobs', methods=['GET', 'POST'])
def all_jobs():
    JOBS = request_data_from_jobs(request_current_jobs())
    response_object = {'status': 'success', 'jobs': JOBS, 'presets': presets_list}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data.get('source'))
        print(post_data.get('output'))
        print(post_data.get('preset'))
        # JOBS.append({
        #     'title': post_data.get('title')
        # })
        response_object['message'] = 'Job added!'
        post_encoding_job(post_data.get('source'),post_data.get('output'), post_data.get('preset'))
    else:
        response_object['jobs'] = JOBS
    return jsonify(response_object)
    
#   # Jobs route DELETE
@app.route('/jobs/<job_id>', methods=['DELETE','POST'])
def del_job(job_id):
    response_object = {'status' : 'success'}
    print("received", job_id)
    
    if request.method == 'DELETE':
        # remove_job(job_id)
        remove_job = requests.delete('http://10.0.0.106:8647/CambriaFC/v1/Jobs/{}'.format(job_id))
        response_object['message'] = "Job removed ! {}".format(remove_job)
    return jsonify(response_object)  


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
            job_dict['JobID'] = job.attrib['JobID']

        for x in tree_jobs.iter('Task'):
            job_dict['Progress'] = x.attrib['Progress']
            DJOBS.append(job_dict) # on append DJOBS une fois qu'on atoutes les données
            # print('job_id', job.tag)
      
    return DJOBS


def post_encoding_job(source_file,output_folder, preset):

        # launch a job
    url = "http://10.0.0.106:8647/CambriaFC/v1/Jobs"

    payload = r'<JobDescr Priority="5" NumberOfRetries="1" Description="Test Job" Submitter="10.12.0.155" OutputFolder="{}" OutputBasename="%sourcePath0%_%presetName%">\
            <Job Type="MediaGeneric">\
            # --> replace encoding preset \
            {}\
            # --> replace encoding preset \
                <Source Location="{}" Name="Src1" />\
            </Job>\
    </JobDescr>'.format(output_folder, presets_list[preset], source_file)

    print(payload)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "0e53a64e-eba2-bdf6-60df-f3b1dd61b054"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    # print("out", output_folder, "and source file", source_file)



if __name__ == '__main__':
    app.run(port=5001)