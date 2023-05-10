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
def getMyTradeList(request, email):
    #body = json.loads(request.body)
    #print(body)
    #email = request.GET.get('email')
    print(request)
    print(email)

    sqlQuery ='''
                WITH Mytrades AS (
                    SELECT [User].email AS counterpartyEmail, [User].fk_postal_code AS counterpartyPostalCode, Item.title AS desiredItemTitle, Trade.proposedDate AS date, Trade.proposedItemNum, Trade.desiredItemNum
                    FROM [User] INNER JOIN Item ON [User].email = Item.fk_email INNER JOIN Trade ON Item.itemNumber = Trade.desiredItemNum
                    WHERE Item.fk_email = %s AND Trade.status LIKE %s),
                MytradesWP AS (
                    SELECT Mytrades.*, [User].email AS proposerEmail, [User].nickname AS proposer_nickname, [User].first_name AS proposer_first_name,  [User].fk_postal_code AS proposerPostalCode, Item.title AS proposedItemTitle
                    FROM Mytrades, [User] INNER JOIN Item ON [User].email = Item.fk_email
                    WHERE Item.itemNumber = Mytrades.proposedItemNum
                ),
                MytradesWPWR AS (
                    SELECT Item.fk_email,
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
                    WHERE Item.fk_email IN (SELECT DISTINCT proposerEmail FROM MyTradesWP)
                    GROUP BY Item.fk_email 
                ),
                G1 AS (
                    SELECT email, latitude, longitude, city, state, GlobalPostCode.postal_code
                    FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
                    WHERE [User].email IN (SELECT DISTINCT proposerEmail FROM MyTradesWP)
                ),
                G2 AS (
                    SELECT email, latitude, longitude
                    FROM [User] INNER JOIN GlobalPostCode ON [User].fk_postal_code = GlobalPostCode.postal_code
                    WHERE email = %s
                ),
                get_distance AS (
                    SELECT G1.email, G1.latitude AS lat1, G1.longitude AS lon1, G2.latitude AS lat2, G2.longitude AS lon2,
                    ROUND(((acos(sin(radians(G1.latitude))*sin(radians(G2.latitude)) + cos(radians(G1.latitude))*cos(radians(G2.latitude))*cos(radians(G2.longitude)-radians(G1.longitude)))+0.0) * 3958.75),2) AS distance
                    FROM G1, G2
                ) 
                    SELECT MyTradesWP.date, MyTradesWP.desiredItemTitle, MytradesWP.desiredItemNum, MyTradesWP.proposer_nickname, MyTradesWPWR.rank, get_distance.distance, MyTradesWP.proposedItemTitle, MyTradesWP.proposedItemNum, MyTradesWP.proposer_first_name, MyTradesWP.proposerEmail
                    FROM MyTradesWP 
                    LEFT JOIN MyTradesWPWR ON MyTradesWP.proposerEmail = MyTradesWPWR.fk_email
                    LEFT JOIN get_distance ON MyTradesWP.proposerEmail = get_distance.email
                    ORDER BY MytradesWP.date ASC; 
            '''
    with connection.cursor() as cursor:
        data = [email, '%Pending%', '%Accepted%', email]
        #print(data)
        cursor.execute(sqlQuery, data)
        rows = db_helper.dictfetchall(cursor)
        json_data = []
        for row in rows:
            json_data.append({"Date": row['date'], "Desired_Item" : row['desiredItemTitle'], "desiredItemNum" : row['desiredItemNum'], "Proposer" : row['proposer_nickname'], "Rank" : row['rank'], "Distance": row['distance'], "Proposed_Item": row['proposedItemTitle'], "proposedItemNum": row['proposedItemNum'], "proposer_firstname": row['proposer_first_name'], "proposerEmail": row['proposerEmail']})
    return JsonResponse(json_data, safe = False)


@csrf_exempt
@require_http_methods(['POST'])
def arTrade(request):
    #body = json.loads(request.body)
    #print(body)
    body = json.loads(request.body)
    print(body)
    desiredItemNum = body['desiredItemNum']
    proposedItemNum = body['proposedItemNum']
    decision = body['decision']

    # decison id boolean value (true == accept, false = reject)
    if decision == 'accept':
        sqlQuery ='''
                    UPDATE Trade SET decisionDate = GETDATE(), status = 'Accepted'
                    WHERE proposedItemNum = %s AND desiredItemNum = %s;
        
                '''
        try:
            with connection.cursor() as cursor:
                data = [proposedItemNum, desiredItemNum]
                print(data)
                cursor.execute(sqlQuery, data)

                response = {
                    'statusCode' : '200',
                    'data': 'You have accepted a trade'
                }
                return JsonResponse(response, safe = False)
        
        except Exception:
            context = {
                'statusCode' : '500',
                'Error': 'action failed'
            }
            return JsonResponse(context, safe = False)
    elif decision == 'reject':
        sqlQuery ='''
                    UPDATE Trade SET decisionDate = GETDATE(), status = 'Rejected'
                    WHERE proposedItemNum = %s AND desiredItemNum = %s;
                '''
        try:
            with connection.cursor() as cursor:
                data = [proposedItemNum, desiredItemNum]
                print(data)
                cursor.execute(sqlQuery, data)

                response = {
                    'statusCode' : '200',
                    'data': 'You have rejected a trade'
                }
                return JsonResponse(response, safe = False)
        
        except Exception:
            context = {
                'statusCode' : '500',
                'Error': 'action failed'
            }
            return JsonResponse(context, safe = False)
    
    