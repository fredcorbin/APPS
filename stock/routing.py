from django.urls import re_path
from stock.websockets.socket_familles import webSocket_familles
from stock.websockets.socket_modeles import webSocket_modeles

websocket_urlpatterns = [
    re_path(r'ws/familles/$',webSocket_familles.as_asgi()),
    re_path(r'ws/modeles/$', webSocket_modeles.as_asgi())

]