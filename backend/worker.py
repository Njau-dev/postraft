from rq import Worker, Queue, Connection
from app.extensions import redis_client

if __name__ == '__main__':
    with Connection(redis_client):
        worker = Worker(['default', 'poster-generation'])
        worker.work()
