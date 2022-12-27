const std = @import("std");

pub fn main() !void {
    std.log.info("part 1: {!}", .{topCalories(1)});
    std.log.info("part 2: {!}", .{topCalories(3)});
}

fn topCalories(comptime n: u32) !u32 {
    const file = try std.fs.cwd().openFile("../inputs/01.txt", .{});
    const reader = file.reader();
    var sum: u32 = 0;
    var max_n = [_]u32{0} ** n;
    var buf: [6]u8 = undefined;

    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        // `parseInt` fails on empty lines; the `catch` block is run in those cases.
        const calories = std.fmt.parseInt(u32, line, 10) catch {
            // advance `i` if `sum` should be inserted into `max_n`.
            var i: usize = 0;
            while (i < n and sum > max_n[i]) : (i += 1) {}

            // make room for `sum` to be inserted.
            var j: usize = 0;
            while (j + 1 < i) : (j += 1) max_n[j] = max_n[j + 1];

            // insert `sum` into `max_n` if needed.
            if (i > 0) max_n[i - 1] = sum;

            sum = 0;
            continue;
        };

        sum += calories;
    }

    return arraySum(u32, &max_n);
}

fn arraySum(comptime T: type, arr: []const T) T {
    var sum: T = 0;
    for (arr) |x| sum += x;
    return sum;
}
