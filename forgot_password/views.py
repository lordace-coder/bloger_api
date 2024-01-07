from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token

UserModel = get_user_model()




class GenerateTokenApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,*args, **kwargs):

            Token.clear_expired_tokens()
            try:
                user = UserModel.objects.get(email=self.kwargs.get('email'))
                token =Token.objects.create(user = user)
                token.save()
                return Response(status=201)
            except Exception as err:
                return Response(status=404,data={"error":f"{err}"})

            

    
    
    def post(self,*args, **kwargs):
        data = self.request.data
        # data should contain the token and the new password
        if data.get('token') and data.get('new_password'):
            try:
                user = UserModel.objects.get(email=self.kwargs.get('email'))
            except:
                return Response({'error':'matching user does not exist'},404)
            is_valid = Token.validate_user_token(user=user,token=data.get('token'))
            if is_valid and data.get('new_password'):
                # change users password
                user.set_password(data.get('new_password'))
                user.save()
                return Response(status=200,data={'success':"token updated"})
            else:
                return Response(status = 400,data={'error':"Token invalid or expired"})
        return Response({"error":"invalid post data"},404)