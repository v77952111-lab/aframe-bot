def estimate_materials(geo, insulation_mm):
 w, l = geo["width"], geo["length"]
 rafter = geo["rafter_length"]
 perim = 2 * (w + l)
 rafter_count = int(l / 0.6) + 1
 rafter_vol = rafter_count * rafter * 0.05 * 0.20
 stud_count = int(perim / 0.6) + 4
 stud_vol = stud_count * 3.0 * 0.05 * 0.15
 ins_m = insulation_mm / 1000
 insulation_vol = geo["roof_area"] * ins_m
 roofing = geo["roof_area"] * 1.15
 osb_roof = geo["roof_area"] * 1.05
 osb_floor = geo["floor_area"] * 1.1
 osb_gable = geo["gable_area"] * 1.1
 piles = int(perim / 2) + 1
 return {
    "Строп (50x200)": f"{rafter_vol:.2f} m3 ({rafter_count} шт)",
    "Стойки (50x150)": f"{stud_vol:.2f} m3 ({stud_count} шт)",
    "Утеплитель": f"{insulation_vol:.1f} m3",
    "Кровля": f"{roofing:.1f} m2",
    "OSB кровля": f"{osb_roof:.1f} m2",
    "OSB пол": f"{osb_floor:.1f} m2",
    "OSB фронтоны": f"{osb_gable:.1f} m2",
    "Сваи": f"{piles} шт"
}