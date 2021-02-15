from django.utils.text import slugify
from random import randint

import string
import random

import re

def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '_', s)
    return s

def mixed_slug_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return str(''.join(random.choice(chars) for _ in range(size))).lower()

def random_string_generator(n=6):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    r = randint(range_start, range_end)
    return str(r)

def category_slug_generator(instance):
    new_slug = mixed_slug_generator(size=10)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return category_slug_generator(instance)
    slug = new_slug.strip()
    slug = urlify(slug)
    return slug

def item_slug_generator(instance):
    new_slug = mixed_slug_generator(size=10)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return item_slug_generator(instance)
    slug = new_slug.strip()
    slug = urlify(slug)
    return slug
