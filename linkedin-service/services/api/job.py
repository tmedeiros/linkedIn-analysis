import json

class Job:
    def _init_(self):
        self._jobs = []

    def parser(self):
        with open('linkedin.json') as f:
            data = json.load(f)
        return data

    def get_jobs(self):
        job_items = self.parser()
        jobs = [{k: item[k] for k in ('jobid', 'title', 'company', 'description')} for item in job_items]

        return jobs

        