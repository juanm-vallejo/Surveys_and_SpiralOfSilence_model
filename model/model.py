import random
import numpy
import wheelfunctions


class Environment:
    """
    Set the simulation environment
    """

    def __init__(self):
        self.comunitySize = 1000
        self.statusQuo = 1
        self.statusQuoWheight = 0.0 #Wheight of the status quo
        self.reach = 4 #Fixed Number of people reached inside the community
        self.network = [wheelfunctions.agentNetwork(a) for a in range(self.comunitySize)]
        self.surveyInterval = 4
        self.undecidedPer = 0.10
        self.sigmaNetwork = 0.05
        self.sigmaSurvey = 0.05

class Agent:
    """
     Handles people/agents acting in the simulation environment.
    """

    environment = None

    @classmethod
    def set_environment(cls, environment: Environment):
        cls.environment = environment
        

    def __init__(self):
        self.personality = wheelfunctions.normalization(numpy.random.normal(size= Agent.environment.comunitySize, loc = 5 ))
        self.ibd = [0.1, 0.5] #Initial Beliving Distribution
        self.ir = random.uniform(a = self.ibd[0], b=self.ibd[1]) # Aleatory intensity on the red political belief
        self.ib = random.uniform(a = self.ibd[0], b=self.ibd[1]) # Aleatory intensity on the blue political belief

        if random.random() >= Agent.environment.undecidedPer:
            if self.ir < self.ib:
                self.party = 0
                self.ir = 0
            else:
                self.party = 1
                self.ib = 0
        else:
            self.party = 2
            
        if Agent.environment.statusQuo == 0:
            self.socialir = self.ir * (Agent.environment.statusQuo) # Negative impact of the status quo
            self.socialib = self.ib * (1 + Agent.environment.statusQuo) #Positive impact of the status quo
        if Agent.environment.statusQuo == 1:
            self.socialib = self.ib * (Agent.environment.statusQuo) #Negative impact of the status quo
            self.socialir = self.ir * (1 + Agent.environment.statusQuo) #Positive impact of the status quo
        
        if self.party == 0:
            self.preassureB = self.socialib*10*(1 + random.choice(self.personality)) #Influence on other agents + personality
        if self.party == 1:
            self.preassureR = self.socialir*10*(1 + random.choice(self.personality)) #Influence on other agents + personality
        if self.party == 2:
            self.preassureB = self.socialib*10*(1 + random.choice(self.personality))
            self.preassureR = self.socialir*10*(1 + random.choice(self.personality))

class ManipulatedSurveys: #Surveys to maipulate the population thinking
    """
    Manipulated surveys impact
    """
    environment = None

    @classmethod
    def set_environment(cls, environment: Environment):
        cls.environment = environment

    def __init__(self):
        self.surveyb = random.uniform(a= 0.0, b= 0.55)
        self.surveyr = 1 - self.surveyb
        self.statusQuo = ManipulatedSurveys.environment.statusQuo
        self.statusQuoWheight = ManipulatedSurveys.environment.statusQuoWheight

        if (self.statusQuo == 0) & (self.surveyb < self.surveyr):#Arranging to get the status quo happy
            self.surveyrfinal = self.surveyr - ((self.surveyr - self.surveyb) * self.statusQuoWheight)
            self.surveybfinal = self.surveyb + (self.surveyr - self.surveyb) * self.statusQuoWheight
        if (self.statusQuo == 1) & (self.surveyb > self.surveyr):#Arranging to get the status quo happy
            self.surveyrfinal = (self.surveyb - self.surveyr) * self.statusQuoWheight + self.surveyr
            self.surveybfinal = self.surveyb - ((self.surveyb - self.surveyr) * self.statusQuoWheight)
        else: #The status quo is happy
            self.surveybfinal = self.surveyb
            self.surveyrfinal = self.surveyr

class Surveys: # real survey on the population.
    @classmethod
    def set_environment(cls, environment: Environment):
        cls.environment = environment

    def __init__(N):
        Nsurvey = N
        nsurvey = N #Sample "Survey"

class InfluenceMathInitial:
    @classmethod
    def set_environment(cls, environment: Environment):
        cls.environment = environment

    def __init__(self, network):
        network = network
        if network == None:
            self.var = wheelfunctions.AgentsVarIntensity(InfluenceMathInitial.environment.comunitySize , [Agent() for i in range(InfluenceMathInitial.environment.comunitySize)])
            self.partyList = self.var[0]
            self.intensityList = self.var[1]
            self.infPower =  self.var[2]
            self.newNetwork = InfluenceMathInitial.environment.network
            self.network = wheelfunctions.constructNetwork(self.newNetwork, self.partyList, self.intensityList, self.infPower, recursive=False)
        else:
            self.partyList = [i['Party'] for i in network]
            self.intensityList = [i['supIntensity'] for i in network]
            self.infPower =  [i['infPower'] for i in network]
            self.newNetwork = network
            self.network = wheelfunctions.constructNetwork(self.newNetwork, self.partyList, self.intensityList, self.infPower, recursive=False)

class ChangesMath: ## Set al the arithmetics to pass over every t on the network variable
    @classmethod
    def set_environment(cls, environment: Environment):
        cls.environment = environment

    def __init__(self, workingNetwork, surveyInfluence):
        check = lambda x:(ChangesMath.environment.sigmaSurvey if x != None else 0)
        surveyInf = check(surveyInfluence)
        network = workingNetwork
        self.sigmaNetwork = ChangesMath.environment.sigmaNetwork
        self.statusQuo = ChangesMath.environment.statusQuo
        self.quoWheight = ChangesMath.environment.statusQuoWheight

        ## Network influence

        self.Tnetwork = wheelfunctions.mathTimes(network, self.sigmaNetwork, self.statusQuo, self.quoWheight, surveyInf)