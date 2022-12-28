const std = @import("std");
const Allocator = std.mem.Allocator;
const LetterSet = std.AutoArrayHashMap(u8, void);

pub fn main() !void {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    var allocator = gpalloc.allocator();
    defer std.debug.assert(!gpalloc.deinit());
    std.log.info("part 1: {d}", .{try part1(allocator)});
    std.log.info("part 2: {d}", .{try part2(allocator)});
}

fn part1(allocator: Allocator) !u32 {
    const file = try std.fs.cwd().openFile("../inputs/03.txt", .{});
    const reader = file.reader();
    var buf: [60]u8 = undefined;
    var sum: u32 = 0;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const left = line[0 .. line.len / 2];
        const right = line[line.len / 2 ..];
        var left_letters = try lettersHashMap(allocator, left);
        defer left_letters.deinit();
        var right_letters = try lettersHashMap(allocator, right);
        defer right_letters.deinit();

        for (left_letters.keys()) |letter| {
            if (right_letters.contains(letter)) {
                sum += priority(letter);
                break;
            }
        }
    }
    return sum;
}

const GROUP_SIZE: u8 = 3;

fn part2(allocator: Allocator) !u32 {
    const file = try std.fs.cwd().openFile("../inputs/03.txt", .{});
    const reader = file.reader();
    var buf: [60]u8 = undefined;
    var sum: u32 = 0;
    var i = GROUP_SIZE;
    var intersection: LetterSet = undefined;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var letters = try lettersHashMap(allocator, line);
        defer letters.deinit();
        var new_intersection = LetterSet.init(allocator);

        if (i == GROUP_SIZE) {
            new_intersection = try letters.clone();
        } else {
            for (intersection.keys()) |letter| {
                if (letters.contains(letter)) {
                    try new_intersection.put(letter, {});
                }
            }
            intersection.clearAndFree();
        }
        intersection = new_intersection;

        if (i == 1) {
            std.debug.assert(intersection.count() == 1);
            sum += priority(intersection.keys()[0]);
            intersection.clearAndFree();
            i = GROUP_SIZE;
        } else i -= 1;
    }
    return sum;
}

fn lettersHashMap(allocator: Allocator, word: []const u8) !LetterSet {
    var hash_map = LetterSet.init(allocator);
    for (word) |letter| try hash_map.put(letter, {});
    return hash_map;
}

fn priority(letter: u8) u32 {
    if (std.ascii.isUpper(letter)) return letter - 'A' + 27;
    return letter - 'a' + 1;
}
