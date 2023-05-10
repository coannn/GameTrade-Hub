from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from . import db_helper

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def list_item(request):
    try:
        body = json.loads(request.body)
        print(body)
        game_type = body['game_type']
        email = body['email']
        title = body['title']
        condition = body['condition']
        description = body['description']
        cards_offered = body['cards_offered']
        computer_platform = body['computer_platform']
        media = body['media']
        video_game_platform = body['video_game_platform']

        with connection.cursor() as cursor:
            if game_type == 'BoardGame':
                sqlQuery = "INSERT INTO Item (fk_email, title, condition, description) OUTPUT INSERTED.itemNumber INTO BoardGame VALUES (%s, %s, %s, %s)"
                data = [email, title, condition, description]
                print("12312")
                cursor.execute(sqlQuery, data)
                sqlQuery = "SELECT MAX(fk_itemNumber) AS fk_itemNumber FROM BoardGame;"
                cursor.execute(sqlQuery)
                print("456")
                rows = db_helper.dictfetchall(cursor)
            elif game_type == 'PlayingCardGame':
                sqlQuery = "INSERT INTO Item (fk_email, title, condition, description) OUTPUT INSERTED.itemNumber INTO PlayingCardGame VALUES (%s, %s, %s, %s)"
                data = [email, title, condition, description]
                cursor.execute(sqlQuery, data)
                sqlQuery = "SELECT MAX(fk_itemNumber) AS fk_itemNumber FROM PlayingCardGame;"
                cursor.execute(sqlQuery)
                rows = db_helper.dictfetchall(cursor)
            elif game_type == 'CollectiveCardGame':
                sqlQuery = """
                            DECLARE @TempCollectiveCardGame TABLE (fk_itemNumber int);
                            INSERT INTO Item (fk_email, title, condition, description) OUTPUT INSERTED.itemNumber INTO @TempCollectiveCardGame VALUES (%s, %s, %s, %s);
                            INSERT INTO CollectiveCardGame (fk_itemNumber, cardsOffered) VALUES ((SELECT fk_itemNumber FROM @TempCollectiveCardGame), %s);
                        """
                data = [email, title, condition, description, cards_offered]
                cursor.execute(sqlQuery, data)
                sqlQuery = "SELECT MAX(fk_itemNumber) AS fk_itemNumber FROM CollectiveCardGame;"
                cursor.execute(sqlQuery)
                rows = db_helper.dictfetchall(cursor)
            elif game_type == 'ComputerGame':
                sqlQuery = """
                            DECLARE @TempComputerGame TABLE (fk_itemNumber int);
                            INSERT INTO Item (fk_email, title, condition, description) OUTPUT INSERTED.itemNumber INTO @TempComputerGame VALUES (%s, %s, %s, %s);
                            INSERT INTO ComputerGame(fk_itemNumber, computerPlatform) VALUES ((SELECT fk_itemNumber FROM @TempComputerGame), %s);
                        """
                data = [email, title, condition, description, computer_platform]
                cursor.execute(sqlQuery, data)
                sqlQuery = "SELECT MAX(fk_itemNumber) AS fk_itemNumber FROM ComputerGame;"
                cursor.execute(sqlQuery)
                rows = db_helper.dictfetchall(cursor)
            elif game_type == 'VideoGame':
                sqlQuery = """
                            DECLARE @TempVideoGame TABLE (fk_itemNumber int);
                            INSERT INTO Item (fk_email, title, condition, description) OUTPUT INSERTED.itemNumber INTO @TempVideoGame VALUES (%s, %s, %s, %s);
                            INSERT INTO VideoGame(fk_itemNumber, media) VALUES ((SELECT fk_itemNumber FROM @TempVideoGame), %s);
                            INSERT INTO VideoGamePlatform(fk_VideoGame_itemNumber, platform) VALUES ((SELECT fk_itemNumber FROM @TempVideoGame), %s); 
                        """
                data = [email, title, condition, description, media, video_game_platform]
                cursor.execute(sqlQuery, data)
                sqlQuery = "SELECT MAX(fk_itemNumber) AS fk_itemNumber FROM VideoGame;"
                cursor.execute(sqlQuery)
                rows = db_helper.dictfetchall(cursor)
        
        connection.cursor().close()
        connection.close()
        response = {
            'statusCode': '200',
            'data': rows
        }
        return JsonResponse(response)
    except Exception:
        print('Error: 500 Internal error!')
        context = {'statusCode': '500', 'Error': '500 Internal error!'}
        return JsonResponse(context, status=500)