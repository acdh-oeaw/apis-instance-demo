from django.views.generic import TemplateView
from django_cosmograph.views import CosmographView
from django_cosmograph.utils import assign_node_sizes
from apis_core.apis_entities.models import RootObject
from apis_core.relations.models import Relation
import json
from django.core.cache import cache


class GraphView(CosmographView):
    # TODO: How do I restrict the view based on user permissions
    def get_nodes_links(self):
        cache_key = "graph_nodes_links"
        cached_data = cache.get(cache_key)
        if cached_data:
            # Load nodes and links from cached JSON string
            nodes, links = json.loads(cached_data)
            return nodes, links

        nodes = []
        for obj in RootObject.objects_inheritance.select_subclasses():
            nodes.append(
                {"id": obj.id, "label": str(obj), "group": obj.__class__.__name__}
            )
        links = []
        for rel in Relation.objects.all():
            links.append(
                {
                    "source": rel.subj.id,
                    "target": rel.obj.id,
                }
            )
        nodes = assign_node_sizes(nodes, links)

        # Cache nodes and links as a JSON string for 1 hour
        cache.set(cache_key, json.dumps((nodes, links)), 3600)

        return nodes, links
