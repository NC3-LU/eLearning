from django.contrib.staticfiles.finders import FileSystemFinder


class LegacyLeadingSlashFileSystemFinder(FileSystemFinder):
    """Support legacy static asset names that start with a slash."""

    def find(self, path, find_all=False):
        return super().find(path.lstrip("/"), find_all=find_all)
