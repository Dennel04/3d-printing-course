// Lab 2: 1 x 1 Gridfinity calibration print candidate.
// Nominal foot dimensions follow kennetek/gridfinity-rebuilt-openscad,
// src/core/standard.scad (MIT License, Copyright 2023 Kenneth Hodson):
// https://github.com/kennetek/gridfinity-rebuilt-openscad/blob/main/src/core/standard.scad
// The same 0.8 / 1.8 / 2.15 mm profile is specified for this rig in
// ../docs/MG 400 rakis.md, section 5. This file implements the profile
// independently; it does not copy the library's source code.

// All dimensions are in mm. Physical Gridfinity fit is untested.

grid_pitch = 42;
nominal_top_width = 41.5;
nominal_top_radius = 3.75;
nominal_lower_chamfer = 0.8;
nominal_vertical_wall = 1.8;
nominal_upper_chamfer = 2.15;
nominal_profile_height = nominal_lower_chamfer
                       + nominal_vertical_wall
                       + nominal_upper_chamfer; // 4.75 mm
nominal_bridge_height = 7 - nominal_profile_height; // 2.25 mm

// Provisional printer/fit adjustment for the FIRST physical Gridfinity test.
// This is a radial/per-side inward offset in X and Y; each full width is
// reduced by 2 * fit_adjustment. It is NOT a calibrated clearance.
// Start at the library's nominal geometry (0 mm); change only after testing.
// Lab 1 observed free motion at 0.4 mm and binding at 0.2 mm in a DIFFERENT
// cube test. It did not test 0.3 mm or establish the Gridfinity foot fit.
fit_adjustment = 0;

// A recessed cross marks the geometric cell centre (X = 0, Y = 0).
// It prints on the flat upper surface without supports.
target_length = 16;
target_width = 0.6;
target_depth = 0.4;

corner_segments = 12;

nominal_bottom_width = nominal_top_width
                     - 2 * (nominal_lower_chamfer + nominal_upper_chamfer);
nominal_bottom_radius = nominal_top_radius
                      - nominal_lower_chamfer - nominal_upper_chamfer;
nominal_middle_width = nominal_bottom_width + 2 * nominal_lower_chamfer;
nominal_middle_radius = nominal_bottom_radius + nominal_lower_chamfer;
total_height = nominal_profile_height + nominal_bridge_height;

// A rounded-square ring, counter-clockwise when viewed from above.
// Applying one inward offset to all rings retains both 45-degree slopes.
function ring_points(width, radius, z) = [
    for (corner = [0 : 3], step = [0 : corner_segments])
        let(
            angle = 90 * corner + 90 * step / corner_segments,
            centre_x = (corner == 0 || corner == 3) ? width/2 - radius : -width/2 + radius,
            centre_y = (corner == 0 || corner == 1) ? width/2 - radius : -width/2 + radius
        )
        [centre_x + radius * cos(angle),
         centre_y + radius * sin(angle), z]
];

// Distinct nominal levels: lower 45-degree chamfer, vertical band, upper
// 45-degree chamfer, then the 2.25 mm bridge to a simple flat top.
levels = [
    [0, nominal_bottom_width, nominal_bottom_radius],
    [nominal_lower_chamfer, nominal_middle_width, nominal_middle_radius],
    [nominal_lower_chamfer + nominal_vertical_wall,
     nominal_middle_width, nominal_middle_radius],
    [nominal_profile_height, nominal_top_width, nominal_top_radius],
    [total_height, nominal_top_width, nominal_top_radius]
];

points_per_ring = 4 * (corner_segments + 1);

module standard_profile_with_test_adjustment() {
    polyhedron(
        points = [
            for (level = levels)
                each ring_points(level[1] - 2 * fit_adjustment,
                                 level[2] - fit_adjustment,
                                 level[0])
        ],
        faces = concat(
            [[for (i = [points_per_ring - 1 : -1 : 0]) i]],
            [for (level = [0 : len(levels) - 2], i = [0 : points_per_ring - 1])
                each [
                    [level * points_per_ring + i,
                     level * points_per_ring + (i + 1) % points_per_ring,
                     (level + 1) * points_per_ring + (i + 1) % points_per_ring],
                    [level * points_per_ring + i,
                     (level + 1) * points_per_ring + (i + 1) % points_per_ring,
                     (level + 1) * points_per_ring + i]
                ]],
            [[for (i = [0 : points_per_ring - 1])
                (len(levels) - 1) * points_per_ring + i]]
        ),
        convexity = 4
    );
}

assert(grid_pitch == 42 && nominal_top_width == 41.5,
       "Check nominal Gridfinity size against the cited source.");
assert(abs(nominal_profile_height - 4.75) < 0.000001
       && nominal_bottom_radius > 0,
       "Invalid nominal Gridfinity foot profile.");
assert(fit_adjustment >= 0 && fit_adjustment < nominal_bottom_radius,
       "Fit adjustment must leave a positive bottom corner radius.");
assert(target_width > 0 && target_width < target_length
       && target_length < nominal_top_width - 2 * fit_adjustment,
       "Invalid cross dimensions.");
assert(target_depth > 0 && target_depth < nominal_bridge_height,
       "Cross must not cut into the Gridfinity foot profile.");

difference() {
    standard_profile_with_test_adjustment();
    translate([-target_length/2, -target_width/2, total_height - target_depth])
        cube([target_length, target_width, target_depth + 0.1]);
    translate([-target_width/2, -target_length/2, total_height - target_depth])
        cube([target_width, target_length, target_depth + 0.1]);
}
