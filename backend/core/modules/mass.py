# Centre of Mass calculations

mass = {
    'head': 0.08,
    'body': 0.46,
    'arm': 0.03,
    'arm_fore': 0.02,
    'thigh': 0.11,
    'shank': 0.05
}


def get_mass_all():
    return mass


def get_mass(part: str):
    if part in mass.keys():
        return mass[part]