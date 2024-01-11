"""
List backups.
"""

from django_sync_env.storage import get_storage
from django_sync_env.management.commands._base import BaseSyncBackupCommand, make_option, ROW_TEMPLATE
from django_sync_env import settings
import logging


class Command(BaseSyncBackupCommand):
    help = "Connect to configured storage endpoints to get a list of database backups"
    logger = logging.getLogger("sync_env")
    storages = []

    option_list = (
        make_option("-d", "--database", help="Filter by database name"),
        make_option(
            "-z",
            "--compressed",
            help="Exclude non-compressed",
            action="store_true",
            default=None,
            dest="compressed",
        ),
        make_option(
            "-Z",
            "--not-compressed",
            help="Exclude compressed",
            action="store_false",
            default=None,
            dest="compressed",
        ),
    )

    def handle(self, **options):
        self.quiet = options.get("quiet")
        self.logger.info("Connecting to configured storage endpoints to get a list of database backups")
        files_attr = []

        for env, config in settings.SYNC_ENV_ENVIRONMENTS.items():
            options.update({"content_type": "db"})
            storage = get_storage(env, config)
            files_attr += self.get_backups_attrs(storage, options, env)

        if not self.quiet:
            title = ROW_TEMPLATE.format(name="Name", environment="Environment", datetime="Datetime",
                                        content_type="Content Type")
            self.stdout.write(title)
        for file_attr in files_attr:
            row = ROW_TEMPLATE.format(**file_attr)
            self.stdout.write(row)
