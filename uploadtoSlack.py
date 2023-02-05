from io import StringIO
import requests
import json
import glob
import time
import pandas as pd
# StringIO this library will allow us to 
# get a csv content, without actually creating a file.


# read the csv files
headers = {
    'Authorization': 'Bearer xoxb-4383281664871-4410711262321-0FYV46aLphYmzR7OkMd56795',
    'Content-Type': 'application/x-www-form-urlencoded'
}
url = "https://slack.com/api/files.upload"



def csv2fileobj(df):
     
 #   df = pd.read_csv(csvfile) 
    sio = StringIO()
    df.to_csv(sio)
  #  csv_content = sio.getvalue()
    return sio

def uploadFiles(fileobjs,symbols):
    urls = []
    for i,obj in enumerate(fileobjs):
        request_data = {
    'channel': 'C04BPM8G00K', 
    'content': obj.getvalue(), 
    'filename': symbols[i], 
    'filetype': 'csv', 
}
        res = requests.post(
    url, data=request_data, headers=headers
)   

        time.sleep(2) 
        urls.append(res.json()["file"]["url_private_download"])
    return urls

