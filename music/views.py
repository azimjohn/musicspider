from rest_framework.generics import ListAPIView,  RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Song
from .serializers import SongSerializer


class SongsListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SongSerializer
    search_fields = ("name", "artist")
    queryset = Song.objects.all()

class SongsDetailAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Song.objects.all()
    serializer_class = SongSerializer
