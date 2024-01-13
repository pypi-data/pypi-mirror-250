Django Query View
=================

Django view for querying data

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-query-view

Usage
-----

Set up models
-------------

.. code-block:: python

    from django.db import models
    from taggit.managers import TaggableManager
    from taggit.models import TaggedItemBase
    from query_view.models import TypedTag
    from query_view.models import make_typed_tag_tagged_model

    class TaggedThing(TaggedItemBase):
        content_object = models.ForeignKey('Thing', on_delete=models.CASCADE)


    class Thing(models.Model):
        name = models.CharField(max_length=200)
        is_good = models.BooleanField()

        tags = TaggableManager(through=TaggedThing, blank=True)

        def __str__(self):
            return self.name

    # Subclass TypedTag
    class ActorTypedTag(TypedTag):
        pass

    # Create your tagged model like this
    ActorTaggedThing = make_typed_tag_tagged_model('ActorTaggedThing', ActorTypedTag, Thing, app_label='testproject')

    # Or like this
    class ActorTaggedThing(TaggedItemBase):
        typed_tag = models.ForeignKey(
            ActorTypedTag,
            related_name="%(app_label)s_%(class)s_items",
            on_delete=models.CASCADE,
        )
        content_object = models.ForeignKey(Thing, on_delete=models.CASCADE)

        class Meta:
            unique_together = ['typed_tag', 'content_object']

Create a typed tagged item
-----------------------------

.. code-block:: python

    t = Tag.objects.get(name='clint eastwood')
    ActorTaggedThing.objects.create(content_object=thing, typed_tag=t.actortypedtag)

Run the test project
--------------------

.. code-block:: bash

    python manage.py migrate
    python manage.py loaddata testproject/fixtures/tag_thing.json
    python manage.py runserver

Dump fixture
------------

.. code-block:: bash

    python manage.py dumpdata --indent 4 testproject.Thing testproject.TaggedThing taggit.Tag testproject.LanguageTypedTag testproject.LanguageTaggedThing testproject.DirectorTypedTag testproject.DirectorTaggedThing testproject.ActorTypedTag testproject.ActorTaggedThing --output testproject/fixtures/tag_thing.json
