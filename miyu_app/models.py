from django.contrib.auth.models import User
from django.db import models

class EmotionWavFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="you don't have to send this property") # wav 파일 업로드 일시
    #owner = models.ForeignKey(User, to_field='id') # 파일 소유주
    uploaded_file = models.FileField(help_text="post user's wav file here!") # settings.MEDIA_ROOT 내 저장된 하위 경로를 저장
    #emotion = models.CharField() # 나중에 유추한 사용자의 감정과 실제 일치 여부를 확인할 필드

    def __str__(self):
        return str(self.uploaded_file)