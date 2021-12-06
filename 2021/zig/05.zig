const std = @import("std");
const parseInt = std.fmt.parseInt;
const indexOf = std.mem.indexOf;

const SEP = " -> ";
const Coord = struct { x: i32, y: i32 };
const Coords = std.AutoHashMap(Coord, u32);

pub fn main() !void {
    const file = try std.fs.cwd().openFile("../inputs/05.txt", .{});
    defer file.close();
    std.log.info("part 1: {d}", .{run(file, false)});
    std.log.info("part 2: {d}", .{run(file, true)});
}

pub fn run(file: std.fs.File, with_diagonals: bool) !u32 {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    var allocator = &gpalloc.allocator;
    defer std.debug.assert(!gpalloc.deinit());
    try file.seekTo(0);
    var reader = file.reader();
    var buf: [32]u8 = undefined;
    var coords = Coords.init(allocator);
    defer coords.deinit();
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const sep_idx = indexOf(u8, line, SEP) orelse return error.InvalidCoords;
        const from = try parseCoord(line[0..sep_idx]);
        const to = try parseCoord(line[sep_idx + SEP.len ..]);
        if (with_diagonals or from.x == to.x or from.y == to.y) {
            try addCoords(&coords, from, to);
        }
    }

    var answer: u32 = 0;
    var coords_iter = coords.valueIterator();
    while (coords_iter.next()) |count| {
        if (count.* > 1) answer += 1;
    }
    return answer;
}

fn parseCoord(text: []const u8) !Coord {
    const comma_idx = indexOf(u8, text, ",") orelse return error.InvalidCoords;
    const x = try parseInt(i32, text[0..comma_idx], 10);
    const y = try parseInt(i32, text[comma_idx + 1 ..], 10);
    return Coord{ .x = x, .y = y };
}

fn addCoords(coords: *Coords, from: Coord, to: Coord) !void {
    var inc_x: i8 = 0;
    var inc_y: i8 = 0;
    if (from.x > to.x) inc_x = -1 else if (from.x < to.x) inc_x = 1;
    if (from.y > to.y) inc_y = -1 else if (from.y < to.y) inc_y = 1;
    var x = from.x;
    var y = from.y;
    while (true) {
        const result = try coords.getOrPut(Coord{ .x = x, .y = y });
        if (!result.found_existing) result.value_ptr.* = 0;
        result.value_ptr.* += 1;
        if (x == to.x and y == to.y) break;
        x += inc_x;
        y += inc_y;
    }
}
