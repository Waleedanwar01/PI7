from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone

def seed_home_content(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    BlogPost = apps.get_model('core', 'BlogPost')
    QuickFAQ = apps.get_model('core', 'QuickFAQ')
    
    # 1. Best Category and Subcategories
    best_cat, _ = BlogCategory.objects.get_or_create(
        slug='best',
        defaults={'name': 'Best', 'is_active': True, 'order': 1}
    )
    
    best_subcats = [
        "No Down Payment", "Bad Credit", "Bad Driving Record", 
        "Low Mileage Driver", "Military / Veteran Discounts", "Most Affordable", 
        "No License", "Non-Owner", "Pay-Per-Mile", 
        "Popular Providers", "Senior Drivers", "Teacher Discounts"
    ]
    
    for i, name in enumerate(best_subcats):
        slug = slugify(name)
        BlogCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'parent': best_cat,
                'is_active': True,
                'order': i
            }
        )

    # 2. Section Posts
    # Helper to create/get post
    def create_post(title, summary, category_name, **kwargs):
        slug = slugify(title)
        cat, _ = BlogCategory.objects.get_or_create(
            slug=slugify(category_name),
            defaults={'name': category_name, 'is_active': True}
        )
        defaults = {
            'title': title,
            'summary': summary,
            'category': cat,
            'content': f"<p>{summary}</p><p>Lorem ipsum dolor sit amet...</p>",
            'is_active': True,
            # 'published_at': timezone.now(), # Removed as field does not exist
            'meta_title': title,
            'meta_description': summary,
        }
        defaults.update(kwargs)
        post, created = BlogPost.objects.update_or_create(
            slug=slug,
            defaults=defaults
        )
        return post

    # Recommendations
    recs = [
        ("Best Car Insurance for Teens", "Adding a teen driver can be expensive. Find out which companies offer the best rates.", "Recommendations"),
        ("Cheapest Full Coverage Insurance", "Get the best value for your money with our top picks for affordable full coverage.", "Recommendations"),
        ("Best Insurance for High Risk Drivers", "Don't let a bad record stop you. Compare insurers that specialize in high-risk coverage.", "Recommendations"),
    ]
    for title, summary, cat in recs:
        create_post(title, summary, cat, show_in_recommendations=True)

    # Guides
    guides = [
        ("How to File a Claim", "Step-by-step guide on what to do after an accident and how to file a car insurance claim.", "Guides"),
        ("Understanding Deductibles", "High deductible vs. low deductible? Learn how your choice affects your premium and wallet.", "Guides"),
        ("Full Coverage vs Liability", "What's the difference? We break down coverage types so you can choose what's right for you.", "Guides"),
    ]
    for title, summary, cat in guides:
        create_post(title, summary, cat, show_in_guides=True)

    # Driving Research
    research = [
        ("Traffic Laws by State", "Stay legal on the road. Check out our comprehensive guide to traffic laws in every state.", "Driving Research"),
        ("Car Seat Safety", "Keep your little ones safe. Current car seat laws and safety recommendations.", "Driving Research"),
        ("Teen Driving Statistics", "Important stats every parent and teen driver should know before hitting the road.", "Driving Research"),
    ]
    for title, summary, cat in research:
        create_post(title, summary, cat, show_in_research=True)

    # 3. Popular Topics (Mix of existing and new)
    popular = [
        ("Fuel Cost Calculator", "Get an estimate on how much you can expect to pay in gas based on your vehicle.", "Tools"),
        ("Moving Out of State", "Location impacts your policy, so plan ahead to get the best rate when moving.", "Guides"),
        ("Shopping for a New Car", "Resources to maximize savings when buying and insuring a new car.", "Guides"),
    ]
    # Add some from above to popular
    popular_titles = [p[0] for p in popular] + ["Best Car Insurance for Teens", "How to File a Claim", "Understanding Deductibles"]
    
    for title, summary, cat in popular:
        create_post(title, summary, cat, is_popular=True)
        
    BlogPost.objects.filter(title__in=["Best Car Insurance for Teens", "How to File a Claim", "Understanding Deductibles"]).update(is_popular=True)

    # 4. Quick FAQs
    faqs = [
        ("How do I compare car insurance quotes?", "Comparing quotes is easy! Just enter your zip code, answer a few questions about your vehicle and driving history, and we'll show you rates from top providers side-by-side."),
        ("Is this service free to use?", "Yes. There are no fees to get quotes or compare offers. You only pay the insurer if you choose a policy."),
        ("Will checking rates affect my credit score?", "No. Getting quotes is a soft inquiry and does not impact your credit score."),
        ("Can I switch insurance companies before my policy ends?", "Yes, you can usually switch at any time. Your old insurer will refund any unused premium."),
    ]
    
    for i, (q, a) in enumerate(faqs):
        QuickFAQ.objects.get_or_create(
            question=q,
            defaults={'answer': a, 'is_active': True, 'order': i}
        )

def remove_home_content(apps, schema_editor):
    # We generally don't delete data in reverse migrations unless strictly necessary to avoid data loss on rollback
    # But for a seed migration, we might want to cleanup specific items created.
    # For now, we'll leave it as no-op or partial cleanup.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_blogpost_show_in_guides_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_home_content, remove_home_content),
    ]
