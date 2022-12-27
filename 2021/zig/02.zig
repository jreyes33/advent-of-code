const std = @import("std");

pub fn main() !void {
    const file = try std.fs.cwd().openFile("../inputs/02.txt", .{});
    defer file.close();
    const reader = file.reader();
    var dir: [8]u8 = undefined;
    var n_str: [2]u8 = undefined;
    var depth: u32 = 0;
    var horizontal: u32 = 0;
    var aim: u32 = 0;
    var real_depth: u32 = 0;
    while (true) {
        _ = reader.readUntilDelimiter(&dir, ' ') catch break;
        _ = reader.readUntilDelimiter(&n_str, '\n') catch break;
        const n = try std.fmt.parseInt(u8, n_str[0..1], 10);
        switch (dir[0]) {
            'f' => {
                horizontal += n;
                real_depth += n * aim;
            },
            'u' => {
                depth -= n;
                aim -= n;
            },
            'd' => {
                depth += n;
                aim += n;
            },
            else => return error.UnknownDirection,
        }
    }
    std.log.info("part 1: {d}", .{depth * horizontal});
    std.log.info("part 2: {d}", .{real_depth * horizontal});
}
