from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import  json
from . import db_helper

@csrf_exempt
@require_http_methods(['GET'])
def display_myitem_count(request, email):

    try:
        sqlQuery = "WITH A AS (SELECT itemNumber, (CASE WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame AS B WHERE B.fk_itemNumber = Item.itemNumber) THEN 'BoardGame'  WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame AS Col WHERE Col.fk_itemNumber = Item.itemNumber) THEN 'CollectiveCardGame' WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame AS Com WHERE Com.fk_itemNumber = Item.itemNumber) THEN 'ComputerGame' WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame AS V WHERE V.fk_itemNumber = Item.itemNumber) THEN 'VideoGame' WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame AS P WHERE P.fk_itemNumber = Item.itemNumber) THEN 'PlayingCardGame' END) AS game_type FROM Item WHERE fk_email = %s AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s))) SELECT 'BoardGame' as game_type, COUNT(itemNumber) AS count FROM A WHERE game_type = 'BoardGame' UNION SELECT 'CollectiveCardGame' as game_type, COUNT(itemNumber) AS count FROM A WHERE game_type = 'CollectiveCardGame' UNION SELECT 'ComputerGame' as game_type, COUNT(itemNumber) AS count FROM A WHERE game_type = 'ComputerGame' UNION SELECT 'PlayingCardGame' as game_type, COUNT(itemNumber) AS count FROM A WHERE game_type = 'PlayingCardGame' UNION  SELECT 'VideoGame' as game_type, COUNT(itemNumber) AS count FROM A WHERE game_type = 'VideoGame' UNION ALL SELECT 'Total', COUNT(*)  FROM A"
        data =[email, '%Pending%', '%Accepted%']
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)

        # re-form the dictionary
        data = {}
        for i in range(len(rows)):
            data[rows[i]['game_type']] = rows[i]['count']


        # data = []
        # for i in range(len(rows)):
        #     item = {rows[i]['game_type']: rows[i]['count']}
        #     data.append(item)
       
        
        # context = {
        #     'statusCode': '200',
        #     'count': data
        # }
        connection.cursor().close()
        connection.close()
        return JsonResponse(data)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)