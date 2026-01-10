from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import re

register = template.Library()

@register.filter
def state_code(name):
    """Converts state name to 2-letter code."""
    mapping = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
        'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
        'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
        'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
        'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
        'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    return mapping.get(name, name)

@register.filter
def format_content(html):
    if not html:
        return ""
    parts = re.split(r'(<p[^>]*>.*?</p>)', html, flags=re.IGNORECASE|re.DOTALL)
    out = []
    list_open = False
    section_open = False
    for part in parts:
        if not part:
            continue
        m = re.match(r'<p[^>]*>(.*?)</p>', part, flags=re.IGNORECASE|re.DOTALL)
        if not m:
            if list_open:
                out.append('</ul>')
                list_open = False
            if section_open:
                out.append('</div>')
                section_open = False
            out.append(part)
            continue
        text = m.group(1).strip()
        plain = re.sub(r'<[^>]+>', '', text).strip()
        if re.match(r'^(\-|\*|•)\s+', plain):
            if not list_open:
                out.append('<ul>')
                list_open = True
            item = re.sub(r'^(\-|\*|•)\s+', '', plain)
            out.append(f'<li>{item}</li>')
            continue
        else:
            if list_open:
                out.append('</ul>')
                list_open = False
        words = plain.split()
        is_heading = (
            len(plain) <= 100 and
            len(words) <= 12 and
            not re.search(r'(http|@|\d{4,})', plain, flags=re.IGNORECASE)
        )
        if is_heading:
            if section_open:
                out.append('</div>')
                section_open = False
            out.append('<div class="pc-section">')
            section_open = True
            out.append(f'<h2>{plain}</h2>')
        else:
            if not section_open:
                out.append('<div class="pc-section">')
                section_open = True
            out.append(f'<p>{plain}</p>')
    if list_open:
        out.append('</ul>')
    if section_open:
        out.append('</div>')
    return mark_safe(''.join(out))

@register.filter
def add_heading_ids(html):
    if not html:
        return ""
    def _repl(m):
        tag = m.group(1).lower()
        inner = m.group(2)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        hid = slugify(plain)[:60]
        return f'<{tag} id="{hid}">{inner}</{tag}>'
    out = re.sub(r'<(h[2-3])[^>]*>(.*?)</h[2-3]>', _repl, html, flags=re.IGNORECASE|re.DOTALL)
    return mark_safe(out)

@register.filter
def extract_headings(html):
    if not html:
        return []

@register.filter
def cloudinary_optimize(url):
    """
    Temporarily disabled optimization to fix image loading issues.
    """
    return url
    
    # if not url or 'cloudinary.com' not in url:
    #     return url
    # if '/upload/' in url and '/upload/f_auto,q_auto/' not in url:
    #     return url.replace('/upload/', '/upload/f_auto,q_auto/')
    # return url
    heads = []
    for m in re.finditer(r'<h[2-3][^>]*>(.*?)</h[2-3]>', html, flags=re.IGNORECASE|re.DOTALL):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if not text:
            continue
        hid = slugify(text)[:60]
        heads.append((hid, text))
    return heads

@register.simple_tag
def render_faq_content(post):
    html = post.content or ""
    # Shortcodes for notes/protips
    def _protip_repl(m):
        text = m.group(1).strip()
        return f'''<div class="my-6 rounded-2xl border border-blue-200 bg-blue-50 p-6">
  <div class="flex items-start gap-3">
    <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-yellow-100 text-yellow-600">!</span>
    <div>
      <div class="font-extrabold tracking-wide text-blue-800">PRO TIP</div>
      <div class="mt-2 text-blue-900/90">{text}</div>
    </div>
  </div>
</div>'''
    def _note_repl(m):
        text = m.group(1).strip()
        return f'''<div class="my-4 rounded-xl border border-blue-200 bg-blue-50 p-4">
  <div class="font-semibold text-blue-800">Note</div>
  <div class="mt-1 text-blue-900/90">{text}</div>
</div>'''
    html = re.sub(r'\[protip\](.*?)\[/protip\]', _protip_repl, html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'\[note\](.*?)\[/note\]', _note_repl, html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<div[^>]*class="[^"]*ai-protip[^"]*"[^>]*>(.*?)</div>', _protip_repl, html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<div[^>]*class="[^"]*ai-note[^"]*"[^>]*>(.*?)</div>', _note_repl, html, flags=re.DOTALL|re.IGNORECASE)
    images = list(post.images.filter(is_active=True).order_by('order'))
    if not html:
        return ""
    parts = re.split(r'(<h[1-3][^>]*>.*?</h[1-3]>|<p[^>]*>.*?</p>)', html, flags=re.IGNORECASE|re.DOTALL)
    out = []
    img_idx = 0
    para_count = 0
    for part in parts:
        if not part:
            continue
        is_para = re.match(r'<p[^>]*>(.*?)</p>', part, flags=re.IGNORECASE|re.DOTALL)
        is_head = re.match(r'<h[1-3][^>]*>(.*?)</h[1-3]>', part, flags=re.IGNORECASE|re.DOTALL)
        if is_para or is_head:
            out.append(part)
            if is_para:
                para_count += 1
            if (is_head or para_count % 2 == 0) and img_idx < len(images):
                img = images[img_idx]
                caption_html = f'<figcaption class="text-sm text-gray-500 mt-1 text-center">{img.caption}</figcaption>' if img.caption else ''
                out.append(f'<figure class="my-4 max-w-sm mx-auto faq-figure"><img src="{img.image.url}" data-index="{img_idx}" loading="lazy" class="faq-content-img w-full h-48 object-contain rounded-lg cursor-zoom-in" alt="{img.caption or post.title}"/>{caption_html}</figure>')
                img_idx += 1
        else:
            out.append(part)
    while img_idx < len(images):
        img = images[img_idx]
        caption_html = f'<figcaption class="text-sm text-gray-500 mt-1 text-center">{img.caption}</figcaption>' if img.caption else ''
        out.append(f'<figure class="my-4 max-w-sm mx-auto faq-figure"><img src="{img.image.url}" data-index="{img_idx}" loading="lazy" class="faq-content-img w-full h-48 object-contain rounded-lg cursor-zoom-in" alt="{img.caption or post.title}"/>{caption_html}</figure>')
        img_idx += 1
    return mark_safe(''.join(out))
