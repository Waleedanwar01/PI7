from django.db import migrations
from django.utils.text import slugify
from django.utils.timezone import now

def seed_states(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    BlogPost = apps.get_model('core', 'BlogPost')

    # Ensure parent category exists
    parent_cat_name = "Auto Insurance by State"
    parent_cat_slug = slugify(parent_cat_name)
    parent_cat, created = BlogCategory.objects.get_or_create(
        slug=parent_cat_slug,
        defaults={
            'name': parent_cat_name,
            'is_active': True,
            'order': 10,  # Adjust order as needed
            'nav_group': 'resources' # Assign to a group to ensure it appears in lists
        }
    )

    states = [
        ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"),
        ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"), ("DC", "District of Columbia"),
        ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"),
        ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"),
        ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"),
        ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"),
        ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"),
        ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"), ("OR", "Oregon"),
        ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"),
        ("TN", "Tennessee"), ("TX", 'Texas'), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"),
        ("WA", "Washington"), ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")
    ]

    for code, name in states:
        # Create Child Category
        cat_slug = slugify(name)
        category, _ = BlogCategory.objects.get_or_create(
            slug=cat_slug,
            defaults={
                'name': name,
                'parent': parent_cat,
                'is_active': True,
                'order': 0,
                'nav_group': 'states'
            }
        )

        # Create Blog Post
        post_title = f"Best Auto Insurance in {name}"
        post_slug = slugify(post_title)
        
        # Check if post exists to avoid duplication
        if not BlogPost.objects.filter(slug=post_slug).exists():
            BlogPost.objects.create(
                slug=post_slug,
                title=post_title,
                category=category,
                summary=f"Compare the best auto insurance rates and companies in {name}. Find cheap coverage options today.",
                content=(
                    f"<h2>Auto Insurance in {name}</h2>"
                    f"<p>Finding the best auto insurance in {name} requires comparing quotes from multiple providers. "
                    f"Whether you live in a major city or a rural area, rates can vary significantly based on your driving history and coverage needs.</p>"
                    f"<h3>Minimum Requirements in {name}</h3>"
                    f"<p>Drivers in {name} are required to carry minimum liability coverage. However, experts often recommend full coverage for better protection.</p>"
                    f"<h3>How to Save on Car Insurance in {name}</h3>"
                    f"<ul>"
                    f"<li>Bundle your home and auto policies</li>"
                    f"<li>Maintain a clean driving record</li>"
                    f"<li>Ask about discounts for students or safe drivers</li>"
                    f"</ul>"
                ),
                is_active=True,
                meta_title=post_title,
                meta_description=f"Find affordable auto insurance in {name}. Compare top rated carriers and save on your premiums.",
                meta_keywords=f"{name} auto insurance, car insurance {name}, cheap insurance {code}",
                author_name="Editorial Team",
                updated_at=now()
            )

def remove_states(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    # Optional: Delete created categories and posts
    parent_cat_name = "Auto Insurance by State"
    parent = BlogCategory.objects.filter(slug=slugify(parent_cat_name)).first()
    if parent:
        parent.children.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0041_state_company_states'),
    ]

    operations = [
        migrations.RunPython(seed_states, reverse_code=remove_states),
    ]
