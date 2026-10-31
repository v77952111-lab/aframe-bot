import math
def calculate_geometry(width, length, height, loft_height):
 angle = math.atan(height / (width / 2))
 rafter = math.sqrt((width / 2) ** 2 + height ** 2)
 floor_area = width * length
 loft_width = width * (1 - loft_height / height)
 loft_area = loft_width * length
 roof_area = 2 * rafter * length
 gable_area = width * height
 return {
    "width": width,
    "length": length,
    "height": height,
    "loft_height": loft_height,
    "loft_width": loft_width,
    "angle_deg": math.degrees(angle),
    "rafter_length": rafter,
    "floor_area": floor_area,
    "loft_area": loft_area,
    "roof_area": roof_area,
    "gable_area": gable_area
}