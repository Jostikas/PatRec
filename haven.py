from havenondemand.hodclient import *
import time
from os import path

API_KEY = "5e0bc8be-6a52-454c-b2ba-a1b09be5c476"
hodApp = HODApps.RECOGNIZE_SPEECH
hodClient = HODClient(API_KEY, version="v1")

def asyncRequestCompleted(response, error=None, **context):
    print("Started jobID {}, for file {}".format(response["jobID"], context['file']))
    if error is not None:
        for err in error.errors:
            print ("Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail))
    elif response is not None:
        jobID = response["jobID"]
        hodClient.get_job_status(jobID, requestCompleted, **context)


def handle_errors(response, **context):
    if response['status'] == 'queued':
        # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
        print(context['file'], " - Q")
        time.sleep(10)
        hodClient.get_job_status(response['jobID'], requestCompleted, **context)
        return
    elif response['status'] == 'in progress':
        # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
        print(context['file'], " - P")
        time.sleep(20)
        hodClient.get_job_status(response['jobID'], requestCompleted, **context)
        return
    else:
        print(response)


def requestCompleted(response, **context):
    if response['status'] != 'finished':
        handle_errors(response, **context)
    else:
        doc = response['actions'][0]['result']['document'][0]
        text = doc['content']
        outfile = context['outfile']
        with open(outfile, "w") as f:
            f.write(text)
        print(context['file'], " - D")


def dispatchFile(fname, **context):
    params = {'file': fname, 'language_model': 'en-US'}
    time.sleep(5)
    hodClient.post_request(params, hodApp, True, asyncRequestCompleted, **context)
    return True

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Run HavenOnDemand speech detection on input sound file\n"
              "\tUsage: python haven.py <infile> [<outfile>]\n"
              "\t<infile> - Input sound file. Accepts some different formats, depending on ffmpeg install.\n"
              "\t<outfile> - Optional. When specified, stores results in this file. Defaults to 'basename(<infile>)-haven.txt'.")
    else:
        fname = sys.argv[1]
        if len(sys.argv) == 3:
            outfile = sys.argv[2]
        else:
            outfile = os.path.splitext(fname)[0] + "-ibm.txt"
        context = {'file': fname, 'outfile': outfile}
        dispatchFile(fname, **context)
