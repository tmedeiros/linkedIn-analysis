import os, json
import pandas as pd
from googlemaps import Client
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')

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
        path_to_json = 'services/api/data/' + state + '/'
        #path_to_json = 'data/' + state + '/'
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
        with open(state + '.json', 'w') as state_data:
            json.dump(job_items, state_data)
        return job_items

    def fetch_data(self, state):
        with open(state + '.json') as state_data:
            job_items = json.load(state_data)
            return job_items
       

    def get_jobs(self, state):
        job_items = self.fetch_data(state)
        #jobs = [{k: item[k] for k in ('jobid', 'title', 'location', 'company', 'description')} for item in job_items]
        return job_items
    
    def get_job_by_count2(self, state):
        most_popular_jobs = ['java', 'web', 'python', 'javascript', 'C#', 'C', 'swift', 'php', 'scala', 'ruby', 'dart', 'R', 'typescript', 'julia', 'Go']
        job_items = self.fetch_data(state)
        jobs = []
        for job_item in job_items:
            job = {}
            if 'Machine Learning'.lower() in job_item['title'].lower() \
                or 'AI'.lower() in job_item['title'].lower() \
                or 'ML'.lower() in job_item['title'].lower() \
                or 'Data Anal'.lower() in job_item['title'].lower(): 
                    job_item['title'] = 'Machine Learning'
            elif 'Data Engineer'.lower() in job_item['title'].lower() \
                or 'AI'.lower() in job_item['title'].lower() \
                or 'ML'.lower() in job_item['title'].lower():
                    job_item['title'] = 'Data Engineer'
            job['title'] =  job_item['title']
            job['lat'] =  job_item['lat']
            job['lon'] =  job_item['lon']
            words = nltk.word_tokenize(job_item['description'])
            text = nltk.Text(words)
            words = [word for word in words if word.lower() in most_popular_jobs]
            word_count = nltk.FreqDist(words)
            #['count'] = word_count;
            job_count = []
            for word, frequency in word_count.most_common():
                job_name_count = {}
                job_name_count['name'] = word
                job_name_count['count'] = frequency
                if frequency > 0:
                    job_count.append(job_name_count)
            job['name_count'] = job_count
            if len(job['name_count']) > 0:
                jobs.append(job)
        len(word_count)
        #filter_words = dict([(m, n) for m, n in data_analysis.items() if len(m) > 3])
        #for key in sorted(filter_words):
            #print("%s: %s" % (key, filter_words[key]))

    def get_job_freqeuncy(self, description):
        most_popular_jobs = ['java', 'spark', 'python', 'javascript', \
                            'C#', 'C', 'swift', 'php', 'scala', 'ruby', \
                            'dart', 'R', 'typescript', 'julia', 'Go']
        words = nltk.word_tokenize(description)
        text = nltk.Text(words)
        words = [word for word in words if word.lower() in most_popular_jobs]
        word_count = nltk.FreqDist(words)
        job_count = []
        for word, frequency in word_count.most_common():
            job_name_count = {}
            job_name_count['name'] = word.lower()
            job_name_count['count'] = frequency
            if frequency > 0:
                job_count.append(job_name_count)
        return job_count

    def set_title(self, title):
        if 'machine learning' in title.lower() \
                or 'ai' in title.lower() \
                or 'data scientist'.lower() in title.lower() \
                or 'data science'.lower() in title.lower() \
                or 'data anal'.lower() in title.lower() \
                or 'data & applied scientist'.lower() in title.lower() \
                or 'ml' in title.lower():
                    title = 'Machine Learning'
        elif 'data engineer' in title.lower():
                title = 'Data Engineer'
        elif 'mobile' in title.lower() \
            or 'ios' in title.lower() \
            or 'android' in title.lower():
                title = 'Mobile'
        elif 'web developer' in title.lower() \
            or 'frontend' in title.lower() \
            or 'front end' in title.lower() \
            or 'software developer' in title.lower() \
            or 'software engineer' in title.lower() \
            or 'application developer' in title.lower() \
            or 'angular developer' in title.lower() \
            or 'developer i' in title.lower() \
            or 'web' in title.lower() \
            or 'applications developer' in title.lower():
                title = 'Web'
        else:
            title = title
        return title
    
    def get_job_name_count(self, job_data):
        titles = job_data.groupby('job')
        titles = titles.groups.keys()
        jobs = []
        data = {}
        for job_type in titles:
            skills = job_data[job_data['job'] == job_type]['skill']
            job_skill = {}
            for skill in skills:
                for index, job in enumerate(skill):
                    title = job['name']
                    job_count = job['count']
                    if not job_skill:
                        job_skill[title] = job['count']
                    else:
                        if title in job_skill:
                            job_skill[title] += job_count
                        else:
                            job_skill[title] = job_count
            jobs.append({job_type : job_skill})
        df = pd.DataFrame(columns=['job', 'name', 'count'])
        counter = 0
        for job_items in jobs:
            for item in job_items.items():
                keys = item[1].keys()
                values = item[1].values()
            for index, key  in enumerate(keys):
                counter += 1
                job = item[0]
                name = key
                count = item[1][name]
                df.loc[counter] = [job, name, count]
        print(df)
        return df
        #return df.values.tolist()

            

            #new_job[job['job']] = job['skill']
            #jobs.append(new_job)


    def get_job_by_count(self, state):
        job_items = self.fetch_data(state)
        job_data = pd.DataFrame(columns=['job', 'city', 'state', 'lat', 'long', 'company', 'skill', 'count'])
        for index, job  in enumerate(job_items):
            title = self.set_title(job['title'])
            location = job['location']
            if 'Dallas-Fort'.lower() in location.lower():
                city = 'Dallas'
                state = 'TX'
            elif 'New York City'.lower() in location.lower():
                city = 'NY'
                state = 'NY'
            elif 'Utica'.lower() in location.lower():
                city = 'Utica'
                state = 'NY'
            else:
                location = job['location'].split(',')
                city = location[0]
                state = location[1]
            lat = job['lat']
            lon = job['lon']
            company = job['company']
            #description = job['description']
            skill = self.get_job_freqeuncy(job['description'])
            count = 0
            job_data.loc[index] = [title, city, state, lat, lon, company, skill, count]
        #print(job_data.iloc[100:120,6].head(120))
        print(job_data)
        df = self.get_job_name_count(job_data)
        return df
        




    #def get_state_description(self, state):
#job = Job()
#job.get_job_by_count('texas')
#job.get_job_by_count('texas')
#job.get_job_by_count('services/api/california')



        