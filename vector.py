#coding=utf-8
import math
from decimal import Decimal, getcontext

getcontext().prec = 15

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'Zero vector has no unique parallel component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two or three dims'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    '''向量的加法'''
    def plus (self , v):
        new_coordinates = [x + y for x , y in zip(self.coordinates,v.coordinates)]
        return new_coordinates


    '''向量的减法'''
    def minus (self, v):
        new_coordinates = [x - y for x , y in zip(self.coordinates, v.coordinates)]
        return new_coordinates

    '''数和向量的乘积'''
    def times_scalar(self , v):
        new_coordinates = [Decimal(v) * x for x in self.coordinates]
        return new_coordinates

    '''求向量的大小'''
    def magnitude (self):
        #size = 0
        #for x in self.coordinates:
        #    size += x * x
        #return math.sqrt(size)
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return Decimal(math.sqrt(sum(coordinates_squared))) 

    '''向量的标准化'''
    def normalized (self):
        #size = self.compute_size()
        #if size == 0:
        #    return "该向量是零向量"
        #else :
        #    new_coordinates = [1 / size * x for x in self.coordinates]
        #return new_coordinates
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0') / magnitude)
        except ZeroDivisionError :
            raise Exception('Cannot normalize the zero vector')

    '''向量的点积'''
    def dot(self, v):
        coordinates_products = [x * y for x , y in zip(self.coordinates, v.coordinates)]
        return sum(coordinates_products)

    '''向量之间的夹角'''
    def angle_with(self, v , in_degree = False):
        #dot = self.dot(v)
        #try:
        #    if in_degree:
        #        return math.acos(dot /(self.magnitude() * v.magnitude() * 1.0) ) * 180. / math.pi
        #    return math.acos(dot /(self.magnitude() * v.magnitude() * 1.0) )
        #except ZeroDivisionError :
        #    raise Exception('Cannot normalize the zero vector')
        try:
            u1 = Vector(self.normalized())
            u2 = Vector(v.normalized())
            angle_in_radians = math.acos(u1.dot(u2))
            if in_degree:
                degrees_per_radian = 180. / math.pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot comput an angle with the zero vector')
            else:
                raise e

    '''两个向量是否垂直'''
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    '''两个向量是否平行'''
    def is_parallel_to(self, v):
        return(self.is_zero() or 
            v.is_zero() or
            self.angle_with(v) == 0 or
            self.angle_with(v) == math.pi)

    '''向量是否为零'''
    def is_zero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance

    '''在某个向量上的垂直分量'''
    def component_orthogonal_to(self, v):
        #u2 = Vector(self.component_orthogonal_to(v))
        #return self.minus(u2)
        try:
            projection = Vector(self.component_parallel_to(v))
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
        
    '''在某个向量上的平行分量'''
    def component_parallel_to(self, v):
        #u1 = Vector(v.normalized())
        #dot_result = self.dot(u1)
        #return u1.times_scalar(dot_result)
        try:
            u = Vector(v.normalized())
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    '''向量积'''
    def cross(self, v):        
        #new_self = []
        #for e in self.coordinates:
        #    new_self.append(e)
#
        #new_v = []
        #for e in v.coordinates:
        #    new_v.append(e)
#
        #while len(new_self) < 3 :
        #    new_self.append(0)
#
        #while len(new_v) < 3 :
        #    new_v.append(0)   
        #        
        #x_axis = Vector(new_self).coordinates[1] * Vector(new_v).coordinates[2] * Decimal('1.0') - Vector(new_self).coordinates[2] * Vector(new_v).coordinates[1] * Decimal('1.0')
        #y_axis = Vector(new_self).coordinates[2] * Vector(new_v).coordinates[0] * Decimal('1.0') - Vector(new_self).coordinates[0] * Vector(new_v).coordinates[2] * Decimal('1.0')
        #z_axis = Vector(new_self).coordinates[0] * Vector(new_v).coordinates[1] * Decimal('1.0') - Vector(new_self).coordinates[1] * Vector(new_v).coordinates[0] * Decimal('1.0')
        #return Vector([x_axis, y_axis, z_axis])

        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [ y_1 * z_2 - y_2 * z_1 ,
                                -(x_1 * z_2 - x_2 * z_1) ,
                                x_1 * y_2 - x_2 * y_1 ]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    '''两个向量构成的平行四边形的面积'''
    def area_of_parallelogram(self, v):
        return self.cross(v).magnitude()

    '''两个向量构成的三角形的面积'''
    def area_of_traigle(self, v):
        return self.area_of_parallelogram(v) / Decimal('2.0') 
        


v = Vector([3.039, 1.879])
w = Vector([0.825, 2.036])

#print v.magnitude()
#
#print v.component_parallel_to(w)
#print v.component_orthogonal_to(w)

#print v.cross(w)
#print v.area_of_parallelogram(w)
#print v.area_of_traigle(w)
#print v.is_parallel_to(w)
#print v.is_orthogonal_to(w)
