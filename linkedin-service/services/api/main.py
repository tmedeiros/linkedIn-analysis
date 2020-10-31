from fastapi import FastAPI
from job import Job

app = FastAPI()

@app.get("/")
async def jobs():
    job = Job()
    jobs = job.get_jobs()
    return jobs