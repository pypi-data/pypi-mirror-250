from django.db import models
from taggit.models import Tag


class TypedTag(models.Model):
    tag = models.OneToOneField(Tag, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True

    def __str__(self):
        return self.tag.name


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model

    From https://code.djangoproject.com/wiki/DynamicModels
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    return model


def make_typed_tag_tagged_model(name, type_tag_model, content_model, app_label):
    fields = {
        'typed_tag': models.ForeignKey(type_tag_model, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE, ),
        'content_object': models.ForeignKey(content_model, on_delete=models.CASCADE),
    }
    return create_model(
        name,
        fields=fields,
        app_label=app_label,
        options={'unique_together': ['typed_tag', 'content_object']}
    )
