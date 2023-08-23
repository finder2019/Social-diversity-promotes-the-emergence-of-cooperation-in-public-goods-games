def output2File(Graph_name, GameType, NS, M, RT, G1, G2,xpoint,ypoint,time):
    # with open(filename, wORa) as external_file:
    #     print(add_text, file=external_file)
    #     external_file.close()
    #  + '_M_' + str(M)
    with open('./' + 'result' + '/' + Graph_name + '_' + GameType + '_NS_' + str(NS) + '_M_' + str(M) + '_RT_' + str(RT) +
              '_G1_' + str(G1) + '_G2_'+ str(G2) + '_' + time + '.txt', 'w') as f:
        for i in range(len(ypoint)):
            f.write(str(xpoint[i]) + ' ' + str(ypoint[i]) + '\n')
    pass
# def output_visual():
#