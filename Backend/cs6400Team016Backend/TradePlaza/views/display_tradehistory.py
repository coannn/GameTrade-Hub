from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper
@csrf_exempt
@require_http_methods(['GET'])

def display_tradehistory(request, email):
    try:
        print(email)
        sqlQuery = """
        WITH t1 AS (SELECT T.proposedItemNum, T.desiredItemNum, T.proposedDate, T.decisionDate, T.status, DATEDIFF(DAY, proposedDate, decisionDate) as response_time, 'Proposer' as role, I1.title as proposed_item, I2.title as desired_item, U.nickname as other_user, U.email as other_email 
FROM Trade AS T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber AND (T.status LIKE %s OR T.status LIKE %s)
INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber 
INNER JOIN [User] as U on I2.fk_email=U.email where I1.fk_email=%s),
t2 AS (SELECT T.proposedItemNum, T.desiredItemNum, proposedDate, decisionDate, status, DATEDIFF(DAY, proposedDate, decisionDate) as response_time, 'Counterparty' as role, I1.title as proposed_item, I2.title as desired_item, U.nickname as other_user, U.email as other_email
FROM Trade AS T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber AND (T.status LIKE %s OR T.status LIKE %s)
INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber 
INNER JOIN [User] as U on I1.fk_email=U.email where I2.fk_email=%s)

SELECT proposedItemNum,desiredItemNum,proposedDate, decisionDate, status, response_time, role, proposed_item, desired_item, other_user, other_email from t1
UNION ALL
SELECT proposedItemNum,desiredItemNum,proposedDate, decisionDate, status, response_time, role, proposed_item, desired_item, other_user, other_email from t2

ORDER BY decisionDate DESC, proposedDate ASC


        
        """
        data=['%Accepted%','%Rejected%',email,'%Accepted%','%Rejected%',email]
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