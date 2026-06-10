from .models import Tag

def get_create_tag(tag):
    
    Tag.objects.get_or_create(name=tag)