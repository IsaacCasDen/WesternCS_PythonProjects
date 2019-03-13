def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


class Blocks:
    def __init__(self, height: int, max_block_height=3):
        self.max_block_height = max_block_height
        if max_block_height < 1:
            max_block_height = 1
        self.block_size = [size for size in range(1, int(max_block_height) + 1)]
        self.height = height

    def get_stacks(self):
        value = []

        for i in range(1, self.height + 1):
            v = self.get_layouts(i)
            if len(v) > 0:
                value += v
                # print(str(i) + " position contraint processed")

        return value

    def get_layouts(self, positions: int):

        list = self.get_blocks([], positions)
        select = [item for item in list if sum(item) == self.height]

        return select

    def get_layout(self):
        return None

    def get_blocks(self, prev_blocks: list, max_length: int):
        values = []

        if max_length <= 0:
            return values

        if len(prev_blocks) == 0:
            for size in self.block_size:
                values += [[size]]
                values += self.get_blocks(values[len(values) - 1], max_length)
        elif len(prev_blocks) < max_length:
            if sum(prev_blocks) < self.height:
                diff = max_length - len(prev_blocks)
                if (sum(prev_blocks) + diff * self.max_block_height) >= self.height:
                    if (sum(prev_blocks) + diff) <= self.height:
                        for size in self.block_size:
                            values += self.get_blocks(prev_blocks + [size], max_length)
        elif len(prev_blocks) == max_length:
            values = [prev_blocks]

        return values

def old_blocks(h: int):
    value = 0

    blocks = Blocks(h)
    value = blocks.get_stacks()

    return value

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


fib = memoize(fib)

def blocks(h: int):
    if h == 1:
        return 1
    elif h == 2:
        return 2
    elif h == 3:
        return 4
    else:
        return blocks(h - 1) + blocks(h - 2) + blocks(h - 3)

blocks = memoize(blocks)

if __name__ == "__main__":
    # val = fib(499)
    # print(val)
    # for i in range (1 , (16 + 1)):
    #    print(blocks(i))
    val = blocks(500)
    print(len(str(val)))
