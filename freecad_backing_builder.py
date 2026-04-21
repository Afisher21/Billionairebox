import FreeCAD as App
import Part

try:
    import FreeCADGui as Gui
except ImportError:
    Gui = None


DOC_NAME = "BillionaireBoxBacking"
SPREADSHEET_NAME = "BackingParams"
GROUP_NAME = "GeneratedBacking"


PARAM_SPECS = [
    # (alias, default_value, description, status)
    # status: MEASURED | ESTIMATED | DERIVED | STANDARD
    ("OverallWidth", "100 mm", "Outer width of the replacement backing.", "MEASURED"),
    ("OverallHeight", "163 mm", "Outer height of the replacement backing.", "MEASURED"),
    ("OverallDepth", "49 mm", "Total stand-off depth from the device body.", "MEASURED"),
    ("PerimeterWall", "2.25 mm", "Wall thickness around the open perimeter.", "MEASURED"),
    ("BackWall", "2.25 mm", "Thickness of the exterior back wall.", "MEASURED"),
    ("ScrewSideInset", "7.35 mm", "Inset of the left/right screw columns from the outside edges.", "DERIVED"),
    ("ScrewLeftBottomY", "20 mm", "Y position of the bottom-left screw boss center.", "MEASURED"),
    ("ScrewLeftMiddleY", "67.7 mm", "Y position of the middle-left screw boss center.", "MEASURED"),
    ("ScrewLeftTopY", "116.3 mm", "Y position of the top-left screw boss center.", "MEASURED"),
    ("ScrewRightBottomY", "20 mm", "Y position of the bottom-right screw boss center.", "MEASURED"),
    ("ScrewRightMiddleY", "85.8 mm", "Y position of the middle-right screw boss center.", "MEASURED"),
    ("ScrewRightTopY", "151.6 mm", "Y position of the top-right screw boss center.", "MEASURED"),
    ("ScrewThreadDiameter", "2.4 mm", "Clearance diameter for the screw threads.", "DERIVED"),
    ("ScrewHeadDiameter", "3.8 mm", "Diameter of the screw-head capture pocket.", "DERIVED"),
    ("ScrewDriverDiameter", "10 mm", "Access shaft diameter for a typical screwdriver.", "MEASURED"),
    ("ScrewInnerWeb", "2.5 mm", "Material left at the inside end so the screw head stays captured.", "DERIVED"),
    ("ScrewBossDiameter", "8 mm", "Outer diameter of the reinforced screw towers.", "DERIVED"),
    ("AACellDiameter", "14.5 mm", "Nominal AA battery diameter.", "STANDARD"),
    ("AACellLength", "50.5 mm", "Nominal AA battery length.", "STANDARD"),
    ("BatteryTrayX", "20 mm", "Left edge of the 3xAA tray footprint.", "ESTIMATED"),
    ("BatteryTrayY", "18 mm", "Bottom edge of the 3xAA tray footprint.", "ESTIMATED"),
    ("BatterySideClearance", "1.2 mm", "Side clearance around each AA cell.", "ESTIMATED"),
    ("BatteryEndClearance", "2.0 mm", "End clearance for the AA cells and contacts.", "ESTIMATED"),
    ("BatteryRailHeight", "16 mm", "Height of the battery tray rails above the interior back wall.", "ESTIMATED"),
    ("BatteryWallThickness", "2.2 mm", "Wall thickness for the battery tray rails.", "ESTIMATED"),
    ("BatteryDividerThickness", "2.0 mm", "Divider thickness between the three cells.", "ESTIMATED"),
    ("BatteryWireNotchWidth", "8 mm", "Wire exit notch in the battery tray.", "ESTIMATED"),
    ("MotorKeepoutX", "13 mm", "Left edge of the existing motor keep-out volume.", "DERIVED"),
    ("MotorKeepoutY", "108 mm", "Bottom edge of the existing motor keep-out volume (OverallHeight minus 48).", "DERIVED"),
    ("MotorKeepoutZ", "0 mm", "Distance from the device body to the keep-out start.", "MEASURED"),
    ("MotorKeepoutWidth", "55 mm", "Width of the motor keep-out box.", "MEASURED"),
    ("MotorKeepoutLength", "48 mm", "Height of the motor keep-out box.", "MEASURED"),
    ("MotorKeepoutHeight", "22 mm", "Depth of the motor keep-out box.", "MEASURED"),
    ("LegacyPCBX", "92 mm", "Left edge of the original PCB keep-out volume.", "ESTIMATED"),
    ("LegacyPCBY", "74 mm", "Bottom edge of the original PCB keep-out volume.", "ESTIMATED"),
    ("LegacyPCBZ", "4 mm", "Distance from the device body to the legacy PCB keep-out start.", "ESTIMATED"),
    ("LegacyPCBWidth", "28 mm", "Width of the original PCB keep-out box.", "MEASURED"),
    ("LegacyPCBLength", "22 mm", "Height of the original PCB keep-out box.", "MEASURED"),
    ("LegacyPCBHeight", "10 mm", "Depth of the original PCB keep-out box.", "MEASURED"),
    ("AddonPCBX", "20 mm", "Left edge of the new PCB tray.", "ESTIMATED"),
    ("AddonPCBY", "84 mm", "Bottom edge of the new PCB tray.", "ESTIMATED"),
    ("AddonPCBWidth", "40 mm", "Board width for the new PCB tray.", "MEASURED"),
    ("AddonPCBLength", "50 mm", "Board height for the new PCB tray.", "MEASURED"),
    ("AddonPCBThickness", "1.8 mm", "Board thickness for the new PCB tray.", "MEASURED"),
    ("AddonPCBTrayHeight", "5.5 mm", "Rail height for the new PCB tray.", "ESTIMATED"),
    ("AddonPCBClipWidth", "6 mm", "Width of each low-flex retaining clip.", "ESTIMATED"),
    ("AddonPCBClipInset", "1.0 mm", "Amount the retaining clip overlaps the board edge.", "ESTIMATED"),
    ("BreadboardX", "20 mm", "Left edge of the breadboard tray.", "ESTIMATED"),
    ("BreadboardY", "48 mm", "Bottom edge of the breadboard tray.", "ESTIMATED"),
    ("BreadboardWidth", "47 mm", "Board width for the breadboard tray.", "ESTIMATED"),
    ("BreadboardLength", "35 mm", "Board height for the breadboard tray.", "ESTIMATED"),
    ("BreadboardThickness", "8.5 mm", "Thickness of the breadboard body to retain.", "ESTIMATED"),
    ("BreadboardTrayHeight", "10 mm", "Rail height for the breadboard tray.", "ESTIMATED"),
    ("BreadboardClipWidth", "7 mm", "Width of each breadboard retaining clip.", "ESTIMATED"),
    ("BreadboardClipInset", "1.2 mm", "Amount the breadboard clips overlap the board edge.", "ESTIMATED"),
    ("UsbCutoutX", "124 mm", "Left edge of the micro-USB cut-out.", "ESTIMATED"),
    ("UsbCutoutY", "14 mm", "Bottom edge of the micro-USB cut-out.", "ESTIMATED"),
    ("UsbCutoutWidth", "12 mm", "Width of the micro-USB opening.", "ESTIMATED"),
    ("UsbCutoutHeight", "7 mm", "Height of the micro-USB opening.", "ESTIMATED"),
    ("UsbCradleDepth", "14 mm", "Depth of the micro-USB receiver cradle.", "ESTIMATED"),
    ("UsbCradleWall", "2.0 mm", "Wall thickness of the micro-USB cradle.", "ESTIMATED"),
    ("UsbShelfHeight", "4.5 mm", "Capture height above the micro-USB opening.", "ESTIMATED"),
    ("BatteryDoorInset", "2.5 mm", "Inset from battery tray footprint to exterior battery door opening.", "ESTIMATED"),
    ("BatteryDoorOverlap", "4.0 mm", "How far the battery cover overlaps around the opening.", "ESTIMATED"),
    ("BatteryDoorFrameHeight", "1.2 mm", "Exterior locating frame height around the battery opening.", "ESTIMATED"),
    ("BatteryDoorClearance", "0.3 mm", "Clearance between the battery cover and the locating frame.", "ESTIMATED"),
    ("BatteryDoorPlateThickness", "2.0 mm", "Thickness of the removable battery cover plate.", "ESTIMATED"),
    ("BatteryDoorPlugDepth", "2.5 mm", "Depth of the inner guide plug on the battery cover.", "ESTIMATED"),
    ("BatteryDoorLift", "10 mm", "Display lift used to place the battery cover outside the shell for printing.", "ESTIMATED"),
]


def mm(sheet, alias):
    return App.Units.Quantity(sheet.get(alias)).Value


def vector(x, y, z):
    return App.Vector(float(x), float(y), float(z))


def fuse_all(shapes):
    valid = [shape for shape in shapes if shape is not None]
    if not valid:
        return None

    result = valid[0]
    for shape in valid[1:]:
        result = result.fuse(shape)
    return result.removeSplitter()


def cut_if_possible(base_shape, cutter):
    if base_shape is None or cutter is None:
        return base_shape
    return base_shape.cut(cutter).removeSplitter()


def ensure_document():
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument(DOC_NAME)
    return doc


def ensure_spreadsheet(doc):
    sheet = doc.getObject(SPREADSHEET_NAME)
    if sheet is None:
        sheet = doc.addObject("Spreadsheet::Sheet", SPREADSHEET_NAME)

    sheet.set("A1", "Alias")
    sheet.set("B1", "Value")
    sheet.set("C1", "Description")
    sheet.set("D1", "Status")
    sheet.set("E1", "Coordinates")
    sheet.set("E2", "Origin is the open-face lower-left corner.")
    sheet.set("E3", "X = width, Y = height, Z = depth away from the device body.")
    sheet.set("E5", "Status key:")
    sheet.set("E6", "MEASURED = caliper/ruler value")
    sheet.set("E7", "DERIVED = computed from a measurement + clearance/offset")
    sheet.set("E8", "STANDARD = published spec (e.g. AA cell size)")
    sheet.set("E9", "ESTIMATED = placeholder, needs real measurement")

    for row, (alias, default_value, description, status) in enumerate(PARAM_SPECS, start=2):
        alias_cell = f"A{row}"
        value_cell = f"B{row}"
        description_cell = f"C{row}"
        status_cell = f"D{row}"

        sheet.set(alias_cell, alias)
        sheet.set(description_cell, description)
        sheet.set(status_cell, status)

        # Only write the default value if this alias cannot already be resolved.
        # sheet.get(alias) is the same call used at build time, so if it succeeds
        # the user's edited value is intact and should not be overwritten.
        try:
            sheet.get(alias)
        except Exception:
            sheet.set(value_cell, default_value)

        try:
            sheet.setAlias(value_cell, alias)
        except Exception:
            pass

    doc.recompute()
    return sheet


def ensure_group(doc):
    group = doc.getObject(GROUP_NAME)
    if group is None:
        group = doc.addObject("App::DocumentObjectGroup", GROUP_NAME)
    return group


def clear_group(doc, group):
    for obj in list(group.Group):
        doc.removeObject(obj.Name)


def add_part_feature(doc, group, name, shape, color=None, transparency=None):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = name
    obj.Shape = shape
    group.addObject(obj)

    if hasattr(obj, "ViewObject"):
        if color is not None:
            obj.ViewObject.ShapeColor = color
        if transparency is not None:
            obj.ViewObject.Transparency = transparency

    return obj


def build_shell(sheet):
    width = mm(sheet, "OverallWidth")
    height = mm(sheet, "OverallHeight")
    depth = mm(sheet, "OverallDepth")
    perimeter_wall = mm(sheet, "PerimeterWall")
    back_wall = mm(sheet, "BackWall")

    outer = Part.makeBox(width, height, depth, vector(0, 0, 0))
    inner = Part.makeBox(
        width - (2 * perimeter_wall),
        height - (2 * perimeter_wall),
        max(depth - back_wall, 0.1),
        vector(perimeter_wall, perimeter_wall, 0),
    )
    return outer.cut(inner).removeSplitter()


def screw_positions(sheet):
    width = mm(sheet, "OverallWidth")
    side_inset = mm(sheet, "ScrewSideInset")
    left_x = side_inset
    right_x = width - side_inset
    return [
        (left_x, mm(sheet, "ScrewLeftBottomY")),
        (left_x, mm(sheet, "ScrewLeftMiddleY")),
        (left_x, mm(sheet, "ScrewLeftTopY")),
        (right_x, mm(sheet, "ScrewRightBottomY")),
        (right_x, mm(sheet, "ScrewRightMiddleY")),
        (right_x, mm(sheet, "ScrewRightTopY")),
    ]


def build_screw_bosses(sheet):
    depth = mm(sheet, "OverallDepth")
    boss_radius = mm(sheet, "ScrewBossDiameter") / 2.0
    return fuse_all(
        [
            Part.makeCylinder(boss_radius, depth, vector(x, y, 0), vector(0, 0, 1))
            for x, y in screw_positions(sheet)
        ]
    )


def build_screw_cuts(sheet):
    depth = mm(sheet, "OverallDepth")
    thread_radius = mm(sheet, "ScrewThreadDiameter") / 2.0
    access_radius = max(mm(sheet, "ScrewDriverDiameter"), mm(sheet, "ScrewHeadDiameter")) / 2.0
    inner_web = mm(sheet, "ScrewInnerWeb")
    relief_depth = max(depth - inner_web, 0.1)

    cuts = []
    for x, y in screw_positions(sheet):
        cuts.append(Part.makeCylinder(thread_radius, depth, vector(x, y, 0), vector(0, 0, 1)))
        cuts.append(
            Part.makeCylinder(
                access_radius,
                relief_depth,
                vector(x, y, depth - relief_depth),
                vector(0, 0, 1),
            )
        )

    return fuse_all(cuts)


def internal_surface_z(sheet):
    return mm(sheet, "OverallDepth") - mm(sheet, "BackWall")


def battery_tray_size(sheet):
    cell_diameter = mm(sheet, "AACellDiameter")
    cell_length = mm(sheet, "AACellLength")
    side_clearance = mm(sheet, "BatterySideClearance")
    end_clearance = mm(sheet, "BatteryEndClearance")
    divider = mm(sheet, "BatteryDividerThickness")

    tray_width = (cell_diameter * 3.0) + (side_clearance * 2.0) + (divider * 2.0)
    tray_length = cell_length + (end_clearance * 2.0)
    return tray_width, tray_length


def battery_tray_origin(sheet):
    return mm(sheet, "BatteryTrayX"), mm(sheet, "BatteryTrayY")


def keepout_box(x, y, z, width, length, height):
    return Part.makeBox(width, length, height, vector(x, y, z))


def build_keepouts(sheet):
    motor = keepout_box(
        mm(sheet, "MotorKeepoutX"),
        mm(sheet, "MotorKeepoutY"),
        mm(sheet, "MotorKeepoutZ"),
        mm(sheet, "MotorKeepoutWidth"),
        mm(sheet, "MotorKeepoutLength"),
        mm(sheet, "MotorKeepoutHeight"),
    )
    legacy = keepout_box(
        mm(sheet, "LegacyPCBX"),
        mm(sheet, "LegacyPCBY"),
        mm(sheet, "LegacyPCBZ"),
        mm(sheet, "LegacyPCBWidth"),
        mm(sheet, "LegacyPCBLength"),
        mm(sheet, "LegacyPCBHeight"),
    )
    return motor, legacy, fuse_all([motor, legacy])


def build_battery_tray(sheet, keepout_union):
    tray_x, tray_y = battery_tray_origin(sheet)
    rail_height = mm(sheet, "BatteryRailHeight")
    wall_thickness = mm(sheet, "BatteryWallThickness")
    notch_width = mm(sheet, "BatteryWireNotchWidth")
    base_z = internal_surface_z(sheet) - rail_height

    tray_width, tray_length = battery_tray_size(sheet)

    left_wall = Part.makeBox(wall_thickness, tray_length, rail_height, vector(tray_x, tray_y, base_z))
    right_wall = Part.makeBox(
        wall_thickness,
        tray_length,
        rail_height,
        vector(tray_x + tray_width - wall_thickness, tray_y, base_z),
    )
    bottom_stop = Part.makeBox(tray_width, wall_thickness, rail_height, vector(tray_x, tray_y, base_z))

    notch_x = tray_x + ((tray_width - notch_width) / 2.0)
    left_top_stop = Part.makeBox(
        notch_x - tray_x,
        wall_thickness,
        rail_height,
        vector(tray_x, tray_y + tray_length - wall_thickness, base_z),
    )
    right_top_stop = Part.makeBox(
        (tray_x + tray_width) - (notch_x + notch_width),
        wall_thickness,
        rail_height,
        vector(notch_x + notch_width, tray_y + tray_length - wall_thickness, base_z),
    )

    side_clearance = mm(sheet, "BatterySideClearance")
    cell_diameter = mm(sheet, "AACellDiameter")
    divider = mm(sheet, "BatteryDividerThickness")
    divider_one_x = tray_x + side_clearance + cell_diameter
    divider_two_x = divider_one_x + divider + cell_diameter
    divider_height = max(rail_height - 2.0, 1.0)
    divider_y = tray_y + wall_thickness
    divider_length = tray_length - (2.0 * wall_thickness)
    divider_z = base_z + 1.0

    divider_one = Part.makeBox(divider, divider_length, divider_height, vector(divider_one_x, divider_y, divider_z))
    divider_two = Part.makeBox(divider, divider_length, divider_height, vector(divider_two_x, divider_y, divider_z))

    tray = fuse_all([left_wall, right_wall, bottom_stop, left_top_stop, right_top_stop, divider_one, divider_two])
    return cut_if_possible(tray, keepout_union)


def build_battery_access(sheet):
    tray_x, tray_y = battery_tray_origin(sheet)
    tray_width, tray_length = battery_tray_size(sheet)
    depth = mm(sheet, "OverallDepth")
    back_wall = mm(sheet, "BackWall")
    wall_thickness = mm(sheet, "BatteryWallThickness")

    inset = mm(sheet, "BatteryDoorInset")
    overlap = mm(sheet, "BatteryDoorOverlap")
    frame_height = mm(sheet, "BatteryDoorFrameHeight")
    clearance = mm(sheet, "BatteryDoorClearance")
    plate_thickness = mm(sheet, "BatteryDoorPlateThickness")
    plug_depth = mm(sheet, "BatteryDoorPlugDepth")
    door_lift = mm(sheet, "BatteryDoorLift")

    opening_x = tray_x + inset
    opening_y = tray_y + inset
    opening_width = max(tray_width - (2.0 * inset), 8.0)
    opening_length = max(tray_length - (2.0 * inset), 8.0)

    opening_cut = Part.makeBox(
        opening_width,
        opening_length,
        back_wall + 0.4,
        vector(opening_x, opening_y, depth - back_wall - 0.2),
    )

    frame_outer_x = opening_x - overlap
    frame_outer_y = opening_y - overlap
    frame_outer_w = opening_width + (2.0 * overlap)
    frame_outer_l = opening_length + (2.0 * overlap)

    frame_outer = Part.makeBox(frame_outer_w, frame_outer_l, frame_height, vector(frame_outer_x, frame_outer_y, depth))
    frame_inner = Part.makeBox(
        opening_width + (2.0 * clearance),
        opening_length + (2.0 * clearance),
        frame_height + 0.2,
        vector(opening_x - clearance, opening_y - clearance, depth - 0.1),
    )
    frame_ring = frame_outer.cut(frame_inner).removeSplitter()

    plate_w = max(frame_outer_w - (2.0 * clearance), 6.0)
    plate_l = max(frame_outer_l - (2.0 * clearance), 6.0)
    plug_w = max(opening_width - (2.0 * clearance), 4.0)
    plug_l = max(opening_length - (2.0 * clearance), 4.0)
    plug_d = min(max(plug_depth, 0.8), max(back_wall - 0.4, 0.8))

    plate_origin = vector(frame_outer_x + clearance, frame_outer_y + clearance, depth + frame_height + door_lift)
    cover_plate = Part.makeBox(plate_w, plate_l, plate_thickness, plate_origin)
    plug_origin = vector(opening_x + clearance, opening_y + clearance, depth + frame_height + door_lift - plug_d)
    cover_plug = Part.makeBox(plug_w, plug_l, plug_d, plug_origin)

    # Keep battery side rails intact by excluding them from the opening volume.
    side_guard_left = Part.makeBox(
        wall_thickness,
        tray_length,
        back_wall + 0.4,
        vector(tray_x, tray_y, depth - back_wall - 0.2),
    )
    side_guard_right = Part.makeBox(
        wall_thickness,
        tray_length,
        back_wall + 0.4,
        vector(tray_x + tray_width - wall_thickness, tray_y, depth - back_wall - 0.2),
    )
    guarded_cut = cut_if_possible(opening_cut, fuse_all([side_guard_left, side_guard_right]))

    return guarded_cut, frame_ring, fuse_all([cover_plate, cover_plug])


def build_board_tray(sheet, prefix, keepout_union):
    tray_x = mm(sheet, f"{prefix}X")
    tray_y = mm(sheet, f"{prefix}Y")
    board_width = mm(sheet, f"{prefix}Width")
    board_length = mm(sheet, f"{prefix}Length")
    board_thickness = mm(sheet, f"{prefix}Thickness")
    tray_height = mm(sheet, f"{prefix}TrayHeight")
    clip_width = mm(sheet, f"{prefix}ClipWidth")
    clip_inset = mm(sheet, f"{prefix}ClipInset")

    side_wall = 2.0
    end_stop = 2.5
    base_z = internal_surface_z(sheet) - tray_height
    rail_height = max(board_thickness + 1.2, 2.0)
    clip_height = max(board_thickness + 0.8, 1.5)

    left_rail = Part.makeBox(side_wall, board_length, rail_height, vector(tray_x, tray_y, base_z))
    right_rail = Part.makeBox(
        side_wall,
        board_length,
        rail_height,
        vector(tray_x + board_width - side_wall, tray_y, base_z),
    )
    bottom_stop = Part.makeBox(board_width, end_stop, rail_height, vector(tray_x, tray_y, base_z))

    clip_z = internal_surface_z(sheet) - clip_height
    clip_y = tray_y + board_length - end_stop
    left_clip = Part.makeBox(
        clip_width,
        end_stop,
        clip_height,
        vector(tray_x, clip_y, clip_z),
    )
    right_clip = Part.makeBox(
        clip_width,
        end_stop,
        clip_height,
        vector(tray_x + board_width - clip_width, clip_y, clip_z),
    )

    left_clip_relief = Part.makeBox(
        clip_width,
        end_stop,
        max(clip_height - clip_inset, 0.4),
        vector(tray_x + clip_inset, clip_y, clip_z),
    )
    right_clip_relief = Part.makeBox(
        clip_width,
        end_stop,
        max(clip_height - clip_inset, 0.4),
        vector(tray_x + board_width - clip_width, clip_y, clip_z),
    )

    tray = fuse_all([left_rail, right_rail, bottom_stop, left_clip, right_clip])
    tray = cut_if_possible(tray, fuse_all([left_clip_relief, right_clip_relief]))
    return cut_if_possible(tray, keepout_union)


def build_usb_mount(sheet, keepout_union):
    cutout_x = mm(sheet, "UsbCutoutX")
    cutout_y = mm(sheet, "UsbCutoutY")
    cutout_width = mm(sheet, "UsbCutoutWidth")
    cutout_height = mm(sheet, "UsbCutoutHeight")
    cradle_depth = mm(sheet, "UsbCradleDepth")
    cradle_wall = mm(sheet, "UsbCradleWall")
    shelf_height = mm(sheet, "UsbShelfHeight")
    back_wall = mm(sheet, "BackWall")
    depth = mm(sheet, "OverallDepth")

    cutout = Part.makeBox(cutout_width, cutout_height, back_wall + 0.2, vector(cutout_x, cutout_y, depth - back_wall - 0.1))

    cradle_base_z = depth - back_wall - cradle_depth
    left_guide = Part.makeBox(cradle_wall, cutout_height, cradle_depth, vector(cutout_x - cradle_wall, cutout_y, cradle_base_z))
    right_guide = Part.makeBox(
        cradle_wall,
        cutout_height,
        cradle_depth,
        vector(cutout_x + cutout_width, cutout_y, cradle_base_z),
    )
    bottom_shelf = Part.makeBox(
        cutout_width + (2.0 * cradle_wall),
        cradle_wall,
        cradle_depth,
        vector(cutout_x - cradle_wall, cutout_y - cradle_wall, cradle_base_z),
    )
    top_capture = Part.makeBox(
        cutout_width + (2.0 * cradle_wall),
        shelf_height,
        cradle_wall,
        vector(cutout_x - cradle_wall, cutout_y + cutout_height, depth - back_wall - cradle_wall),
    )

    mount = fuse_all([left_guide, right_guide, bottom_shelf, top_capture])
    return cutout, cut_if_possible(mount, keepout_union)


def build_model(doc=None):
    doc = doc or ensure_document()
    sheet = ensure_spreadsheet(doc)
    group = ensure_group(doc)
    clear_group(doc, group)

    shell = build_shell(sheet)
    screw_bosses = build_screw_bosses(sheet)
    shell_with_bosses = fuse_all([shell, screw_bosses])
    shell_with_bosses = cut_if_possible(shell_with_bosses, build_screw_cuts(sheet))

    motor_keepout, legacy_keepout, keepout_union = build_keepouts(sheet)
    battery_tray = build_battery_tray(sheet, keepout_union)
    battery_opening_cut, battery_frame, battery_cover = build_battery_access(sheet)
    addon_pcb_tray = build_board_tray(sheet, "AddonPCB", keepout_union)
    breadboard_tray = build_board_tray(sheet, "Breadboard", keepout_union)
    usb_cutout, usb_mount = build_usb_mount(sheet, keepout_union)

    final_shape = fuse_all([shell_with_bosses, battery_frame, battery_tray, addon_pcb_tray, breadboard_tray, usb_mount])
    final_shape = cut_if_possible(final_shape, usb_cutout)
    final_shape = cut_if_possible(final_shape, battery_opening_cut)

    add_part_feature(doc, group, "BackingShell", final_shape, color=(0.83, 0.83, 0.86), transparency=0)
    add_part_feature(doc, group, "BatteryCover", battery_cover, color=(0.78, 0.78, 0.8), transparency=0)
    add_part_feature(doc, group, "MotorKeepout", motor_keepout, color=(0.95, 0.35, 0.35), transparency=75)
    add_part_feature(doc, group, "LegacyPCBKeepout", legacy_keepout, color=(0.95, 0.65, 0.25), transparency=75)

    doc.recompute()
    return doc


def build(doc=None):
    doc = build_model(doc)
    if App.GuiUp and Gui is not None:
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(doc.getObject("BackingShell"))
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.SendMsgToActiveView("ViewFit")
    return doc


if __name__ == "__main__":
    build()
