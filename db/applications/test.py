class Parent:
    x=4
    
    class Foo:
#        p=Parent()
#        y=p.x
        
        baz = 'hello from Parent.Foo'

class Child(Parent):
    #Foo.baz = 'hello from Child.Foo'
    pass

#p=Parent()
#print p.Foo.y

class Outer:
  def __init__(self):
    self.x = 5

  class Inner:
    def __init__(self):
      self.y = 10

if __name__ == '__main__':
  outer =  Outer()
  inner = outer.Inner()
  print outer.x
  print inner.y
  print inner.x