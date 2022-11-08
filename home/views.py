from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Sendmoney
from .models import Registration
from .serializers   import *
from django.http import Http404 #to treat not found 
from rest_framework.views import APIView #Apiview class
from rest_framework.response import Response #response
from rest_framework import status #status code
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class LoginApi(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'userID': user.pk,
            'email': user.email,
            'first_name':user.first_name,
            'last_name':user.last_name

        })
class LoanApi(APIView):
##to access this loanAPiwe did before , user must logged in
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        loan = Loan.objects.all()
        serializer = LoanSerializer(loan, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanApiDetail(APIView):
    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan = self.get_object(pk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def sendmoney(request):
    if request.method == 'GET':
        sendnow = Sendmoney.objects.all()
        serializer = SendmoneySerializer(sendnow, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SendmoneySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

        
@csrf_exempt
def sendoneyDetail(request, pk):
    try:
        onesend= Sendmoney.objects.get(id=pk)
    except Sendmoney.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SendmoneySerializer(onesend)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer =SendmoneySerializer(onesend, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        delete =Sendmoney.objects.get(id=pk).delete()
        return JsonResponse({'message':'Data has been deleted'},status=490)

def Regist(request):
    if request.method == 'GET':
        getregistration = Registration.objects.all()
        serreg = RegistrationSerializers(getregistration, many=True)
        return JsonResponse(serreg.data, safe=False)