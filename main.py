from mp_api.client import MPRester
import pandas as pd

with MPRester("1cMv3nt6gzMHzWKFNNNHXJqkmmsf43T3") as mpr:
    docs = mpr.materials.summary.search(
        theoretical=False, num_elements=(2,10), band_gap=(13.0, 14.0)
    )

data = pd.DataFrame({
    'Formula':[],
    'MP_Calc_Bandgap':[],
    'Magnetic':[],
    'efermi':[],
    'Energy/atom': [],
    'Volume': [],
    'Density': [],
    'LP_A':[],
    'LP_B':[],
    'LP_C':[],
    'LP_angle1':[],
    'LP_angle2':[],
    'LP_angle3':[]
})

for material in docs:
    s=str(material.structure)
    lines = s.split('\n')
    abc_line = lines[2].strip()
    angles_line = lines[3].strip()
    abc_values = abc_line.split(':')[1].strip().split()
    angle_values = angles_line.split(':')[1].strip().split()    

    a = float(abc_values[0])  # 10.97563797
    b = float(abc_values[1])  # 5.1754324420857145
    c = float(abc_values[2])  # 7.207007895025302

    angle1 = float(angle_values[0])  # 49.82343523463095
    angle2 = float(angle_values[1])  # 90.0
    angle3 = float(angle_values[2]) 

    new_row = pd.DataFrame({'Formula':[material.formula_pretty],
    'MP_Calc_Bandgap':[material.band_gap],
    'Magnetic':[material.is_magnetic],
    'efermi':[material.efermi],
    'Energy/atom': [material.energy_per_atom],
    'Volume': [material.volume],
    'Density': [material.density],
    'LP_A':[a],
    'LP_B':[b],
    'LP_C':[c],
    'LP_angle1':[angle1],
    'LP_angle2':[angle2],
    'LP_angle3':[angle3]})
    data = pd.concat([data, new_row], ignore_index=True)

data.to_excel('data3.xlsx', index=False)
