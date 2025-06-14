from time import sleep
from ninja import NinjaAPI

from core.api.schema import ServerOut
from core.models import Server


api = NinjaAPI(auth=None, csrf=False)


@api.get("/servers", response=list[ServerOut])
def list_servers(request):
    """
    List all servers.
    """
    sleep(2)
    return Server.objects.all()
