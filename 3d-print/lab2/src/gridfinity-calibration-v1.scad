// Lab 2: 1x1 Gridfinity fit and robot-calibration holder.
// Confirm the foot against the real grid before using this geometry for other holders.

$fn = 48;

grid_pitch = 42;
foot_top_width = 41.5;
foot_bottom_width = 35.5;
foot_corner_radius = 3;
foot_taper_height = 4.75;

body_width = 41.5;
body_height = 12;
body_corner_radius = 3;

// Replace these placeholders with the measured test object or calibration target.
pocket_x = 20;
pocket_y = 20;
pocket_depth = 8;
pocket_corner_radius = 1;
lead_in = 1;

// Provisional initial test value only: Lab 1 did not physically test 0.3 mm.
// Lab 1 showed 0.4 mm moving freely and 0.2 mm binding, so only the
// 0.2-0.4 mm range is supported by physical evidence.
// Verify this value on the real rig before reuse.
foot_clearance = 0.3;

// This foot is an unverified prototype. Before finalizing, compare its full
// profile with standard Gridfinity geometry from a trusted generator/library
// and test it on the real table. Successful OpenSCAD compilation alone does
// not confirm Gridfinity compliance or physical fit.

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

module holder_body() {
    translate([0, 0, foot_taper_height + body_height / 2])
        linear_extrude(height = body_height, center = true)
            rounded_rectangle(body_width, body_width, body_corner_radius);
}

module pocket_cutout() {
    pocket_floor_z = foot_taper_height + body_height - pocket_depth;
    pocket_straight_depth = pocket_depth - lead_in;

    translate([0, 0, pocket_floor_z])
        linear_extrude(height = pocket_straight_depth)
            rounded_rectangle(pocket_x, pocket_y, pocket_corner_radius);

    translate([0, 0, pocket_floor_z + pocket_straight_depth])
        hull() {
            linear_extrude(height = 0.01)
                rounded_rectangle(pocket_x, pocket_y, pocket_corner_radius);
            translate([0, 0, lead_in])
                linear_extrude(height = 0.01)
                    rounded_rectangle(
                        pocket_x + 2 * lead_in,
                        pocket_y + 2 * lead_in,
                        pocket_corner_radius + lead_in
                    );
        }
}

assert(grid_pitch > foot_top_width, "Foot must fit inside one Gridfinity pitch.");
assert(foot_clearance >= 0, "Foot clearance cannot be negative.");
assert(foot_bottom_width > 2 * foot_clearance, "Clearance leaves no foot at the bottom.");
assert(pocket_depth > lead_in && pocket_depth < body_height, "Pocket depth must leave a floor.");
assert(pocket_x + 2 * lead_in < body_width, "Pocket is too wide for the holder body.");
assert(pocket_y + 2 * lead_in < body_width, "Pocket is too long for the holder body.");

difference() {
    union() {
        gridfinity_foot();
        holder_body();
    }
    pocket_cutout();
}
