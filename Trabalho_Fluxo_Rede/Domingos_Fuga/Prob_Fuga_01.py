#!/usr/bin/env python
# coding: utf-8

# Universidade Estadual do Cear - UECE 
# Programa de Pós-graduação em Ciência da Computação
# Otimização em Grafos 2021.1

# O problema da Fuga
# Domingos Bruno Sousa Santos

import networkx 
import matplotlib.pyplot as plt
from networkx.algorithms.flow import edmonds_karp


# Função para gerar o grafo modificado como proplema de fluxo máximo
def geraGrafo(len_grid, coord_part):

    grafoT = networkx.DiGraph()

    nx = len_grid # Largura do grid
    ny = len_grid # Altura do grid

    # Ordenando as coordenadas de partidas
    coord_part = sorted(coord_part)
    
    #adicionand os vértices S e T
    grafoT.add_node('S')
    grafoT.add_node('T')

    #criando os vértices do grid já duplicados e com as arestas Vin-Vout
    for i in range(1, nx + 1):
        for j in range(1, ny + 1):
            grafoT.add_node(str(i) + '-' + str(j) + '-IN')
            grafoT.add_node(str(i) + '-' + str(j) + '-OUT')
            grafoT.add_edge(str(i) + '-' + str(j) + '-IN', str(i) + '-' + str(j) + '-OUT', capacity=1.0)

            
    
    #arestas de origem S para pontos de fuga
    for cord in coord_part:
        grafoT.add_edge('S', str(cord[0])+'-'+str(cord[1])+'-IN', capacity=1.0)
        

    #Demais arestas do grid
    for i in range(1, nx + 1):
        for j in range(1, ny + 1):
            if( i > 1 and i <= nx and j > 1 and j <= ny):
                grafoT.add_edge(str(i - 1) + '-' + str(j) + '-OUT', str(i) + '-' + str(j) + '-IN', capacity=1.0)
                grafoT.add_edge(str(i) + '-' + str(j) + '-OUT', str(i - 1) + '-' + str(j) + '-IN', capacity=1.0)
                grafoT.add_edge(str(i) + '-' + str(j - 1) + '-OUT', str(i) + '-' + str(j) + '-IN', capacity=1.0)
                grafoT.add_edge(str(i) + '-' + str(j) + '-OUT', str(i) + '-' + str(j - 1) + '-IN', capacity=1.0)

    for i in range(1, nx):
        grafoT.add_edge(str(1) + '-' + str(i) + '-OUT', str(1) + '-' + str(i + 1) + '-IN', capacity=1.0)
        grafoT.add_edge(str(1) + '-' + str(i + 1) + '-OUT', str(1) + '-' + str(i) + '-IN', capacity=1.0)
        grafoT.add_edge(str(i) + '-' + str(1) + '-OUT', str(i + 1) + '-' + str(1) + '-IN', capacity=1.0)
        grafoT.add_edge(str(i + 1) + '-' + str(1) + '-OUT', str(i) + '-' + str(1) + '-IN', capacity=1.0)


    #arestas das bordas para T
    for i in range(1, nx + 1):
        grafoT.add_edge(str(1) + '-' + str(i) + '-OUT', 'T', capacity=1.0)
        grafoT.add_edge(str(i) + '-' + str(1) + '-OUT', 'T', capacity=1.0)
        grafoT.add_edge(str(nx) + '-' + str(i) + '-OUT', 'T', capacity=1.0)
        grafoT.add_edge(str(i) + '-' + str(nx) + '-OUT', 'T', capacity=1.0)

    print("Nós:", grafoT.nodes)
    print("")
    print("Arestas: ", grafoT.edges)

    pos = networkx.spring_layout(grafoT)
    networkx.draw_networkx_nodes(grafoT, pos)
    networkx.draw_networkx_labels(grafoT, pos)
    networkx.draw_networkx_edges(grafoT, pos, edge_color='r', arrows = True)
    plt.show()
    
    return grafoT


# Função para  fornecer uma lista com os  𝑚  caminhos disjuntos, caso o grid permita fura
def pathFlow(flow_dic, cord_part, len_grid):
    
    list_path_flow = []
    
    for coord in cord_part:
        path_flow = []
        path_flow.append(coord) # Ponto de partida
        # Verificar se a coordenada de escape ta na borda do gride
        if coord[0] == 1 or coord[1] == 1 or coord[0] == len_grid or coord[1] == len_grid:
            path_flow.append(coord)
        
        else:
            pont_part = str(coord[0])+'-'+str(coord[1])+'-OUT'
            aux = True
            out_flow = list(flow_dic[pont_part])
            # Pegando as rotas de saida de cada ponto de partida
            while aux:
                for i in  out_flow:
                    if int(flow_dic[pont_part][i]) == 1:
                        b = i.split('-')
                        c = [int(b[0]), int(b[1])]
                        path_flow.append(c)
                # Atualizando as chaves 
                out_flow = list(flow_dic[str(c[0])+'-'+str(c[1])+'-OUT'])
                pont_part = str(c[0])+'-'+str(c[1])+'-OUT'
                if c[0] == 1 or c[1] == 1 or c[0] == len_grid or c[1] == len_grid:
                    aux = False
        list_path_flow.append(path_flow)
    return list_path_flow


# Exemplo da figura (a) da imagem de exemplo do problema de Fuga


# Criando o grafo modificado
# Coordenadas de partidas
cord_part = [ [2, 2], [2, 4], [2, 6], [3, 1], [3, 2], [3, 4], [3, 6], [4, 2], [4, 4], [4, 6] ]
len_grid = 6  # Tamannho do grid (len_grid x len_grid)
grafo_01 = geraGrafo(len_grid, cord_part) # Gerando o grafo de fluxo

# Calculando o Fluxo maximo
flow_value, flow_dict = networkx.maximum_flow(grafo_01, "S", "T")
print(flow_value)
print(flow_dict)


# Se o fluxo maximo tiver a mesma quantiade que os pontos de partidas (Tem solução)
if int(flow_value) == len(cord_part):
    caminho = pathFlow(flow_dict, cord_part, len_grid)
    caminho = sorted(caminho)
    for cam in caminho:
        print(cam)
else:
    print("Não tem solução")

