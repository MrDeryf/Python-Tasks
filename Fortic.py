import operator

OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}
possible_letters = {chr(ord("a") + i): i for i in range(26)}
possible_letters["-"] = 26


def show(vm):
    print(vm.stack.pop(), end="")


def emit(vm):
    print(chr(vm.stack.pop()), end="")


def if_statement(vm):
    address_false = vm.stack.pop()
    address_true = vm.stack.pop()
    condition = vm.stack.pop()
    address = address_true if condition else address_false
    vm.call_single_use_func(address)


def for_statement(vm):
    address = vm.stack.pop()
    iteration_number = vm.stack.pop()
    vm.stack.append(0)
    vm.call_single_use_func(address, times_to_use=iteration_number)


def inp(vm):
    return vm.stack.append(int(input()))


def create_array(vm):
    size = vm.stack.pop()
    arr_name = vm.create_unique_name("array", False)
    vm.scope[vm.curr_func][arr_name] = [-1] * size
    vm.stack.append(arr_name)


def read_el(vm):
    index = vm.stack.pop()
    arr_name = vm.stack.pop()
    func_where_to_look = vm.find_name(arr_name)
    vm.stack.append(vm.scope[func_where_to_look][arr_name][index])


def write_el(vm):
    index = vm.stack.pop()
    arr_name = vm.stack.pop()
    el = vm.stack.pop()
    func_where_to_look = vm.find_name(arr_name)
    vm.scope[func_where_to_look][arr_name][index] = el


LIB = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,  # Целочисленный вариант деления
    '%': operator.mod,
    '&': operator.and_,
    '|': operator.or_,
    '^': operator.xor,
    '<': operator.lt,
    '>': operator.gt,
    '=': operator.eq,
    '<<': operator.lshift,
    '>>': operator.rshift,
    'if': if_statement,
    'for': for_statement,
    '.': show,
    'emit': emit,
    '?': inp,
    'array': create_array,
    '@': read_el,
    '!': write_el
}

LIB_OPS = list(LIB.keys())

op_name_rev = {value: key for key, value in OP_NAMES.items()}
lib_ops_rev = {value: index for index, value in enumerate(LIB_OPS)}

print(op_name_rev)
print(lib_ops_rev)


class VirtualMachine:
    def __init__(self, code=None):
        self.stack = []
        self.is_comp = (code is not None)
        if self.is_comp:
            self.pc = code[0]
            self.code = code[1:]
        else:
            self.pc = []
            self.code = []
        self.scope = dict()
        self.func_stack = []
        self.curr_func = "main"
        self.func_relation = dict()
        self.scope["main"] = dict()

    def op_realisation(self, op_code):
        lib_op = LIB_OPS[op_code] if self.is_comp else op_code
        chosen_func = LIB[lib_op]
        if lib_op in ['if', 'for', '.', 'emit', '?', 'array', '@', '!']:
            chosen_func(self)
        else:
            arg2 = self.stack.pop()
            arg1 = self.stack.pop()
            self.stack.append(chosen_func(arg1, arg2))

    def is_realisation(self, func_name):
        func_start = self.stack.pop()
        self.scope[self.curr_func][func_name] = ("func", func_start)

    def to_realisation(self, var_name):
        var_value = self.stack.pop()
        self.scope[self.curr_func][var_name] = ("var", var_value)

    def find_name(self, name_to_find):
        func_where_looking = self.curr_func
        while name_to_find not in self.scope[func_where_looking].keys():
            if func_where_looking == "main":
                print(self.scope, self.func_relation)
                raise Exception(f"Нет переменной или функции с таким именем: {name_to_find}")
            func_where_looking = self.func_relation[func_where_looking]
        return func_where_looking

    def call_realisation(self, name_to_call):
        func_where_to_look = self.find_name(name_to_call)
        found_code = self.scope[func_where_to_look][name_to_call]
        if found_code[0] == "func":
            func_name = self.create_unique_name(name_to_call)
            self.func_stack.append((func_name, self.pc))
            self.func_relation[func_name] = self.curr_func
            self.pc = (found_code[1] - 1) if self.is_comp else found_code[1]
            self.curr_func = func_name
            self.scope[func_name] = dict()
        elif found_code[0] == "var":
            self.stack.append(found_code[1])

    def create_unique_name(self, func_name, func=True):
        i = 1
        while (str(func_name) + str(i) in self.scope.keys()) if func else ((str(func_name) + str(i)) in self.scope[self.curr_func].keys()):
            i += 1
        return str(func_name) + str(i)

    def call_single_use_func(self, func_start, times_used=0, times_to_use=1):
        func_name = self.create_unique_name("nameless")
        self.scope[func_name] = dict()

        self.func_stack.append((func_name, self.pc, times_used, times_to_use, func_start))
        self.func_relation[func_name] = self.curr_func
        self.pc = (func_start - 1) if self.is_comp else func_start
        self.curr_func = func_name

    def exit_realisation(self):
        if len(self.func_stack) > 0:
            finished_func_name, ret_code, *times = self.func_stack.pop()
            self.curr_func = self.func_relation[finished_func_name]
            self.scope.pop(finished_func_name)
            self.func_relation.pop(finished_func_name)
            self.pc = ret_code
            if len(times) > 0 and times[0] + 1 < times[1]:
                self.stack.append(times[0] + 1)
                self.call_single_use_func(times[2], times[0] + 1, times[1])

    def run_command(self, op, arg_code):
        if op == 'push':
            self.stack.append(arg_code)
        elif op == 'op':
            self.op_realisation(arg_code)
        elif op == "is":
            self.is_realisation(arg_code)
        elif op == "to":
            self.to_realisation(arg_code)
        elif op == "call":
            self.call_realisation(arg_code)
        elif op == "exit":
            self.exit_realisation()

    def run_given_code(self):
        while self.pc < len(self.code):
            op_code = self.code[self.pc] % 8
            arg_code = self.code[self.pc] // 8
            op = OP_NAMES[op_code]
            self.run_command(op, arg_code)
            self.pc += 1

    def run_by_line(self):
        while True:
            line_of_code = input(">")
            interpreter(self, parse(line_of_code))
            print()


def disassemble(code):
    i = 0
    entry = code[0]
    code = code[1:]
    for command in code:
        if i == entry:
            print("entry")
        op_code = command % 8
        arg_code = command // 8
        op = OP_NAMES[op_code]
        if op == "op":
            print(i, op, list(LIB.keys())[arg_code])
        else:
            print(i, op, arg_code)
        i += 1


def parse(code: str):
    i = 0
    splitted = code.split()
    parse_res = []
    func_stack = []
    curr_func = parse_res
    while i < len(splitted):
        if splitted[i].isdigit():
            curr_func.append(("push", int(splitted[i])))
        elif splitted[i] in ["to", "is"]:
            curr_func.append((splitted[i], splitted[i + 1]))
            i += 1
        elif splitted[i] in LIB_OPS:
            curr_func.append(("op", splitted[i]))
        elif splitted[i] == "[":
            new_func = []
            func_stack.append(curr_func)
            curr_func.append(("push", new_func))
            curr_func = new_func
        elif splitted[i] == "]":
            curr_func = func_stack.pop()
        else:
            curr_func.append(("call", splitted[i]))
        i += 1
    return parse_res


def interpreter(vm: VirtualMachine, parsed_code):
    for command in parsed_code:
        op, arg = command
        vm.run_command(op, arg)
        if op == "call" and vm.scope[vm.find_name(arg)][arg][0] == "func":
            func_code = vm.pc
            interpreter(vm, func_code)
            vm.run_command("exit", 0)
        elif arg == "if":
            func_code = vm.pc
            interpreter(vm, func_code)
            vm.run_command("exit", 0)
        elif arg == "for":
            func_code = vm.pc
            number_of_iter = vm.func_stack[-1][3]
            for _ in range(number_of_iter):
                interpreter(vm, func_code)
                vm.run_command("exit", 0)


def to_bin_num(op_code, arg_code):
    return arg_code * 8 + op_code


def convert_name(name):
    power = 0
    out = 0
    for letter in name[::-1]:
        if letter not in possible_letters.keys():
            raise Exception(f"Не корректное название: {name}")
        out += (possible_letters[letter]) * (len(possible_letters) ** power)
        power += 1
    return out


def convert_code(parsed_code):
    code_of_funcs = [[]]
    for command in parsed_code:
        op, arg = command
        op_code = op_name_rev[op]
        if op == "push":
            if isinstance(arg, int):
                code_of_funcs[0].append(to_bin_num(op_code, arg))
            else:
                code_of_funcs[0].append([len(code_of_funcs) - 1, None])
                code_of_funcs.append(convert_code(arg))
        elif op == "op":
            code_of_funcs[0].append(to_bin_num(op_code, lib_ops_rev[arg]))
        elif op == "call":
            code_of_funcs[0].append(to_bin_num(op_code, convert_name(arg)))
        elif op in ("is", "to"):
            code_of_funcs[0].append(to_bin_num(op_code, convert_name(arg)))
    pointers = [0]
    index = 0
    for i in range(2, len(code_of_funcs)):
        index += len(code_of_funcs[i - 1]) - 1
        pointers.append(index)
    print(code_of_funcs)
    for i in range(0, len(code_of_funcs)):
        for num in code_of_funcs[i]:
            if isinstance(num, list):
                if num[1] is None:
                    num[1] = pointers[num[0]] + code_of_funcs[num[0]+1][0]
                else:
                    num[1] += pointers[i-1]
    out = []
    for i in range(1, len(code_of_funcs)):
        code_of_funcs[i].pop(0)
        out += code_of_funcs[i]
    out += code_of_funcs[0]
    out.insert(0, -1)
    for i in range(len(out)-1, -1, -1):
        if out[i] == 5:
            out[0] = i
            break
    if out[0] == -1:
        out[0] = 0
    out.append(5)
    return out


def compiler(code):
    parsed_code = parse(code)
    compile_res = convert_code(parsed_code)
    for i in range(len(compile_res)):
        if isinstance(compile_res[i], list):
            compile_res[i] = compile_res[i][1] * 8
    return compile_res


ex1 = "[ to n  n 2 < [ 1 ] [ n n 1 - fact * ] if ] is fact 5 fact ."
ex2 = """[ to a  a a ] is dup
[ to a ] is drop
[ 10 emit ] is cr
[
  to gen to scale to bits
  1 gen [ drop scale * ] for to width 
  width dup * array to buf
  width dup * [ to i  35 buf i ! ] for
  width scale /
  gen [ drop
    dup to block
    width [ to y
      width [ to x
        x block / scale % to loc-x
        y block / scale % to loc-y
        loc-y scale * loc-x + to loc-pos
        bits loc-pos >> 1 & [ ] [
          32 buf y width * x + !
        ] if
      ] for
    ] for
    scale /
  ] for drop
  width [ to y
    width [ to x  buf y width * x + @ emit ] for cr 
  ] for
] is fractal ? 3 3 fractal"""
ex = """[ to a a a ] is dup
[ to a ] is drop
[ to a 1 a [ ] if ] is exec
[ 10 emit ] is cr
1 array to seed 1 seed 0 !
[ seed 0 @ to x
  x 13 << x ^ to x
  x 17 >> x ^ to x
  x 5 << x ^ 1 32 << 1 - &
  dup seed 0 ! ] is rnd
32 array to pairs [ ] pairs 0 ! [ 108 emit 101 emit ] pairs 1 !
[ 120 emit 101 emit ] pairs 2 ! [ 103 emit 101 emit ] pairs 3 !
[ 122 emit 97 emit ] pairs 4 ! [ 99 emit 101 emit ] pairs 5 !
[ 98 emit 105 emit ] pairs 6 ! [ 115 emit 111 emit ] pairs 7 !
[ 117 emit 115 emit ] pairs 8 ! [ 101 emit 115 emit ] pairs 9 !
[ 97 emit 114 emit ] pairs 10 ! [ 109 emit 97 emit ] pairs 11 !
[ 105 emit 110 emit ] pairs 12 ! [ 100 emit 105 emit ] pairs 13 !
[ 114 emit 101 emit ] pairs 14 ! [ 97 emit ] pairs 15 !
[ 101 emit 114 emit ] pairs 16 ! [ 97 emit 116 emit ] pairs 17 !
[ 101 emit 110 emit ] pairs 18 ! [ 98 emit 101 emit ] pairs 19 !
[ 114 emit 97 emit ] pairs 20 ! [ 108 emit 97 emit ] pairs 21 !
[ 118 emit 101 emit ] pairs 22 ! [ 116 emit 105 emit ] pairs 23 !
[ 101 emit 100 emit ] pairs 24 ! [ 111 emit 114 emit ] pairs 25 !
[ 113 emit 117 emit ] pairs 26 ! [ 97 emit 110 emit ] pairs 27 !
[ 116 emit 101 emit ] pairs 28 ! [ 105 emit 115 emit ] pairs 29 !
[ 114 emit 105 emit ] pairs 30 ! [ 111 emit 110 emit ] pairs 31 !
[ 3 rnd 1 & + [ drop pairs rnd 31 & @ exec ] for ] is gen-star
100 [ drop gen-star cr ] for"""

compile_result = compiler(ex)
print(compile_result)
print(disassemble(compile_result))
#disassemble([17, 8, 5, 2, 2, 8, 9, 10, 17, 5, 4, 2, 16, 65, 0, 16, 105, 5, 72, 11, 40, 10, 121, 5])
vm = VirtualMachine(compile_result)
vm.run_given_code()
# print(parse(ex))
# ar1 = parse(ex)
# ar2 = [('push',
#   [('to', 'n'),
#    ('call', 'n'),
#    ('push', 2),
#    ('op', '<'),
#    ('push', [('push', 1)]),
#    ('push',
#     [('call', 'n'),
#      ('call', 'n'),
#      ('push', 1),
#      ('op', '-'),
#      ('call', 'fact'),
#      ('op', '*')]),
#    ('op', 'if')]),
#  ('is', 'fact'),
#  ('push', 5),
#  ('call', 'fact'),
#  ('op', '.')]
#
#
# print(ar1 == ar2)
# print("Вывод дизассеблера")
# disassemble(ex)
# vm = VirtualMachine(ex)
# print("Вывод кода")
# vm.run()
