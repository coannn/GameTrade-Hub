from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import db_helper

# Create your views here.
@csrf_exempt
@require_http_methods(['GET'])
def main_menu(request, email):
    try:
        sqlQuery = "SELECT first_name, last_name, nickname FROM [User] WHERE email = %s;"
        data = [email]
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery, data)
            rows = db_helper.dictfetchall(cursor)
            json_data1 = []
            for row in rows:
                json_data1.append({"first_name": row['first_name'], "last_name" : row['last_name'], "nickname" : row['nickname']})
        print(json_data1)

        sqlQuery1 = '''
        SELECT COUNT(I.itemNumber) AS unacceptedTrades FROM Item AS I INNER JOIN Trade AS T ON I.itemNumber = T.desiredItemNum WHERE I.fk_email LIKE %s AND T.status LIKE %s;'''
        sqlQuery2 = '''SELECT (CASE WHEN COUNT(T.status) = 0 THEN 'None' WHEN (COUNT(T.status) >= 1 AND COUNT(T.status)<= 2) THEN 'Aluminium' WHEN COUNT(T.status) = 3 THEN 'Bronze' WHEN (COUNT(T.status) >= 4 AND COUNT(T.status)<= 5) THEN 'Silver' WHEN (COUNT(T.status) >= 6 AND COUNT(T.status)<= 7) THEN 'Gold' WHEN (COUNT(T.status) >= 8 AND COUNT(T.status)<= 9)THEN 'Platinum' ELSE 'Alexandinium' END) AS rank
FROM Item AS I LEFT JOIN Trade AS T ON I.itemNumber = T. desiredItemNum OR I.itemNumber = T. proposedItemNum WHERE I.fk_email = %s AND T.status LIKE %s;'''
        sqlQuery3 = '''SELECT ISNULL(CONVERT(varchar(10), CAST(ROUND(AVG(DATEDIFF(day, T.proposedDate, T.decisionDate)+0.0), 1) AS decimal (10,1))), 'None') AS responseTime FROM Item AS I LEFT JOIN Trade AS T ON I.itemNumber = T. desiredItemNum WHERE I.fk_email = %s AND (T.status LIKE %s OR T.status LIKE %s);
        '''
        

        json_data = []
        with connection.cursor() as cursor:
            cursor.execute(sqlQuery1, [email, '%Pending%'])
            rows1 = db_helper.dictfetchall(cursor)
            for row in rows1:
                json_data.append({"unacceptedTrades": row['unacceptedTrades'] })

        with connection.cursor() as cursor:
            cursor.execute(sqlQuery2, [email, '%Accepted%'])
            rows2 = db_helper.dictfetchall(cursor)
            for row in rows2:
                json_data.append({"rank": row['rank'] })


        with connection.cursor() as cursor:
            cursor.execute(sqlQuery3, [email, '%Reject%', '%Accepted%'])
            rows3 = db_helper.dictfetchall(cursor)
            for row in rows3:
                json_data.append({"responseTime": row['responseTime'] })
        json_data=json_data1+json_data
        print(json_data)
        context = {
            'statusCode': '200',
            'data': json_data
        }
        return JsonResponse(context)

    except:
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)