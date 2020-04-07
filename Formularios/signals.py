from django.db.models.signals import post_delete
from django.dispatch import receiver
from google.cloud import storage
from .models import Evidencia
from nefrovida.settings import BUCKET


@receiver(post_delete, sender=Evidencia)
def remove_file_after_delete(sender, instance, using, **kwargs):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    blob = bucket.blob(instance.urn)
    if blob.exists():
        blob.delete()
