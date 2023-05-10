from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from . import db_helper


# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def search_item(request):
    try:        
        body = json.loads(request.body)
        print(body)
        email = body['email']
        select = body['select']
        keyword = body['keyword']
        miles = body['miles']
        postalCode = body['postalCode']
        json_data = []
        with connection.cursor() as cursor:
            if select == 'keyword':
                sqlQuery = '''
WITH get_type (fk_email, itemNumber, title, condition, description, game_type) AS (
SELECT fk_email, Item.itemNumber AS itemNumber, title, condition, 
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
WHERE (title like %s OR description like %s) AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s))
),
get_response_time AS (
SELECT Item.fk_email,
ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, Trade.proposedDate, Trade.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS response_time
FROM Item
LEFT JOIN Trade ON Item.itemNumber = Trade.desiredItemNum AND (Trade.status LIKE %s OR Trade.status LIKE %s)
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
),
get_rank AS (
SELECT fk_email, 
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
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
),
G1 AS (
SELECT email, latitude, longitude
FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
WHERE email IN (SELECT DISTINCT fk_email FROM get_type) 
),
G2 AS (
SELECT email, latitude, longitude
FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
WHERE email = %s
),
get_distance AS(
SELECT G1.email, G1.latitude AS lat1, G1.longitude AS lon1, G2.latitude AS lat2, G2.longitude AS lon2,
ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2) AS distance
FROM G1, G2
)

SELECT get_type.fk_email, get_type.itemNumber, get_type.game_type, get_type.title, get_type.condition, get_type.description, get_response_time.response_time, get_rank.rank, get_distance.distance
FROM get_type
LEFT JOIN get_response_time ON get_type.fk_email = get_response_time.fk_email
LEFT JOIN get_rank ON get_type.fk_email = get_rank.fk_email
LEFT JOIN get_distance ON get_type.fk_email = get_distance.email
ORDER BY get_distance.distance, get_type.itemNumber ASC;
'''
                data = ['%'+keyword+'%', '%'+keyword+'%', '%Pending%', '%Accepted%', 
                 '%Accepted%','%Rejected%',
                 '%Accepted%',
                 email ]
                cursor.execute(sqlQuery, data)
                rows1 = db_helper.dictfetchall(cursor)
                for row in rows1:
                    json_data.append({"fk_email": row['fk_email'],"itemNumber": row['itemNumber'] , "game_type": row['game_type'] , "title": row['title'] ,
                    "condition": row['condition'] , "description": row['description'] , "response_time": row['response_time'] ,
                    "rank": row['rank'] , "distance": row['distance'] })      

            if select == 'myPostalCode':
                sqlQuery = '''
                WITH get_email AS (
SELECT U1.email
FROM [User] AS U1, [User] AS U2
WHERE U1.fk_postal_code = U2.fk_postal_code AND U2.email = %s 
),
get_type AS (
SELECT fk_email, Item.itemNumber AS itemNumber, title, condition, 
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
WHERE fk_email IN (SELECT DISTINCT email from get_email) AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s))
),
get_response_time AS (
SELECT Item.fk_email,
ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, Trade.proposedDate, Trade.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS response_time
FROM Item
LEFT JOIN Trade ON Item.itemNumber = Trade.desiredItemNum AND (Trade.status LIKE %s OR Trade.status LIKE %s)
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
),
get_rank AS (
SELECT fk_email, 
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
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
)
SELECT get_type.fk_email, get_type.itemNumber, get_type.game_type, get_type.title, get_type.condition, get_type.description, get_response_time.response_time, get_rank.rank, 0 AS distance
FROM get_type
LEFT JOIN get_response_time ON get_type.fk_email = get_response_time.fk_email
LEFT JOIN get_rank ON get_type.fk_email = get_rank.fk_email
ORDER BY get_type.itemNumber ASC;
'''
                data = [email, '%Pending%', '%Accepted%', 
                 '%Accepted%','%Rejected%',
                 '%Accepted%']
                cursor.execute(sqlQuery, data)
                
                rows1 = db_helper.dictfetchall(cursor)
                for row in rows1:
                    json_data.append({"fk_email": row['fk_email'],"itemNumber": row['itemNumber'] , "game_type": row['game_type'] , "title": row['title'] ,
                    "condition": row['condition'] , "description": row['description'] , "response_time": row['response_time'] ,
                    "rank": row['rank'] , "distance": row['distance'] })   

            if select == 'distance':
                sqlQuery = ''' WITH G1 AS (
SELECT email, latitude, longitude
FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
),
G2 AS (
SELECT email, latitude, longitude
FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
WHERE email = %s
),
cal_distance AS (
SELECT G1.email AS email, G1.latitude AS lat1, G1.longitude AS lon1, G2.latitude AS lat2, G2.longitude AS lon2,
ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2) AS distance
FROM G1, G2
),
get_distance AS (
SELECT email, distance
FROM cal_distance
WHERE distance <= %s
),
get_type AS (
SELECT fk_email, Item.itemNumber AS itemNumber, title, condition, 
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
WHERE fk_email IN (SELECT DISTINCT email from get_distance) AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s))
),
get_response_time AS (
SELECT Item.fk_email,
ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, Trade.proposedDate, Trade.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS response_time
FROM Item
LEFT JOIN Trade ON Item.itemNumber = Trade.desiredItemNum AND (Trade.status LIKE %s OR Trade.status LIKE %s)
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
),
get_rank AS (
SELECT fk_email, 
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
WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
GROUP BY Item.fk_email
)
SELECT get_type.fk_email, get_type.itemNumber, get_type.game_type, get_type.title, get_type.condition, get_type.description, get_response_time.response_time, get_rank.rank, get_distance.distance
FROM get_type
LEFT JOIN get_response_time ON get_type.fk_email = get_response_time.fk_email
LEFT JOIN get_rank ON get_type.fk_email = get_rank.fk_email
LEFT JOIN get_distance ON get_type.fk_email = get_distance.email
ORDER BY get_distance.distance, get_type.itemNumber ASC;
'''           
                data = [email, miles, '%Pending%', '%Accepted%',  
                 '%Accepted%','%Rejected%',
                 '%Accepted%']
                cursor.execute(sqlQuery, data)
                
                rows1 = db_helper.dictfetchall(cursor)
                for row in rows1:
                    json_data.append({"fk_email": row['fk_email'],"itemNumber": row['itemNumber'] , "game_type": row['game_type'] , "title": row['title'] ,
                    "condition": row['condition'] , "description": row['description'] , "response_time": row['response_time'] ,
                    "rank": row['rank'] , "distance": row['distance'] })  

            if select == 'PostalCode':
                sqlQuery = "SELECT postal_code from [GlobalPostCode] WHERE [GlobalPostCode].postal_code=%s;"
                data = [postalCode]
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
                else:              
                    sqlQuery = ''' WITH G1 AS (
    SELECT email, latitude, longitude
    FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
    WHERE GlobalPostCode.postal_code = %s
    ),
    G2 AS (
    SELECT email, latitude, longitude
    FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
    WHERE email = %s
    ),
    get_email AS (
    SELECT G1.email AS email, G1.latitude AS lat1, G1.longitude AS lon1, G2.latitude AS lat2, G2.longitude AS lon2,
    ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2) AS distance
    FROM G1, G2
    ),
    get_type AS (
    SELECT fk_email, Item.itemNumber AS itemNumber, title, condition, 
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
    WHERE fk_email IN (SELECT DISTINCT email from get_email) AND NOT EXISTS (SELECT proposedItemNum, desiredItemNum FROM Trade WHERE (proposedItemNum = Item.itemNumber OR desiredItemNum = Item.itemNumber) AND (status LIKE %s OR status LIKE %s))
    ),
    get_response_time AS (
    SELECT Item.fk_email,
    ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, Trade.proposedDate, Trade.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS response_time
    FROM Item
    LEFT JOIN Trade ON Item.itemNumber = Trade.desiredItemNum AND (Trade.status LIKE %s OR Trade.status LIKE %s)
    WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
    GROUP BY Item.fk_email
    ),
    get_rank AS (
    SELECT fk_email, 
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
    WHERE fk_email IN (SELECT DISTINCT fk_email FROM get_type)
    GROUP BY Item.fk_email
    )

    SELECT get_type.fk_email, get_type.itemNumber, get_type.game_type, get_type.title, get_type.condition, get_type.description, get_response_time.response_time, get_rank.rank, get_email.distance
    FROM get_type
    LEFT JOIN get_response_time ON get_type.fk_email = get_response_time.fk_email
    LEFT JOIN get_rank ON get_type.fk_email = get_rank.fk_email
    LEFT JOIN get_email ON get_type.fk_email = get_email.email
    ORDER BY get_email.distance, get_type.itemNumber ASC;
    '''
                    print(postalCode)
                    data = [postalCode, email, '%Pending%', '%Accepted%',  
                    '%Accepted%','%Rejected%',
                    '%Accepted%']
                    cursor.execute(sqlQuery, data)
                    
                    rows1 = db_helper.dictfetchall(cursor)
                    for row in rows1:
                        json_data.append({"fk_email": row['fk_email'],"itemNumber": row['itemNumber'] , "game_type": row['game_type'] , "title": row['title'] ,
                        "condition": row['condition'] , "description": row['description'] , "response_time": row['response_time'] ,
                        "rank": row['rank'] , "distance": row['distance'] })

        print(json_data)
        response = {
            'statusCode': '200',
            'data': json_data
        }
        return JsonResponse(response)

    except Exception:
        print('Error: 500 Internal error!')
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context)


