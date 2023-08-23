import time

import matplotlib.pyplot as plt
import numpy as np
import random

from Player import Build_Network, NETWORK_SIZE
from PGG_EvolutionGame import Evolution,c
from output import output2File


#------------中间过程 可视化---------------#

M = 3         # 网络个数
RT = 4        # 重复次数
G1 = 20000    # 前置演化轮数
G2 = 2000     # 平衡轮数，用来取fc平均
z = 4         # 网络的度
NETWORK_SIZE = 200      #网络大小
# M = 2
# RT = 4
# G1 = 6000
# G2 = 1000
# z = 4

# M = 4
# RT = 5
# G1 = 6000
# G2 = 2000
# z = 4
if __name__ == '__main__':
    random.seed(25)
    fig = plt.figure()

    # 时间戳转换成时间字符串
    time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))

    xpoint = []
    ypoint = []

    _RG = []
    _SF = []
    for i in range(M):
        _RG.append(Build_Network('Regular_Ring_NOCs', NETWORK_SIZE, z,c))
        print("Regular_Ring_NOCs, PGGs, M_i={}".format(i))
        _SF.append(Build_Network('Scale_Free_NOCs', NETWORK_SIZE, z,c))
        print("Scale_Free_NOCs, PGGs,M_i={}".format(i))

    # #---------------固定每次博弈的合作成本-----------------------#
    # for graph in ['RG','SF']:
    #     xpoint.clear()
    #     ypoint.clear()
    #     if graph == 'RG':
    #         print("Regular_Ring_NOCs, PGGs——Fixed cost per game")
    #         for _eta in np.arange(0.2,1,0.05):
    #             fc = 0
    #             for RG in _RG:
    #                 Evol_RG_PGGs = Evolution(RG, _eta*(z+1))
    #                 fc += Evol_RG_PGGs.Evolution_Game_Process(G1, G2, RT,True)
    #             fc /= M
    #             print("graph: {}; eta: {}; fc:{} ".format(graph, _eta, fc))
    #             print("------------------------------------------------")
    #             xpoint.append(_eta)
    #             ypoint.append(fc)
    #     if graph == 'SF':
    #         print("Scale_Free_NOCs, PGGs——Fixed cost per game")
    #         for _eta in np.arange(0.2, 1, 0.05):
    #             fc = 0
    #             for SF in _SF:
    #                 Evol_SF_PGGs = Evolution(SF, _eta*(z+1))
    #                 fc += Evol_SF_PGGs.Evolution_Game_Process(G1, G2, RT,True)
    #             fc /= M
    #             print("graph: {}; eta: {}; fc:{} ".format(graph, _eta, fc))
    #             print("------------------------------------------------")
    #             xpoint.append(_eta)
    #             ypoint.append(fc)
    #
    #     # 输出结果，写入 result文件夹的相应.txt文件中
    #     output2File("{}".format(graph), "PGGs", NETWORK_SIZE, M, RT, G1, G2, xpoint, ypoint,time_str)
    #     ax1 = plt.subplot(2, 1, 1)
    #     plt.title("PGGs——Fixed cost per game")
    #     plt.ylabel("frequnency of cooperators")
    #     plt.plot(xpoint, ypoint, marker='o', ms=3, label="{}".format(graph))
    #     plt.legend(loc='upper right')

    # #测试
    # plt.show()

    # for graph in [ 'SF']:
    for graph in ['RG','SF']:

        xpoint.clear()
        ypoint.clear()
        # if graph == 'RG':
        #     print("Regular_Ring_NOCs, PGGs——Fixed cost per individual")
        #     for _eta in np.arange(0.2,1,0.05):
        #         fc = 0
        #         for RG in _RG:
        #             Evol_RG_PGGs2 = Evolution(RG, _eta*(z+1))
        #             fc += Evol_RG_PGGs2.Evolution_Game_Process(G1, G2, RT,False)
        #         fc /= M
        #         print("graph: {}; eta: {}; fc:{} ".format(graph, _eta, fc))
        #         print("------------------------------------------------")
        #         xpoint.append(_eta)
        #         ypoint.append(fc)

        if graph == 'SF':
            print("Scale_Free_NOCs, PGGs——Fixed cost per individual")
            for _eta in np.arange(0.2, 1, 0.05):
            # for _eta in np.arange(0.2, 1.15, 0.05):
                fc = 0
                for SF in _SF:
                    Evol_SF_PGGs2 = Evolution(SF, _eta*(z+1))
                    fc += Evol_SF_PGGs2.Evolution_Game_Process(G1, G2, RT,False)
                    #测试 输出收入
                    # Evol_SF_PGGs2.get_PlayerPayoff()

                fc /= M
                print("graph: {}; eta: {}; fc:{} ".format(graph, _eta, fc))
                print("------------------------------------------------")
                xpoint.append(_eta)
                ypoint.append(fc)


        # 输出结果，写入 result文件夹的相应.txt文件中
        output2File("{}".format(graph), "PGGs", NETWORK_SIZE, M, RT, G1, G2, xpoint, ypoint,time_str)
        ax1 = plt.subplot(2, 1, 2)
        plt.title("PGGs——Fixed cost per individual")
        plt.plot(xpoint, ypoint, marker='o', ms=3, label="{}".format(graph))
        plt.legend(loc='upper right')

    #

    plt.savefig('./result_visual/'+ "PGGs_RG&SF" +'_NS_' + str(NETWORK_SIZE) +'_M_'+ str(M) + '_RT_' + str(RT) +
              '_G1_' + str(G1) + '_G2_'+ str(G2) +'_'+time_str +'.png')
    plt.show()