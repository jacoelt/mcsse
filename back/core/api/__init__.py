
from ninja import NinjaAPI

from core.api.schema import ServerOut
from core.models import Server


api = NinjaAPI()

@api.get("/servers", response=list[ServerOut])
def list_servers(request):
    """
    List all servers.
    """
    return Server.objects.all()
