from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class PersonPage(Page):
    first_name = models.CharField(
        max_length=255,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Last Name',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ], 'Person'),
        InlinePanel('addresses', label='Address'),
    ]

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'


@register_snippet
class Address(index.Indexed, ClusterableModel, Orderable):
    address = models.CharField(
        max_length=255,
        verbose_name='Address',
    )
    tags = ClusterTaggableManager(
        through='home.AddressTag',
        blank=True,
    )
    person = ParentalKey(
        to='home.PersonPage',
        related_name='addresses',
        verbose_name='Person'
    )

    panels = [
        PageChooserPanel('person'),
        FieldPanel('address'),
        FieldPanel('tags'),
    ]

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'


class AddressTag(TaggedItemBase):
    content_object = ParentalKey(
        to='home.Address',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )
