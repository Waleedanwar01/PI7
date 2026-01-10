import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import QuickFAQ

faqs = [
    {
        "question": "How do I compare car insurance quotes?",
        "answer": "Comparing quotes is easy! Just enter your zip code, answer a few questions about your vehicle and driving history, and we'll show you rates from top providers side-by-side."
    },
    {
        "question": "Is this service free to use?",
        "answer": "Yes, AutoInsurance.com is 100% free to use. We don't charge any fees for comparing quotes. Our service is supported by the insurance providers we partner with."
    },
    {
        "question": "Will checking rates affect my credit score?",
        "answer": "Most insurance quotes use a 'soft pull' of your credit history, which does not affect your credit score. You will be notified if a hard inquiry is required before you purchase a policy."
    },
    {
        "question": "Can I switch insurance companies before my policy ends?",
        "answer": "Yes, you can switch at any time. If you paid in full, your previous insurer will refund the unused portion of your premium."
    }
]

for i, data in enumerate(faqs):
    obj, created = QuickFAQ.objects.get_or_create(
        question=data['question'],
        defaults={
            'answer': data['answer'],
            'order': i,
            'is_active': True
        }
    )
    if created:
        print(f"Created FAQ: {data['question']}")
    else:
        print(f"FAQ already exists: {data['question']}")

print("Seeded QuickFAQs")
