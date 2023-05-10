from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# from numpy import row_stack

from . import db_helper
@csrf_exempt
@require_http_methods(['GET'])


def display_user_detail(request):
    try:
        proposedItemNum = request.GET.get('proposedItemNum')
        desiredItemNum = request.GET.get('desiredItemNum')
        email = request.GET.get('email')
        sqlQuery="""
        WITH t1 AS (SELECT T.proposedItemNum, T.desiredItemNum, U1.email as proposer_email,  U1.fk_postal_code as proposer_postcode, U1.nickname as proposer_nickname, U1.first_name as proposer_firstname, U2.email as counterparty_email, U2.fk_postal_code as counterparty_postcode, U2.nickname as counterparty_nickname, U2.first_name as counterparty_firstname, decisionDate, status 
FROM Trade AS T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber 
INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber 
INNER JOIN [User] as U1 on I1.fk_email=U1.email 
INNER JOIN [User] as U2 on I2.fk_email = U2.email 
where T.proposedItemNum= %s AND T.desiredItemNum=%s)

SELECT 
(CASE WHEN t1.proposer_email = %s THEN counterparty_nickname
WHEN t1.counterparty_email = %s THEN proposer_nickname
END) AS nickname, ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2)  AS distance, 
(CASE WHEN t1.proposer_email = %s THEN counterparty_firstname
WHEN t1.counterparty_email = %s THEN proposer_firstname
END) AS first_name,
(CASE WHEN t1.proposer_email = %s THEN counterparty_email
WHEN t1.counterparty_email = %s THEN proposer_email
END) AS email
FROM t1 INNER JOIN GlobalPostCode AS G1 ON G1.postal_code = t1.proposer_postcode INNER JOIN GlobalPostCode AS G2 ON G2.postal_code=t1.counterparty_postcode;

        """
        data=[proposedItemNum,desiredItemNum,email,email,email,email,email,email]
        with connection.cursor() as cursor:
            print(data)
            cursor.execute(sqlQuery,data)
            rows = db_helper.dictfetchall(cursor)
        json_data = []
        for row in rows:
            json_data.append(row)
        context = {
            'statusCode': '200',
            'data': rows
        }
        return JsonResponse(json_data,safe=False)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context)

def display_proposedItem(request,proposedItemNum):
    try:
        #proposedItemNum = request.GET.get('proposedItemNum')
        #proposedItemNum = "9"
        sqlQuery="""
        SELECT Item.itemNumber AS itemNumber, title, condition, 
    (CASE WHEN LEN(description) > 100 THEN CONCAT(LEFT(description, 100), '...') 
    ELSE COALESCE(description, '') 
    END) AS description,
    (CASE WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame AS B WHERE B.fk_itemNumber = Item.itemNumber) THEN 'BoardGame' 
    WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame AS Col WHERE Col.fk_itemNumber = Item.itemNumber) THEN 'CollectiveCardGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame AS Com WHERE Com.fk_itemNumber = Item.itemNumber) THEN 'ComputerGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame AS V WHERE V.fk_itemNumber = Item.itemNumber) THEN 'VideoGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame AS P WHERE P.fk_itemNumber = Item.itemNumber) THEN 'PlayingCardGame'
    END) AS game_type
    FROM Item
    WHERE itemNumber = %s;

        """
        data=[proposedItemNum]
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery,data)
            rows = db_helper.dictfetchall(cursor)
            print(rows)
        if rows[0]['game_type']=="CollectiveCardGame":
            sqlQuery="""
            SELECT CollectiveCardGame.cardsOffered
            FROM Item INNER JOIN CollectiveCardGame ON Item.itemNumber = CollectiveCardGame.fk_itemNumber 
            WHERE Item.itemNumber = %s;
            """
            data=[proposedItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        if rows[0]['game_type']=="ComputerGame":
            sqlQuery="""
            SELECT ComputerGame.computerPlatform as platform
            FROM Item INNER JOIN ComputerGame ON Item.itemNumber = ComputerGame.fk_itemNumber 
            WHERE Item.itemNumber = %s;
            """
            data=[proposedItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        if rows[0]['game_type']=="VideoGame":
            sqlQuery="""
            SELECT VideoGame.media, VideoGamePlatform.platform FROM Item
            INNER JOIN VideoGame ON Item.itemNumber = VideoGame.fk_itemNumber INNER JOIN VideoGamePlatform ON Item.itemNumber = VideoGamePlatform.fk_VideoGame_itemNumber
            WHERE Item.itemNumber = %s;
            """
            data=[proposedItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        json_data = []
        for row in rows:
            json_data.append(row)
        context = {
            'statusCode': '200',
            'data': rows[0]
        }
        return JsonResponse(context)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context)

def display_desiredItem(request,desiredItemNum):
    try:
        #desiredItemNum = request.GET.get('desiredItemNum')
        #desiredItemNum = "8"
        sqlQuery="""
        SELECT Item.itemNumber AS itemNumber, title, condition, 
    (CASE WHEN LEN(description) > 100 THEN CONCAT(LEFT(description, 100), '...') 
    ELSE COALESCE(description, '') 
    END) AS description,
    (CASE WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame AS B WHERE B.fk_itemNumber = Item.itemNumber) THEN 'BoardGame' 
    WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame AS Col WHERE Col.fk_itemNumber = Item.itemNumber) THEN 'CollectiveCardGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame AS Com WHERE Com.fk_itemNumber = Item.itemNumber) THEN 'ComputerGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame AS V WHERE V.fk_itemNumber = Item.itemNumber) THEN 'VideoGame'
    WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame AS P WHERE P.fk_itemNumber = Item.itemNumber) THEN 'PlayingCardGame'
    END) AS game_type
    FROM Item
    WHERE itemNumber = %s;

        """
        data=[desiredItemNum]
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery,data)
            rows = db_helper.dictfetchall(cursor)
            print(rows)
        if rows[0]['game_type']=="CollectiveCardGame":
            sqlQuery="""
            SELECT CollectiveCardGame.cardsOffered
            FROM Item INNER JOIN CollectiveCardGame ON Item.itemNumber = CollectiveCardGame.fk_itemNumber 
            WHERE Item.itemNumber = %s;
            """
            data=[desiredItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        if rows[0]['game_type']=="ComputerGame":
            sqlQuery="""
            SELECT ComputerGame.computerPlatform as platform
            FROM Item INNER JOIN ComputerGame ON Item.itemNumber = ComputerGame.fk_itemNumber 
            WHERE Item.itemNumber = %s;
            """
            data=[desiredItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        if rows[0]['game_type']=="VideoGame":
            sqlQuery="""
            SELECT VideoGame.media, VideoGamePlatform.platform FROM Item
            INNER JOIN VideoGame ON Item.itemNumber = VideoGame.fk_itemNumber INNER JOIN VideoGamePlatform ON Item.itemNumber = VideoGamePlatform.fk_VideoGame_itemNumber
            WHERE Item.itemNumber = %s;
            """
            data=[desiredItemNum]
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery,data)
                additional_rows = db_helper.dictfetchall(cursor)
            print(additional_rows)
            rows[0].update(additional_rows[0])
        json_data = []
        for row in rows:
            json_data.append(row)
        context = {
            'statusCode': '200',
            'data': rows[0]
        }
        return JsonResponse(context)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context)