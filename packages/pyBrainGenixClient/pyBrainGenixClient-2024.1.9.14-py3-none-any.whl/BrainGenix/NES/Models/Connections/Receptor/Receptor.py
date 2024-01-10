# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler

import BrainGenix.LibUtils.GetID


class Receptor:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = _Configuration.Name
        self.RequestHandler = _RequestHandler
        

        # Create Box On Server
        SourceCompartmentID = BrainGenix.LibUtils.GetID.GetID(_Configuration.SourceCompartment)
        DestinationCompartmentID = BrainGenix.LibUtils.GetID.GetID(_Configuration.DestinationCompartment)
        ReceptorLocation = json.dumps(_Configuration.ReceptorLocation_um)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Connection/Receptor/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&SourceCompartmentID={SourceCompartmentID}&DestinationCompartmentID={DestinationCompartmentID}&Conductance_nS={_Configuration.Conductance_nS}&TimeConstant_ms={_Configuration.TimeConstant_ns}&ReceptorLocation_um={ReceptorLocation}")
        assert(Response != None)
        self.ID = Response["ReceptorID"]