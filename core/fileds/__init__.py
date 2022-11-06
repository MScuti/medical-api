
from rest_framework.fields import ListField

class CommaListField(ListField):


    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return [self.child.to_representation(item) if item is not None else None for item in data.split(",")]