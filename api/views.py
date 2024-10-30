from django.shortcuts import render,redirect
# from rest_framework import generics
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from allauth.account.views import SignupView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

# class LoginView(generics.GenericAPIView):
#     serializer_class = UserSerializer

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(generics.GenericAPIView):
#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


def IndexPage(request):
    return render(request,'index.html')


class CustomSignupView(SignupView):
    def form_valid(self, form):
        user=form.save(self.request)
        Token.objects.get_or_create(user=user)
        return super().form_valid(form)
    

class DeleteAccountView(APIView):

    def get(self,request,username,*args, **kwargs):
        try:
            user=User.objects.get(username=username)
            user_data={
                'username':user.username,
                'email':user.email,
                'password':user.password,
                'date_joined':user.date_joined,
            }
            return Response(user_data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error':"Username not found"},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,username,*args, **kwargs):
        b=User.objects.filter(username=username)
        if b.exists():
            a=User.objects.get(username=username)
            a.delete()
            return Response({'detail': "User account deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Foydalanuvchi topilmadi"},status=status.HTTP_404_NOT_FOUND)
        

class UserSignUp1(APIView):
    def get(self,requests):
        users=User.objects.all().values('id','username',"email")
        return Response({'users':list(users)},status=status.HTTP_200_OK)
    

    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        password1=request.data.get('password1')
        password2=request.data.get('password2')

        if not username or not email or not password1 or not password2:
            return Response({'error':'All fields are required'},status=status.HTTP_400_BAD_REQUEST)
        if password1 !=password2:
            return Response({"error":'Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error":"Username already exists"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error":'Email already exists'},status=status.HTTP_400_BAD_REQUEST)
        

        new_user=User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        return Response({"user":model_to_dict(new_user,fields=['id','username','email'])},status=status.HTTP_201_CREATED)
    

def register(request):
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form=CustomUserCreationForm()
    return render(request,'register.html',{'form':form})



