import os

from PIL import Image
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics, views, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from classroom.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from courses.serializer import ClassroomSerializer, UserSerializer, AddUserSerializer, AvatarSerializer
from courses.models import Classroom, Avatar


class ClassroomList(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def perform_create(self, serializer):
        error_text = "You don't have permission to create a new classroom."
        account = self.request.user
        permission = account.is_staff or account.is_superuser
        if not permission: raise PermissionDenied(error_text)
        serializer.save()


class ClassroomDetail(generics.RetrieveUpdateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ClassroomUserDetail(generics.RetrieveDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        classroom, user_id = super().get_object(), self.kwargs.get('user_id')
        return generics.get_object_or_404(classroom.accounts, id=user_id)

    def delete(self, request, *args, **kwargs):
        classroom, user_id = super().get_object(), self.kwargs.get('user_id')
        classroom.accounts.remove(classroom.accounts.get(id=user_id))
        return Response(ClassroomSerializer(classroom).data, status.HTTP_200_OK)


class ClassroomAddUser(views.APIView):
    queryset = Classroom.objects.all()
    serializer_class = AddUserSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request, pk):
        classroom = Classroom.objects.get(pk=pk)
        user_id = request.data.get('user_id')
        classroom.accounts.add(user_id)
        code = status.HTTP_201_CREATED
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data, code)


class AvatarDetail(generics.RetrieveUpdateDestroyAPIView, views.APIView):
    queryset = Avatar.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AvatarSerializer

    def get_object(self):
        get_object = generics.get_object_or_404
        account_id = self.kwargs.get('pk')
        return get_object(Avatar, account__id=account_id)

    def save_image(self, image_path, account):
        image = Image.open(image_path)
        username = account.username
        new_path = image_path.split(os.sep)[-1]
        new_path = image_path.replace(new_path, '')
        new_path = f"{new_path}/{username}.png"
        image.save(new_path, "PNG")

    def post(self, request: Request, pk: int):
        account = generics.get_object_or_404(User, id=pk)
        avatar = request.FILES['image']
        avatar = Avatar(image=avatar, account=account)
        avatar.save()
        self.save_image(avatar.image.path, account)
        avatar.image = f'avatars/{account.username}.png'
        avatar.save()
        image = open(avatar.image.path, 'rb').read()
        return HttpResponse(image, content_type="image/jpeg")

    def get(self, request, *args, **kwargs):
        avatar = generics.get_object_or_404(Avatar, account__id=kwargs['pk'])
        image = open(avatar.image.path, 'rb').read()
        return HttpResponse(image, content_type="image/jpeg")
