from django.core.management.base import BaseCommand
from core.models import ReportStatus


class Command(BaseCommand):
    help = "Create report statuses"

    def handle(self, *args, **options):
        report_statuses = [
            {
                "status": "Pending",
                "description": "The report is awaiting initial action"
            },
            {
                "status": "Resolved",
                "description": "Both the reporter and moderator have confirmed the issue is resolved"
            },
            {
                "status": "Under Investigation",
                "description": "For reports that require further inquiry"
            },
            {
                "status": "Duplicate",
                "description": "If the report is a duplicate of an existing one"
            },
            {
                "status": "Rejected",
                "description": "If the report is deemed invalid"
            }
        ]

        for status in report_statuses:
            ReportStatus.objects.get_or_create(**status)
        print(f"{len(report_statuses)} statuses created")