from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from member.models import McccDir


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Serializers define the API representation.
class McccDirSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = McccDir
        fields = ('last_nm','first_nm','chinese_nm','wf_first','wf_chinese_nm','home_phone', 'cell_phone','address', 'worship')

# ViewSets define the view behavior.
class McccDirViewSet(viewsets.ModelViewSet):
    queryset = McccDir.objects.all()
    serializer_class = McccDirSerializer



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/members', McccDirViewSet)
