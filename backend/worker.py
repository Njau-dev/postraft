"""
RQ Worker Entry Point

Run with: python worker.py
Or with specific queues: python worker.py poster-generation default
"""

import sys
import os
from rq import Worker, Queue, Connection
from app import create_app
from app.workers.queue_manager import QueueManager


def main():
    """Start RQ worker"""

    # Create Flask app for context
    app = create_app()

    with app.app_context():
        # Get Redis connection
        redis_conn = QueueManager.get_redis_connection()

        # Get queue names from command line or use defaults
        queue_names = sys.argv[1:] if len(sys.argv) > 1 else [
            'poster-generation', 'default']

        print(f"\n🔧 Starting RQ Worker")
        print(f"📋 Listening on queues: {', '.join(queue_names)}")
        print(f"🔄 Press Ctrl+C to stop\n")

        # Create queues
        queues = [Queue(name, connection=redis_conn) for name in queue_names]

        # Start worker
        with Connection(redis_conn):
            worker = Worker(queues, connection=redis_conn)
            worker.work()

if __name__ == '__main__':
    main()
