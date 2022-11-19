# -*- coding: utf-8 -*-
# Copyright (c) 2020,
# Maaz Ali <maazali.se1947@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.


from Functions import *


class BibliometricEngine(object):
    def __init__(self, citations_file_path):
        self.data = process_citations(citations_file_path)

    def compute_impact_factor(self, dois, year):
        return do_compute_impact_factor(self.data, dois, year)

    def get_co_citations(self, doi1, doi2):
        return do_get_co_citations(self.data, doi1, doi2)

    def get_bibliographic_coupling(self, doi1, doi2):
        return do_get_bibliographic_coupling(self.data, doi1, doi2)

    def get_citation_network(self, start, end):
        return do_get_citation_network(self.data, start, end)
    
    def merge_graphs(self, g1, g2):
        return do_merge_graphs(self.data, g1, g2)

    def search_by_prefix(self, prefix, is_citing, dump):
        if dump is None:
            return do_search_by_prefix(self.data, prefix, is_citing)
        else:
            return do_search_by_prefix(dump, prefix, is_citing)

    def search(self, query, field, dump):
        if dump is None:
            return do_search(self.data, query, field)
        else:
            return do_search(dump, query, field)
    
    def filter_by_value(self, query, field, dump):
        if dump is None:
            return do_filter_by_value(self.data, query, field)
        else:
            return do_filter_by_value(dump, query, field)
        
