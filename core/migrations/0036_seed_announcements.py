from django.db import migrations

def seed_announcements(apps, schema_editor):
    Announcement = apps.get_model('core', 'Announcement')
    if not Announcement.objects.exists():
        Announcement.objects.create(
            text="Save up to $500/year on car insurance!",
            link="/blog/how-to-lower-your-car-insurance-overview/",
            order=1
        )
        Announcement.objects.create(
            text="New Guide: Best Car Insurance in Florida",
            link="/blog/best-car-insurance-in-florida-overview/",
            order=2
        )
        Announcement.objects.create(
            text="Compare Quotes & Save Today!",
            link="/#",
            order=3
        )

def unseed_announcements(apps, schema_editor):
    Announcement = apps.get_model('core', 'Announcement')
    Announcement.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_announcement'),
    ]

    operations = [
        migrations.RunPython(seed_announcements, reverse_code=unseed_announcements),
    ]
