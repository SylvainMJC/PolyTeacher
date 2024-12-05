from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
import google.generativeai as genai
import os

# Create your views here.

class FrenchSpanishTranslationViewSet(APIView):

    def get(self, request):
        result = Translation.objects.all()
        result = result.filter(source_language="FR")
        result = result.filter(target_language="ES")
        serialized_data = TranslationSerializer(result, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)
    
class FrenchEnglishTranslationViewSet(APIView):

    def get(self, request):
        result = Translation.objects.all()
        result = result.filter(source_language="EN")
        result = result.filter(target_language="FR")
        serialized_data = TranslationSerializer(result, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)

class AllTranslation(APIView):

    def get(self, request):
        result = Translation.objects.all()
        serialized_data = TranslationSerializer(result, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

class TranslateTextView(APIView):
    def get(self, request):
        try:
            source_text = request.GET.get('source_text') 
            source_language = request.GET.get('source_language') 
            target_language = request.GET.get('target_language') 
            if not source_text or not target_language:
                return Response(
                    {"error": "source_text and target_language are required."},
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
            return Response({"translation": response.text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def post(self, request):
        try:
            source_text = request.data.get("source_text", None)
            target_language = request.data.get("target_language", None)
            if not source_text or not target_language:
                return Response(
                    {"error": "source_text and target_language are required."},
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
            return Response({"translation": response.text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    return render(request, 'index.html', context={})


