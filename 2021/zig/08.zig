const std = @import("std");
const indexOf = std.mem.indexOf;
const indexOfScalar = std.mem.indexOfScalar;
const tokenize = std.mem.tokenize;

const SEP = " | ";

pub fn main() !void {
    const file = try std.fs.cwd().openFile("../inputs/08.txt", .{});
    defer file.close();

    const reader = file.reader();
    var buf: [256]u8 = undefined;
    var unique_lengths: u32 = 0;
    var outputs_total: usize = 0;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const sep_idx = indexOf(u8, line, SEP) orelse return error.InvalidSignals;
        const patterns = line[0..sep_idx];
        var digits = [_]?[]const u8{null} ** 10;
        // unique signal appearances: 4 => e, 6 => b, 9 => f
        var signals = [_]u32{0} ** 7;
        var patterns_iter = tokenize(u8, patterns, " ");
        // len 5 => 2, 3, 5
        var five_lens = [_]?[]const u8{null} ** 3;
        var five_lens_i: usize = 0;
        // len 6 => 0, 6, 9
        var six_lens = [_]?[]const u8{null} ** 3;
        var six_lens_i: usize = 0;
        while (patterns_iter.next()) |pattern| {
            switch (pattern.len) {
                2 => digits[1] = pattern,
                3 => digits[7] = pattern,
                4 => digits[4] = pattern,
                7 => digits[8] = pattern,
                5 => {
                    five_lens[five_lens_i] = pattern;
                    five_lens_i += 1;
                },
                6 => {
                    six_lens[six_lens_i] = pattern;
                    six_lens_i += 1;
                },
                else => {},
            }
            for (pattern) |signal| {
                // lowercase ascii values
                signals[signal - 97] += 1;
            }
        }

        next_five_len: for (five_lens) |pattern| {
            for (pattern.?) |signal| {
                switch (signals[signal - 97]) {
                    4 => {
                        digits[2] = pattern;
                        continue :next_five_len;
                    },
                    6 => {
                        digits[5] = pattern;
                        continue :next_five_len;
                    },
                    else => {},
                }
            }
            digits[3] = pattern;
        }

        for (six_lens) |pattern| {
            for ("abcdefg") |signal| {
                if (indexOfScalar(u8, pattern.?, signal) == null) {
                    switch (signals[signal - 97]) {
                        4 => digits[9] = pattern,
                        7 => digits[0] = pattern,
                        8 => digits[6] = pattern,
                        else => {},
                    }
                    break;
                }
            }
        }

        const output = line[sep_idx + SEP.len ..];
        var output_iter = tokenize(u8, output, " ");
        var coefficient: u32 = 1000;
        while (output_iter.next()) |v| {
            switch (v.len) {
                2...4 | 7 => unique_lengths += 1,
                else => {},
            }
            outputs_total += coefficient * findDigit(digits, v).?;
            coefficient /= 10;
        }
    }

    std.log.info("part 1: {d}", .{unique_lengths});
    std.log.info("part 2: {d}", .{outputs_total});
}

fn findDigit(digits: [10]?[]const u8, pattern: []const u8) ?usize {
    next_digit: for (digits) |digit, i| {
        if (digit.?.len != pattern.len) continue;
        for (pattern) |signal| {
            if (indexOfScalar(u8, digit.?, signal) == null) continue :next_digit;
        }
        return i;
    }
    return null;
}
