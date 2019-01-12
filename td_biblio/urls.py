# -*- coding: utf-8 -*-
from django.conf.urls import url

import td_biblio.views.entry_batch_import
import td_biblio.views.entry_list
import td_biblio.views.find_duplicated_authors
from . import views

app_name = "td_biblio"
urlpatterns = [
    # Entry List
    url("^$", td_biblio.views.entry_list.EntryListView.as_view(),
        name="entry_list"),
    url("^import/$", td_biblio.views.entry_batch_import.EntryBatchImportView
        .as_view(), name="import"),
    url("^duplicates/$", td_biblio.views.find_duplicated_authors
        .FindDuplicatedAuthorsView.as_view(), name="duplicates"),
]
