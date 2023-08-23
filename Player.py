import networkx as nx  # 导入建网络模型包，命名nx
import matplotlib.pyplot as plt  # 导入科学绘图包，命名plt
import random

NETWORK_SIZE = 200
#生成网络
class Build_Network():
    def __init__(self, type, Node_num, aver_degree,c):
        self.Node_num = Node_num
        self.aver_degree = aver_degree
        self.type = type
        if type == 'Regular_Ring_NOCs':
            RG_Ring = nx.watts_strogatz_graph(self.Node_num, self.aver_degree, 0)  # （重连概率p=0）生成节点数为NETWORK_SIZE，平均度为k的规则环形图？
            self.NOCs = RG_Ring
            # print("已生成节点数为{}，平均度为{}的规则环形图".format(self.Node_num, self.aver_degree))
        elif type == 'Scale_Free_NOCs':
            m = int(aver_degree / 2)
            SF = nx.barabasi_albert_graph(self.Node_num, m)  # 生成一个有NETWORK_SIZE个节点，每次加入m条边的无标度网络
            self.NOCs = SF
            # print("已生成节点数为{}，每次加边为{},平均度为{}的无标度网络".format(self.Node_num, m, self.aver_degree))
        players = self.NOCs.nodes
        D = self.NOCs.degree
        friends = self.NOCs.adj
        # 计算理论最大最小支付
        z = aver_degree
        for id in range(self.Node_num):
            # 理论最大支付——节点为D，所参与的公共池全是C
            # 理论最小支付——节点是C，所参与的公共池全是D
            players[id]['P_max_pg'] = 0  # Fixed cost per game (缩放了eta倍，使用时还需乘以eta)
            players[id]['P_max_pi'] = 0  # Fixed cost per individual  (缩放了eta倍，使用时还需乘以eta,再减去c*(D[id]+1))
            players[id]['P_min_pg'] = 0  # Fixed cost per game       (缩放了eta倍，使用时还需乘以eta)
            players[id]['P_min_pi'] = 0  # Fixed cost per individual   (缩放了eta倍，使用时还需乘以eta,再减去c)
            CP = 0
            for f in friends[id]:
                players[id]['P_max_pg'] += D[f]*c/(D[f]+1) #邻居f池子给我的支付
                players[id]['P_min_pg'] += c/(D[f]+1) #邻居f池子给我的支付

                players[id]['P_max_pi'] += c / (D[f] + 1)  #邻居f池子，邻居f投入的支付
                players[id]['P_min_pi'] += c/(D[id]+1)/(D[f] + 1) #邻居f池子给我的支付
                for ff in friends[f]:
                    players[id]['P_max_pi'] += c / (D[ff] + 1) #邻居f池子，邻居f的邻居ff投入的支付

                players[id]['P_max_pi'] = players[id]['P_max_pi']  / (D[f]+1) #邻居f池子给我的支付
                CP += c / (D[f] + 1)  #我id的池子,邻居f投入的支付

            players[id]['P_max_pg'] += D[id]*c/(D[id]+1) #我id的池子给我的支付
            players[id]['P_min_pg'] += c/ (D[id] + 1) #我id的池子给我的支付

            players[id]['P_max_pi'] += CP/(D[id]+1) #我id的池子给我的支付
            players[id]['P_min_pi'] += c / (D[id] + 1)/ (D[id] + 1)  # 我id的池子给我的支付
        # # ----------- 绘图 ----------#
        # G = self.NOCs
        # pos_cir = nx.circular_layout(G)  # positions for all nodes
        # print("G.degree:{}".format(G.degree))
        # d = dict(G.degree)
        # print("dict(G.degree:{})".format(d))
        #
        # nx.draw(G,
        #         node_color=['blue' if self.NOCs.nodes[i]['strategy'] else 'red' for i in range(Node_num)],
        #         with_labels=True,
        #         node_size= [v*10 for v in d.values()],
        #         edge_color=[random.random() for i in range(len(G.edges))],
        #         width=3,
        #         cmap=plt.cm.Dark2,  # matplotlib的调色板，可以搜搜，很多颜色呢
        #         edge_cmap=plt.cm.Blues
        #         )
        # plt.show()



        # self.Init_of_Nodes()
    # def __str__(self):
    #     return ("已生成节点数为{}，平均度为{}的规则环形图".format(self.Node_nums,self.aver_degree))
    # 配置节点的策略、累计支付属性
    def Configure_Player(self,index,strategy, AccPayoffs=0):
        self.NOCs.nodes[index]['strategy'] = strategy
        self.NOCs.nodes[index]['new_strategy'] = strategy
        self.NOCs.nodes[index]['AccPayoffs'] = AccPayoffs
        # print("{}节点的属性为：{}".format(index, self.NOCs.nodes[index]))

    # 随机设置网络中的节点的策略，并使得最终两种策略的数量各占总结点数的1/2
    def Init_of_Nodes(self):
        C_num = 0  # 合作者的数量初始化为0
        D_num = 0  # 背叛者的数量初始化为0
        Stra = True
        arr = [False] * self.Node_num  # 创建一个大小为n的数组，并初始化为False
        indices = random.sample(range(self.Node_num), int(self.Node_num / 2))  # 生成一半Node_num随机不重复的索引
        for i in indices:
            arr[i] = True  # 将相应的索引位置设置为True

        for i in range(self.Node_num):
            # if max(C_num, D_num) < self.Node_num / 2:
            #     Stra = True if random.random() > 0.5 else False
            #     if Stra:
            #         C_num = C_num + 1
            #     else:
            #         D_num = D_num + 1
            # elif C_num == self.Node_num / 2:
            #     # print("C_num = {}".format(C_num))
            #     Stra = False
            #     D_num = D_num + 1
            # elif D_num == NETWORK_SIZE / 2:
            #     # print("D_num = {}".format(D_num))
            #     Stra = True
            #     C_num = C_num + 1
            # self.Configure_Player(i, Stra)  # 给节点i增加strategy属性
            if arr[i] == True:
                C_num += 1
            self.Configure_Player(i, arr[i])  # 给节点i增加strategy属性
        print("已完成{}的节点的属性配置，其中合作者数量为：{}".format(self.type, C_num))

 # ----------- 绘图 ----------#
 #        G = self.NOCs
 #        pos_cir = nx.circular_layout(G)  # positions for all nodes
 #        print("G.degree:{}".format(G.degree))
 #        d = dict(G.degree)
 #        print("dict(G.degree:{})".format(d))
 #
 #        nx.draw(G,
 #                node_color=['blue' if self.NOCs.nodes[i]['strategy'] else 'red' for i in range(self.Node_num)],
 #                with_labels=True,
 #                node_size= [v*10 for v in d.values()],
 #                edge_color=[random.random() for i in range(len(G.edges))],
 #                width=3,
 #                cmap=plt.cm.Dark2,  # matplotlib的调色板，可以搜搜，很多颜色呢
 #                edge_cmap=plt.cm.Blues
 #                )
 #        plt.show()

# class Player():
#     def __init__(self, index, strategy, AccPayOffs = 0):
#         self.index = index

# for k in [4,16,32,64]:
#     print("k={}:".format(k))
#     RG_Ring =nx.watts_strogatz_graph(NETWORK_SIZE,k,0) #（重连概率p=0）生成节点数为NETWORK_SIZE，平均度为k的规则环形图？
#     C_num = 0
#     # # 绘制规则环形网络
#     # ps = nx.shell_layout(RG_Ring)  # 布置框架
#     # nx.draw(RG_Ring, ps, with_labels=False, node_size=30)
#     # plt.show()
#     for i in range(NETWORK_SIZE):
#         if C_num < NETWORK_SIZE/2:
#             Stra = True if random.random() > 0.5 else False
#             if Stra== True:
#                 C_num = C_num + 1
#         else:
#             Stra = False
#         RG_Ring.nodes[i]['strategy'] = Stra # 给节点i增加strategy属性

# #生成无标度网络
# class Scale_Free_NOCs():
#     def __init__(self, Node_nums,aver_degree):
#         for m in [2,8,16,32]:
#             print("k={}:".format(2*m))
#             SF = nx.barabasi_albert_graph(NETWORK_SIZE, m) # 生成一个有m个节点，每次加入m条边的无标度网络
#             C_num = 0
#             # # 绘制无标度网络
#             # ps = nx.shell_layout(SF)  # 布置框架
#             # nx.draw(SF, ps, with_labels=False, node_size=30)
#             # plt.show()
#             for i in range(NETWORK_SIZE):
#                 if C_num < NETWORK_SIZE/2:
#                     Stra = True if random.random() > 0.5 else False
#                     if Stra== True:
#                         C_num = C_num + 1
#                 else:
#                     Stra = False
#                 SF.nodes[i]['strategy'] = Stra # 给节点i增加strategy属性


# if __name__ == '__main__':
    # random.seed(2022)
    # for k in [4, 16, 32, 64]:
    #     RG = Regular_Ring_NOCs(NETWORK_SIZE, k)  # 实例化Regular_Ring_NOCs类
    #     C_num = 0  # 合作者的数量初始化为0
    #     D_num = 0  # 背叛者的数量初始化为0
    #     Stra = True
    #     # 随机设置网络中的节点的策略，并使得最终两种策略的数量各占总结点数的1/2
    #     for i in range(NETWORK_SIZE):
    #         if max(C_num, D_num) < NETWORK_SIZE/2:
    #             Stra = True if random.random() > 0.5 else False
    #             if Stra:
    #                 C_num = C_num + 1
    #             else:
    #                 D_num = D_num + 1
    #         elif C_num == NETWORK_SIZE/2:
    #             # print("C_num = {}".format(C_num))
    #             Stra = False
    #             D_num = D_num + 1
    #         elif D_num == NETWORK_SIZE/2:
    #             # print("D_num = {}".format(D_num))
    #             Stra = True
    #             C_num = C_num + 1
    #         RG.Configure_Player(i, Stra)  # 给节点i增加strategy属性
    #     print(C_num)  # 仅用C_num= 0 做限制，无法满足每次合作者数量都=50，还有可能会＜50
    #     print(RG.NOCs.nodes[4]['AccPayoffs'])#获取节点4的AccPayoffs属性值
    #
