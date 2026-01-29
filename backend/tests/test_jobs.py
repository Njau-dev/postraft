import time
from app import create_app
from app.models import Template, Product, User
from app.workers.batch_job import enqueue_single_poster, enqueue_batch_posters
from app.workers.queue_manager import QueueManager

def test_jobs():
    """Test background job system"""
    print("\n🧪 Testing Job Queue System\n")
    
    app = create_app()
    
    with app.app_context():
        # Get test data
        user = User.query.filter_by(email='demo@postcraft.com').first()
        if not user:
            print("❌ User not found. Please login first.")
            return
        
        template = Template.query.filter_by(is_system=True).first()
        if not template:
            print("❌ No templates found. Run seed_templates.py first")
            return
        
        product = Product.query.filter_by(user_id=user.id).first()
        if not product:
            print("❌ No products found. Create a product first.")
            return
        
        print(f"✅ Test data ready:")
        print(f"   User: {user.email}")
        print(f"   Template: {template.name}")
        print(f"   Product: {product.name}")
        
        # Test 1: Enqueue single poster
        print("\n1️⃣ Enqueueing single poster job...")
        job_id = enqueue_single_poster(
            template_id=template.id,
            product_id=product.id,
            user_id=user.id
        )
        print(f"   ✅ Job enqueued: {job_id}")
        
        # Wait and check status
        print("   ⏳ Waiting for job to complete...")
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            status = QueueManager.get_job_status(job_id)
            print(f"   Status: {status['status']}", end='\r')
            
            if status['status'] in ['completed', 'failed']:
                break
        
        print()  # New line
        final_status = QueueManager.get_job_status(job_id)
        
        if final_status['status'] == 'completed':
            print(f"   ✅ Job completed!")
            print(f"   Result: {final_status.get('result')}")
        elif final_status['status'] == 'failed':
            print(f"   ❌ Job failed: {final_status.get('error')}")
        else:
            print(f"   ⏸️  Job still {final_status['status']}")
        
        # Test 2: Check job retrieval
        print("\n2️⃣ Testing job status retrieval...")
        retrieved_status = QueueManager.get_job_status(job_id)
        print(f"   ✅ Retrieved status: {retrieved_status['status']}")
        
        # Test 3: Invalid job ID
        print("\n3️⃣ Testing invalid job ID...")
        invalid_status = QueueManager.get_job_status('invalid-id-12345')
        print(f"   ✅ Invalid job handled: {invalid_status['status']}")
        
        print("\n✅ Job queue tests complete!")
        print("\n💡 To see jobs processing in real-time, run:")
        print("   python worker.py")

if __name__ == '__main__':
    test_jobs()
