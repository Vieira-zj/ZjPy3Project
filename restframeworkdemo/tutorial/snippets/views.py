from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

# Fix: {"code":["This field is required."]}

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
