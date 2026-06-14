from .models import Tag

def get_create_tag(tag):
    
    return Tag.objects.get_or_create(name=tag)