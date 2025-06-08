from rest_framework.response import Response

def custom_response(data=None, status=200, message=""):
    return Response({"status": status,"message": message,"data": data}, status=status)

