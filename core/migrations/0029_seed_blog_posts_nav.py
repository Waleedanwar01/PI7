from django.db import migrations
from django.utils.text import slugify
from django.utils.timezone import now

def seed_posts(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    BlogPost = apps.get_model('core', 'BlogPost')

    entries = [
        ("Get Auto Insurance Quotes", "Your step-by-step guide to comparing auto insurance quotes and getting the best rate.", "quotes"),
        ("Switch & Save: How to Switch Insurance", "Learn how to switch insurers smoothly and save money.", "quotes"),
        ("Best Car Insurance in Florida", "Top providers and average rates in Florida with tips to save.", "quotes"),
        ("Best Car Insurance in Texas", "Best Texas insurers, coverage options, and savings strategies.", "quotes"),
        ("GEICO Pricing", "Overview of GEICO pricing, discounts, and when it’s a good fit.", "companies"),
        ("Progressive Pricing", "Progressive pricing, Snapshot program, and pros/cons.", "companies"),
        ("State Farm Review", "Detailed State Farm review: coverage, claims, and pricing.", "companies"),
        ("USAA Review", "USAA review for military members and eligible families.", "companies"),
        ("Full Coverage vs Liability", "Understand full coverage vs. liability and when you need each.", "cost"),
        ("Collision Insurance", "What collision insurance covers and how deductibles work.", "cost"),
        ("Comprehensive Insurance", "Comprehensive coverage explained with real-world examples.", "cost"),
        ("Average Cost of Car Insurance", "National averages, factors affecting rates, and how to lower costs.", "cost"),
        ("Popular Insurance Discounts", "Common discounts and how to qualify for them.", "save"),
        ("How to Lower Your Car Insurance", "Actionable steps to reduce premiums without sacrificing coverage.", "save"),
        ("Pay-Per-Mile Auto Insurance", "How usage-based insurance works and who benefits most.", "save"),
        ("How Car Insurance Works", "Beginner-friendly overview of auto insurance and key terms.", "resources"),
        ("Accident & Claims Guide", "Exactly what to do after an accident and how to file claims.", "resources"),
        ("Managing Rate Increases", "Why rates go up and practical ways to manage increases.", "resources"),
        ("Florida Minimum Coverage", "State minimum requirements and recommended add-ons for Florida.", "resources"),
        ("Texas Minimum Coverage", "State minimum requirements and recommended add-ons for Texas.", "resources"),
        ("Why Did My Insurance Go Up?", "Common reasons for premium hikes and how to respond.", "resources"),
    ]

    for title, summary, group in entries:
        cat_slug = slugify(title)
        category = BlogCategory.objects.filter(slug=cat_slug, is_active=True).first()
        if not category:
            # Some entries are children; if not found by title slug, try by nav_group plus title hints
            # Fall back: skip if category missing
            continue
        post_slug = slugify(f"{title}-overview")
        BlogPost.objects.get_or_create(
            slug=post_slug,
            defaults={
                'title': title,
                'category': category,
                'summary': summary,
                'content': (
                    f"<h2>{title}</h2>"
                    "<p>This article provides a practical overview with tips tailored to drivers. "
                    "Use quotes comparison and discounts to optimize your rate. Always review coverage needs.</p>"
                    "<h3>Key Takeaways</h3>"
                    "<ul><li>Know your coverage</li><li>Compare multiple quotes</li><li>Leverage discounts</li></ul>"
                ),
                'order': 0,
                'is_active': True,
                'meta_title': title,
                'meta_description': summary,
                'meta_keywords': 'auto insurance, car insurance, guide, savings',
                'author_name': 'Editorial Team',
                'updated_at': now(),
            }
        )

def unseed_posts(apps, schema_editor):
    BlogPost = apps.get_model('core', 'BlogPost')
    titles = [
        "Get Auto Insurance Quotes",
        "Switch & Save: How to Switch Insurance",
        "Best Car Insurance in Florida",
        "Best Car Insurance in Texas",
        "GEICO Pricing",
        "Progressive Pricing",
        "State Farm Review",
        "USAA Review",
        "Full Coverage vs Liability",
        "Collision Insurance",
        "Comprehensive Insurance",
        "Average Cost of Car Insurance",
        "Popular Insurance Discounts",
        "How to Lower Your Car Insurance",
        "Pay-Per-Mile Auto Insurance",
        "How Car Insurance Works",
        "Accident & Claims Guide",
        "Managing Rate Increases",
        "Florida Minimum Coverage",
        "Texas Minimum Coverage",
        "Why Did My Insurance Go Up?",
    ]
    for t in titles:
        slug = slugify(f"{t}-overview")
        BlogPost.objects.filter(slug=slug).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0028_seed_nav_structure'),
    ]
    operations = [
        migrations.RunPython(seed_posts, reverse_code=unseed_posts),
    ]
