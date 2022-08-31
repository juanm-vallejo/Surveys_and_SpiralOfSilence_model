## Check strategies of influence
## Changes on the status quo.
## Test the whole program


import model
from copy import deepcopy

from wheelfunctions import surveyInfluence


def main():
    env = model.Environment
    model.Agent.set_environment(env())
    model.ManipulatedSurveys.set_environment(env())
    model.InfluenceMathInitial.set_environment(env())
    model.ChangesMath.set_environment(env())

    # totalSurveys = []
    # surveys = 200
    # for q in surveys:
    #     survey = model.ManipulatedSurveys()
    #     results = [survey.surveyb, survey.surveyr]
    #     totalSurveys.append(results)
    # return(totalSurveys)

    model.InfluenceMathInitial(network=None).network
    interactions = [deepcopy(model.InfluenceMathInitial(network=None).network)]
    surveyResults = []
    for i in range(1000):
        surveyResults.append(model.ManipulatedSurveys().surveybfinal)
        y = interactions[i]
        if i == 0:
            x = y
        else: 
            x = model.ChangesMath(workingNetwork=y).Tnetwork
        interactions.append(deepcopy(x))

    return(interactions)
        
