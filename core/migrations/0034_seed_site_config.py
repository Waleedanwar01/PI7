from django.db import migrations

def seed_site_config(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    if not SiteConfig.objects.exists():
        SiteConfig.objects.create(
            site_name="AutoInsurance.com",
            phone_number="(866) 843-5386",
            email="support@autoinsurance.com",
            home_title="Compare Cheap Car Insurance Quotes",
            hero_title="Affordable Car Insurance Starts Here",
            hero_subtitle="Compare quotes in minutes and maximize savings on a policy that’s right for you. Rates as low as $29/month*",
            hero_button_text="Continue",
            footer_text="AutoInsurance.com © 2026. All Rights Reserved.",
            address="12130 Millennium Drive, Ste 600 Los Angeles, CA 90094",
            footer_disclaimer="The Site is owned and operated by AutoInsurance.com. AutoInsurance.com is an insurance provider matching service and not an insurance broker or insurance company. Not all insurance companies are able to provide you with a quote. Make sure to compare carriers.",
            facebook_url="https://facebook.com",
            twitter_url="https://twitter.com",
            instagram_url="https://instagram.com",
            linkedin_url="https://linkedin.com",
            youtube_url="https://youtube.com",
            announcement_text="Save up to $500/year on car insurance!"
        )

def unseed_site_config(apps, schema_editor):
    # We generally don't want to delete the config on reverse, but for completeness:
    # SiteConfig = apps.get_model('core', 'SiteConfig')
    # SiteConfig.objects.all().delete()
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_seed_home_content'),
    ]

    operations = [
        migrations.RunPython(seed_site_config, reverse_code=unseed_site_config),
    ]
