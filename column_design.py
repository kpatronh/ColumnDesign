import numpy as np


class ColumnDesign:
    '''
    Formulas for the structural design of axially loaded columns (no excentric loadings)
    Reference:  Budyunas, G., Nisbett, K. (2008) Shigley's Mechanical Design, McGrawHill
    '''


    @staticmethod
    def area_req_compression(F, S):
        '''
        Minimum required area against compression 
        F: compression load 
        S: material allowable compression strength
        '''
        return F/S

    @staticmethod
    def Euler_buckling_critical_load(E, I, L, C):
        '''
        Buckling critical load for Euler columns
        E: material Young's modulus
        I: cross section moment of inertia
        L: column length
        C: constant related to boundary conditions
        '''
        try:
            return (C*(np.pi**2)*E*I)/(L**2)
        except ZeroDivisionError:
            print('Invalid length')

    @staticmethod
    def radius_gyration(I,A):
        '''
        Cross section radius of gyration
        I: cross section moment of inertia
        A: cross section area
        '''
        try:
            return np.sqrt(I/A)
        except ZeroDivisionError:
            print('Invalid area')


    @staticmethod
    def slenderness_ratio(L, k):
        '''
        Slenderness ratio
        L: column length
        k: radius of gyration
        '''
        try:
            return L/k
        except ZeroDivisionError:
            print('Invalid radius of gyration')

    
    @staticmethod
    def Euler_unit_buckling_critical_load(E, I, L, C, A):
        '''
        Unitary buckling critical load      
        E: material Young's modulus
        I: cross section moment of inertia
        L: column length
        C: constant related to boundary conditions
        '''
        try:
            k = ColumnDesign.radius_gyration(I, A)
            return (C*(np.pi**2)*E)/(ColumnDesign.slenderness_ratio(L,k)**2)
        except ZeroDivisionError:
            print('Invalid slenderness ratio')

    @staticmethod
    def is_Euler_column(C, E, Sy, L, A, I):
        '''
        This method indicates whether a given column is an Euler column (see reference)
        
        E : material Young's modulus
        I : cross section moment of inertia
        L : column length
        C : constant related to boundary conditions
        Sy: material yield strength
        A : cross section area 
        '''
        try:
            k = ColumnDesign.radius_gyration(I, A)
            lk = ColumnDesign.slenderness_ratio(L, k)
            lk1 = np.sqrt((2*(np.pi**2)*C*E)/Sy)
            return lk > lk1
        except ZeroDivisionError:
            print('Invalid input data')

    @staticmethod
    def Jhonson_unit_buckling_critical_load(E, I, L, C, A, Sy):
        '''
        Jhonson's unit buckling critical load

        E : material Young's modulus
        I : cross section moment of inertia
        L : column length
        C : constant related to boundary conditions
        Sy: material yield strength
        A : cross section area 
        '''
        try:
            k = ColumnDesign.radius_gyration(I, A)
            a1 = ((Sy*L)/(2*np.pi*k))**2
            a2 = 1/(C*E)
            return Sy - a1*a2
        except ZeroDivisionError:
            print('Invalid input data')

        
    @staticmethod
    def Jhonson_buckling_critical_load(E, I, L, C, A, Sy):
        '''
        Jhonson's buckling critical load

        E : material Young's modulus
        I : cross section moment of inertia
        L : column length
        C : constant related to boundary conditions
        Sy: material yield strength
        A : cross section area 
        '''
        unit_crit_load = ColumnDesign.Jhonson_unit_buckling_critical_load(E, I, L, C, A, Sy)
        return unit_crit_load*A

    @staticmethod
    def SF_compression(S_allow, F, A):
        try:
            S_compr = F/A
            SF = S_allow/S_compr
            return SF
        except ZeroDivisionError:
            print('Invalid input data')

    @staticmethod
    def SF_buckling(E, I, L, C, A, Sy, F):
        try:
            is_Euler_column = ColumnDesign.is_Euler_column(C, E, Sy, L, A, I)    
            if is_Euler_column:
                print('Euler buckling critical load formula is used')
                p_crit = ColumnDesign.Euler_buckling_critical_load(E, I, L, C)
            else:
                print('Johnson buckling critical load formula is used')
                p_crit = ColumnDesign.Jhonson_buckling_critical_load(E, I, L, C, A, Sy)
            print('Buckling critical load = {} N'.format(p_crit))
            SF = p_crit/F
            return SF
        except Exception:
            print('Invalid input data')
    
    
