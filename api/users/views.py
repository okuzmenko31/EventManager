from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import RegistrationSerializer
from .permissions import IsNotAuthenticated


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]
