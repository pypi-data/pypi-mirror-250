# BrainGenix-NES
# AGPLv3

import json
import base64
import tqdm
import time

from . import Configuration

from BrainGenix.NES.Client import RequestHandler

import BrainGenix.LibUtils.ConfigCheck



class EM:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.RequestHandler = _RequestHandler
        self.SimulationID = _SimulationID

        # Run Configuration Check
        BrainGenix.LibUtils.ConfigCheck.ConfigCheck(_Configuration)

        # Create On Server
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/Initialize?SimulationID={_SimulationID}")
        assert(Response != None)

        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/SetupMicroscope?SimulationID={_SimulationID}&PixelResolution_nm={_Configuration.PixelResolution_nm}&ImageWidth_px={_Configuration.ImageWidth_px}&ImageHeight_px={_Configuration.ImageHeight_px}&SliceThickness_nm={_Configuration.SliceThickness_nm}&ScanRegionOverlap_percent={_Configuration.ScanRegionOverlap_percent}")
        assert(Response != None)



    ## Access Methods
    def DefineScanRegion(self, _Point1_um:list, _Point2_um:list):
        Point1 = json.dumps(_Point1_um)
        Point2 = json.dumps(_Point2_um)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/DefineScanRegion?SimulationID={self.SimulationID}&Point1_um={Point1}&Point2_um={Point2}")
        assert(Response != None)
        self.ScanRegionID = Response["ScanRegionID"]


    def QueueRenderOperation(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/QueueRenderOperation?SimulationID={self.SimulationID}&ScanRegionID={self.ScanRegionID}")
        assert(Response != None)
        return Response["StatusCode"]


    def GetRenderStatus(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetRenderStatus?SimulationID={self.SimulationID}")
        assert(Response != None)
        return Response
    

    def GetImageStack(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetImageStack?SimulationID={self.SimulationID}&ScanRegionID={self.ScanRegionID}")
        assert(Response != None)
        return Response["RenderedImages"]


    def GetImage(self, _ImageHandle:str):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetImage?SimulationID={self.SimulationID}&ImageHandle={_ImageHandle}")
        assert(Response != None)
        return bytes(Response["ImageData"], 'utf-8')
    

    def WaitForRender(self):

        # Setup Status Information
        StatusInfo:dict = self.GetRenderStatus()
        Bar = tqdm.tqdm("Rendering Image Stack", total=1)
        Bar.leave = True
        Bar.colour = "green"

        # Block Execution Until Render Finishes, Update Bar As We Wait
        while (StatusInfo["RenderStatus"] != 5):

            # Update Bar
            Bar.total = int(StatusInfo["TotalSlices"])
            Bar.n = max(int(StatusInfo["CurrentSlice"]), 0)
            Bar.refresh()
            Bar.set_description(f"Rendering Slice {StatusInfo['CurrentSlice']}/{StatusInfo['TotalSlices']}")

            # Get Status Info
            StatusInfo:dict = self.GetRenderStatus()

            # Wait, So We Don't Spam The API
            time.sleep(0.1)
        
        Bar.close()



    def SaveImageStack(self, _ImageStackDirectoryPrefix:str = "."):

        # Get Image Stack Manifest
        ImageHandles = self.GetImageStack()

        # Setup Progress Bar
        Bar = tqdm.tqdm("Downloading Image Stack", total=len(ImageHandles))
        Bar.leave = True
        Bar.colour = "green"


        for i in range(len(ImageHandles)):

            # Save This Image
            ImageData = self.GetImage(ImageHandles[i])
            with open(_ImageStackDirectoryPrefix + ImageHandles[i].split("/")[1], "wb") as FileHandler:
                FileHandler.write(base64.decodebytes(ImageData))

            Bar.set_description(f"Downloading Image {i}/{len(ImageHandles)}")

            # Count Up Bar
            Bar.n = i + 1
            Bar.refresh()

        Bar.close()