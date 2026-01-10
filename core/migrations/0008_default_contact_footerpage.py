from django.db import migrations

def create_default_contact_page(apps, schema_editor):
    FooterPage = apps.get_model('core', 'FooterPage')
    if not FooterPage.objects.filter(title='Contact Us').exists():
        FooterPage.objects.create(
            title='Contact Us',
            link='/contact/',
            category='companies',
            order=0,
            is_active=True
        )

def remove_default_contact_page(apps, schema_editor):
    FooterPage = apps.get_model('core', 'FooterPage')
    FooterPage.objects.filter(title='Contact Us', link='/contact/').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_contactsubmission_footerpage'),
    ]
    operations = [
        migrations.RunPython(create_default_contact_page, remove_default_contact_page),
    ]
