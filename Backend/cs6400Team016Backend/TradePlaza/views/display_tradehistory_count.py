from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper
@csrf_exempt
@require_http_methods(['GET'])

def display_tradehistory_count(request, email):
    try:
        print(email)
        sqlQuery = """
        WITH t1 AS (SELECT COUNT(*) as Accepted FROM Trade as T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber where I1.fk_email=%s and T.status LIKE %s),
t2 AS (SELECT COUNT(*) as Rejected FROM Trade as T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber where I1.fk_email=%s and T.status LIKE %s),
t3 AS (SELECT COUNT(*) as Accepted FROM Trade as T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber where I2.fk_email=%s and T.status LIKE %s),
t4 AS (SELECT COUNT(*) as Rejected FROM Trade as T INNER JOIN Item AS I1 ON T.proposedItemNum = I1.itemNumber INNER JOIN Item AS I2 ON T.desiredItemNum=I2.itemNumber where I2.fk_email=%s and T.status LIKE %s)

SELECT 'Proposer' as role, t1.Accepted+t2.Rejected as Total, t1.Accepted as Accepted, t2.Rejected as Rejected , 
CASE WHEN ((t1.Accepted + t2.Rejected) = 0 )THEN CONVERT(varchar(10), 0.0) + %s
ELSE CONVERT(varchar(10), CAST(ROUND(((t2.Rejected+0.0)/(t1.Accepted + t2.Rejected + 0.0))*100.0,1) AS decimal(10,1))) + %s END AS rejected_percentage
FROM t1,t2

UNION ALL

SELECT 'Counterparty' as role, t3.Accepted+t4.Rejected as Total, t3.Accepted as Accepted, t4.Rejected as Rejected , 
CASE WHEN ((t3.Accepted + t4.Rejected) = 0 )THEN CONVERT(varchar(10), 0.0) + %s
ELSE CONVERT(varchar(10), CAST(ROUND(((t4.Rejected+0.0)/(t3.Accepted + t4.Rejected + 0.0))*100.0,1) AS decimal(10,1))) + %s END AS rejected_percentage
FROM t3,t4;

        
        """
        data=[email,'%Accepted%',email,'%Rejected%',email,'%Accepted%',email,'%Rejected%','%','%','%','%']
        with connection.cursor() as cursor:
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