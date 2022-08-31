import random

def sample(N):
    N = N
    confidence = 1.96
    margin = 0.05
    n = 0.5 #sample formula

def agentNetwork(i):
    i = i
    c = [i for i in range(1000)]
    random.shuffle(c)
    ## Support Intensity (own), Influential Power (on others), Network Influence(on agent), Surveys Influence (on agent), Total Influence
    dic = {i:[c[0], c[1], c[2], c[3]], 'Party': None ,'supIntensity':0, 'infPower':0 ,'networkInf': 0, 'surveysInf': 0, 'totalinf': 0}
    return(dic)

def surveyInfluence():
    pass


def normalization(data):
    data_norm = (data - data.min())/ (data.max() - data.min())
    return(data_norm)

def AgentsVarIntensity(comunitySize, networks):
    partyList = []
    intensityList = []
    powerList = []
    for i in range(comunitySize):  
        network = networks[i]      

        if ((network.party) == 0):
            partyList.append(0)
            intensityList.append(network.ib)
            powerList.append(network.preassureB)
        if ((network.party) == 1):
            intensityList.append(network.ir)
            partyList.append(1)
            powerList.append(network.preassureR)
        if ((network.party) == 2):
            intensityList.append([network.ir, network.ib])
            partyList.append(2)
            powerList.append([network.preassureR, network.preassureB])

    return(partyList, intensityList, powerList)

def constructNetwork(network, partyList, intensityList, infPower, recursive):
    network = network
    counter = 0
    recursive = recursive
    if recursive == False:
        for node in network:
            node['Party'] = partyList[counter]
            node['networkInf'] = infPower[counter]
            node['supIntensity'] = intensityList[counter]
            node['infPower'] = infPower[counter]
            counter = counter + 1
    else:
        pass

    c = 0
    for node in network:
        power = 0
        power1 = 0
        power2 = 0
        if node['Party'] != 2:
            for i in node[c]:
                if node['Party'] == network[i]['Party'] and network[i]['Party'] != 2:
                    power = power + network[i]['infPower']
                if node['Party'] != network[i]['Party'] and network[i]['Party'] != 2:
                    power = power - network[i]['infPower']
            node['networkInf'] = power
        else:
            for i in node[c]:
                if network[i]['Party'] == 0:
                    power1 = power + network[i]['infPower']
                if network[i]['Party'] == 1:
                    power2 = power + network[i]['infPower']
            node['networkInf'] = [power1, power2]
 
        c = c + 1

    return(network)

def networkChange(network, statusQuo):

    ## Works on the clustering and virtue signaling with the silence spiral. TEST
    
    c = 0
    for node in network:
        if (node['Party'] != statusQuo) and node['Party'] != 2:
            for i in node[c]:
                if (node['Party'] == network[i]['Party']):
                    nodeName = [node for node in network[i].keys()][0]
                    for j in network[nodeName][nodeName]:
                        infPowerPos = 0
                        if (network[i]['Party'] != 2) and network[i]['infPower'] > infPowerPos:
                            infPowerPos = network[i]['infPower']
                            winnerNodePos = j

            for i in node[c]:
                if node['Party'] != network[i]['Party']:
                    nodeName = [node for node in network[i].keys()][0]
                    infPowerNeg = 0
                    for k in node[c]:
                        if (network[k]['Party'] != 2) and network[k]['infPower'] > infPowerNeg:
                            infPowerNeg = network[k]['infPower']
                            winnerNodeNeg = i  
                    listCount = 0

                    for l in node[c]:
                        try:
                            if l == winnerNodeNeg:
                                node[c][listCount] = winnerNodePos ## Referenced before assignment check the loop winnerNodePos
                        except:
                            pass
                    listCount = listCount + 1
                    
        if (node['Party'] == statusQuo):
            for i in node[c]:
                if (node['Party'] != network[i]['Party']):
                    nodeName = [node for node in network[i].keys()][0]
                    for j in network[nodeName][nodeName]:
                        infPowerPos = 10000
                        if (network[i]['Party'] != 2) and network[i]['infPower'] < infPowerPos:
                            infPowerMin = network[i]['infPower']
                            winnerNodeMin = j

                if node['Party'] != network[i]['Party']:
                    nodeName = [node for node in network[i].keys()][0]
                    infPowerMax = 0
                    for k in node[c]:
                        if (network[k]['Party'] != 2) and network[k]['infPower'] > infPowerMax:
                            infPowerMax = network[k]['infPower']
                            winnerNodeMax = i
                    listCount = 0
                    for l in node[c]:
                        try:
                            if l == winnerNodeMax:
                                node[c][listCount] = winnerNodeMin
                        except:
                            pass
                    listCount = listCount + 1

        c = c + 1

    return(network)


def mathTimes(network, sigma, statusQuo, quoWheight, surveyInf):
    #modifies infpower and supintensity, then constructnetwork() finishes the changes
    surb = [surveyInf, 0]
    bigger = lambda x:(x if x[0] > (1- x[0]) else [1- x[0], 1])
    survey = bigger(surb)

    for node in network:
        if node['Party'] != 2 and node['networkInf'] < 0: ## add in each if the wheigh of the manipulated surveys
            if statusQuo == node['Party']:
                checker = lambda x:(x if node['Party'] == survey[1] else -x)
                sigmaSurvey = checker(0.05)
                node['infPower'] = node['infPower']/(1+quoWheight)/node['supIntensity']/10
                node['supIntensity'] = node['supIntensity'] - (sigma + abs(node['networkInf']*0.01) + sigmaSurvey)
                node['infPower'] = node['infPower']*(1+quoWheight)*node['supIntensity']*10
            if statusQuo != node['Party']:
                checker = lambda x:(x if node['Party'] == survey[1] else -x)
                sigmaSurvey = checker(0.05)
                node['infPower'] = node['infPower']/quoWheight/node['supIntensity']/10
                node['supIntensity'] = node['supIntensity'] - (sigma + abs(node['networkInf']*0.01) + sigmaSurvey)
                node['infPower'] = node['infPower']*quoWheight*node['supIntensity']*10

            if node['supIntensity'] < 0:
                node['supIntensity'] = abs(node['supIntensity'])
                node['infPower'] = abs(node['infPower'])
                func= (lambda: 0 if node['Party'] == 1 else 1) 
                node['Party'] = func()

        if node['Party'] == 2:
            if node['networkInf'][0] < 0:
                node['infPower'][0] = node['infPower'][0]/quoWheight/node['supIntensity'][0]/10
                node['supIntensity'][0] = node['supIntensity'][0] - (sigma + abs(node['networkInf'][0]*0.01))
                node['infPower'][0] = node['infPower'][0]*quoWheight*node['supIntensity'][0]*10
            if node['networkInf'][1] < 0: 
                node['infPower'][1] = node['infPower'][1]/quoWheight/node['supIntensity'][1]/10
                node['supIntensity'][1] = node['supIntensity'][1] - (sigma + abs(node['networkInf'][1]*0.01))
                node['infPower'][1] = node['infPower'][1]*quoWheight*node['supIntensity'][1]*10

            if node['networkInf'][0] > 0:
                node['supIntensity'][0] = node['supIntensity'][0] + (sigma + abs(node['networkInf'][0]*0.01))

            if node['networkInf'][1] > 0:
                node['supIntensity'][1] = node['supIntensity'][1] + (sigma + abs(node['networkInf'][1]*0.01))
            
            if node['supIntensity'][0]*0.7 > node['supIntensity'][1]:
                node['supIntensity'] = node['supIntensity'][0]
                node['networkInf'] = node['networkInf'][0] 
                node['infPower'] = node['infPower'][0]
                node['Party'] = 0
            else:
                if node['supIntensity'][1]*0.7 > node['supIntensity'][0]:
                    node['supIntensity'] = node['supIntensity'][1]
                    node['networkInf'] = node['networkInf'][1] 
                    node['infPower'] = node['infPower'][1]
                    node['Party'] = 1

        if node['Party'] != 2 and node['networkInf'] > 0:
            node['supIntensity'] = node['supIntensity'] + (sigma + abs(node['networkInf']*0.01))
    network = networkChange(network, statusQuo=statusQuo)
    
    network = constructNetwork(network=network, partyList=None, intensityList=None, infPower=None, recursive=True)

    return(network)

    # if operation == 'Survey Influence':
    #     for node in network:
    #         if (surveys[0] > surveys[1]) and (network['Party'] == 0):
    #             network['supIntensity'] = network['supIntensity'] + self.sigmaSurvey
    #         if (surveys[0] > surveys[1]) and (network['Party'] == 1):
    #             network['supIntensity'] = network['supIntensity'] - self.sigmaSurvey

    #         if (surveys[1] > surveys[0]) and (network['Party'] == 1):
    #             network['supIntensity'] = network['supIntensity'] + self.sigmaSurvey
    #         if (surveys[1] > surveys[0]) and (network['Party'] == 0):
    #             network['supIntensity'] = network['supIntensity'] - self.sigmaSurvey
