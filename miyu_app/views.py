from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from miyu_app import serializers
from miyu_app.models import EmotionWavFile
from miyu_app.serializers import FileUploadSerializer, EmotionResultSerializer
from miyu_app.extract_emotion_from_voice import extract_emotion

# TODO:
#  - 개인 맞춤 모델 돌리는 코드 짜기
#  - 모델 예외 처리 error status code 내려주기
#  - 디비 설계 -> RDS


# extract emotion from wav file
# emotion/{pk}
class Emotion(APIView):

    @csrf_exempt
    @swagger_auto_schema(
        operation_id="emotion_result",
        operation_description="id값을 pk로 갖는 wav파일의 emotion 받아오기",
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="uploaded wav file's primary key(id)",
                required=True
            ),
        ],
        responses={
            200 :EmotionResultSerializer,
        }
    )
    def get(self,request,pk):
        file = EmotionWavFile.objects.get(id = pk)
        print("파일명 :", str(file.uploaded_file))
        emotion = extract_emotion(str(file.uploaded_file))
        serializer = EmotionResultSerializer({'result' : emotion})

        return Response(serializer.data)

# file upload
# emotion/
class UploadFile(APIView):
    """사용자 음성 wav 파일 업로드 api"""
    parser_classes = (MultiPartParser, FormParser,)

    @csrf_exempt
    @swagger_auto_schema(
        operation_id="upload_wavfile",
        operation_description="this is redirect to /emotion/{id}",
        request_body=serializers.FileUploadSerializer
    )
    def post(self, request):

        if request.FILES['uploaded_file'] :
            print("there is uploaded file")
            serializer = FileUploadSerializer(data=request.data)
            #uploaded_file = request.FILES['uploaded_file']

            if serializer.is_valid():
                print("db에 저장됨")
                recent_file = serializer.save()
                print("save()후 리턴하는 것 :", recent_file) # file이름
                print("recent_file.id : ", recent_file.id) # 저장된 file의 pk값

        return redirect('get_emotion', pk=recent_file.id)
    '''
    #this is for test
    @csrf_exempt
    def get(self, request, format = None):
        print("Upload view로 GET요청 받음")
        return render(request, 'upload_page.html')
    '''
