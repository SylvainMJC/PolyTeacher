from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
import google.generativeai as genai
import os
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class AllTranslationViewSet(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('source_text', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="source_text"),
            openapi.Parameter('source_language', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="source_language"),
            openapi.Parameter('target_language', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="target_language"),
        ])
    def get(self, request):
        result = Translation.objects.all()
        source_text = request.GET.get('source_text') 
        source_language = request.GET.get('source_language') 
        target_language = request.GET.get('target_language') 
        result = result.filter(source_text=source_text)
        result = result.filter(source_language=source_language)
        result = result.filter(target_language=target_language)
        serialized_data = TranslationSerializer(result, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=TranslationSerializer,
        responses={
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        if request.GET.get('source_text') :
            source_text = request.GET.get("source_text", None)
        else:
            source_text = request.data.get("source_text", None)

        if request.GET.get('source_language') :
            source_language = request.GET.get("source_language", None)
        else:
            source_language = request.data.get("source_language", None)
            
        if request.GET.get('target_language') :
            target_language = request.GET.get("target_language", None)
        else:
            target_language = request.data.get("target_language", None)


        if not source_text or not source_language or not target_language:
            return Response(
                {"error": "source_text, source_language and target_language are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        if not api_key:
            return Response(
                {"error": "API key not configured properly."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f'Traduis "{source_text}" en {target_language}. La réponse ne doit contenir que la traduction.'
        response = model.generate_content(prompt)
        target_text = response.text.replace("\n", "")

        Translation.objects.create(source_language=source_language, target_language=target_language, source_text=source_text, target_text=target_text)
        return Response(data = {
            "Result": "Translation added",
            "Translation": target_text
        }, status = status.HTTP_201_CREATED)



