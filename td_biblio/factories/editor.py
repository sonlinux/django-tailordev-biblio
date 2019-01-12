from td_biblio.factories.abstract_human import AbstractHumanFactory
from td_biblio.models import Editor


class EditorFactory(AbstractHumanFactory):
    class Meta:
        model = Editor
