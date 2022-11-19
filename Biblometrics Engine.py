# -*- coding: utf-8 -*-
# Copyright (c) 2020, Maaz Ali <maazali.se1947@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#



import re
import pandas as pd

def process_citations(citations_file_path):
    column_name = ['citing', 'cited', 'creation', 'timespan'] # Headers in CSV file
    read_file = pd.read_csv(citations_file_path, usecols=column_name) # Read the CSV file by columns
    citing = read_file.citing.tolist()        # Citing column is stored in a list
    cited = read_file.cited.tolist()          # Cited column is stored in a list
    creation = read_file.creation.tolist()    # Creation column is stored in a list
    timespan = read_file.timespan.tolist()    # timespan column is stored in a list
    date_time=[]
    data=[]
    def convert_timespan_int(index):
        lst_int_timespan = []
        timespan_split= re.split('\D+',timespan[index])
        if len(timespan_split)==3:
            lst_int_timespan.append(int(timespan_split[1]))
        elif len(timespan_split)==4:
            lst_int_timespan.append(int(timespan_split[1]))
            lst_int_timespan.append(int(timespan_split[2]))
        else:
            lst_int_timespan.append(int(timespan_split[1]))
            lst_int_timespan.append(int(timespan_split[2]))
            lst_int_timespan.append(int(timespan_split[3]))
        return lst_int_timespan


    for i in range(len(creation)):
        int_timespan=convert_timespan_int(i)
        if len(creation[i])==4:
            date_time.append([int(creation[i])])
        elif len(creation[i])==7:
            i_split_lst=re.split('-', creation[i])
            date_time.append([int(i_split_lst[0]),int(i_split_lst[1])])
        elif len(creation[i])==10:
            i_split_lst=re.split('-', creation[i])
            date_time.append([int(i_split_lst[0]),int(i_split_lst[1]),int(i_split_lst[2])])
        data.append([date_time[i],citing[i],cited[i],creation[i], timespan[i],int_timespan])

    sorted_data= sorted(data, key = lambda x: x[0])
    return sorted_data

#print(process_citations('citations_sample.csv'))


def do_compute_impact_factor(data, dois, year):
    year=int(year)
    numerator=0
    denominator=0
    for i in range(len(data)):
        if data[i][0][0]==year and (data[i][2] in dois):
            numerator+=1
            if data[i][5][0]<2 or (data[i][5][0]== 2 and ((data[i][5][1]== None) or (data[i][5][1]== 0) and data[i][5][2]==None)):
                denominator += 1
    if denominator!=0 :
        impact_factor= numerator/denominator
        return impact_factor
    return "No document in set of DIOs is published in previous two years"
lst= ('10.1016/j.vaccine.2018.10.005','10.1080/14760584.2019.1639502','10.1056/nejmp1209051')
#print(do_compute_impact_factor(process_citations('citations_sample.csv'),lst,2019))

def do_get_co_citations(data, doi1, doi2):
    doi1_lst=[]
    doi2_lst=[]
    cited_together=0
    for i in range(len(data)):
        if data[i][2]==doi1:
            doi1_lst.append(data[i][1])
        elif data[i][2]==doi2:
            doi2_lst.append(data[i][1])

    for i in (doi1_lst):
        if i in doi2_lst:
            cited_together+=1
    return cited_together


#print(do_get_co_citations(process_citations('citations_sample.csv'),'10.1001/archpediatrics.2009.42','10.1016/s0140-6736(97)11096-0'))#

def do_get_bibliographic_coupling(data, doi1, doi2):
    dictio={}
    counter=0
    for i in range(len(data)):
        if data[i][1]==(str(doi1))or data[i][1]==str(doi2):
            if data[i][2] in dictio.keys():
                dictio[str(data[i][2])]= 2
                counter+=1
            else:
                dictio[str(data[i][2])]= 1
    return counter

#print(do_get_bibliographic_coupling(process_citations('citations_sample.csv'),"10.1097/mop.0000000000000929","10.1177/000313481107700711"))

def do_search_by_prefix(data, prefix, is_citing):
    lst_prefix=[]
    if is_citing==True:
        index= 1
    elif is_citing==False:
        index=2
    else:
        return None
    for i in range(len(data)):
        split_citation= re.split("/",data[i][index])
        if split_citation[0]==prefix:
            lst_prefix.append([data[i][1],data[i][2],data[i][3],data[i][4]])
    return lst_prefix

#print(do_search_by_prefix(process_citations('citations_sample.csv'),"10.2307",False))

def do_search(data, query, field):
    lst_search=[]
    query_updated=query.replace("*",".+").lower()
    if field.lower() =="citing":
        index=1
    elif field.lower()=="cited":
        index=2
    elif field.lower()=="creation":
        index=3
    elif field.lower()=="timespan":
        index=4
    else:
        return None

    for i in range(len(data)):
        if re.search(query_updated,data[i][index].lower()):
            lst_search.append([data[i][1],data[i][2],data[i][3],data[i][4]])
    return lst_search
#print(do_search(process_citations('citations_sample.csv'),"200*06*","creation"))
def do_filter_by_value(data, query, field):
    lst_search=[]
    if field.lower() =="citing":
        index=1
    elif field.lower()=="cited":
        index=2
    elif field.lower()=="creation":
        index=3
    elif field.lower()=="timespan":
        index=4
    else:
        return None

    for i in range(len(data)):
        if query.lower()== data[i][index].lower():
            lst_search.append([data[i][1],data[i][2],data[i][3],data[i][4]])
    return lst_search

#print(do_filter_by_value(process_citations('citations_sample.csv'),"1999-04","creation"))

def do_get_citation_network(data, start, end):
    start=int(start)
    end=int(end)
    my_graph = MultiDiGraph()
    for i in range(len(data)):
        if int(start)<= data[i][0][0]<=int(end):
            if len(data[i][0])==1:
                round_off_date= [data[i][0][0],12,31]
            elif len(data[i][0])==2:
                if data[i][0][1] <= 7 and data[i][0][1] != 2:
                    if data[i][0][1] % 2 == 0:
                        round_off_date = [data[i][0][0], data[i][0][1], 30]
                    else:
                        round_off_date = [data[i][0][0], data[i][0][1], 31]
                elif data[i][0][1] == 2:
                    if data[i][0][0] % 4 == 0:
                        round_off_date = [data[i][0][0], data[i][0][1], 29]
                    else:
                        round_off_date = [data[i][0][0], data[i][0][1], 28]
                else:
                    if data[i][0][1] % 2 == 0:
                        round_off_date = [data[i][0][0], data[i][0][1], 31]
                    else:
                        round_off_date = [data[i][0][0], data[i][0][1], 30]
            else:
                round_off_date= data[i][0]
            diffrence= datetime(round_off_date[0],round_off_date[1],round_off_date[2])-relativedelta(years=data[i][5][0],months=data[i][5][1],days=data[i][5][2])
            diffrence_new= str(diffrence)[:4]
            if start<=int(diffrence_new)<=end:
                my_graph.add_edge(data[i][1], data[i][2])


    return my_graph

def do_merge_graphs(data, g1, g2):
    new_graph= MultiDiGraph()
    nodes_g1=list(g1.nodes())
    nodes_g2= list(g2.nodes())
    edges_g1= list(g1.edges())
    length_g1_edges=len(edges_g1)-1
    edges_g2= list(g2.edges())
    length_g2_edges=len(edges_g2)-1
    if len(nodes_g1)>= len(nodes_g2):
        max_nodes= nodes_g1
        min_nodes= nodes_g2
    else:
        max_nodes= nodes_g2
        min_nodes= nodes_g1

    length_min_nodes= len(min_nodes)
    length_max_nodes= len(max_nodes)
    length_data= len(data)-1
    pointer_g1_edges=0
    pointer_g2_edges=0
    for i in range(length_max_nodes):
        if pointer_g1_edges<=length_g1_edges:
            new_graph.add_edge(edges_g1[i][0],edges_g1[i][1])
            pointer_g1_edges+=1

        if pointer_g2_edges<=length_g2_edges:
            new_graph.add_edge(edges_g2[i][0],edges_g2[i][1])
            pointer_g2_edges+=1
        for j in range(length_min_nodes):
            for k in range(length_data):
                if (data[k][1]==max_nodes[i] and data[k][2]==min_nodes[j]) or (data[k][2]==max_nodes[i] and data[k][1]==min_nodes[j]):
                    new_graph.add_edge(data[k][1], data[k][2])

    return new_graph

# g1=do_get_citation_network(process_citations('citations_sample.csv'),'2018','2021')
# g2=do_get_citation_network(process_citations('citations_sample.csv'),'2008','2014')
# do_merge_graphs(process_citations('citations_sample.csv'),g1,g2)


