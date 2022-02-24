from turtle import distance
from pronto import Ontology
# load the DOID ontology
doid = Ontology("http://purl.obolibrary.org/obo/doid.obo")

# Select a node by ID
root_node = doid['DOID:0050117'] # disease by infectious agent
# print all children(distance=1) without the node itself
for term in root_node.subclasses(distance=1, with_self=False).to_set():
    print(term.name)

