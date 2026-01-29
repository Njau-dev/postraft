from redis import Redis
from rq import Queue
from flask import current_app


class QueueManager:
    """Manages job queues"""

    _redis_conn = None
    _queues = {}

    @classmethod
    def get_redis_connection(cls):
        """Get Redis connection (singleton)"""
        if cls._redis_conn is None:
            redis_url = current_app.config.get(
                'REDIS_URL', 'redis://localhost:6379/0')
            cls._redis_conn = Redis.from_url(redis_url)
        return cls._redis_conn

    @classmethod
    def get_queue(cls, queue_name='default'):
        """
        Get or create a queue

        Args:
            queue_name: Name of the queue

        Returns:
            Queue: RQ Queue instance
        """
        if queue_name not in cls._queues:
            redis_conn = cls.get_redis_connection()
            cls._queues[queue_name] = Queue(queue_name, connection=redis_conn)

        return cls._queues[queue_name]

    @classmethod
    def enqueue_job(cls, func, *args, queue_name='default', timeout=None, **job_kwargs):
        """
        Enqueue a job

        Args:
            func: Function to execute
            *args: Function arguments
            queue_name: Queue name
            timeout: Job timeout in seconds
            **job_kwargs: Additional job parameters (result_ttl, etc.)

        Returns:
            Job: RQ Job instance
        """
        queue = cls.get_queue(queue_name)

        defaults = {
            'timeout': 600,      # 10 minutes
            'result_ttl': 3600,  # 1 hour
            'failure_ttl': 86400,  # 24 hours
        }

        # Merge defaults with provided job kwargs (provided values take precedence)
        final_job_kwargs = {**defaults, **(job_kwargs or {})}

        # explicit `timeout` argument takes precedence over job_kwargs
        if timeout is not None:
            final_job_kwargs['timeout'] = timeout

        # Use enqueue_call to clearly separate function args from job options.
        try:
            job = queue.enqueue_call(
                func=func, args=args, kwargs=None, **final_job_kwargs)
        except TypeError:
            # Fallback for older RQ versions that may not expose enqueue_call
            job = queue.enqueue(func, *args, **final_job_kwargs)

        return job

    @classmethod
    def get_job(cls, job_id, queue_name='default'):
        """
        Get job by ID

        Args:
            job_id: Job ID
            queue_name: Queue name

        Returns:
            Job: RQ Job instance or None
        """
        from rq.job import Job
        redis_conn = cls.get_redis_connection()

        try:
            return Job.fetch(job_id, connection=redis_conn)
        except:
            return None

    @classmethod
    def get_job_status(cls, job_id):
        """
        Get job status

        Args:
            job_id: Job ID

        Returns:
            dict: Job status info
        """
        job = cls.get_job(job_id)

        if not job:
            return {
                'status': 'not_found',
                'message': 'Job not found'
            }

        status_map = {
            'queued': 'pending',
            'started': 'processing',
            'finished': 'completed',
            'failed': 'failed',
        }

        result = {
            'status': status_map.get(job.get_status(), 'unknown'),
            'created_at': job.created_at.isoformat() if job.created_at else None,
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'ended_at': job.ended_at.isoformat() if job.ended_at else None,
        }

        # Add result if completed
        if job.is_finished:
            result['result'] = job.result

        # Add error if failed
        if job.is_failed:
            result['error'] = str(
                job.exc_info) if job.exc_info else 'Unknown error'

        return result
