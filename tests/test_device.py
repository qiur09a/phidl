import pytest
import numpy as np

from phidl import Device#, Layer, LayerSet, make_device, Port
# import phidl.geometry as pg
# import phidl.routing as pr
# import phidl.utilities as pu

def test_add_polygon1():
    D = Device()
    D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'c0629d2a7c557f72fad131ae8260df22c1df2d56')

def test_add_polygon2():
    D = Device()
    D.add_polygon( [(8,6), (6,8), (7,9), (9,5)] )
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'c0629d2a7c557f72fad131ae8260df22c1df2d56')

def test_add_polygon3():
    D = Device()
    D.add_polygon( [(8,6), (6,8), (7,9), (9,5)], layer = 7)
    D.add_polygon( [(8,0), (6,8), (7,9), (9,5)], layer = (8,0))
    D.add_polygon( [(8,1), (6,8), (7,9), (9,5)], layer = (9,1))
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '96abc3c9e30f3bbb32c5a39aeea2ba0fa3b13ebe')
    
    
# Test polygon manipulation
def test_move():
    # Test polygon move
    D = Device()
    p = D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    p.move([1.7,0.8])
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '57a86bce5f60f7bc78c7c30473a544b736d2afb3')
    p.movex(13.9)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '8fe6706e05ebe1512ee2efe2582546b949fbc48f')
    p.movey(19.2)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '7df43241eca2dd11f267c25876e650eadaca7d9f')
    # Test Device move
    D = Device()
    D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    D.add_polygon( [(8,6,7,9,7,0), (6,8,9,5,7,0)] )
    D.move([1.7,0.8])
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'c863156dd00a590dc02823e1791554d4142b1ea9')

def test_rotate():
    # Test polygon rotation
    D = Device()
    p = D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    p.rotate(37.5)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '2e4815072eabe053c3029d9e29a5b3ed59fe9bb7')
    # Test Device rotation
    D = Device()
    p = D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    D.rotate(37.5)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '2e4815072eabe053c3029d9e29a5b3ed59fe9bb7')

def test_reflect():
    # Test polygon reflection
    D = Device()
    p = D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    p.reflect(p1 = (1.7,2.5), p2 = (4.5, 9.1))
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'bc6ae5308c2240e425cd503e0cdda30007bbfc4d')
    # Test Device reflection
    D = Device()
    p = D.add_polygon( [(8,6,7,9), (6,8,9,5)] )
    D.reflect(p1 = (1.7,2.5), p2 = (4.5, 9.1))
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'bc6ae5308c2240e425cd503e0cdda30007bbfc4d')


def test_port_add():
    D = Device()
    D.add_port(name = 'test123', midpoint = (5.7, 9.2), orientation = 37)
    D.add_port(name = 'test456', midpoint = (1.5, 6.7), orientation = 99)
    assert(len(D.ports) == 2)
    assert(np.allclose(D.ports['test123'].midpoint, (5.7, 9.2)))
    assert(np.allclose(D.ports['test456'].midpoint, (1.5, 6.7)))
    assert(D.ports['test123'].orientation == 37)
    assert(D.ports['test456'].orientation == 99)

def test_port_reference_manipulate():
    D = Device()
    D.add_port(name = 'test123', midpoint = (5.7, 9.2), orientation = 37)
    d = D.add_ref(D).move([1,1]).rotate(45)
    assert(np.allclose(d.ports['test123'].midpoint,
        (-2.474873734152916, 11.950104602052654)))
    assert(d.ports['test123'].orientation == 37+45)


def test_port_remove():
    D = Device()
    D.add_port(name = 'test123', midpoint = (5.7, 9.2), orientation = 37)
    D.add_port(name = 'test456', midpoint = (1.5, 6.7), orientation = 99)
    E = Device()
    d = E << D
    D.remove(D.ports['test123'])
    assert(len(D.ports) == 1)
    assert(len(d.ports) == 1)
    assert(D.ports['test456'])
    assert(d.ports['test456'])


def test_flatten():
    D = Device()
    E1 = Device()
    E2 = Device()
    E1.add_polygon( [(8,6,7,9,7,0), (6,8,9,5,7,0)], layer = 8)
    E2.add_polygon( [(18,16,17,19,17,10), (16,18,19,15,17,10)], layer = 9)
    D << E1
    D << E2
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '8a057feca51d8097f2a915eda558fe2a9b88fb13')
    D.flatten()
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '8a057feca51d8097f2a915eda558fe2a9b88fb13')
    D.flatten(single_layer = (5,5))
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'cfc1ba30384f5f1f7d888f47f16d1f310f95b464')


def test_remove_layers():
    D = Device()
    D.add_polygon( [(8,6,7,9,7), (6,8,9,5,7)], layer = 13)
    D.add_polygon( [(18,16,17,19,17), (16,18,19,15,17)], layer = 14)
    xpts = list(range(1000))
    ypts = [x % 73 for x in xpts]
    p = D.add_polygon([xpts,ypts], layer = 15)
    p.fracture(max_points = 13, precision = 1e-4)
    # Switch part of the polygons to layer (14,0)
    p.layers[13:17] = [14]*4
    # Switch part of the polygons to layer (14,1)
    p.layers[23:27] = [14]*4
    p.datatypes[23:27] = [1]*4
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '7a7aa6a22b3d0b852a0e465398018dd19a1be305')
    D.remove_layers(layers = [13,(14,0)])
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'bb81ec3b3a6be2372a7ffc32f57121a9f1a97b34')