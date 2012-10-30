class Person(object):
    
    def get_name(self):
        pass

    def get_full_name(self):
        return 'Foo Bar'

    def get_foo(this, foo, bar, baz='foo'):
        pass


class Student(Person): 

    def get_name(this):
        pass

    def get_full_name(self):
        pass

    def get_foo(self, name='foo', *args, **kwargs):
        pass

