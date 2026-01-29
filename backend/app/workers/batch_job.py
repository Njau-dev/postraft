from app.workers.queue_manager import QueueManager
from app.workers.render_job import generate_poster, generate_batch

def enqueue_single_poster(template_id: int, product_id: int, user_id: int, campaign_id: int = None):
    """
    Enqueue a single poster generation job
    
    Returns:
        str: Job ID
    """
    job = QueueManager.enqueue_job(
        generate_poster,
        template_id,
        product_id,
        user_id,
        campaign_id,
        queue_name='poster-generation',
        timeout=300  # 5 minutes
    )
    
    return job.id


def enqueue_batch_posters(template_id: int, product_ids: list, user_id: int, campaign_id: int = None):
    """
    Enqueue a batch poster generation job
    
    Returns:
        str: Job ID
    """
    job = QueueManager.enqueue_job(
        generate_batch,
        template_id,
        product_ids,
        user_id,
        campaign_id,
        queue_name='poster-generation',
        timeout=1800  # 30 minutes for batch
    )
    
    return job.id
