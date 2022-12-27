const std = @import("std");
const ArrayList = std.ArrayList;
const Matrix = ArrayList(Row);
const Row = ArrayList(u32);

pub fn main() !void {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    var allocator = gpalloc.allocator();
    defer std.debug.assert(!gpalloc.deinit());

    var matrix = Matrix.init(allocator);
    defer {
        for (matrix.items) |row| row.deinit();
        matrix.deinit();
    }

    const file = try std.fs.cwd().openFile("../inputs/09.txt", .{});
    const reader = file.reader();
    var buf: [128]u8 = undefined;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var row = Row.init(allocator);
        for (line) |c| {
            // ascii to int
            try row.append(c - 48);
        }
        try matrix.append(row);
    }

    var risk_level: u32 = 0;
    for (matrix.items) |row, j| {
        next_point: for (row.items) |point, i| {
            for ([_]i32{ -1, 0, 1 }) |dx| {
                for ([_]i32{ -1, 0, 1 }) |dy| {
                    var x = @intCast(i32, i) + dx;
                    var y = @intCast(i32, j) + dy;
                    if (dx == 0 and dy == 0) continue;
                    if (x < 0 or x >= row.items.len or y < 0 or y >= matrix.items.len) continue;
                    if (point >= matrix.items[@intCast(usize, y)].items[@intCast(usize, x)]) continue :next_point;
                }
            }
            risk_level += 1 + point;
        }
    }

    std.log.info("part 1: {d}", .{risk_level});
}
