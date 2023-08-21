from django.http import JsonResponse

def api_test(request, *args, **kwargs):
    return JsonResponse({"result": "Henlo"})