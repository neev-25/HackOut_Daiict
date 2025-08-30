EFFECTS = {
    0: ["All clear. Normal operations."],
    1: ["Waterlogging possible on low-lying roads.", "Fisherfolk: check harbor conditions."],
    2: ["Shoreline flooding likely.", "Close schools in coastal ward.", "Suspend small craft operations."],
    3: ["Evacuate low-lying areas.", "Close coastal roads.", "Activate shelters."]
}


def choose_effects(severity: int):
    return EFFECTS.get(int(severity), EFFECTS[0])


# expects a list of GeoJSON features
def affected_features(all_features, severity: int):
    out = []
    for f in all_features:
        vuln = f.get('properties', {}).get('vulnerability', 'med')
        if severity >= 2 or (severity == 1 and vuln == 'high'):
            out.append(f)
    return out
