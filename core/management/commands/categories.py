from django.core.management.base import BaseCommand
from core.models import Category


class Command(BaseCommand):
    help = "Create report categories"

    def handle(self, *args, **options):
        report_categories = [
            {
                "category": "Infrastructure",
                "description": "Issues related to public infrastructure"
            },
            {
                "category": "Corruption",
                "description": "Reports of corruption and abuse of power"
            },
            {
                "category": "Safety and Security",
                "description": "Issues related to personal safety and security"
            },
            {
                "category": "Environment",
                "description": "Environmental concerns and issues"
            },
            {
                "category": "Public Services",
                "description": "Issues related to public services"
            },
            {
                "category": "Governance",
                "description": "Issues related to governance and leadership"
            },
            {
                "category": "Human Rights",
                "description": "Human rights violations and discrimination"
            },
            {
                "category": "Housing",
                "description": "Issues related to housing and shelter"
            },
            {
                "category": "Agriculture",
                "description": "Agricultural challenges and concerns"
            },
            {
                "category": "Other",
                "description": "Issues not covered by other categories"
            }
        ]

        for category in report_categories:
            Category.objects.get_or_create(**category)
            
        print(f"{len(report_categories)} categories created")