
import datetime
import os

class SPACECRAFT:
    def __init__(self):
        self.DateFormat = 'UTCGregorian'
        self.Epoch = "'01 Jan 2000 12:00:00.000'"
        self.CoordinateSystem = 'EarthMJ2000Eq'
        self.DisplayStateType = 'Keplerian'
        self.SMA = 7121.000000000004
        self.ECC = 0.004322600000000422
        self.INC = 24.9707
        self.RAAN = 25.52980000000001
        self.AOP = 91.59760000000064
        self.TA = 360
        self.DryMass = 850
        self.Cd = 2.2
        self.Cr = 1.8
        self.DragArea = 15
        self.SRPArea = 1
        self.SPADDragScaleFactor = 1
        self.SPADSRPScaleFactor = 1
        self.NAIFId = -10000001
        self.NAIFIdReferenceFrame = -9000001
        self.OrbitColor = 'Red'
        self.TargetColor = 'Teal'
        self.OrbitErrorCovariance = '[ 1e+70 0 0 0 0 0  0 1e+70 0 0 0 0  0 0 1e+70 0 0 0  0 0 0 1e+70 0 0  0 0 0 0 1e+70 0  0 0 0 0 0 1e+70 ]'
        self.CdSigma = 1e+70
        self.CrSigma = 1e+70
        self.Id = "'SatId'"
        self.Attitude = 'CoordinateSystemFixed'
        self.SPADSRPInterpolationMethod = 'Bilinear'
        self.SPADSRPScaleFactorSigma = 1e+70
        self.SPADDragInterpolationMethod = 'Bilinear'
        self.SPADDragScaleFactorSigma = 1e+70
        self.ModelFile = "'aura.3ds'"
        self.ModelOffsetX = 0
        self.ModelOffsetY = 0
        self.ModelOffsetZ = 0
        self.ModelRotationX = 0
        self.ModelRotationY = 0
        self.ModelRotationZ = 0
        self.ModelScale = 1
        self.AttitudeDisplayStateType = "'Quaternion'"
        self.AttitudeRateDisplayStateType = "'AngularVelocity'"
        self.AttitudeCoordinateSystem = "'EarthMJ2000Eq'"
        self.EulerAngleSequence = "'321'"

    def write_script(self,path_to_file,name='ExampleSC'):
        f = open(path_to_file,'w')

        f.write(f'Create Spacecraft {name};\n')
        
        for attr, value in self.__dict__.items():
            f.writelines(f'GMAT {name}.{attr} = {value};\n')

        f.close()

class GROUND_STATION:
        def __init__(self):
            self.CentralBody = 'Earth'
            self.StateType = 'Spherical'
            self.HorizonReference = 'Sphere'
            self.Location1 = -15.5
            self.Location2 = 303.99
            self.Location3 = 0
            self.Id = "'StationId'"
            self.IonosphereModel = "'None'"
            self.TroposphereModel = "'None'"
            self.DataSource = "'Constant'"
            self.Temperature = 295.1
            self.Pressure = 1013.5
            self.Humidity = 55
            self.MinimumElevationAngle = 7

        def write_script(self,path_to_file,name='ExampleGS'):
            f = open(path_to_file,'w')

            f.write(f'Create GroundStation {name};\n')

            for attr, value in self.__dict__.items():
                f.writelines(f'GMAT {name}.{attr} = {value};\n')

            f.close()

class FORCE_MODEL:
    def __init__(self) :
        self.CentralBody = 'Earth'
        self.PointMasses = '{Earth}'
        self.Drag = 'None'
        self.SRP = 'Off'
        self.RelativisticCorrection = 'Off'
        self.ErrorControl = 'RSSStep'

    def write_script(self,path_to_file,name='EarthPointProp_ForceModel'):
            f = open(path_to_file,'w')

            f.write(f'Create ForceModel {name};\n')

            for attr, value in self.__dict__.items():
                f.writelines(f'GMAT {name}.{attr} = {value};\n')

            f.close()

class PROPAGATOR:
    def __init__(self):
        self.FM = 'EarthPointProp_ForceModel'
        self.Type = 'RungeKutta89'
        self.InitialStepSize = 60
        self.Accuracy = 9.999999999999999e-12
        self.MinStep = 0.001
        self.MaxStep = 2700
        self.MaxStepAttempts = 50
        self.StopIfAccuracyIsViolated = 'true'

    def write_script(self,path_to_file,name='EarthPointProp'):
        f = open(path_to_file,'w')

        f.write(f'Create Propagator {name};\n')

        for attr, value in self.__dict__.items():
            f.writelines(f'GMAT {name}.{attr} = {value};\n')

        f.close()

class ECLIPSE_LOCATOR():
    def __init__(self):
        self.Spacecraft = 'SCD1'
        self.Filename = "'EclipseLocator1.txt'"
        self.OccultingBodies = "{Earth, Luna}"
        self.InputEpochFormat = "'TAIModJulian'"
        self.InitialEpoch = "'21545'"
        self.StepSize = 10
        self.FinalEpoch = "'21545.138'"
        self.UseLightTimeDelay = 'true'
        self.UseStellarAberration = 'true'
        self.WriteReport = 'true'
        self.RunMode = 'Automatic'
        self.UseEntireInterval = 'true'
        self.EclipseTypes = "{'Umbra', 'Penumbra', 'Antumbra'}"

    def write_script(self,path_to_file):
        f = open(path_to_file,'w')

        name = f'Eclipse_{self.Spacecraft}'

        f.write(f'Create EclipseLocator {name};\n')

        for attr, value in self.__dict__.items():
            f.writelines(f'GMAT {name}.{attr} = {value};\n')

class CONTACT_LOCATOR:
    def __init__(self):
        self.Target = 'SCD1'
        self.Filename = "'SCD1Contact.txt'"
        self.InputEpochFormat = "'TAIModJulian'"
        self.InitialEpoch = "'21545'"
        self.StepSize = 600
        self.FinalEpoch = "'21545.138'"
        self.UseLightTimeDelay = 'true'
        self.UseStellarAberration = 'true'
        self.WriteReport = 'true'
        self.RunMode = 'Automatic'
        self.UseEntireInterval = 'true'
        self.Observers = '{EMMN, ETA, ETC}'
        self.LightTimeDirection = 'Transmit'

    def write_script(self,path_to_file):
        f = open(path_to_file,'w')

        name = f'Contact{self.Target}'

        f.write(f'Create ContactLocator {name};\n')

        for attr, value in self.__dict__.items():
            f.writelines(f'GMAT {name}.{attr} = {value};\n')

        f.close()

def mission_sequence(path_to_file,propagator='EarthPointProp',spacecrafts="SCD1,SCD2,CBERS4A",time=1,ref_sat="SCD1"):
    f = open(path_to_file,'w')

    f.write('BeginMissionSequence;\n')
    f.writelines('Propagate \'defaultPropagator\' '+propagator+f'({spacecrafts})'+'{'+f'{ref_sat}.ElapsedDays = {time}'+'};')

    f.close()

def write_script(includes='./output/'):
    results = []
    results += [each for each in os.listdir(includes) if each.endswith('.txt')]

    file = open("./template.script","w")

    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    author = "@clgbatista"
    msg = "Full Script File"

    file.write("% General Mission Analysis Tool(GMAT) Script\n")
    file.write("% Created on : "+date_time+"\n")
    file.write("% Created by : "+author+"\n")

    file.write("\n")
    file.write("%----------------------------------------\n")
    file.write("%---------- "+msg+"\n")
    file.write("%----------------------------------------\n\n")

    results.sort()

    for i in results :
        file.write(f"#Include {includes}"+i+"\n\n")

    file.close()