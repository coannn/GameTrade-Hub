from unittest import skip
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import  json
from . import db_helper

@csrf_exempt
@require_http_methods(['GET'])

def display_item_details(request):
    # get item details
    email = request.GET.get('email') # user's email (not owner's email!!!)
    itemID = request.GET.get('itemNumber')
    
    
    json_data = []
    try:
        sql_item = """
        SELECT fk_email, Item.itemNumber AS itemNumber, title, condition, 
description,
(CASE WHEN EXISTS (SELECT fk_itemNumber FROM BoardGame AS B WHERE B.fk_itemNumber = Item.itemNumber) THEN 'BoardGame' 
WHEN EXISTS (SELECT fk_itemNumber FROM CollectiveCardGame AS Col WHERE Col.fk_itemNumber = Item.itemNumber) THEN 'CollectiveCardGame'
WHEN EXISTS (SELECT fk_itemNumber FROM ComputerGame AS Com WHERE Com.fk_itemNumber = Item.itemNumber) THEN 'ComputerGame'
WHEN EXISTS (SELECT fk_itemNumber FROM VideoGame AS V WHERE V.fk_itemNumber = Item.itemNumber) THEN 'VideoGame'
WHEN EXISTS (SELECT fk_itemNumber FROM PlayingCardGame AS P WHERE P.fk_itemNumber = Item.itemNumber) THEN 'PlayingCardGame'
END) AS game_type
FROM Item
WHERE itemNumber = %s 
        """
        item_data = [itemID]
        with connection.cursor() as cursor:
            cursor.execute(sql_item, item_data)
            rows = db_helper.dictfetchall(cursor)

        game_type = rows[0]['game_type']
        json_data.append(rows[0])
        
        if game_type=='BoardGame' or game_type=='PlayingCardGame':
           skip
        if game_type=='CollectiveCardGame':
            sql_gametype = """
                SELECT CollectiveCardGame.cardsOffered
                FROM Item INNER JOIN CollectiveCardGame ON Item.itemNumber = CollectiveCardGame.fk_itemNumber 
                WHERE Item.itemNumber = %s;
            """
            game_type_data = [itemID]
            with connection.cursor() as cursor:
                cursor.execute(sql_gametype, game_type_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])
            
        if game_type=='ComputerGame':
            sql_gametype = """
                SELECT ComputerGame.computerPlatform as platform
                FROM Item INNER JOIN ComputerGame ON Item.itemNumber = ComputerGame.fk_itemNumber 
                WHERE Item.itemNumber = %s;
            """
            game_type_data = [itemID]
            with connection.cursor() as cursor:
                cursor.execute(sql_gametype, game_type_data)
                rows = db_helper.dictfetchall(cursor)
           
            json_data.append(rows[0])
            
        if game_type=='VideoGame':
            sql_gametype = """
                SELECT VideoGame.media, VideoGamePlatform.platform
                FROM Item
                INNER JOIN VideoGame ON Item.itemNumber = VideoGame.fk_itemNumber INNER JOIN VideoGamePlatform ON Item.itemNumber = VideoGamePlatform.fk_VideoGame_itemNumber
                WHERE Item.itemNumber = %s;
            """
            game_type_data = [itemID]
            with connection.cursor() as cursor:
                cursor.execute(sql_gametype, game_type_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])

        # trading details -----------
        ## Check the user if the current login user
    
        sql_owner_email = "SELECT fk_email FROM item WHERE itemNumber="+str(itemID)
        with connection.cursor() as cursor:
            cursor.execute(sql_owner_email)
            rows = db_helper.dictfetchall(cursor)
        owner_email = rows[0]['fk_email']
        if owner_email == email: # my owner listing
            skip      
        if owner_email != email: # check other's listing

            sql_trader = """
            SELECT U1.nickname
            FROM [User] AS U1
            WHERE U1.email = %s
            """
            trader_data = [owner_email]
            with connection.cursor() as cursor:
                cursor.execute(sql_trader, trader_data)
                rows = db_helper.dictfetchall(cursor)
           
            json_data.append(rows[0]) 

            sql_loc = """
            WITH G1 AS (
            SELECT email, latitude, longitude, city, state, GlobalPostCode.postal_code
            FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
            WHERE [User].email = %s
            ),
            G2 AS (
            SELECT email, latitude, longitude
            FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
            WHERE email = %s
            )

            SELECT G1.city AS city, G1.state AS state, G1.postal_code AS postal_code, 
            ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2) AS distance
            FROM G1, G2;
            """
            loc_data = [owner_email, email]
            with connection.cursor() as cursor:
                cursor.execute(sql_loc, loc_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0]) 

            sql_responstime = """
                SELECT
                ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, Trade.proposedDate, Trade.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS response_time
                FROM Item
                LEFT JOIN Trade ON Item.itemNumber = Trade.desiredItemNum AND (Trade.status LIKE %s OR Trade.status LIKE %s)
                WHERE fk_email = %s
                GROUP BY Item.fk_email
            """
            responsetime_data = ['%Accepted%', '%Rejected%', owner_email]
            with connection.cursor() as cursor:
                cursor.execute(sql_responstime, responsetime_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])

            sql_rank = """
            SELECT
            (CASE WHEN COUNT(Trade.status) = 0 THEN 'None'
            WHEN (COUNT(Trade.status) >= 1 AND COUNT(Trade.status)<= 2) THEN 'Aluminium'
            WHEN COUNT(Trade.status) = 3 THEN 'Bronze'
            WHEN (COUNT(Trade.status) >= 4 AND COUNT(Trade.status)<= 5) THEN 'Silver'
            WHEN (COUNT(Trade.status) >= 6 AND COUNT(Trade.status)<= 7) THEN 'Gold'
            WHEN (COUNT(Trade.status) >= 8 AND COUNT(Trade.status)<= 9) THEN 'Platinum'
            ELSE 'Alexandinium'
            END) AS rank
            FROM Item
            LEFT JOIN Trade ON (Item.itemNumber = Trade.desiredItemNum OR  Item.itemNumber = Trade.proposedItemNum) AND Trade.status LIKE %s
            WHERE fk_email = %s
            GROUP BY Item.fk_email
            """
            rank_data = [ '%Accepted%', owner_email]
            with connection.cursor() as cursor:
                cursor.execute(sql_rank, rank_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])
            
            sql_isTradable = """
             SELECT (CASE WHEN count(*) = 1 THEN 'false'
                ELSE 'true' END) as isTradable FROM Trade WHERE 
                (proposedItemNum = %s OR desiredItemNum = %s) AND (status LIKE %s OR status LIKE %s)
            """
            isTradable_data = [itemID, itemID, '%Pending%', '%Accepted%']
            with connection.cursor() as cursor:
                cursor.execute(sql_isTradable, isTradable_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])

            sql_pendingItemNum = """
            SELECT count(*) as pendingItemNum
            FROM Trade
            LEFT JOIN Item on desiredItemNum = itemNumber
            WHERE status like %s and fk_email=%s
            """
            pendingItemNum_data=['%Pending%', email]
            with connection.cursor() as cursor:
                cursor.execute(sql_pendingItemNum, pendingItemNum_data)
                rows = db_helper.dictfetchall(cursor)
            json_data.append(rows[0])
        connection.cursor().close()
        connection.close()

        result = {}
        for i in range(len(json_data)):
            result = {**result, **json_data[i]}
        print(result)
        response = {
            'statusCode': '200',
            'data': result
        }
        return JsonResponse(response)
    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}