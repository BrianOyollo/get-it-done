from django.core.management.base import BaseCommand
from core.models import Category, Subcategory


class Command(BaseCommand):
    help = "Create report subcategories"

    def handle(self, *args, **options):
        subcategories = [
            {
                "category": "Infrastructure",
                "subcategories": [
                    {"subcategory": "Roads and Transportation", "description": "Issues related to roads, traffic, and public transport"},
                    {"subcategory": "Water and Sanitation", "description": "Issues related to water supply, sanitation, and waste management"},
                    {"subcategory": "Energy and Utilities", "description": "Issues related to electricity, power, and other utilities"}
                ]
            },
            {
                "category": "Corruption",
                "subcategories": [
                    {"subcategory": "Bribery and Extortion", "description": "Reports of bribery and extortion by public officials"},
                    {"subcategory": "Embezzlement and Fraud", "description": "Reports of embezzlement, fraud, and misuse of public funds"},
                    {"subcategory": "Nepotism and Favoritism", "description": "Reports of nepotism, favoritism, and unfair practices"}
                ]
            },
            {
                "category": "Safety and Security",
                "subcategories": [
                    {"subcategory": "Crime and Violence", "description": "Reports of crime, violence, and insecurity"},
                    {"subcategory": "Traffic Accidents", "description": "Reports of traffic accidents and road safety issues"},
                    {"subcategory": "Emergency Services", "description": "Issues related to emergency services response"}
                ]
            },
            {
                "category": "Environment",
                "subcategories": [
                    {"subcategory": "Pollution", "description": "Reports of air, water, and noise pollution"},
                    {"subcategory": "Deforestation and Land Degradation", "description": "Issues related to deforestation and land degradation"},
                    {"subcategory": "Wildlife and Biodiversity", "description": "Issues related to wildlife conservation and biodiversity"}
                ]
            },
            {
                "category": "Public Services",
                "subcategories": [
                    {"subcategory": "Education", "description": "Issues related to education and schools"},
                    {"subcategory": "Healthcare", "description": "Issues related to healthcare and hospitals"},
                    {"subcategory": "Social Welfare", "description": "Issues related to social welfare and support services"}
                ]
            },
            {
                "category": "Governance",
                "subcategories": [
                    {"subcategory": "Leadership and Accountability", "description": "Issues related to leadership and accountability"},
                    {"subcategory": "Public Participation", "description": "Issues related to public participation and engagement"},
                    {"subcategory": "Rule of Law", "description": "Issues related to the rule of law and justice"}
                ]
            },
            {
                "category": "Human Rights",
                "subcategories": [
                    {"subcategory": "Discrimination and Inequality", "description": "Reports of discrimination and inequality"},
                    {"subcategory": "Freedom of Expression", "description": "Issues related to freedom of expression and speech"},
                    {"subcategory": "Violence and Abuse", "description": "Reports of violence, abuse, and human rights violations"}
                ]
            }
        ]

        for item in subcategories:
            category = Category.objects.get(category=item['category'])
            for subcategory in item['subcategories']:
                Subcategory.objects.get_or_create(category=category, **subcategory)

            print(f"{len(item['subcategories'])} subcategories created for category {item['category']}")