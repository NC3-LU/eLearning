from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.exceptions import SuspiciousFileOperation
from django.test import SimpleTestCase, override_settings

from elearning.staticfiles import LegacyLeadingSlashFileSystemFinder


class LegacyLeadingSlashFileSystemFinderTest(SimpleTestCase):
    def test_finds_legacy_path_starting_with_slash(self):
        with TemporaryDirectory() as directory:
            asset = Path(directory, "media/images/icons/trophy-white.svg")
            asset.parent.mkdir(parents=True)
            asset.touch()

            with override_settings(STATICFILES_DIRS=[directory]):
                finder = LegacyLeadingSlashFileSystemFinder()

            self.assertEqual(
                finder.find(f"/{asset.relative_to(directory)}"), str(asset)
            )

    def test_does_not_allow_parent_directory_traversal(self):
        with TemporaryDirectory() as directory:
            with override_settings(STATICFILES_DIRS=[directory]):
                finder = LegacyLeadingSlashFileSystemFinder()

            with self.assertRaises(SuspiciousFileOperation):
                finder.find("../secret.txt")
