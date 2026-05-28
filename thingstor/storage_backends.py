from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class SupabaseStorage(S3Boto3Storage):
    def url(self, name):
        url = super().url(name)
        project_id = settings.SUPABASE_PROJECT_ID
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        path = name
        return f'https://{project_id}.supabase.co/storage/v1/object/public/{bucket}/{path}'
