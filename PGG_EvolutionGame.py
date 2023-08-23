import random
from Player import *

# # M = 1
# RT = 3
# G1 = 6000
# G2 = 2000
# # cost
c = 1
# r = 2####
class Evolution():
    # 公共品博弈参数
    def __init__(self, NOCs_obj, In_r):
        self.NOCs_obj = NOCs_obj
        self.r = In_r
        print("传入的r:{}".format(self.r))
        # 收入

    def get_PlayerPayoff(self):
        fig_NP = plt.figure()

        G = self.NOCs_obj.NOCs
        Nlist = []
        Plist = []
        GPlist = []
        AcPlist = []
        for i in range(self.NOCs_obj.Node_num):
            Nlist.append(i)
            Plist.append(G.nodes[i]["AccPayoffs"])
            GPlist.append(G.nodes[i]["GBPP"])
        for i in range(self.NOCs_obj.Node_num):
            AcPlist.append(G.nodes[i]["GBPP"])
            if G.nodes[i]["strategy"]:
                AcPlist[i] -= c
            for j in G.adj[i]:
                AcPlist[i] += G.nodes[j]["GBPP"]
            print("i:{},ACP：{}".format(i, AcPlist))
        print("nodes:{}".format(dict(G.nodes())))
        print("edges:{}".format(dict(G.edges())))
        print("Plist:{}".format(Plist))
        print("AcPlist:{}".format(AcPlist))
        print("GPlist:{}".format(GPlist))

        plt.subplot(1, 2, 1)
        plt.ylabel("Player's Payoffs")
        plt.plot(Nlist, Plist, marker='o', ms=3, label="Payoffs")
        plt.plot(Nlist, AcPlist, marker='^', ms=3, label="AcPayoffs")
        plt.legend(loc='upper right')

        plt.subplot(1, 2, 2)
        plt.ylabel("Group's Payoffs")
        plt.plot(Nlist, GPlist, marker='o', ms=3, label="Group's Benefit Per Player")
        plt.legend(loc='upper right')
        plt.show()

    # -----------------更新策略方法-------------------- #
    def Strategy_Update(self, x, friends,fixed_flag):
        y = random.choice(friends)
        players = self.NOCs_obj.NOCs.nodes
        Px = players[x]['AccPayoffs']
        Py = players[y]['AccPayoffs']
        player_x = players[x]
        player_y = players[y]
        # 测试输出
        # print("Px:{}，Py:{}".format(Px,Py))
        Dx = self.NOCs_obj.NOCs.degree[x]
        Dy = self.NOCs_obj.NOCs.degree[y]

        if Py > Px:
            #M ensures the proper normalization and is given
            # by the maximum possible difference between the payoffs of x and y
            # Px,Py的最大的可能理论差值为M
            if fixed_flag:
                if Dx > Dy:
                    P_max = players[x]['P_max_pg'] * self.r
                    P_min = players[y]['P_min_pg'] *self.r - c*(Dy+1)
                else:
                    P_max = players[y]['P_max_pg'] * self.r
                    P_min = players[x]['P_min_pg'] * self.r - c*(Dx+1)
            else:
                if Dx > Dy:
                    P_max = players[x]['P_max_pg'] * self.r
                    P_min = players[y]['P_min_pg'] *self.r - c
                else:
                    P_max = players[y]['P_max_pg'] * self.r
                    P_min = players[x]['P_min_pg'] * self.r - c
            M = P_max-P_min

            UpdateProbability = (Py - Px) / M #更新概率
            # 测试输出
            # print("Py-Px: {}; M: {}; UpdateProbability: {}".format(Py - Px, M, UpdateProbability))
            if UpdateProbability > random.random(): # 注意这里是大于！
                player_x['new_strategy'] = player_y['strategy']
                return  # 执行遇到return时，函数就会执行完毕并将结果返回
        player_x['new_strategy'] = player_x['strategy']

    # -----一轮演化过程, 返回一代博弈后的合作者比例-------- #
    def Evolution_Game_Round(self,fixed_flag):
        NOCs = self.NOCs_obj.NOCs
        players = NOCs.nodes
        # 每轮演化之前都要清零一下累计支付！
        for id in range(self.NOCs_obj.Node_num):
            players[id]['AccPayoffs'] = 0
            # print("清零players[{}]['AccPayoffs']:{}".format(id,players[id]['AccPayoffs']))

        # -------------公共品博弈-------------- #
        if fixed_flag: # True,代表 fixed cost per game；False,代表 fixed cost per individual
            # print("PGGs——Fixed cost per game")
            #计算每个节点进行公共品博弈的累计收益
            for id in range(self.NOCs_obj.Node_num):
                players[id]['GBPP'] = 0 # Group Benefit Per Player
                # id号group博弈。合作者付出c，背叛者不付出。
                for friend in NOCs.adj[id]:
                    if players[friend]['strategy']:
                       players[friend]['AccPayoffs'] -= c
                       players[id]['GBPP'] += c
                # 如果我是C，那么公共池总收益也增加
                if players[id]['strategy']:
                    players[id]['AccPayoffs'] -= c  # fixed cost per game
                    players[id]['GBPP'] += c

                # 计算公共池内人均benefit, eta = r/(k+1)
                players[id]['GBPP'] = players[id]['GBPP'] * self.r / (NOCs.degree[id] + 1)
                # 公共池收益下发，分给“我”      和“我”邻居，计算博弈后的净收入
                players[id]['AccPayoffs'] += players[id]['GBPP']
                for friend in NOCs.adj[id]:
                    players[friend]['AccPayoffs'] += players[id]['GBPP']


        else:  # False,代表 fixed cost per individual
            # print("PGGs——Fixed cost per individual")
            # 计算每个节点进行公共品博弈的累计收益
            for id in range(self.NOCs_obj.Node_num):
                # print("博弈 {}号group开始-------------------------".format(id))
                # print("players[{}]['AccPayoffs']:{}".format(id,players[id]['AccPayoffs']))
                players[id]['GBPP'] = 0  # Group Benefit Per Player
                # 合作者付出c，背叛者不付出。
                for friend in NOCs.adj[id]:
                    if players[friend]['strategy']:
                        players[friend]['AccPayoffs'] -= (c / (NOCs.degree[friend] + 1))
                        # print("朋友{}号，合作  players[{}]['AccPayoffs']:{}".format(friend, friend, players[friend]['AccPayoffs']))
                        players[id]['GBPP'] += (c / (NOCs.degree[friend] + 1))
                # 如果我是C，那么我的Group中合作者数量+1,公共池总收益也增加
                if players[id]['strategy']:
                    players[id]['AccPayoffs'] -= (c / (NOCs.degree[id] + 1)) # fixed cost per individual
                    # print("我{}号，合作  players[{}]['AccPayoffs']:{}".format(id, id, players[id]['AccPayoffs']))
                    players[id]['GBPP'] += (c / (NOCs.degree[id] + 1))
                # 计算公共池内人均benefit, eta = r/(k+1)
                players[id]['GBPP'] = players[id]['GBPP'] * self.r / (NOCs.degree[id] + 1)
                # print("{}号池，人均收益{}".format(id,players[id]['GBPP']))

                # 公共池收益下发，分给“我”    和“我”邻居，计算博弈后的净收入
                players[id]['AccPayoffs'] += players[id]['GBPP']
                # print("我{}号，博弈后收益下发  players[{}]['AccPayoffs']:{}".format(id, id, players[id]['AccPayoffs']))
                for friend in NOCs.adj[id]:
                    players[friend]['AccPayoffs'] += players[id]['GBPP']
                    # print(
                    #     "朋友{}号，博弈后收益下发  players[{}]['AccPayoffs']:{}".format(friend, friend, players[friend]['AccPayoffs']))
        # 收入
        # self.get_PlayerPayoff()


        # --------策略更新-------- #
        #先将新策略记录下来
        for id in range(self.NOCs_obj.Node_num):
            friends = list(NOCs.adj[id])
            self.Strategy_Update(id, friends,fixed_flag)
        #策略更新，重新扫描并用新策略替换原策略
        Cer_num = 0
        for id in range(self.NOCs_obj.Node_num):
            players[id]['strategy'] = players[id]['new_strategy']
            if players[id]['strategy']:
                Cer_num += 1
        # print("C_n:{}".format(Cer_num))
        return  Cer_num / self.NOCs_obj.Node_num #返回合作者所占比例

    # 重复整个演化过程Repeat_Times次
    # 每次都是先进行Pre_Rounds轮数的前置演化以达到平衡状态，然后进行达到平衡后Balanced_Rounds轮数的演化
    # 对所有重复的演化过程，求合作者比例的均值
    def Evolution_Game_Process(self, _Pre_Rounds, _Balanced_Rounds, Repeat_Times,fixed_flag):
        FC = 0

        for repeat in range(Repeat_Times):
            print("RT : {}".format(repeat+1))
            self.NOCs_obj.Init_of_Nodes()


            # 前置演化博弈过程，保证到达博弈平衡状态
            break_flag = 0
            fc_flag = 0
            fc_tmp = 0
            Pre_Rounds = _Pre_Rounds
            Balanced_Rounds = _Balanced_Rounds
            # print('Balanced_Rounds')
            # print(Balanced_Rounds)
            for i in range(Pre_Rounds):
                # print(i)
                fcPR = self.Evolution_Game_Round(fixed_flag)
                if fcPR == 0 or fcPR == 1:
                    Pre_Rounds = i+1
                    Balanced_Rounds = 0
                    break_flag = 1
                    # print("break_flag = 1")
                    fc_tmp = fcPR
                    break
            print("已完成{}轮前置演化博弈".format(Pre_Rounds))


            # 达到平衡后的博弈过程
            if break_flag == 0 or Pre_Rounds == 0:
                # print(break_flag)
                # print(Balanced_Rounds)
                for i in range(Balanced_Rounds):
                    # print(Balanced_Rounds)
                    fcPR = self.Evolution_Game_Round(fixed_flag) #本轮fc
                    fc_tmp += fcPR  # 累计fc
                    if fcPR == 0 or fcPR == 1: #如果全合作 或者 全背叛，看作已经达到平衡 就停止演化（方便程序快速跑完）
                        Balanced_Rounds = i+1
                        # fc_tmp = (fc_tmp + fcPR * (_Balanced_Rounds - Balanced_Rounds)) / _Balanced_Rounds #计算本次跑（G1+G2）轮之后的fc
                        fc_tmp = fcPR
                        fc_flag = 1
                        break
                if fc_flag==0:
                    fc_tmp /= Balanced_Rounds #存在问题，见197行的修改
                # print("fcPR:{}".format(fcPR))

                print("已完成{}轮平衡后的博弈,本次整个演化博弈的合作者所占比例为：{}".format(Balanced_Rounds, fc_tmp))
            FC += fc_tmp
        FC /= Repeat_Times
        # print("Repeat_Times = {}, 合作者所占比例为：{}".format(Repeat_Times, FC))
        return FC






if __name__ == '__main__':
    random.seed(2022)
    RG = Build_Network('Regular_Ring_NOCs',NETWORK_SIZE,4)
    ev_RG = Evolution(RG, 'PD', 1.0)
    ev_RG.Evolution_Game_Process(1000,100,8)
    SF = Build_Network('Scale_Free_NOCs',NETWORK_SIZE,4)
    ev_SF = Evolution(SF, 'PD', 1.8)
    ev_SF.Evolution_Game_Process(1000, 100, 3)







