from django.core.management.base import BaseCommand
from core.models import ZipRange

class Command(BaseCommand):
    help = 'Seeds ZipRange with US States and their zip ranges'

    def handle(self, *args, **kwargs):
        state_ranges = {
            'AL': [(35000, 36999)],
            'AK': [(99500, 99999)],
            'AZ': [(85000, 86999)],
            'AR': [(71600, 72999)],
            'CA': [(90000, 96199)],
            'CO': [(80000, 81699)],
            'CT': [(6000, 6999)],
            'DE': [(19700, 19999)],
            'DC': [(20000, 20599)],
            'FL': [(32000, 34999)],
            'GA': [(30000, 31999)],
            'HI': [(96700, 96899)],
            'ID': [(83200, 83899)],
            'IL': [(60000, 62999)],
            'IN': [(46000, 47999)],
            'IA': [(50000, 52999)],
            'KS': [(66000, 67999)],
            'KY': [(40000, 42799)],
            'LA': [(70000, 71499)],
            'ME': [(3900, 4999)],
            'MD': [(20600, 21999)],
            'MA': [(1000, 2799)],
            'MI': [(48000, 49999)],
            'MN': [(55000, 56799)],
            'MS': [(38600, 39799)],
            'MO': [(63000, 65899)],
            'MT': [(59000, 59999)],
            'NE': [(68000, 69399)],
            'NV': [(88900, 89899)],
            'NH': [(3000, 3899)],
            'NJ': [(7000, 8999)],
            'NM': [(87000, 88499)],
            'NY': [(10000, 14999)],
            'NC': [(27000, 28999)],
            'ND': [(58000, 58899)],
            'OH': [(43000, 45999)],
            'OK': [(73000, 74999)],
            'OR': [(97000, 97999)],
            'PA': [(15000, 19699)],
            'RI': [(2800, 2999)],
            'SC': [(29000, 29999)],
            'SD': [(57000, 57799)],
            'TN': [(37000, 38599)],
            'TX': [(75000, 79999)],
            'UT': [(84000, 84799)],
            'VT': [(5000, 5999)],
            'VA': [(22000, 24699)],
            'WA': [(98000, 99499)],
            'WV': [(24700, 26999)],
            'WI': [(53000, 54999)],
            'WY': [(82000, 83199)]
        }

        # Clear existing state ranges to avoid duplicates
        # ZipRange.objects.filter(state__isnull=False).delete()
        # Actually, let's just update_or_create to preserve any existing company relations if possible,
        # but matching on state alone might be tricky if user modified ranges.
        # User said "already show hon" -> implies clean start or standard set.
        # Let's check if they exist first.
        
        count = 0
        for state, ranges in state_ranges.items():
            for start, end in ranges:
                obj, created = ZipRange.objects.get_or_create(
                    state=state,
                    defaults={
                        'start_zip': start,
                        'end_zip': end
                    }
                )
                if not created:
                    # Update range just in case, but keep companies
                    obj.start_zip = start
                    obj.end_zip = end
                    obj.save()
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} state zip ranges'))
