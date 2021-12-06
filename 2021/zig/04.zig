const std = @import("std");

const Cell = struct { row: u8, col: u8, marked: bool };
const Cells = std.AutoHashMap(u32, Cell);

const Board = struct {
    cells: Cells,
    row_sums: [5]u32,
    col_sums: [5]u32,
    won: bool,

    fn justWon(self: Board, row: u8, col: u8) bool {
        return !self.won and (self.row_sums[row] == 0 or self.col_sums[col] == 0);
    }

    fn score(self: Board, called_num: u32) u32 {
        var unmarked_sum: u32 = 0;
        var contents_iter = self.cells.iterator();
        while (contents_iter.next()) |entry| {
            if (!entry.value_ptr.*.marked) {
                unmarked_sum += entry.key_ptr.*;
            }
        }
        return called_num * unmarked_sum;
    }
};

pub fn main() !void {
    var gpalloc = std.heap.GeneralPurposeAllocator(.{}){};
    var allocator = &gpalloc.allocator;
    defer std.debug.assert(!gpalloc.deinit());
    const file = try std.fs.cwd().openFile("../inputs/04.txt", .{});
    defer file.close();
    const reader = file.reader();
    var calls_buf: [512]u8 = undefined;
    const calls_line = try reader.readUntilDelimiter(&calls_buf, '\n');
    var boards = std.ArrayList(Board).init(allocator);
    defer {
        for (boards.items) |*board| {
            board.cells.deinit();
        }
        boards.deinit();
    }
    var row: u8 = 0;
    var col: u8 = 0;
    var buf: [32]u8 = undefined;
    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        if (line.len == 0) {
            const board = Board{
                .cells = Cells.init(allocator),
                // There are zeros in the boards, so we need to add 1 for each number.
                .row_sums = [_]u32{5} ** 5,
                .col_sums = [_]u32{5} ** 5,
                .won = false,
            };
            try boards.append(board);
            row = 0;
            col = 0;
            continue;
        }
        col = 0;
        var board = &boards.items[boards.items.len - 1];
        var iter = std.mem.tokenize(u8, line, " ");
        while (iter.next()) |v| {
            const num = try std.fmt.parseInt(u32, v, 10);
            try board.cells.put(num, Cell{ .row = row, .col = col, .marked = false });
            board.row_sums[row] += num;
            board.col_sums[col] += num;
            col += 1;
        }
        row += 1;
    }

    var winners: u32 = 0;
    var iter = std.mem.tokenize(u8, calls_line, ",");
    while (iter.next()) |v| {
        const num = try std.fmt.parseInt(u32, v, 10);
        for (boards.items) |*board| {
            if (board.cells.getPtr(num)) |cell| {
                cell.marked = true;
                board.row_sums[cell.row] -= 1 + num;
                board.col_sums[cell.col] -= 1 + num;
                if (board.justWon(cell.row, cell.col)) {
                    board.won = true;
                    winners += 1;
                    if (winners == 1) {
                        std.log.info("Bingo! Part 1: {d}", .{board.score(num)});
                    } else if (winners == boards.items.len) {
                        std.log.info("Bingo! Part 2: {d}", .{board.score(num)});
                        return;
                    }
                }
            }
        }
    }
}
