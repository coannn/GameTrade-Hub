from django.http import JsonResponse
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import db_helper
import json

# Create your views here.
@csrf_exempt
@require_http_methods(['GET'])
def getMyItemList(request):
    desiredItemNum = request.GET.get('desiredItemNum')
    email = request.GET.get('email')

    sqlQuery ='''
                WITH MyProposedItems AS ( SELECT itemNumber, title, condition FROM Item WHERE fk_email = %s
	            EXCEPT
	            ( SELECT itemNumber, title, condition FROM Item INNER JOIN Trade ON Item.itemNumber = Trade.proposedItemNum OR Item.itemNumber = Trade.desiredItemNum
	                WHERE Item.fk_email = %s AND (Trade.status LIKE %s OR Trade.status LIKE %s)
	                UNION
	                SELECT itemNumber, title, condition FROM Item INNER JOIN Trade ON Item.itemNumber = Trade.proposedItemNum
	                WHERE Trade.proposedItemNum = Item.itemNumber  AND Trade.desiredItemNum = %s AND Trade.status LIKE %s
	                )
                )
                SELECT MyProposedItems.*, (CASE
                WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame  WHERE fk_itemNumber = MyProposedItems.itemNumber) THEN 'BoardGame' 
                WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame WHERE fk_itemNumber = MyProposedItems.itemNumber) THEN 'CollectiveCardGame'
                WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame WHERE fk_itemNumber = MyProposedItems.itemNumber) THEN 'ComputerGame'
                WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame WHERE fk_itemNumber = MyProposedItems.itemNumber) THEN 'VideoGame'
                WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame WHERE fk_itemNumber = MyProposedItems.itemNumber) THEN 'PlayingCardGame'
                END) AS game_type
                From MyProposedItems
                ORDER BY MyProposedItems.itemNumber ASC;
            '''
    with connection.cursor() as cursor:
        data = [email, email, '%Accepted%', '%Pending%', desiredItemNum, '%Rejected%']
        cursor.execute(sqlQuery, data)
        rows = db_helper.dictfetchall(cursor)
        json_data = []
        for row in rows:
            json_data.append({"itemNumber": row['itemNumber'], "game_type" : row['game_type'], "title" : row['title'], "condition" : row['condition']})
    return JsonResponse(json_data, safe = False)


@csrf_exempt
@require_http_methods(['POST'])
def proposeTrade(request, desiredItemNum = 1, proposedItemNum = 2):
    #body = json.loads(request.body)
    #print(body)
    body = json.loads(request.body)
    print(body)
    desiredItemNum = body['desiredItemNum']
    proposedItemNum = body['proposedItemNum']
    
    sqlQuery ='''
                INSERT INTO Trade (proposedItemNum, desiredItemNum, proposedDate, decisionDate, status)
                VALUES (%s, %s, GETDATE(), NULL, 'Pending');
    
            '''
    try:
        with connection.cursor() as cursor:
            data = [proposedItemNum, desiredItemNum]
            print(data)
            cursor.execute(sqlQuery, data)

        response = {
            'statusCode' : '200',
            'data': 'You have successfully proposed a trade, please wait for the response from counterparty'
        }
        return JsonResponse(response)
    
    except Exception:
        context = {
            'statusCode' : '500',
            'Error': 'trade proposal failed'
        }
        return JsonResponse(context)