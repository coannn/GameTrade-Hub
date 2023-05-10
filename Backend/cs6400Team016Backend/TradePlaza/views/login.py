from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper

# Create your views here.
@csrf_exempt
@require_http_methods(['GET'])
def login(request, username):
    try:
        print(username)
        sqlQuery = "SELECT email, nickname, password FROM [User] Where email = %s or nickname = %s;"
        data = [username, username]
        print(sqlQuery)
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)

        connection.cursor().close()
        connection.close()
        context = {
            'statusCode': '200',
            'data': rows
        }
        return JsonResponse(context)
    except Exception:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)