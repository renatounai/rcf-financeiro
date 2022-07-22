from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.before_save()
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)
        self.after_save()

    def delete(self, using=None, keep_parents=False):
        self.before_delete()
        try:
            return super().delete(using, keep_parents)
        finally:
            self.after_delete()

    def before_save(self):
        pass

    def after_save(self):
        pass

    def before_delete(self):
        pass

    def after_delete(self):
        pass

    class Meta:
        abstract = True
