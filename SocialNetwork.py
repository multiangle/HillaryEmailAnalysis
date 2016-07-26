__author__ = 'multiangle'

import os
import File_Interface as FI
import networkx as nx
import json

def generate_node_and_edge():
    pkl_list = os.listdir('.\static')
    node_list = {}
    edge_list = {}
    for path in pkl_list:
        info = FI.load_pickle('.\static\{x}'.format(x=path))
        # print(info)

        # 处理 From情况
        try:
            sender_mail = info['From']['mail']
        except:
            continue # 如果其中没有From 则该邮件作废
        sender_node = node_list.get(sender_mail)
        if sender_node:
            sender_node['send'] += 1
        else:
            node_list[sender_mail] = dict(
                mail = sender_mail,
                send = 1,
                receive = 0,
                cc = 0
            )
            if info.get('name'):
                node_list[sender_mail]['name'] = info['name']

        # 处理To情况
        receiver_list = info.get('To')
        if not receiver_list:
            continue
        for receiver in receiver_list:
            mail = receiver['mail']
            node = node_list.get(mail)
            if node:
                node['receive'] += 1
            else:
                node_list[mail] = dict(
                    mail = mail,
                    send = 0 ,
                    receive = 1,
                    cc = 0
                )
                if receiver.get('name'):
                    node_list[mail]['name'] = receiver['name']
            edge_key = sender_mail + '|----->' + mail
            edge = edge_list.get(edge_key)
            if edge:
                edge[2] += 1 # 如果该条边已经存在
            else:
                edge_list[edge_key] = [sender_mail,mail,1] #如果该条边不存在，则新加一条边

        # 处理CC的情况
        cc_list = info.get('CC')
        if cc_list:
            for cc in cc_list:
                mail = cc['mail']
                node = node_list.get(mail)
                if node:
                    node['cc'] += 1
                else:
                    node_list[mail] = dict(
                        mail = mail,
                        send = 0 ,
                        receive = 0 ,
                        cc = 1
                    )
                    if cc.get('name'):
                        node_list[mail]['name'] = cc['name']
                edge_key = sender_mail + '|----->' + mail
                edge = edge_list.get(edge_key)
                if edge:
                    edge[2] += 1 # 如果该条边已经存在
                else:
                    edge_list[edge_key] = [sender_mail,mail,1] #如果该条边不存在，则新加一条边
        print('{id} is dealed'.format(id=path))
    FI.save_pickle(node_list,'.\\temp_res\\node.pkl')
    FI.save_pickle(edge_list,'.\\temp_res\\edge.pkl')
    # G = nx.Graph()

def generate_data_for_gelphi():
    generate_node_and_edge()
    nodes = FI.load_pickle('.\\temp_res\\node.pkl')
    edges = FI.load_pickle('.\\temp_res\\edge.pkl')
    nodes = list(nodes.values())
    edges = list(edges.values())
    nodes_mail = [x['mail'] for x in nodes]
    # edges = [tuple(x) for x in edges]
    G = nx.Graph()
    G.add_nodes_from(nodes_mail)
    G.add_weighted_edges_from(edges)
    nx.write_gexf(G,'.\\temp_res\\data.gexf')




