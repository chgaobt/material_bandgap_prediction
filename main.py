from mp_api.client import MPRester
import pandas as pd

with MPRester("1cMv3nt6gzMHzWKFNNNHXJqkmmsf43T3") as mpr:
    docs = mpr.materials.summary.search(
        theoretical=False, num_elements=(2,10), band_gap=(0.01, 10)
    )

data = pd.DataFrame({
    'Formula': [],
    'Magnetic': [],
    'efermi': [],
    'Energy/atom': [],
    'Volume': [],
    'Density': [],
    'LP_A': [],
    'LP_B': [],
    'LP_C': [],
    'LP_angle1': [],
    'LP_angle2': [],
    'LP_angle3': [],
    'Crystal_System': [], 
    'Space_Group': [],
    'Point_Group': []
})

crysys_types = {"Monoclinic":0,"Trigonal":1,"Hexagonal":2,"Tetragonal":3, "Orthorhombic":4, "Cubic":5,"Triclinic":6}
pointgroup_types = {'422':0, '432':1, 'm':2, '23':3, '1':4, '4/mmm':5, '4':6, '3m':7, '-43m':8, '2':9, '-3m':10, 'm-3m':11, '6mm':12, '6/m':13, '-1':14, '-42m':15, '4mm':16, '222':17, 'm-3':18, '32':19, '-4':20, '-3':21, '2/m':22, '-6m2':23, '6':24, 'mmm':25, '4/m':26, '622':27, '6/mmm':28, '3':29, 'mm2':30, '-6':31}

for material in docs:
    s = str(material.structure)
    lines = s.split('\n')
    abc_line = lines[2].strip()
    angles_line = lines[3].strip()
    abc_values = abc_line.split(':')[1].strip().split()
    angle_values = angles_line.split(':')[1].strip().split()    

    a = float(abc_values[0])
    b = float(abc_values[1])
    c = float(abc_values[2])
    angle1 = float(angle_values[0])
    angle2 = float(angle_values[1])
    angle3 = float(angle_values[2])

    # Extract crystal system from symmetry data
    crystal_system = crysys_types[material.symmetry.crystal_system]  # Direct access
    space_group = material.symmetry.number
    point_group = pointgroup_types[material.symmetry.point_group]

    magnetic = 1 if material.is_magnetic else 0

    new_row = pd.DataFrame({
        'Formula': [material.formula_pretty],
        'Magnetic': [magnetic],
        'efermi': [material.efermi],
        'Energy/atom': [material.energy_per_atom],
        'Volume': [material.volume],
        'Density': [material.density],
        'LP_A': [a],
        'LP_B': [b],
        'LP_C': [c],
        'LP_angle1': [angle1],
        'LP_angle2': [angle2],
        'LP_angle3': [angle3],
        'Crystal_System': [crystal_system],
        'Space_Group': [space_group],
        'Point_Group': [point_group]
    })
    data = pd.concat([data, new_row], ignore_index=True)

data.to_excel('Numericalized_DS.xlsx', index=False)