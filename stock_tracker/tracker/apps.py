from django.apps import AppConfig
import sys
import os
from django.conf import settings


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        if not getattr(settings, 'SCHEDULER_AUTOSTART', True):
            return

        # 開發環境：只在主進程中運行
        if 'runserver' in sys.argv:
            if os.environ.get('RUN_MAIN') == 'true':
                from . import scheduler
                scheduler.start()
        # 生產環境：直接運行
        elif not any(arg in sys.argv for arg in ['makemigrations', 'migrate', 'collectstatic']):
            from . import scheduler
            scheduler.start()
