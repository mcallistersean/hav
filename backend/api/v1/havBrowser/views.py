from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from hav.sets.models import Node
from ..permissions import IncomingBaseMixin
from .serializers import HAVNodeSerializer, RootHAVCollectionSerializer, CreateHAVCollectionSerializer


class HAVNodeBrowser(IncomingBaseMixin, APIView):

    _node = None
    keys = []

    @property
    def node(self):

        if not self._node and self.kwargs.get('node_id'):
            self._node = Node.objects.get(pk=self.kwargs['node_id'])
        return self._node


    def get_context(self):
        return {
            'request': self.request,
            'keys': self.keys
        }

    def get_serializer_class(self):
        if self.node:
            return HAVNodeSerializer
        else:
            return RootHAVCollectionSerializer

    def get(self, *args, **kwargs):
        sc = self.get_serializer_class()
        serializer = sc(
            # any truthy object will do if there is no node
            instance=self.node or object(),
            context=self.get_context()
        )
        return Response(serializer.data)

    def post(self, request, node_id=None):
        if not node_id:
            return Response('Cannot create root nodes', status=400)
        sc = self.get_serializer_class()
        serializer = sc(
            data=request.data,
            instance=self.node or object(),
            context=self.get_context()
        )
        if serializer.is_valid():
            serializer.create(serializer.validated_data, parent=self.node)

        return Response(serializer.data, status=201)








