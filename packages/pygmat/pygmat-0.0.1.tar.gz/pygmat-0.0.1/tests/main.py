
import pandas as pd
from  api.pygmat import SPACECRAFT, GROUND_STATION, FORCE_MODEL, PROPAGATOR, ECLIPSE_LOCATOR, CONTACT_LOCATOR
import api.pygmat as gmat
import os

output_path = './output/golds/'
try:
    os.path.isdir(output_path)
except:
    os.mkdir(output_path)

spc_list = pd.read_csv('input/golds/spacecraft_golds.csv')

for i in range(len(spc_list)):
    spacecraft = SPACECRAFT()
    name = spc_list.satellite[i]
    spacecraft.SMA = spc_list.sma[i]
    spacecraft.ECC = spc_list.ecc[i]
    spacecraft.INC = spc_list.inc[i]
    spacecraft.RAAN = spc_list.raan[i]
    spacecraft.AOP = spc_list.aop[i]
    spacecraft.TA = spc_list.ta[i]
    spacecraft.DryMass = spc_list.dryMass[i]
    spacecraft.write_script(f'{output_path}0_spc_{name}.txt',name=f'{name}')


gst_list = pd.read_csv('input/golds/groundstation_golds.csv')

for i in range(len(gst_list)):
    groundStation = GROUND_STATION()
    name = gst_list.groundStation[i]
    groundStation.Location1 = gst_list.latitude[i]
    groundStation.Location2 = gst_list.longitude[i]
    groundStation.Location3 = gst_list.height[i]
    groundStation.write_script(f'{output_path}1_gst_{name}.txt',name=f'{name}')

forceModel = FORCE_MODEL()
forceModel.write_script(f'{output_path}200_fm_example.txt')

propagator = PROPAGATOR()
propagator.write_script(f'{output_path}300_pr_example.txt')

eclipse = ECLIPSE_LOCATOR()
for i in range(len(spc_list)):
    eclipse.Spacecraft = spc_list.satellite[i]
    eclipse.Filename = f"\'{eclipse.Spacecraft}_ecl.txt\'"
    eclipse.write_script(f'{output_path}4_ecl_{eclipse.Spacecraft}.txt')

all_gst = gst_list.groundStation.tolist()
all_gst = ','.join(all_gst)

contact = CONTACT_LOCATOR()
for i in range(len(spc_list)):
    contact.Observers = "{"+all_gst+"}"
    contact.Target = spc_list.satellite[i]
    contact.Filename = f"\'{contact.Target}_contact.txt\'"
    contact.write_script(f'{output_path}5_cnt_{contact.Target}.txt')
    
all_spc = spc_list.satellite.tolist()
all_spc = ','.join(all_spc)

gmat.mission_sequence(
    path_to_file=f"{output_path}999_mission_sequence.txt",
    spacecrafts=all_spc,
    ref_sat="CBERS4A",
    time=1
)

gmat.write_script(
    includes=output_path
)

print(f'SUCCESS')