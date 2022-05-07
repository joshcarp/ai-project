from collections import deque

# initialising a deque() of arbitrary length
linked_lst = deque()
a = {"foo": "bar"}

b = ["one", "two", a]

c = b.copy()

a["foo"] = "blah"
print(b)
print(c)


# filling deque() with elements
linked_lst.append(a)
linked_lst.append('second')
linked_lst.append('third')

linked_lstcpy = linked_lst.copy()

linked_lstcpy.appendleft("zeroth")

a["nah"] = "foo"
print("elements in the linked_list:")
print(linked_lst)
print(linked_lstcpy)


if __name__ == "__main__":
    pass
