from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from word.validation import is_valid_email, clean_and_verify_url


class MainViewset(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @decorators.action(methods=["post"], detail=False)
    def arr_to_sorted_string(self, request, *args, **kwargs):
        try:
            data = request.data.get("data")
            if not data or data == "":
                return Response({"error": "Missing 'data' field."}, status=status.HTTP_400_BAD_REQUEST)
            
            arr = sorted(data.lower())
            return Response({"word": arr}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    @decorators.action(methods=["post"], detail=False)
    def validation(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            url = request.data.get("url")
            if not email or email == "" and not url or url == "":
                return Response({"error": "Missing 'data' field."}, status=status.HTTP_400_BAD_REQUEST)
            clean_email = is_valid_email(email=email)
            clean_url = clean_and_verify_url(url=url)
            if clean_email and clean_url:
                data = {
                    "message": "Success",
                    "data": {
                        "email": clean_email,
                        "url": clean_url
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK)
            return Response({"error": "Incorrect 'data' field."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    