import requests
import json
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serilaizers import PersonSerializer, UserSerializer, UserSerializer, GroupSerializer
from .models import Personal
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework import permissions, routers, serializers, viewsets
from django.contrib.auth.models import User, Group

@api_view(['GET'])
def home(request):
    random_joke = requests.get("https://official-joke-api.appspot.com/jokes/random")
    adviceslip = requests.get("https://api.adviceslip.com/advice")
    chucknorris = requests.get("https://api.chucknorris.io/jokes/random")
    woof = requests.get("https://random.dog/woof.json")
    catfact = requests.get("https://catfact.ninja/fact")
    randomuser = requests.get("https://randomuser.me/api/")
    quotable = requests.get("https://api.quotable.io/random")
    jokeapi = requests.get("https://v2.jokeapi.dev/joke/Any")
    data = {"random_joke": json.loads(random_joke.content),
            "adviceslip": json.loads(adviceslip.content),
            "chucknorris":  json.loads(chucknorris.content),
            "woof":  json.loads(woof.content),
            "catfact":  json.loads(catfact.content),
            "randomuser":  json.loads(randomuser.content),
            "quotable":  json.loads(quotable.content),
            "jokeapi":  json.loads(jokeapi.content)
    }
    return Response({"data": data})

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class Register(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        token = Token.objects.get_or_create(user=user)
        return Response({"message": f"{serializer.data['username']} is created succesyflly", "token": token[0].pk},
                        status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def index(request):
    if request.method == "GET":
        data = User.objects.all()
        serilaizer = UserSerializer(data, many=True)
        return Response(serilaizer.data)
    elif request.method == "POST":
        return Response({"data": "This is a post method"})
    elif request.method == "DELETE":
        return Response({"data": "This is a delete method"})
    elif request.method == "PATCH":
        return Response({"data": "This is a PATCH method"})


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def person(request):
    if request.method == "GET":
        obj = Personal.objects.filter(color__isnull=False)
        serializer = PersonSerializer(obj, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PUT":
        obj = Personal.objects.get(id=request.data.get("id"))
        serializer = PersonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error_messages)

    elif request.method == "PATCH":
        obj = Personal.objects.get(id=request.data.get('id'))
        serializer = PersonSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error_messages)

    elif request.method == "DELETE":
        obj = Personal.objects.get(id=request.data.get('id'))
        obj.delete()
        return Response({"Message": f"{obj.name} is deleted"})


class PersonalViewClassBased(APIView):
    def get(self, request):
        obj = Personal.objects.filter(color__isnull = False)
        serializer = PersonSerializer(obj, many= True)
        return Response(serializer.data)
    def post(self, request):
        return Response({"data": "This is class based post method"})



class PersonalGenericView(mixins.ListModelMixin, generics.GenericAPIView ):
    queryset = Personal.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PersonalView(generics.ListCreateAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonSerializer
