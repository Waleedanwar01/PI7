from django.db import migrations
from django.utils.text import slugify

def enable_footer_for_states(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    
    parent_cat_name = "Auto Insurance by State"
    try:
        category = BlogCategory.objects.get(slug=slugify(parent_cat_name))
        category.show_in_footer = True
        category.save()
    except BlogCategory.DoesNotExist:
        pass

def disable_footer_for_states(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    
    parent_cat_name = "Auto Insurance by State"
    try:
        category = BlogCategory.objects.get(slug=slugify(parent_cat_name))
        category.show_in_footer = False
        category.save()
    except BlogCategory.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0042_seed_states_data'),
    ]

    operations = [
        migrations.RunPython(enable_footer_for_states, reverse_code=disable_footer_for_states),
    ]
