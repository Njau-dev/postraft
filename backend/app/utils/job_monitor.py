from app.workers.queue_manager import QueueManager


def get_queue_info(queue_name='poster-generation'):
    """
    Get information about a queue

    Returns:
        dict: Queue statistics
    """
    queue = QueueManager.get_queue(queue_name)

    return {
        'name': queue_name,
        'count': len(queue),  # Jobs waiting
        'failed_count': queue.failed_job_registry.count,
        'finished_count': queue.finished_job_registry.count,
        'started_count': queue.started_job_registry.count,
    }


def get_all_queues_info():
    """Get info for all queues"""
    return {
        'poster-generation': get_queue_info('poster-generation'),
        'default': get_queue_info('default'),
    }


def clear_failed_jobs(queue_name='poster-generation'):
    """Clear all failed jobs from queue"""
    queue = QueueManager.get_queue(queue_name)
    registry = queue.failed_job_registry

    job_ids = registry.get_job_ids()
    count = len(job_ids)

    for job_id in job_ids:
        registry.remove(job_id)

    return count
