# -*- coding: utf-8 -*-
from django.conf.urls import url

from td_biblio.views.entry_batch_import import EntryBatchImportView
from td_biblio.views.entry_list import EntryListView
from td_biblio.views.find_duplicated_authors import FindDuplicatedAuthorsView


app_name = "td_biblio"
urlpatterns = [
    # Entry List
    url("^$", EntryListView.as_view(), name="entry_list"),
    url("^import/$", EntryBatchImportView.as_view(), name="import"),
    url("^duplicates/$", FindDuplicatedAuthorsView.as_view(),
        name="duplicates"),
]
