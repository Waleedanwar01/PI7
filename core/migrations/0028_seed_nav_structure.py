from django.db import migrations
from django.utils.text import slugify

def seed(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    def get_or_create(name, parent=None, nav_group='', is_dropdown=False, show_in_navbar=False, order=0):
        s = slugify(name or '')
        obj = BlogCategory.objects.filter(slug=s).first()
        if not obj:
            obj = BlogCategory(name=name, slug=s, parent=parent, nav_group=nav_group, is_dropdown=is_dropdown, show_in_navbar=show_in_navbar, order=order, is_active=True)
            try:
                obj.save()
            except Exception:
                obj = BlogCategory.objects.filter(slug=s).first()
                if obj:
                    obj.parent = parent
                    obj.nav_group = nav_group or obj.nav_group
                    obj.is_dropdown = is_dropdown or obj.is_dropdown
                    obj.show_in_navbar = show_in_navbar or obj.show_in_navbar
                    obj.is_active = True
                    obj.order = order
                    obj.save()
        else:
            if parent is not None and obj.parent_id != (parent.id if hasattr(parent, 'id') else None):
                obj.parent = parent
            obj.nav_group = nav_group or obj.nav_group
            obj.is_dropdown = is_dropdown or obj.is_dropdown
            obj.show_in_navbar = show_in_navbar or obj.show_in_navbar
            obj.is_active = True
            obj.order = order
            obj.save()
        return obj
    q1 = get_or_create('Start Here', None, 'quotes', True, True, 1)
    get_or_create('Get Auto Insurance Quotes', q1, '', False, False, 1)
    get_or_create('Switch & Save: How to Switch Insurance', q1, '', False, False, 2)
    q2 = get_or_create('By State', None, 'quotes', True, True, 2)
    get_or_create('Best Car Insurance in Florida', q2, '', False, False, 1)
    get_or_create('Best Car Insurance in Texas', q2, '', False, False, 2)
    get_or_create('Best Car Insurance in California', q2, '', False, False, 3)
    get_or_create('Best Car Insurance in Pennsylvania', q2, '', False, False, 4)
    c1 = get_or_create('Top Picks', None, 'companies', False, True, 1)
    c2 = get_or_create('Best Auto Insurance Companies', None, 'companies', False, True, 2)
    c3 = get_or_create('Cheapest Car Insurance Companies', None, 'companies', False, True, 3)
    c4 = get_or_create('Best for Full Coverage', None, 'companies', False, True, 4)
    c5 = get_or_create('Best for Liability-Only', None, 'companies', False, True, 5)
    c6 = get_or_create('By Need', None, 'companies', True, True, 6)
    get_or_create('Best for New Drivers', c6, '', False, False, 1)
    get_or_create('Best for Seniors', c6, '', False, False, 2)
    get_or_create('Best for Non-Owners', c6, '', False, False, 3)
    get_or_create('No License Owners', c6, '', False, False, 4)
    get_or_create('No Down Payment', c6, '', False, False, 5)
    c7 = get_or_create('Insurance Providers', None, 'companies', True, True, 7)
    get_or_create('GEICO Pricing', c7, '', False, False, 1)
    get_or_create('Progressive Pricing', c7, '', False, False, 2)
    get_or_create('State Farm Review', c7, '', False, False, 3)
    get_or_create('USAA Review', c7, '', False, False, 4)
    get_or_create('View All Reviews →', c7, '', False, False, 5)
    k1 = get_or_create('Coverage Types', None, 'cost', True, True, 1)
    get_or_create('Full Coverage vs Liability', k1, '', False, False, 1)
    get_or_create('Collision Insurance', k1, '', False, False, 2)
    get_or_create('Comprehensive Insurance', k1, '', False, False, 3)
    get_or_create('Uninsured/Underinsured Motorist', k1, '', False, False, 4)
    get_or_create('SR-22 Insurance Guide', k1, '', False, False, 5)
    k2 = get_or_create('Costs & Pricing', None, 'cost', True, True, 2)
    get_or_create('Average Cost of Car Insurance', k2, '', False, False, 1)
    get_or_create('What Affects Your Rate', k2, '', False, False, 2)
    get_or_create('Car Insurance Deductibles Explained', k2, '', False, False, 3)
    k3 = get_or_create('Tools', None, 'cost', True, True, 3)
    get_or_create('Fuel Cost Calculator', k3, '', False, False, 1)
    get_or_create('Car Loan Calculator', k3, '', False, False, 2)
    s1 = get_or_create('Discounts', None, 'save', True, True, 1)
    get_or_create('Popular Insurance Discounts', s1, '', False, False, 1)
    get_or_create('Veteran Discounts', s1, '', False, False, 2)
    get_or_create('Home & Auto Policy Bundling', s1, '', False, False, 3)
    get_or_create('Teachers & Educator Discounts', s1, '', False, False, 4)
    s2 = get_or_create('Savings Guides', None, 'save', True, True, 2)
    get_or_create('How to Lower Your Car Insurance', s2, '', False, False, 1)
    get_or_create('Pay-Per-Mile Auto Insurance', s2, '', False, False, 2)
    s3 = get_or_create('Shop Smart', None, 'save', True, True, 3)
    get_or_create('Switch & Save After a Rate Increase', s3, '', False, False, 1)
    get_or_create('Cheapest Cars to Insure', s3, '', False, False, 2)
    get_or_create('5 Ways to Lower Your Deductible', s3, '', False, False, 3)
    r1 = get_or_create('Starter Guides', None, 'resources', True, True, 1)
    get_or_create('How Car Insurance Works', r1, '', False, False, 1)
    get_or_create('Fault vs No-Fault Accidents', r1, '', False, False, 2)
    get_or_create('Accident & Claims Guide', r1, '', False, False, 3)
    get_or_create('Managing Rate Increases', r1, '', False, False, 4)
    get_or_create('Insurance for New Cars', r1, '', False, False, 5)
    r2 = get_or_create('State Requirements', None, 'resources', True, True, 2)
    get_or_create('Florida Minimum Coverage', r2, '', False, False, 1)
    get_or_create('Texas Minimum Coverage', r2, '', False, False, 2)
    get_or_create('California Minimum Coverage', r2, '', False, False, 3)
    r3 = get_or_create('Popular FAQs', None, 'resources', True, True, 3)
    get_or_create('Why Did My Insurance Go Up?', r3, '', False, False, 1)
    get_or_create('What is Proof of Insurance?', r3, '', False, False, 2)
    get_or_create('Should You Report Minor Accidents', r3, '', False, False, 3)

def unseed(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    names = [
        'Start Here','Get Auto Insurance Quotes','Switch & Save: How to Switch Insurance','By State',
        'Best Car Insurance in Florida','Best Car Insurance in Texas','Best Car Insurance in California','Best Car Insurance in Pennsylvania',
        'Top Picks','Best Auto Insurance Companies','Cheapest Car Insurance Companies','Best for Full Coverage','Best for Liability-Only',
        'By Need','Best for New Drivers','Best for Seniors','Best for Non-Owners','No License Owners','No Down Payment',
        'Insurance Providers','GEICO Pricing','Progressive Pricing','State Farm Review','USAA Review','View All Reviews →',
        'Coverage Types','Full Coverage vs Liability','Collision Insurance','Comprehensive Insurance','Uninsured/Underinsured Motorist','SR-22 Insurance Guide',
        'Costs & Pricing','Average Cost of Car Insurance','What Affects Your Rate','Car Insurance Deductibles Explained',
        'Tools','Fuel Cost Calculator','Car Loan Calculator',
        'Discounts','Popular Insurance Discounts','Veteran Discounts','Home & Auto Policy Bundling','Teachers & Educator Discounts',
        'Savings Guides','How to Lower Your Car Insurance','Pay-Per-Mile Auto Insurance',
        'Shop Smart','Switch & Save After a Rate Increase','Cheapest Cars to Insure','5 Ways to Lower Your Deductible',
        'Starter Guides','How Car Insurance Works','Fault vs No-Fault Accidents','Accident & Claims Guide','Managing Rate Increases','Insurance for New Cars',
        'State Requirements','Florida Minimum Coverage','Texas Minimum Coverage','California Minimum Coverage',
        'Popular FAQs','Why Did My Insurance Go Up?','What is Proof of Insurance?','Should You Report Minor Accidents'
    ]
    BlogCategory.objects.filter(name__in=names).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0027_siteconfig_announcement_text'),
    ]
    operations = [
        migrations.RunPython(seed, unseed),
    ]
