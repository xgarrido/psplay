from itertools import product


def get_tiles(layers):
    """ Fonction that converts a dictionary into a complete list of tiles """

    # Set color range
    vrange = [[-500, +500], [-100, +100], [-100, +100]]
    _range = layers.get("range")
    if _range:
        _val = _range.get("temperature")
        vrange[0] = [-_val, +_val] if _val else vrange[0]
        _val = _range.get("polarization")
        vrange[1] = [-_val, +_val] if _val else vrange[1]
        vrange[2] = vrange[1] if _val else vrange[2]
    for i, j in enumerate(["min", "max"]):
        _m = layers.get(j)
        if _m:
            _val = _m.get("temperature")
            vrange[0][i] = _val if _val else vrange[0][i]
            _val = _m.get("polarization")
            vrange[1][i] = _val if _val else vrange[1][i]
            vrange[2][i] = vrange[1][i] if _val else vrange[2][i]

    tags = layers.get("tags")
    tile_tmpl = layers.get("tile_tmpl")
    name_tmpl = layers.get("name_tmpl")

    tiles = []

    tile_dict = dict(x="{x}", y="{y}", z="{z}")
    name_dict = dict()

    keys = list(tags.keys())
    values = [value.get("values") for value in tags.values()]
    for value in product(*values):
        tag_id = 0
        for i, v in enumerate(value):
            tag = tags.get(keys[i])
            idx = tag.get("values").index(v)
            tag_id += idx * 10 ** i

            tile_dict.update({keys[i]: v})
            name_dict.update({keys[i]: v})
            if tag.get("substitutes"):
                name_dict.update({keys[i]: tag.get("substitutes")[idx]})

        url = tile_tmpl.format(**tile_dict)
        name = name_tmpl.format(**name_dict)
        # Hardcode temperature vs. polarization range
        value_min, value_max = vrange[0] if "T" in name_dict.values() else vrange[1]
        tiles += [
            dict(
                tag_id=tag_id,
                url=url,
                name=name,
                attribution=name,
                value_min=value_min,
                value_max=value_max,
            )
        ]

    return tiles


def get_keybindings(layers):
    tags = layers.get("tags")
    keybindings = {
        k: dict(keys=v.get("keybindings"), level=i, depth=len(v.get("values")))
        for i, (k, v) in enumerate(tags.items())
    }
    return keybindings
