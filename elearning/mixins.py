from .widgets import TranslatedNameWidget


class TranslationImportMixin:
    def after_save_instance(self, instance, using_transactions, dry_run):
        fields = instance._parler_meta.get_all_fields()
        defaults = {}
        for field in fields:
            field_value = getattr(instance, field)
            defaults[field] = field_value
        instance.translations.update_or_create(
            master_id=instance.id,
            language_code=instance.language_code,
            defaults=defaults,
        )

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        if isinstance(field.widget, TranslatedNameWidget) and not data[field.attribute]:
            return

        return super().import_field(field, obj, data, is_m2m, **kwargs)
