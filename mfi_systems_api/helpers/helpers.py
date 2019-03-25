"""
GLOBAL Helper methods
"""

from django.http import Http404

def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404