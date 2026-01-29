from app import create_app
from app.extensions import db
from app.models import Poster, Product, Template, Campaign, User
from renderer.engine import PosterRenderer
from app.infrastructure.storage import upload_image
from io import BytesIO
import traceback

# Create app context for workers
app = create_app()


def generate_poster(template_id: int, product_id: int, user_id: int, campaign_id: int = None):
    """
    Generate a single poster (runs as background job)

    Args:
        template_id: Template ID
        product_id: Product ID
        user_id: User ID
        campaign_id: Optional campaign ID

    Returns:
        dict: Result with poster_id and image_url
    """
    with app.app_context():
        try:
            print(
                f"🎨 Starting poster generation: Template {template_id}, Product {product_id}")

            # Load data
            template = Template.query.get(template_id)
            product = Product.query.get(product_id)
            user = User.query.get(user_id)
            campaign = Campaign.query.get(campaign_id) if campaign_id else None

            if not template:
                raise ValueError(f"Template {template_id} not found")

            if not product:
                raise ValueError(f"Product {product_id} not found")

            if not user:
                raise ValueError(f"User {user_id} not found")

            # Prepare data context
            data = {
                'product': {
                    'name': product.name,
                    'price': product.price,
                    'image': product.image_url,
                    'category': product.category,
                    'sku': product.sku,
                    'description': product.description,
                }
            }

            # Add campaign data if present
            if campaign:
                data['campaign'] = campaign.rules or {}

            print(f"📦 Data prepared: {data['product']['name']}")

            # Render poster
            renderer = PosterRenderer()
            image_bytes = renderer.render(template.json_definition, data)

            print(f"✅ Poster rendered: {len(image_bytes)} bytes")

            # Upload to cloud storage
            image_file = BytesIO(image_bytes)
            image_file.name = f"poster_{product_id}_{template_id}.png"

            image_url = upload_image(image_file, folder='posters')

            if not image_url:
                raise Exception("Failed to upload poster to storage")

            print(f"☁️  Uploaded to: {image_url}")

            # Save poster to database
            poster = Poster(
                user_id=user_id,
                product_id=product_id,
                campaign_id=campaign_id,
                template_id=template_id,
                image_url=image_url,
                format=template.format,
                status='generated'
            )

            db.session.add(poster)

            # Increment user's generation count
            user.monthly_generations += 1

            db.session.commit()

            print(f"✅ Poster saved to database: ID {poster.id}")

            return {
                'poster_id': poster.id,
                'image_url': image_url,
                'product_name': product.name,
                'template_name': template.name,
            }

        except Exception as e:
            print(f"❌ Error generating poster: {e}")
            traceback.print_exc()

            # Try to save failed poster record
            try:
                poster = Poster(
                    user_id=user_id,
                    product_id=product_id,
                    campaign_id=campaign_id,
                    template_id=template_id,
                    image_url='',
                    format='square',
                    status='failed',
                    error_message=str(e)
                )
                db.session.add(poster)
                db.session.commit()
            except:
                pass

            raise


def generate_batch(template_id: int, product_ids: list, user_id: int, campaign_id: int = None):
    """
    Generate multiple posters (runs as background job)

    Args:
        template_id: Template ID
        product_ids: List of product IDs
        user_id: User ID
        campaign_id: Optional campaign ID

    Returns:
        dict: Results summary
    """
    with app.app_context():
        print(f"🚀 Starting batch generation: {len(product_ids)} posters")

        results = []
        errors = []

        for product_id in product_ids:
            try:
                result = generate_poster(
                    template_id, product_id, user_id, campaign_id)
                results.append(result)
            except Exception as e:
                errors.append({
                    'product_id': product_id,
                    'error': str(e)
                })

        print(
            f"✅ Batch complete: {len(results)} success, {len(errors)} failed")

        return {
            'total': len(product_ids),
            'successful': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        }
