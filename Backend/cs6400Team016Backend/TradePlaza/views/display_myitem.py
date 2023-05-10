from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper
@csrf_exempt
@require_http_methods(['GET'])

def display_myitem(request, email):

    try:
        sqlQuery = "SELECT fk_email, Item.itemNumber, title, condition, (CASE WHEN LEN(description) > 100 THEN CONCAT(LEFT(description, 100), '...') ELSE COALESCE(description, '') END) AS description,(CASE WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame AS B WHERE B.fk_itemNumber = Item.itemNumber) THEN 'BoardGame' WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame AS Col WHERE Col.fk_itemNumber = Item.itemNumber) THEN 'CollectiveCardGame'WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame AS Com WHERE Com.fk_itemNumber = Item.itemNumber) THEN 'ComputerGame'WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame AS V WHERE V.fk_itemNumber = Item.itemNumber) THEN 'VideoGame'WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame AS P WHERE P.fk_itemNumber = Item.itemNumber) THEN 'PlayingCardGame'END) AS game_type FROM Item WHERE fk_email = %s AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s ))ORDER BY itemNumber ASC"
        data = [email, '%Pending%', '%Accepted%']
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
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)