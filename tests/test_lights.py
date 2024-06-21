import panda3d.core as p3d


def test_lights_intensity(load_blend):
    model = p3d.NodePath(load_blend('litplane'))
    model.ls()

    point_light = model.find('**/+PointLight')
    assert point_light
    assert point_light.node().color == p3d.LColor(20, 20, 20, 20)

    directional_light = model.find('**/+DirectionalLight')
    assert directional_light
    assert directional_light.node().color == p3d.LColor(1, 1, 1, 1)
