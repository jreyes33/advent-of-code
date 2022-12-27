const std = @import("std");

const Move = enum(u2) { rock = 1, paper = 2, scissors = 3 };
const Result = enum(u4) { loss = 0, draw = 3, win = 6 };

pub fn main() !void {
    const file = try std.fs.cwd().openFile("../inputs/02.txt", .{});
    const reader = file.reader();
    var sum_part1: u32 = 0;
    var sum_part2: u32 = 0;
    var buf: [4]u8 = undefined;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const their_move = switch (line[0]) {
            'A' => Move.rock,
            'B' => Move.paper,
            'C' => Move.scissors,
            else => return error.InvalidMove,
        };
        const my_move = switch (line[2]) {
            'X' => Move.rock,
            'Y' => Move.paper,
            'Z' => Move.scissors,
            else => return error.InvalidMove,
        };
        const target_result = switch (line[2]) {
            'X' => Result.loss,
            'Y' => Result.draw,
            'Z' => Result.win,
            else => return error.InvalidResult,
        };
        sum_part1 += pointsPart1(their_move, my_move);
        sum_part2 += pointsPart2(their_move, target_result);
    }
    std.log.info("part 1: {d}", .{sum_part1});
    std.log.info("part 2: {d}", .{sum_part2});
}

fn pointsPart1(their_move: Move, my_move: Move) u32 {
    const result = switch (their_move) {
        .rock => switch (my_move) {
            .rock => Result.draw,
            .paper => Result.win,
            .scissors => Result.loss,
        },
        .paper => switch (my_move) {
            .rock => Result.loss,
            .paper => Result.draw,
            .scissors => Result.win,
        },
        .scissors => switch (my_move) {
            .rock => Result.win,
            .paper => Result.loss,
            .scissors => Result.draw,
        },
    };
    return @enumToInt(result) + @enumToInt(my_move);
}

fn pointsPart2(their_move: Move, target_result: Result) u32 {
    const my_move = switch (target_result) {
        .draw => their_move,
        .win => switch (their_move) {
            .rock => Move.paper,
            .paper => Move.scissors,
            .scissors => Move.rock,
        },
        .loss => switch (their_move) {
            .rock => Move.scissors,
            .paper => Move.rock,
            .scissors => Move.paper,
        },
    };
    return @enumToInt(target_result) + @enumToInt(my_move);
}
