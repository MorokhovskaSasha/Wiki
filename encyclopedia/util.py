import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File


def list_entries():
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    
    filename = f"entries/{title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        file = File(f)
        file.write(content)
    
def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None