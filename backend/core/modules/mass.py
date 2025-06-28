# Centre of Mass calculations

mass_percent = {
    'head': 0.08,
    'body': 0.46,
    'arm': 0.03,
    'forearm': 0.02,
    'thigh': 0.11,
    'lowerleg': 0.05
}


def get_mass_all(weight):
    dict_mass = {
        part: weight * mass_percent[part] for part in mass_percent.keys()
    }
    dict_mass['total'] = weight
    return dict_mass


def get_mass(weight, part: str):
    if part in mass_percent.keys():
        return mass_percent[part] * weight
