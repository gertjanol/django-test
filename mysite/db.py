from django.conf import settings


class SplitDatabaseRouter(object):
    """
    DB router that will use a different database for each specified app. A mapping is
    defined in the dbmap-dict.
    """
    dbmap = settings.DATABASE_MAP_FOR_SPLIT_ROUTER

    def db_for_read(self, model, **hints):
        app_name = model._meta.app_label
        if app_name in self.dbmap:
            return self.dbmap[app_name]
        return None

    db_for_write = db_for_read

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.dbmap:
            return db == self.dbmap[app_label]
        if db in self.dbmap.values():
            return False
        return None
