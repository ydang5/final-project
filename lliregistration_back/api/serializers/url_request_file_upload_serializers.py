from django.db import transaction
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from foundation.models import LLIStudentMasterSheetUpload

from django.core.files.base import ContentFile
import base64
import six
import uuid
def get_content_file_from_base64_string(data, filename):
    """
    Function will convert the string and filename parameter and return a
    `ContentFile` object.

    Special thanks:
    (1) https://github.com/tomchristie/django-rest-framework/pull/1268
    (2) https://stackoverflow.com/a/39587386
    """
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            print("Failed conversion.")
            return None

        # Convert it to the content file.
        data = ContentFile(decoded_file, name=filename)
    return data

class LLIStudentMasterSheetUploadSerializer(serializers.Serializer):
    attached_file_name = serializers.CharField(write_only=True, allow_null=False,)
    attached_file = serializers.CharField(write_only=True, allow_null=False,)
    title = serializers.CharField(required=False, allow_null=True,)
    description = serializers.CharField(required=False, allow_null=True,)

    @transaction.atomic
    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """

        # Extract our upload file data
        content = validated_data.get('attached_file')
        filename = validated_data.get('attached_file_name')

        # Convert the base64 data into a `ContentFile` object.
        content_file = get_content_file_from_base64_string(content, filename)

        # Create our file.
        private_file = LLIStudentMasterSheetUpload.objects.create(
            title = validated_data.get('title'),
            description = validated_data.get('description'),
            data_file = content_file, # When you attack a `ContentFile`, Django handles all file uploading.
        )

        # Return our validated data.
        return private_file
