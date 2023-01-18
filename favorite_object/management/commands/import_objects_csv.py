import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import FavoriteObject


class Command(BaseCommand):
    """
    Create favorite objects from CSV file
    """

    help = "Import objects CSV file and create FavoriteObject instances"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file_path",
            type=str,
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "fav_objects.csv"),
        )

    def handle(self, *args, **options):
        csv_file_path = options.get("csv_file_path", None)
        if csv_file_path and csv_file_path.endswith(".csv"):
            with open(csv_file_path, newline="") as csvfile:
                reader = csv.reader(csvfile)
                # skip the headers:
                next(reader, None)

                fav_objects = [
                    FavoriteObject(
                        name=row[0],
                        img_url=row[1],
                        description=row[2],
                    )
                    for row in reader
                ]

                FavoriteObject.objects.bulk_create(
                    fav_objects,
                    batch_size=100,
                    # ignore_conflicts=True,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Nb of favorite objects imported to the database: "
                        f"{len(fav_objects)}."
                    )
                )
        else:
            self.stderr.write(self.style.ERROR("This is not a CSV file."))
