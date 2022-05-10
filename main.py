
class Foo:
    a = {}


a = Foo()
a.a["blah"] = 4

b = Foo()

print(a.a)
print(b.a)

if __name__ == "__main__":
    pass
