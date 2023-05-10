from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from . import db_helper

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    try:
        body = json.loads(request.body)
        print(body)
        email = body['email']
        nickname = body['nickname']
        first_name = body['first_name']
        last_name = body['last_name']
        password = body['password']
        postal_code = body['postal_code']

        with connection.cursor() as cursor:
            sqlQuery = "SELECT email from [User] WHERE [User].email=%s;"
            data = [email]
            print(email)
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)
            print(rows)
            if rows:
                print(rows)
                connection.cursor().close()
                connection.close()
                response = {
                    'statusCode': '200',
                    'data': "User email already exists."
                }
                return JsonResponse(response)
            
            sqlQuery = "SELECT nickname from [User] WHERE [User].nickname=%s;"
            data = [nickname]
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)
            print(rows)
            if rows:
                connection.cursor().close()
                connection.close()
                response = {
                    'statusCode': '200',
                    'data': "User nickname already exists."
                }
                return JsonResponse(response)

            sqlQuery = "SELECT postal_code from [GlobalPostCode] WHERE [GlobalPostCode].postal_code=%s;"
            data = [postal_code]
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)
            print(rows)

            if not rows:
                connection.cursor().close()
                connection.close()
                response = {
                    'statusCode': '200',
                    'data': "Invalid postal code."
                }
                return JsonResponse(response)

            sqlQuery = """
                INSERT INTO [User](email, nickname, first_name, last_name, password, fk_postal_code)
	            VALUES (%s, %s, %s, %s,%s, %s);
            """
            data = [email, nickname, first_name, last_name, password, postal_code]
            cursor.execute(sqlQuery, data)
        
        connection.cursor().close()
        connection.close()
        response = {
            'statusCode': '200',
            'data': "completed."
        }
        return JsonResponse(response)
    except Exception:
        print('Error: 500 Internal error!')
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)