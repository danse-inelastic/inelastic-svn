    def _convert(self, data):
        '''a list read from the commandline is parsed as ['[1','2','3','4]']
instead of [1,2,3,4,5]; if so, force conversion of list items to floats'''
        if (data != []) and (data[0].__class__() == ''):
            z = []
            y = []
            for x in data:
                islist = True
                if x[0] == '[': y = []
                try:
                    y.append(float(x.lstrip('[').rstrip(']')))
                except:
                    w = x.lstrip('[').lstrip('"').lstrip("'")
                    w = w.rstrip(']').rstrip('"').rstrip("'")
                    z.append(w)
                    islist = False
                if (x[-1] == ']') and (islist): z.append(y)
            data = z
        return data

