class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, class_name):
        if class_name not in self.graph:
            self.graph[class_name] = {
                'parent': set(),
                'children': set(),
                'ancestors': set()
            }

    def add_edge(self, parent_class, child_class):
        if parent_class in self.graph and child_class in self.graph:
            self.graph[parent_class]['children'].add(child_class)
            self.graph[child_class]['parent'].add(parent_class)

            # Update ancestors of the child class
            self.graph[child_class]['ancestors'].add(parent_class)
            self.graph[child_class]['ancestors'].update(self.graph[parent_class]['ancestors'])

    def get_siblings(self, class_name):
        if class_name in self.graph and self.graph[class_name]['parent']:
            parent = self.graph[class_name]['parent']
            siblings = set()
            for p in parent:
                siblings.update(self.graph[p]['children'])
            siblings.remove(class_name)
            return siblings
        return []

    def get_parent(self, class_name):
        if class_name in self.graph:
            return self.graph[class_name]['parent']
        return None

    def get_ancestors(self, class_name):
        if class_name in self.graph:
            return self.graph[class_name]['ancestors']
        return set()

    def has_common_ancestor(self, class1, class2):
        ancestors1 = self.get_ancestors(class1)
        ancestors2 = self.get_ancestors(class2)
        return bool(ancestors1.intersection(ancestors2))
