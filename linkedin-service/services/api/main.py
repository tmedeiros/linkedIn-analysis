from fastapi import FastAPI
from job import Job
#import debugpy

#debugpy.listen(8888)
#debugpy.wait_for_client()

app = FastAPI()

@app.get("/")
async def jobs():
    job = Job()
    jobs = job.get_jobs('california')
    return jobs

@app.get("/descriptions/{state}")
async def jobs(state):
    job = Job()
    jobs = job.get_jobs(state)
    return jobs

@app.get("/job_count/{state}")
async def jobs(state):
    job = Job()
    jobs = job.get_job_by_count(state)
    return jobs

