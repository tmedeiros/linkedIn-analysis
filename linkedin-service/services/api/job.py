import os, json
import pandas as pd
from googlemaps import Client

class Job:
    def _init_(self):
        self._jobs = []

    def get_lat_long(self, location):
        gmaps = Client(key='AIzaSyADU4JlRIaly445PDXwCpBUs8Mq5tZsndo')
        geocode_result = gmaps.geocode(location)
        lat_long = {}
        lat_long["latitude"] = geocode_result[0]['geometry']['location']['lat']
        lat_long["longitude"] = geocode_result[0]['geometry']['location']['lng']
        return lat_long

    def parser(self, state):
        #path_to_json = 'services/api/data/' + state + '/'
        path_to_json = 'data/' + state + '/'
        job_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        #print(json_files)  # for me this prints ['foo.json']
        job_items = []
        for index, file in enumerate(job_files):
            with open(os.path.join(path_to_json, file)) as f:
                items = json.load(f)
                for job_item in items:
                    job = {}
                    job['title'] = job_item['title']
                    job['location'] = job_item['location']
                    lat_long = self.get_lat_long(job_item['location'])
                    job['lat'] = lat_long['latitude']
                    job['lon'] = lat_long['longitude']
                    job['company'] = job_item['company']
                    job['description'] = job_item['description']
                    job_items.append(job)
        return job_items

       

    def get_jobs(self, state):
        job_items = self.parser(state)
        #jobs = [{k: item[k] for k in ('jobid', 'title', 'location', 'company', 'description')} for item in job_items]
        return job_items

    #def get_state_description(self, state):
job = Job()
job.parser('california')



        