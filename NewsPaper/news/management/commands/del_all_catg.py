from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'deleting all news/articles of the selected category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Are you sure you want to delete the category article {options["category"]}? y/n')

        if answer != 'y':

            self.stdout.write(self.style.ERROR('Canceled'))
            return
        try:
            category = Category.objects.get(category_name=options['category'])

            Post.objects.filter(category=category).delete()

            self.stdout.write((self.style.SUCCESS(f'Succesfully deleted all news from category {category.category_name}')))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Could not find category"))
