import pytest
from django.core.management import call_command

from favorite_object.models import FavoriteObject

@pytest.mark.django_db
def test_import_favorite_objects_csv_file(capsys) -> None:
    """Test import favorite objects CSV file"""
    
    call_command("import_objects_csv")
    assert FavoriteObject.objects.count() == 344

    expected = "Nb of favorite objects imported to the database: 344.\n"
    assert expected == capsys.readouterr().out