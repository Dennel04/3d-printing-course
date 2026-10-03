// Lab 2: configurable Gridfinity tray for input, workstation, or output holders.
// Set pocket dimensions from caliper measurements before exporting a print.

$fn = 48;

grid_pitch = 42;
units_x = 2;
units_y = 2;
foot_top_width = 41.5;
foot_bottom_width = 35.5;
foot_corner_radius = 3;
foot_taper_height = 4.75;
foot_clearance = 0.3;

tray_width = units_x * grid_pitch - 0.5;
tray_length = units_y * grid_pitch - 0.5;
tray_height = 20;
tray_corner_radius = 3;

pocket_columns = 2;
pocket_rows = 2;
// Placeholder values; measure each held object and adjust the fit allowance.
pocket_x = 30;
pocket_y = 30;
pocket_depth = 16;
pocket_corner_radius = 1;
lead_in = 1.5;
pocket_fit = 0.3;

module rounded_rectangle(width, length, radius) {
    offset(r = radius)
        offset(delta = -radius)
            square([width, length], center = true);
}

module gridfinity_foot() {
    linear_extrude(
        height = foot_taper_height,
        scale = (foot_top_width - 2 * foot_clearance) / (foot_bottom_width - 2 * foot_clearance)
    )
        rounded_rectangle(
            foot_bottom_width - 2 * foot_clearance,
            foot_bottom_width - 2 * foot_clearance,
            foot_corner_radius
        );
}

module tray_body() {
    translate([0, 0, foot_taper_height + tray_height / 2])
        linear_extrude(height = tray_height, center = true)
            rounded_rectangle(tray_width, tray_length, tray_corner_radius);
}

module pocket_cutout(center_x, center_y) {
    pocket_width = pocket_x + 2 * pocket_fit;
    pocket_length = pocket_y + 2 * pocket_fit;
    pocket_floor_z = foot_taper_height + tray_height - pocket_depth;
    straight_depth = pocket_depth - lead_in;

    translate([center_x, center_y, pocket_floor_z])
        linear_extrude(height = straight_depth)
            rounded_rectangle(pocket_width, pocket_length, pocket_corner_radius);

    translate([center_x, center_y, pocket_floor_z + straight_depth])
        hull() {
            linear_extrude(height = 0.01)
                rounded_rectangle(pocket_width, pocket_length, pocket_corner_radius);
            translate([0, 0, lead_in])
                linear_extrude(height = 0.01)
                    rounded_rectangle(
                        pocket_width + 2 * lead_in,
                        pocket_length + 2 * lead_in,
                        pocket_corner_radius + lead_in
                    );
        }
}

assert(units_x >= 1 && units_y >= 1, "Tray must use at least one Gridfinity unit per axis.");
assert(pocket_columns >= 1 && pocket_rows >= 1, "Pocket rows and columns must be positive.");
assert(foot_clearance >= 0 && foot_bottom_width > 2 * foot_clearance, "Invalid foot clearance.");
assert(pocket_depth > lead_in && pocket_depth < tray_height, "Pocket depth must leave a floor.");
assert(pocket_x + 2 * (pocket_fit + lead_in) < tray_width / pocket_columns,
       "Pockets are too wide for their tray cells.");
assert(pocket_y + 2 * (pocket_fit + lead_in) < tray_length / pocket_rows,
       "Pockets are too long for their tray cells.");

difference() {
    union() {
        for (x_index = [0 : units_x - 1]) {
            for (y_index = [0 : units_y - 1]) {
                translate([
                    (x_index - (units_x - 1) / 2) * grid_pitch,
                    (y_index - (units_y - 1) / 2) * grid_pitch,
                    0
                ])
                    gridfinity_foot();
            }
        }
        tray_body();
    }

    for (column = [0 : pocket_columns - 1]) {
        for (row = [0 : pocket_rows - 1]) {
            pocket_x_center = (column + 0.5) * tray_width / pocket_columns - tray_width / 2;
            pocket_y_center = (row + 0.5) * tray_length / pocket_rows - tray_length / 2;
            pocket_cutout(pocket_x_center, pocket_y_center);
        }
    }
}