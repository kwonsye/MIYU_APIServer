from rest_framework import serializers
from miyu_app.models import EmotionWavFile

class FileUploadSerializer(serializers.ModelSerializer):
    '''
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    '''
    class Meta:
        model = EmotionWavFile
        fields = ('created_at', 'uploaded_file')

class EmotionResultSerializer(serializers.Serializer):
    result = serializers.CharField(help_text="this is uploaded_file emotion result")