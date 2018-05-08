# Based on the below answer on the SO question:
# In a Django form, how do I make a field readonly (or disabled) so that it cannot be edited?
# https://stackoverflow.com/a/15134622/4126114
#
# Usage of either widget classes below:
# class MyForm(forms.ModelForm):
#  class Meta:
#    widgets = {
#      'field': ReadOnlyWidgetSimple(),
#      'foreign_key': ReadOnlyWidgetMyModel()
#    }

from django.forms import widgets
from main.models.locataire import Locataire
from main.models.contrat_location import ContratLocation
# For non-foreign-key fields, display them in <p>...</p>
# Note the "str(...)" necessary for things like datetime objects
# Also, without the <p>...</p>, the field in bootstrap_form does not show up aligned properly
class ReadOnlyWidgetSimple(widgets.Widget):
    """Some of these values are read only - just a bit of text..."""
    def render(self, _, value, attrs=None):
        return "<p>"+str(value)+"</p>"

# For foreign-key fields, display their __str()__ result
# Usage: Define a class inheriting from this, and which defines the "model" attribute
# e.g.

class ReadOnlyWidgetModel(widgets.Widget):
    model = None
    """Some of these values are read only - just a bit of text..."""
    def render(self, _, value, attrs=None):
        if not self.model: raise Exception("Define model")
        v2 = self.model.objects.get(id=value)
        v2 = "<p>"+str(v2)+"</p>"
        return v2

class ReadOnlyWidgetContratLocation(ReadOnlyWidgetModel):
    model = ContratLocation
