# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:03:17 2025

@author: jdkem
"""
import mooonpy
#from mooonpy import guis, tools, molspace

#import mooonpy
#from mooonpy import molspace as ms
#from mooonpy import thermospace as ts

# print(mooonpy.molspace.molspace.Molspace())
# print(mooonpy.Molspace())

# print(mooonpy.molspace.doc_examples.add(1,3))
# print(mooonpy.DocExamples.add(1,3))


#print('full : ', mooonpy) #.doc_examples.add(1, 2))
#print('alias: ', ms.hw.hello_world())


#print('full : ', mooonpy.thermospace.multiply(x=5, y=10))
#print('alias: ',  ts.lw.multiply(x=5, y=10))


file = 'EPON_862/all2lmp_Outputs/detda_typed_IFF.data'
#file = 'EPON_862/detda_typed_IFF_merged.data'

#file = 'EPON_862/Cellulose-supercell_morse_IFF.data'
#file = 'EPON_862/system1_cell_replicate.data'

molecule = mooonpy.Molspace(filename=file, astyles=['full', 'all1'], dsect=['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities'])



if __name__ == '__main__':
    import timeit
    
    file = 'EPON_862/detda_typed_IFF_merged.data'
    file = 'EPON_862/system1_cell_replicate.data'
    def call_mooonpy():
        m = mooonpy.Molspace(filename=file, read='mooonpy', astyles=['full', 'all1'])
        # i = 1
        # print(m.atoms[i].comment, m.atoms[i].diameter)
    
    def call_lunar():
        l = mooonpy.Molspace(filename=file, read='lunar', astyles=['full'])    
    
    number = 1
    print('\n\n')
    mooonpy_time = timeit.timeit(stmt=call_mooonpy, number=number)
    print(f'mooonpy read time  : {mooonpy_time} seconds for {number} runs on 100,000 atom system')
    
    print('\n\n')
    lunar_time = timeit.timeit(stmt=call_lunar, number=number)
    print(f'lunar read time  : {lunar_time} seconds for {number} runs on 100,000 atom system')
    
    
    # class A:
    #     def __init__(self, **kwargs):
    #         print(kwargs)
    #         self.a = kwargs.pop('a', None)

    # class B:
    #     def __init__(self, **kwargs):
    #         print(kwargs)
    #         self.b = kwargs.pop('b', None)
    
    # class Combined:
    #     def __init__(self, **kwargs):
    #         self.a_obj = A(**kwargs)
    #         self.b_obj = B(**kwargs)
    #         self.c = kwargs.get('c', None)  # for Combined-specific args
    #         print(kwargs)
            
    # obj = Combined(a=1, b=2, c=3)
    # print(obj.a_obj.a)  # 1
    # print(obj.b_obj.b)  # 2
    # print(obj.c)        # 3
    

    
    

    

        
        
