import re
import ast
import unittest


def parse(data):
    try:
        return ast.parse(data)
    except IndentationError:
        data = data.rstrip()
        line = data.splitlines()[-1]
        whitespaces = re.findall(r'^(\s+)(.*)', line)
        if whitespaces:
            whitespace, line = whitespaces[0]
            data = data.splitlines() + [whitespace + '  pass']
            data = '\n'.join(data)
            return ast.parse(data)
        raise

def get_last_class_def(data):
    tree = parse(data)
    try:
        return [t for t in tree.body if isinstance(t, ast.ClassDef)][-1]
    except IndexError:
        return None

def get_last_function_def(data):
    if isinstance(data, basestring):
        tree = parse(data)
    else:
        tree = data
    try:
        return [t for t in tree.body if isinstance(t, ast.FunctionDef)][-1]
    except IndexError:
        return None

def get_super(data, line=None, indent=False):
    """
    Returns super statement. Statement is computed for the last found method
    in given ``data``.

    :param data: source given as a string
    :param line: line indicating where we should strip source. Defaults to last
      line of the given ``data``.
    """
    lines = data.splitlines()
    if line is None:
        line = len(lines) - 1
    newdata = '\n'.join(lines[:line])
    cdef = get_last_class_def(newdata)
    if cdef:
        class_name = cdef.name
        fun = get_last_function_def(cdef)
        if fun:
            self_name = fun.args.args[0].id
            fun_name = fun.name
            args = [a.id for a in fun.args.args[1:]]
            if fun.args.vararg:
                args.append('*' + fun.args.vararg)
            if fun.args.kwarg:
                args.append('**' + fun.args.kwarg)
            args = ', '.join(args)
            value = "super({cname}, {self_name}).{fname}({args})".format(
                cname=class_name,
                self_name=self_name,
                fname=fun_name,
                args=args,
            )
            if indent:
                value = ' ' * (cdef.col_offset + fun.col_offset * 2) + value
            return value



class GetSuperTests(unittest.TestCase):

    code = '''# 1
class Person(object):
    
    def get_full_name(self):
        return 'Foo Bar' # 5

    def get_foo(this, foo, bar, baz='foo'):
        pass

# 10
class Student(Person): 
    def get_full_name(self):
        pass

    def get_foo(self, name='foo', *args, **kwargs): # 15
        pass

'''

    def test_get_super_Person_get_full_name(self):
        self.assertEqual(get_super(self.code, 5),
            'super(Person, self).get_full_name()')

    def test_Person_get_foo(self):
        self.assertEqual(get_super(self.code, 8),
            "super(Person, this).get_foo(foo, bar, baz)")

    def test_Student_get_foo(self):
        self.assertEqual(get_super(self.code, 16),
            'super(Student, self).get_foo(name, *args, **kwargs)')

    def test_Student_get_foo_with_proper_indent(self):
        self.assertEqual(get_super(self.code, 16, True),
            '        super(Student, self).get_foo(name, *args, **kwargs)')

    def test_works_for_wrong_indent_or_missing_last_line(self):
        code = '''
class Person(object):

    def foo(self):
        pass

    def bar(self):'''

        self.assertEqual(get_super(code, 7), 'super(Person, self).bar()')



if __name__ == '__main__':
    unittest.main()

