// Camera dimensions
camera_height = 30;
camera_width = 40;
camera_depth = 25;

wall_grab_width = 3;
wall_grab_height = 20;


difference() {
    cube(size = [4 * camera_width + 2 * wall_grab_width + 3 * 2 * wall_grab_width, camera_depth + 2 * wall_grab_width, wall_grab_height], center = false);
    
    // 4 cameras
    translate([3, 3, 3]) union() {
        for (i = [0:3]) {
            translate([i * camera_width + 2* wall_grab_width * i, 0, 0]) cube(size = [      camera_width, camera_depth, camera_height], center = false);
            translate([i * camera_width + 2*wall_grab_width * i + wall_grab_width, -1-wall_grab_width, 0]) cube(size = [camera_width - 2*wall_grab_width, camera_depth + 2*wall_grab_width + 2, camera_height], center = false);
        }
    }
}
