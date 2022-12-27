const std = @import("std");

pub fn main() anyerror!void {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpalloc.allocator();
    defer std.debug.assert(!gpalloc.deinit());
    const file = try std.fs.cwd().openFile("../inputs/01.txt", .{});
    defer file.close();
    var br = std.io.bufferedReader(file.reader());
    const reader = br.reader();
    var buf: [8]u8 = undefined;
    var numbers = std.ArrayList(i32).init(allocator);
    defer numbers.deinit();
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const n = try std.fmt.parseInt(i32, line, 10);
        try numbers.append(n);
    }
    var sums = std.ArrayList(i32).init(allocator);
    defer sums.deinit();
    try sums.ensureTotalCapacity(numbers.items.len - 2);
    var i: usize = 0;
    while (i < numbers.items.len - 2) : (i += 1) {
        try sums.append(numbers.items[i] + numbers.items[i + 1] + numbers.items[i + 2]);
    }
    // Also possible:
    // for (numbers.items[2..]) |n, i| {
    //   try sums.append(n + numbers.items[i] + numbers.items[i + 1]);
    // }
    std.debug.print("part 1: {d}\n", .{count_increased(numbers.items)});
    std.debug.print("part 2: {d}\n", .{count_increased(sums.items)});
}

fn count_increased(numbers: []const i32) u32 {
    var count_inc: u32 = 0;
    var prev = numbers[0];
    for (numbers[1..]) |n| {
        if (n > prev) {
            count_inc += 1;
        }
        prev = n;
    }
    return count_inc;
}
