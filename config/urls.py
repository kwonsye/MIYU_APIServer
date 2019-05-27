from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings
from miyu_app import views
from miyu_app.views import Emotion, UploadFile

schema_view = get_schema_view(
   openapi.Info(
      title="MIYU API",
      default_version='v1',
      description=
      """MIYU 졸업 프로젝트 API 문서 `GitHub repository` : <a href="https://github.com/kwonsye/MIYU_APIServer">https://github.com/kwonsye/MIYU_APIServer</a>
   `swagger-ui`로 보기 : <a href="/swagger">/swagger</a>  
   `ReDoc`로 보기 : <a href="/redoc">/redoc</a>  
   """
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def root_redirect(request):
    return redirect('swagger/', permanent=True)


urlpatterns = [
    path('', root_redirect), # go to swagger-doc
    path('admin/', admin.site.urls), # admin 페이지
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # redoc

    path('emotion/', UploadFile.as_view()), # upload file here
    path('emotion/<int:pk>/', Emotion.as_view(), name='get_emotion') # extract emotion here / pk는 db에 저장된 파일의 pk
]

# 개발 서버에서의 media 파일 저장을 위해 지정
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

