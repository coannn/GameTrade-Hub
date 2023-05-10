from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper

# Create your views here.
@csrf_exempt
@require_http_methods(['GET'])
def get_item(request, itemNum):
    try:
        print(itemNum)
        sqlQuery = "SELECT * FROM [Item] WHERE Item.itemNumber = %s"
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery, [itemNum])
            rows = db_helper.dictfetchall(cursor)
        
        context = {
            'statusCode': '200',
            'data': rows
        }
        return JsonResponse(context)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context)