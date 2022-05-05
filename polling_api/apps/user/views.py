"""Views."""

from rest_framework.generics import ListCreateAPIView

from .models import User
from .serializers import UserSimpleSerializer


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
