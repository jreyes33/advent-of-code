const std = @import("std");
const assert = std.debug.assert;
const parseInt = std.fmt.parseInt;

pub fn main() !void {
    const file = try std.fs.cwd().openFile("../inputs/04.txt", .{});
    const reader = file.reader();
    var part1: u16 = 0;
    var part2: u16 = 0;
    var buf: [12]u8 = undefined;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var split_line = std.mem.split(u8, line, ",");
        const first_pair = try readPair(split_line.next().?);
        const second_pair = try readPair(split_line.next().?);
        assert(split_line.next() == null);
        if (fullyContained(first_pair, second_pair)) part1 += 1;
        if (overlaps(first_pair, second_pair)) part2 += 1;
    }
    std.log.info("part 1: {d}", .{part1});
    std.log.info("part 2: {d}", .{part2});
}

fn readPair(input: []const u8) ![2]u8 {
    var split_input = std.mem.split(u8, input, "-");
    const from = try parseInt(u8, split_input.next().?, 10);
    const to = try parseInt(u8, split_input.next().?, 10);
    assert(split_input.next() == null);
    return .{ from, to };
}

fn fullyContained(a: [2]u8, b: [2]u8) bool {
    if ((a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])) return true;
    return false;
}

fn overlaps(a: [2]u8, b: [2]u8) bool {
    if ((a[1] >= b[0] and a[1] <= b[1]) or (b[1] >= a[0] and b[1] <= a[1])) return true;
    return false;
}
