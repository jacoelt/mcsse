from ninja import ModelSchema

from core.models import Server, ServerTag


class ServerTagOut(ModelSchema):
    class Meta:
        model = ServerTag
        fields = ["name", "description", "relevance"]


class ServerOut(ModelSchema):
    tags: list[ServerTagOut] = []

    class Meta:
        model = Server
        fields = "__all__"
