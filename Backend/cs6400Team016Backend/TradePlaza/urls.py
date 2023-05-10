from django.urls import path
from django.urls import re_path

from TradePlaza.views import get_item
from TradePlaza.views import list_item
from TradePlaza.views import display_myitem
from TradePlaza.views import display_myitem_count
from TradePlaza.views import display_item_details
from TradePlaza.views import display_tradehistory_count
from TradePlaza.views import display_tradehistory
from TradePlaza.views import login
from TradePlaza.views import register
from TradePlaza.views import proposeTrade
from TradePlaza.views import main_menu
from TradePlaza.views import search_item
from TradePlaza.views import display_tradedetail
from TradePlaza.views import artrade



urlpatterns = [
    re_path(r'^(?i)get_item/(\d+)$', get_item.get_item, name='get_item'),
    re_path(r'^(?i)list_item/$', list_item.list_item, name='list_item'),
    re_path(r'^(?i)display_myitem/(.+)$', display_myitem.display_myitem, name = 'display_myitem'),
    re_path(r'^(?i)display_myitem_count/(.+)$', display_myitem_count.display_myitem_count, name = 'display_myitem_count'),
    re_path(r'^(?i)display_item_details/', display_item_details.display_item_details, name = 'display_item_details'),
    re_path(r'^(?i)display_tradehistory_count/(.+)$', display_tradehistory_count.display_tradehistory_count, name = 'display_tradehistory_count'),
    re_path(r'^(?i)display_tradehistory/(.+)$', display_tradehistory.display_tradehistory, name = 'display_tradehistory'),
    #re_path(r'^(?i)display_tradedetail/trade_detail/', display_tradedetail.display_trade_detail, name='display_trade_detail'),
    re_path(r'^(?i)display_tradedetail/user_detail/', display_tradedetail.display_user_detail, name='display_user_detail'),
    re_path(r'^(?i)display_tradedetail/proposedItem/(.+)$', display_tradedetail.display_proposedItem, name='display_proposedItem'),
    re_path(r'^(?i)display_tradedetail/desiredItem/(.+)$', display_tradedetail.display_desiredItem, name='display_desiredItem'),
    re_path(r'^(?i)login/(.+)$', login.login, name='login'),
    re_path(r'^(?i)register/$', register.register, name='register'),
    re_path(r'^(?i)proposeTrade/getMyItemList/', proposeTrade.getMyItemList, name='getMyItemList'),
    re_path(r'^(?i)proposeTrade/proposed/', proposeTrade.proposeTrade, name='proposeTrade'),
    re_path(r'^(?i)main_menu/(.+)$', main_menu.main_menu, name='main_menu'),
    re_path(r'^(?i)search_item/', search_item.search_item, name='search_item'),
    re_path(r'^(?i)artrade/getMyTradeList/(.+)$', artrade.getMyTradeList, name='trade_list'),
    re_path(r'^(?i)artrade/post/', artrade.arTrade, name='artrade')
]
