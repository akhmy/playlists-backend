from rest_framework.generics import RetrieveAPIView
from .models import User
from .serializers import UserSerializer


# Create your views here.
class UserRetrieveByUsernameView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
