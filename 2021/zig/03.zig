const std = @import("std");
const ArrayList = std.ArrayList;
const Allocator = std.mem.Allocator;
const parseInt = std.fmt.parseInt;

pub fn main() !void {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    var allocator = gpalloc.allocator();
    defer std.debug.assert(!gpalloc.deinit());
    const file = try std.fs.cwd().openFile("../inputs/03.txt", .{});
    defer file.close();
    const reader = file.reader();
    var zeros = [_]u32{0} ** 12;
    var gamma = [_]u8{'0'} ** 12;
    var epsilon = [_]u8{'1'} ** 12;
    var lines = ArrayList([]u8).init(allocator);
    defer {
        for (lines.items) |line| {
            allocator.free(line);
        }
        lines.deinit();
    }
    while (try reader.readUntilDelimiterOrEofAlloc(allocator, '\n', 13)) |line| {
        try lines.append(line);
        for (line) |char, i| {
            if (char == '0') zeros[i] += 1;
        }
    }
    const majority = lines.items.len / 2;
    for (zeros) |zero_count, i| {
        if (zero_count < majority) {
            gamma[i] = '1';
            epsilon[i] = '0';
        }
    }
    const width = lines.items[0].len;
    const gamma_num = try parseInt(u32, gamma[0..width], 2);
    const epsilon_num = try parseInt(u32, epsilon[0..width], 2);
    std.log.info("part 1: {d}", .{gamma_num * epsilon_num});
    const o2_lines = try reduceToSingle(allocator, lines.items, 0, '1');
    defer allocator.free(o2_lines);
    const o2_rating = try parseInt(u32, o2_lines[0], 2);
    const co2_lines = try reduceToSingle(allocator, lines.items, 0, '0');
    defer allocator.free(co2_lines);
    const co2_rating = try parseInt(u32, co2_lines[0], 2);
    std.log.info("part 2: {d}", .{o2_rating * co2_rating});
}

fn reduceToSingle(allocator: Allocator, lines: []const []u8, index: u32, tiebreak: u8) ![]const []u8 {
    if (lines.len == 1) return lines;
    var ones: u32 = 0;
    for (lines) |line| {
        if (line[index] == '1') ones += 1;
    }
    const majority = try std.math.divCeil(usize, lines.len, 2);
    const o2_rule = tiebreak == '1' and ones >= majority;
    const co2_rule = tiebreak == '0' and ones < majority;
    const keep: u8 = if (o2_rule or co2_rule) '1' else '0';
    var new_lines = ArrayList([]u8).init(allocator);
    for (lines) |line| {
        if (line[index] == keep) {
            try new_lines.append(line);
        }
    }
    // If we're past the first iteration, we need to free the intermediate lines slices.
    if (index > 0) allocator.free(lines);
    return reduceToSingle(allocator, new_lines.toOwnedSlice(), index + 1, tiebreak);
}
