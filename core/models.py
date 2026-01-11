import re
from django.db import models
from django.utils.text import slugify
from django.utils.text import slugify

class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default="AutoInsurance.com")
    phone_number = models.CharField(max_length=20, default="(866) 843-5386")
    email = models.EmailField(blank=True)
    home_title = models.CharField(max_length=200, blank=True)
    announcement_text = models.CharField(max_length=200, blank=True)
    
    hero_title = models.CharField(max_length=200, default="Affordable Car Insurance Starts Here")
    hero_subtitle = models.TextField(default="Compare quotes in minutes and maximize savings on a policy that’s right for you. Rates as low as $29/month*")
    hero_button_text = models.CharField(max_length=50, default="Continue")
    
    footer_text = models.TextField(default="AutoInsurance.com © 2026. All Rights Reserved.")
    address = models.CharField(max_length=255, default="12130 Millennium Drive, Ste 600 Los Angeles, CA 90094")
    footer_disclaimer = models.TextField(default="The Site is owned and operated by AutoInsurance.com. AutoInsurance.com is an insurance provider matching service and not an insurance broker or insurance company. Not all insurance companies are able to provide you with a quote. Make sure to compare carrier rates and fees as they can vary between insurance companies and will depend upon the state in which you reside. Additionally, any savings you receive will depend upon your driving history and other factors as determined by the insurance companies giving you quotes. None of the insurance companies with whom you may be matched through the site sponsor, endorse, or are in any way affiliated with AutoInsurance.com or this site.")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    youtube_channel_name = models.CharField(max_length=100, blank=True, help_text="e.g. @AutoInsuranceExperts")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfig.objects.exists():
            return
        super(SiteConfig, self).save(*args, **kwargs)

class Announcement(models.Model):
    site_config = models.ForeignKey(SiteConfig, on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    text = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, help_text="Optional link for the announcement")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class State(models.Model):
    code = models.CharField(max_length=2, unique=True, help_text="2-letter state code (e.g., CA)")
    name = models.CharField(max_length=100, help_text="Full state name (e.g., California)")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='companies/')
    states = models.ManyToManyField(State, related_name='companies', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    domain = models.CharField(max_length=100, blank=True)
    landing_url = models.URLField(blank=True)
    description = models.TextField(blank=True, help_text="Short description of the company")
    order = models.IntegerField(default=0)
    is_show_on_home = models.BooleanField(default=True)
    
    # New fields for results page
    heading = models.CharField(max_length=255, blank=True, help_text="e.g. TN Drivers Could Save Big with GEICO")
    sub_heading_1 = models.CharField(max_length=255, blank=True)
    sub_heading_2 = models.CharField(max_length=255, blank=True)
    sub_heading_3 = models.CharField(max_length=255, blank=True)
    btn_text = models.CharField(max_length=50, default="View My Quote")

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['order']

    def __str__(self):
        return self.name

class ZipCode(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    companies = models.ManyToManyField(Company, related_name='zip_codes', blank=True)
    
    def __str__(self):
        return self.code

class ZipRangeCompany(models.Model):
    zip_range = models.ForeignKey('ZipRange', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_top_pick = models.BooleanField(default=False, verbose_name="Is Top Pick?")
    
    class Meta:
        verbose_name = "Zip Range Company"
        verbose_name_plural = "Zip Range Companies"
        unique_together = ('zip_range', 'company')

class ZipRange(models.Model):
    STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
        ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
        ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
        ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
        ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
        ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]

    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, help_text="Select a state to automatically set zip range (optional)")
    start_zip = models.IntegerField(help_text="Start of the zip code range (e.g., 38000)")
    end_zip = models.IntegerField(help_text="End of the zip code range (e.g., 38050)")
    companies = models.ManyToManyField(Company, related_name='zip_ranges', blank=True, through='ZipRangeCompany')
    
    class Meta:
        verbose_name = "Zip Code Range"
        verbose_name_plural = "Zip Code Ranges"
        ordering = ['state', 'start_zip']

    def __str__(self):
        if self.state:
            return f"{self.get_state_display()} ({self.start_zip} - {self.end_zip})"
        return f"{self.start_zip} - {self.end_zip}"

    def clean(self):
        if self.start_zip > self.end_zip:
            from django.core.exceptions import ValidationError
            raise ValidationError("Start zip must be less than or equal to end zip.")


class FooterPage(models.Model):
    CATEGORY_CHOICES = [
        ('legal', 'Legal'),
        ('companies', 'Companies'),
    ]
    LAYOUT_CHOICES = [
        ('center', 'Center (max-width)'),
        ('full', 'Full width'),
    ]
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = models.TextField(blank=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='center')
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Footer Page"
        verbose_name_plural = "Footer Pages"
    
    def __str__(self):
        return f"{self.title} ({self.category})"
    
    def save(self, *args, **kwargs):
        title_slug = slugify(self.title or "")
        if (not self.link) and title_slug:
            self.link = f"/pages/{title_slug}/"
        if (not self.meta_title) and self.title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
    
    def __str__(self):
        return f"{self.name} - {self.email}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team/', blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.name} ({self.position})"

class FaqCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def link(self):
        return f"/faq/category/{self.slug}/"
    
    def __str__(self):
        return self.name

class FaqPost(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_photo = models.ImageField(upload_to='faq/authors/', blank=True)
    author_bio = models.TextField(blank=True)
    author_facebook_url = models.URLField(blank=True)
    author_twitter_url = models.URLField(blank=True)
    author_instagram_url = models.URLField(blank=True)
    author_linkedin_url = models.URLField(blank=True)
    author_website_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "FAQ Post"
        verbose_name_plural = "FAQ Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)
        try:
            if self.category and self.category.company:
                if not self.companies.filter(pk=self.category.company.pk).exists():
                    self.companies.add(self.category.company)
        except Exception:
            pass
    
    def link(self):
        return f"/faq/post/{self.slug}/"
    
    def __str__(self):
        return self.title

class FaqImage(models.Model):
    post = models.ForeignKey(FaqPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='faq/images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "FAQ Image"
        verbose_name_plural = "FAQ Images"

    def __str__(self):
        return self.caption or f"FAQ Image {self.pk}"

class QuickFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "Quick FAQ"
        verbose_name_plural = "Quick FAQs"

    def __str__(self):
        return self.question

class BlogCategory(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_dropdown = models.BooleanField(default=False)
    show_in_navbar = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=False)
    nav_group = models.CharField(
        max_length=20,
        default='',
        blank=True,
        choices=[
            ('', 'None'),
            ('quotes', 'Compare Quotes'),
            ('companies', 'Companies'),
            ('cost', 'Coverage & Cost'),
            ('save', 'Ways to Save'),
            ('resources', 'Resources & FAQs'),
        ],
    )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def link(self):
        return f"/blog/category/{self.slug}/"

    @property
    def first_post(self):
        if hasattr(self, '_prefetched_objects_cache') and 'posts' in self._prefetched_objects_cache:
            active_posts = [p for p in self.posts.all() if p.is_active]
            return active_posts[0] if active_posts else None
        return self.posts.filter(is_active=True).order_by('order', 'title').first()

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False, help_text="Check this to show in 'Explore Popular Topics' section on home page")
    show_in_recommendations = models.BooleanField(default=False, help_text="Check to show in 'Our Top Recommendations' / 'Recommendations' section on home page")
    show_in_guides = models.BooleanField(default=False, help_text="Check to show in 'Guides' section on home page")
    show_in_research = models.BooleanField(default=False, help_text="Check to show in 'Driving Research' section on home page")
    icon = models.ImageField(upload_to='blog/icons/', blank=True, help_text="Icon for 'Explore Popular Topics' section")
    hero_image = models.ImageField(upload_to='blog/hero/', blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_photo = models.ImageField(upload_to='blog/authors/', blank=True)
    author_bio = models.TextField(blank=True)
    companies = models.ManyToManyField(Company, blank=True, related_name='blog_posts')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    def link(self):
        return f"/blog/post/{self.slug}/"

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Blog Image"
        verbose_name_plural = "Blog Images"

    def __str__(self):
        return self.caption or f"Blog Image {self.pk}"

class HomeVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Home Video"
        verbose_name_plural = "Home Videos"
        ordering = ['order', '-published_at', '-created_at']
        
    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        if not self.youtube_url:
            return ""
        
        # Extract video ID from YouTube URL
        # Support for:
        # - youtube.com/watch?v=VIDEO_ID
        # - youtu.be/VIDEO_ID
        # - youtube.com/embed/VIDEO_ID
        
        video_id = ""
        pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(pattern, self.youtube_url)
        
        if match:
            video_id = match.group(1)
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            
        return ""
