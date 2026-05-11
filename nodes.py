import bpy
import mathutils

def sprite_color_1_node_group():
    """Initialize Sprite Color node group"""
    sprite_color_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Sprite Color")

    sprite_color_1.color_tag = 'NONE'
    sprite_color_1.description = ""
    sprite_color_1.default_group_node_width = 140
    # sprite_color_1 interface

    # Socket Result
    result_socket = sprite_color_1.interface.new_socket(name="Result", in_out='OUTPUT', socket_type='NodeSocketColor')
    result_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    result_socket.attribute_domain = 'POINT'
    result_socket.description = "Color"
    result_socket.default_input = 'VALUE'
    result_socket.structure_type = 'AUTO'

    # Socket Blend
    blend_socket = sprite_color_1.interface.new_socket(name="Blend", in_out='INPUT', socket_type='NodeSocketFloat')
    blend_socket.default_value = 0.0
    blend_socket.min_value = -3.4028234663852886e+38
    blend_socket.max_value = 3.4028234663852886e+38
    blend_socket.subtype = 'NONE'
    blend_socket.attribute_domain = 'POINT'
    blend_socket.default_input = 'VALUE'
    blend_socket.structure_type = 'AUTO'

    # Initialize sprite_color_1 nodes

    # Node Group Output
    group_output = sprite_color_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Attribute.003
    attribute_003 = sprite_color_1.nodes.new("ShaderNodeAttribute")
    attribute_003.name = "Attribute.003"
    attribute_003.attribute_name = "rendercolor"
    attribute_003.attribute_type = 'OBJECT'

    # Node Gamma
    gamma = sprite_color_1.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Node Mix
    mix = sprite_color_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'

    # Node Attribute.004
    attribute_004 = sprite_color_1.nodes.new("ShaderNodeAttribute")
    attribute_004.name = "Attribute.004"
    attribute_004.attribute_name = "rendermode"
    attribute_004.attribute_type = 'OBJECT'

    # Node Math.005
    math_005 = sprite_color_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'COMPARE'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = 3.0
    # Value_002
    math_005.inputs[2].default_value = 0.0

    # Node Math.006
    math_006 = sprite_color_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'COMPARE'
    math_006.use_clamp = False
    # Value_001
    math_006.inputs[1].default_value = 5.0
    # Value_002
    math_006.inputs[2].default_value = 0.0

    # Node Math.007
    math_007 = sprite_color_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'MAXIMUM'
    math_007.use_clamp = False

    # Node Group Input
    group_input = sprite_color_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Math.001
    math_001 = sprite_color_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 255.0

    # Set locations
    sprite_color_1.nodes["Group Output"].location = (480.0, 120.0)
    sprite_color_1.nodes["Attribute.003"].location = (0.0, -60.0)
    sprite_color_1.nodes["Gamma"].location = (160.0, -40.0)
    sprite_color_1.nodes["Mix"].location = (320.0, 120.0)
    sprite_color_1.nodes["Attribute.004"].location = (-320.0, 120.0)
    sprite_color_1.nodes["Math.005"].location = (-160.0, 120.0)
    sprite_color_1.nodes["Math.006"].location = (0.0, 120.0)
    sprite_color_1.nodes["Math.007"].location = (160.0, 120.0)
    sprite_color_1.nodes["Group Input"].location = (0.0, -240.0)
    sprite_color_1.nodes["Math.001"].location = (160.0, -120.0)

    # Set dimensions
    sprite_color_1.nodes["Group Output"].width  = 140.0
    sprite_color_1.nodes["Group Output"].height = 100.0

    sprite_color_1.nodes["Attribute.003"].width  = 140.0
    sprite_color_1.nodes["Attribute.003"].height = 100.0

    sprite_color_1.nodes["Gamma"].width  = 140.0
    sprite_color_1.nodes["Gamma"].height = 100.0

    sprite_color_1.nodes["Mix"].width  = 140.0
    sprite_color_1.nodes["Mix"].height = 100.0

    sprite_color_1.nodes["Attribute.004"].width  = 140.0
    sprite_color_1.nodes["Attribute.004"].height = 100.0

    sprite_color_1.nodes["Math.005"].width  = 140.0
    sprite_color_1.nodes["Math.005"].height = 100.0

    sprite_color_1.nodes["Math.006"].width  = 140.0
    sprite_color_1.nodes["Math.006"].height = 100.0

    sprite_color_1.nodes["Math.007"].width  = 140.0
    sprite_color_1.nodes["Math.007"].height = 100.0

    sprite_color_1.nodes["Group Input"].width  = 140.0
    sprite_color_1.nodes["Group Input"].height = 100.0

    sprite_color_1.nodes["Math.001"].width  = 140.0
    sprite_color_1.nodes["Math.001"].height = 100.0


    # Initialize sprite_color_1 links

    # math_006.Value -> math_007.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.006"].outputs[0],
        sprite_color_1.nodes["Math.007"].inputs[0]
    )
    # math_005.Value -> math_007.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.005"].outputs[0],
        sprite_color_1.nodes["Math.007"].inputs[1]
    )
    # attribute_003.Color -> gamma.Color
    sprite_color_1.links.new(
        sprite_color_1.nodes["Attribute.003"].outputs[0],
        sprite_color_1.nodes["Gamma"].inputs[0]
    )
    # attribute_004.Factor -> math_005.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Attribute.004"].outputs[2],
        sprite_color_1.nodes["Math.005"].inputs[0]
    )
    # attribute_004.Factor -> math_006.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Attribute.004"].outputs[2],
        sprite_color_1.nodes["Math.006"].inputs[0]
    )
    # mix.Result -> group_output.Result
    sprite_color_1.links.new(
        sprite_color_1.nodes["Mix"].outputs[2],
        sprite_color_1.nodes["Group Output"].inputs[0]
    )
    # gamma.Color -> mix.A
    sprite_color_1.links.new(
        sprite_color_1.nodes["Gamma"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[6]
    )
    # math_001.Value -> mix.B
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.001"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[7]
    )
    # math_007.Value -> mix.Factor
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.007"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[0]
    )
    # group_input.Blend -> math_001.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Group Input"].outputs[0],
        sprite_color_1.nodes["Math.001"].inputs[0]
    )

    return sprite_color_1

def sprite_frame_offset_1_node_group():
    """Initialize Sprite Frame Offset node group"""
    sprite_frame_offset_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Sprite Frame Offset")

    sprite_frame_offset_1.color_tag = 'NONE'
    sprite_frame_offset_1.description = ""
    sprite_frame_offset_1.default_group_node_width = 238
    # sprite_frame_offset_1 interface

    # Socket Vector
    vector_socket = sprite_frame_offset_1.interface.new_socket(name="Vector", in_out='OUTPUT', socket_type='NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'
    vector_socket.default_input = 'VALUE'
    vector_socket.structure_type = 'AUTO'

    # Socket Frames
    frames_socket = sprite_frame_offset_1.interface.new_socket(name="Frames", in_out='INPUT', socket_type='NodeSocketInt')
    frames_socket.default_value = 0
    frames_socket.min_value = 0
    frames_socket.max_value = 2147483647
    frames_socket.subtype = 'NONE'
    frames_socket.attribute_domain = 'POINT'
    frames_socket.default_input = 'VALUE'
    frames_socket.structure_type = 'AUTO'

    # Initialize sprite_frame_offset_1 nodes

    # Node Group Output
    group_output = sprite_frame_offset_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = sprite_frame_offset_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Separate XYZ
    separate_xyz = sprite_frame_offset_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Attribute
    attribute = sprite_frame_offset_1.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "frame"
    attribute.attribute_type = 'OBJECT'

    # Node Math
    math = sprite_frame_offset_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'ADD'
    math.use_clamp = False

    # Node Math.001
    math_001 = sprite_frame_offset_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False

    # Node Combine XYZ
    combine_xyz = sprite_frame_offset_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Texture Coordinate
    texture_coordinate = sprite_frame_offset_1.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False
    texture_coordinate.outputs[0].hide = True
    texture_coordinate.outputs[1].hide = True
    texture_coordinate.outputs[3].hide = True
    texture_coordinate.outputs[4].hide = True
    texture_coordinate.outputs[5].hide = True
    texture_coordinate.outputs[6].hide = True

    # Set locations
    sprite_frame_offset_1.nodes["Group Output"].location = (20.0, -80.0)
    sprite_frame_offset_1.nodes["Group Input"].location = (-460.0, -60.0)
    sprite_frame_offset_1.nodes["Separate XYZ"].location = (-620.0, -80.0)
    sprite_frame_offset_1.nodes["Attribute"].location = (-620.0, 100.0)
    sprite_frame_offset_1.nodes["Math"].location = (-460.0, 100.0)
    sprite_frame_offset_1.nodes["Math.001"].location = (-300.0, 20.0)
    sprite_frame_offset_1.nodes["Combine XYZ"].location = (-140.0, -80.0)
    sprite_frame_offset_1.nodes["Texture Coordinate"].location = (-780.0, -80.0)

    # Set dimensions
    sprite_frame_offset_1.nodes["Group Output"].width  = 140.0
    sprite_frame_offset_1.nodes["Group Output"].height = 100.0

    sprite_frame_offset_1.nodes["Group Input"].width  = 140.0
    sprite_frame_offset_1.nodes["Group Input"].height = 100.0

    sprite_frame_offset_1.nodes["Separate XYZ"].width  = 140.0
    sprite_frame_offset_1.nodes["Separate XYZ"].height = 100.0

    sprite_frame_offset_1.nodes["Attribute"].width  = 140.0
    sprite_frame_offset_1.nodes["Attribute"].height = 100.0

    sprite_frame_offset_1.nodes["Math"].width  = 140.0
    sprite_frame_offset_1.nodes["Math"].height = 100.0

    sprite_frame_offset_1.nodes["Math.001"].width  = 140.0
    sprite_frame_offset_1.nodes["Math.001"].height = 100.0

    sprite_frame_offset_1.nodes["Combine XYZ"].width  = 140.0
    sprite_frame_offset_1.nodes["Combine XYZ"].height = 100.0

    sprite_frame_offset_1.nodes["Texture Coordinate"].width  = 140.0
    sprite_frame_offset_1.nodes["Texture Coordinate"].height = 100.0


    # Initialize sprite_frame_offset_1 links

    # math_001.Value -> combine_xyz.X
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Math.001"].outputs[0],
        sprite_frame_offset_1.nodes["Combine XYZ"].inputs[0]
    )
    # separate_xyz.Y -> combine_xyz.Y
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Separate XYZ"].outputs[1],
        sprite_frame_offset_1.nodes["Combine XYZ"].inputs[1]
    )
    # math.Value -> math_001.Value
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Math"].outputs[0],
        sprite_frame_offset_1.nodes["Math.001"].inputs[0]
    )
    # attribute.Factor -> math.Value
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Attribute"].outputs[2],
        sprite_frame_offset_1.nodes["Math"].inputs[0]
    )
    # separate_xyz.X -> math.Value
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Separate XYZ"].outputs[0],
        sprite_frame_offset_1.nodes["Math"].inputs[1]
    )
    # group_input.Frames -> math_001.Value
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Group Input"].outputs[0],
        sprite_frame_offset_1.nodes["Math.001"].inputs[1]
    )
    # combine_xyz.Vector -> group_output.Vector
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Combine XYZ"].outputs[0],
        sprite_frame_offset_1.nodes["Group Output"].inputs[0]
    )
    # texture_coordinate.UV -> separate_xyz.Vector
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Texture Coordinate"].outputs[2],
        sprite_frame_offset_1.nodes["Separate XYZ"].inputs[0]
    )

    return sprite_frame_offset_1

def additive_shader_1_node_group():
    """Initialize Additive Shader node group"""
    additive_shader_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Additive Shader")

    additive_shader_1.color_tag = 'NONE'
    additive_shader_1.description = ""
    additive_shader_1.default_group_node_width = 180
    # additive_shader_1 interface

    # Socket Shader
    shader_socket = additive_shader_1.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket Color
    color_socket = additive_shader_1.interface.new_socket(name="Color", in_out='INPUT', socket_type='NodeSocketColor')
    color_socket.default_value = (0.5, 0.5, 0.5, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.default_input = 'VALUE'
    color_socket.structure_type = 'AUTO'

    # Initialize additive_shader_1 nodes

    # Node Group Output
    group_output = additive_shader_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = additive_shader_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Attribute
    attribute = additive_shader_1.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "r_blend"
    attribute.attribute_type = 'OBJECT'

    # Node Attribute.001
    attribute_001 = additive_shader_1.nodes.new("ShaderNodeAttribute")
    attribute_001.name = "Attribute.001"
    attribute_001.attribute_name = "rendercolor"
    attribute_001.attribute_type = 'OBJECT'

    # Node Vector Math
    vector_math = additive_shader_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'

    # Node Mix
    mix = additive_shader_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Transparent BSDF
    transparent_bsdf = additive_shader_1.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Emission
    emission = additive_shader_1.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Add Shader
    add_shader = additive_shader_1.nodes.new("ShaderNodeAddShader")
    add_shader.name = "Add Shader"

    # Node Gamma
    gamma = additive_shader_1.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Set locations
    additive_shader_1.nodes["Group Output"].location = (660.0, -40.0)
    additive_shader_1.nodes["Group Input"].location = (20.0, -180.0)
    additive_shader_1.nodes["Attribute"].location = (-300.0, 0.0)
    additive_shader_1.nodes["Attribute.001"].location = (-300.0, -180.0)
    additive_shader_1.nodes["Vector Math"].location = (20.0, -40.0)
    additive_shader_1.nodes["Mix"].location = (180.0, -40.0)
    additive_shader_1.nodes["Transparent BSDF"].location = (340.0, -40.0)
    additive_shader_1.nodes["Emission"].location = (340.0, -140.0)
    additive_shader_1.nodes["Add Shader"].location = (500.0, -40.0)
    additive_shader_1.nodes["Gamma"].location = (-140.0, -180.0)

    # Set dimensions
    additive_shader_1.nodes["Group Output"].width  = 140.0
    additive_shader_1.nodes["Group Output"].height = 100.0

    additive_shader_1.nodes["Group Input"].width  = 140.0
    additive_shader_1.nodes["Group Input"].height = 100.0

    additive_shader_1.nodes["Attribute"].width  = 140.0
    additive_shader_1.nodes["Attribute"].height = 100.0

    additive_shader_1.nodes["Attribute.001"].width  = 140.0
    additive_shader_1.nodes["Attribute.001"].height = 100.0

    additive_shader_1.nodes["Vector Math"].width  = 140.0
    additive_shader_1.nodes["Vector Math"].height = 100.0

    additive_shader_1.nodes["Mix"].width  = 140.0
    additive_shader_1.nodes["Mix"].height = 100.0

    additive_shader_1.nodes["Transparent BSDF"].width  = 140.0
    additive_shader_1.nodes["Transparent BSDF"].height = 100.0

    additive_shader_1.nodes["Emission"].width  = 140.0
    additive_shader_1.nodes["Emission"].height = 100.0

    additive_shader_1.nodes["Add Shader"].width  = 140.0
    additive_shader_1.nodes["Add Shader"].height = 100.0

    additive_shader_1.nodes["Gamma"].width  = 140.0
    additive_shader_1.nodes["Gamma"].height = 100.0


    # Initialize additive_shader_1 links

    # emission.Emission -> add_shader.Shader
    additive_shader_1.links.new(
        additive_shader_1.nodes["Emission"].outputs[0],
        additive_shader_1.nodes["Add Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> add_shader.Shader
    additive_shader_1.links.new(
        additive_shader_1.nodes["Transparent BSDF"].outputs[0],
        additive_shader_1.nodes["Add Shader"].inputs[0]
    )
    # vector_math.Vector -> mix.A
    additive_shader_1.links.new(
        additive_shader_1.nodes["Vector Math"].outputs[0],
        additive_shader_1.nodes["Mix"].inputs[6]
    )
    # attribute.Factor -> vector_math.Vector
    additive_shader_1.links.new(
        additive_shader_1.nodes["Attribute"].outputs[2],
        additive_shader_1.nodes["Vector Math"].inputs[0]
    )
    # gamma.Color -> vector_math.Vector
    additive_shader_1.links.new(
        additive_shader_1.nodes["Gamma"].outputs[0],
        additive_shader_1.nodes["Vector Math"].inputs[1]
    )
    # mix.Result -> emission.Color
    additive_shader_1.links.new(
        additive_shader_1.nodes["Mix"].outputs[2],
        additive_shader_1.nodes["Emission"].inputs[0]
    )
    # group_input.Color -> mix.B
    additive_shader_1.links.new(
        additive_shader_1.nodes["Group Input"].outputs[0],
        additive_shader_1.nodes["Mix"].inputs[7]
    )
    # add_shader.Shader -> group_output.Shader
    additive_shader_1.links.new(
        additive_shader_1.nodes["Add Shader"].outputs[0],
        additive_shader_1.nodes["Group Output"].inputs[0]
    )
    # attribute_001.Color -> gamma.Color
    additive_shader_1.links.new(
        additive_shader_1.nodes["Attribute.001"].outputs[0],
        additive_shader_1.nodes["Gamma"].inputs[0]
    )

    return additive_shader_1

def trans_alpha_shader_1_node_group():
    """Initialize Trans Alpha Shader node group"""
    trans_alpha_shader_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Trans Alpha Shader")

    trans_alpha_shader_1.color_tag = 'NONE'
    trans_alpha_shader_1.description = ""
    trans_alpha_shader_1.default_group_node_width = 140
    # trans_alpha_shader_1 interface

    # Socket Shader
    shader_socket = trans_alpha_shader_1.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket Color
    color_socket = trans_alpha_shader_1.interface.new_socket(name="Color", in_out='INPUT', socket_type='NodeSocketColor')
    color_socket.default_value = (0.5, 0.5, 0.5, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = "Value of the second color input"
    color_socket.default_input = 'VALUE'
    color_socket.structure_type = 'AUTO'

    # Socket Alpha
    alpha_socket = trans_alpha_shader_1.interface.new_socket(name="Alpha", in_out='INPUT', socket_type='NodeSocketFloat')
    alpha_socket.default_value = 0.5
    alpha_socket.min_value = -10000.0
    alpha_socket.max_value = 10000.0
    alpha_socket.subtype = 'NONE'
    alpha_socket.attribute_domain = 'POINT'
    alpha_socket.default_input = 'VALUE'
    alpha_socket.structure_type = 'AUTO'

    # Initialize trans_alpha_shader_1 nodes

    # Node Group Output
    group_output = trans_alpha_shader_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = trans_alpha_shader_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Emission
    emission = trans_alpha_shader_1.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Attribute
    attribute = trans_alpha_shader_1.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "r_blend"
    attribute.attribute_type = 'OBJECT'

    # Node Math.001
    math_001 = trans_alpha_shader_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False

    # Node Mix
    mix = trans_alpha_shader_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = False
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Attribute.001
    attribute_001 = trans_alpha_shader_1.nodes.new("ShaderNodeAttribute")
    attribute_001.name = "Attribute.001"
    attribute_001.attribute_name = "rendercolor"
    attribute_001.attribute_type = 'OBJECT'

    # Node Mix Shader
    mix_shader = trans_alpha_shader_1.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Transparent BSDF
    transparent_bsdf = trans_alpha_shader_1.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Gamma
    gamma = trans_alpha_shader_1.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Set locations
    trans_alpha_shader_1.nodes["Group Output"].location = (300.0, 100.0)
    trans_alpha_shader_1.nodes["Group Input"].location = (-600.0, 0.0)
    trans_alpha_shader_1.nodes["Emission"].location = (-60.0, 200.0)
    trans_alpha_shader_1.nodes["Attribute"].location = (-600.0, -120.0)
    trans_alpha_shader_1.nodes["Math.001"].location = (-240.0, 0.0)
    trans_alpha_shader_1.nodes["Mix"].location = (-240.0, 240.0)
    trans_alpha_shader_1.nodes["Attribute.001"].location = (-600.0, 200.0)
    trans_alpha_shader_1.nodes["Mix Shader"].location = (120.0, 100.0)
    trans_alpha_shader_1.nodes["Transparent BSDF"].location = (-60.0, -60.0)
    trans_alpha_shader_1.nodes["Gamma"].location = (-420.0, 200.0)

    # Set dimensions
    trans_alpha_shader_1.nodes["Group Output"].width  = 140.0
    trans_alpha_shader_1.nodes["Group Output"].height = 100.0

    trans_alpha_shader_1.nodes["Group Input"].width  = 140.0
    trans_alpha_shader_1.nodes["Group Input"].height = 100.0

    trans_alpha_shader_1.nodes["Emission"].width  = 140.0
    trans_alpha_shader_1.nodes["Emission"].height = 100.0

    trans_alpha_shader_1.nodes["Attribute"].width  = 140.0
    trans_alpha_shader_1.nodes["Attribute"].height = 100.0

    trans_alpha_shader_1.nodes["Math.001"].width  = 140.0
    trans_alpha_shader_1.nodes["Math.001"].height = 100.0

    trans_alpha_shader_1.nodes["Mix"].width  = 140.0
    trans_alpha_shader_1.nodes["Mix"].height = 100.0

    trans_alpha_shader_1.nodes["Attribute.001"].width  = 140.0
    trans_alpha_shader_1.nodes["Attribute.001"].height = 100.0

    trans_alpha_shader_1.nodes["Mix Shader"].width  = 140.0
    trans_alpha_shader_1.nodes["Mix Shader"].height = 100.0

    trans_alpha_shader_1.nodes["Transparent BSDF"].width  = 140.0
    trans_alpha_shader_1.nodes["Transparent BSDF"].height = 100.0

    trans_alpha_shader_1.nodes["Gamma"].width  = 140.0
    trans_alpha_shader_1.nodes["Gamma"].height = 100.0


    # Initialize trans_alpha_shader_1 links

    # gamma.Color -> mix.A
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Gamma"].outputs[0],
        trans_alpha_shader_1.nodes["Mix"].inputs[6]
    )
    # math_001.Value -> mix_shader.Factor
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Math.001"].outputs[0],
        trans_alpha_shader_1.nodes["Mix Shader"].inputs[0]
    )
    # mix.Result -> emission.Color
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Mix"].outputs[2],
        trans_alpha_shader_1.nodes["Emission"].inputs[0]
    )
    # attribute_001.Color -> gamma.Color
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Attribute.001"].outputs[0],
        trans_alpha_shader_1.nodes["Gamma"].inputs[0]
    )
    # attribute.Factor -> math_001.Value
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Attribute"].outputs[2],
        trans_alpha_shader_1.nodes["Math.001"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Transparent BSDF"].outputs[0],
        trans_alpha_shader_1.nodes["Mix Shader"].inputs[1]
    )
    # emission.Emission -> mix_shader.Shader
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Emission"].outputs[0],
        trans_alpha_shader_1.nodes["Mix Shader"].inputs[2]
    )
    # group_input.Alpha -> math_001.Value
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Group Input"].outputs[1],
        trans_alpha_shader_1.nodes["Math.001"].inputs[0]
    )
    # group_input.Color -> mix.B
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Group Input"].outputs[0],
        trans_alpha_shader_1.nodes["Mix"].inputs[7]
    )
    # mix_shader.Shader -> group_output.Shader
    trans_alpha_shader_1.links.new(
        trans_alpha_shader_1.nodes["Mix Shader"].outputs[0],
        trans_alpha_shader_1.nodes["Group Output"].inputs[0]
    )

    return trans_alpha_shader_1

def transparent_geometry_1_node_group():
    """Initialize Transparent Geometry node group"""
    transparent_geometry_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Transparent Geometry")

    transparent_geometry_1.color_tag = 'NONE'
    transparent_geometry_1.description = ""
    transparent_geometry_1.default_group_node_width = 140
    transparent_geometry_1.is_modifier = True
    transparent_geometry_1.show_modifier_manage_panel = True

    # transparent_geometry_1 interface

    # Socket Geometry
    geometry_socket = transparent_geometry_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = transparent_geometry_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Initialize transparent_geometry_1 nodes

    # Node Group Input
    group_input = transparent_geometry_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Group Output
    group_output = transparent_geometry_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Object Info
    object_info = transparent_geometry_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'RELATIVE'
    object_info.inputs[1].hide = True
    object_info.outputs[0].hide = True
    object_info.outputs[1].hide = True
    object_info.outputs[2].hide = True
    object_info.outputs[3].hide = True
    if "model_0" in bpy.data.objects:
        object_info.inputs[0].default_value = bpy.data.objects["model_0"]
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Delete Geometry
    delete_geometry = transparent_geometry_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'FACE'
    delete_geometry.mode = 'ONLY_FACE'

    # Node Geometry Proximity
    geometry_proximity = transparent_geometry_1.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'FACES'
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    # Node Compare
    compare = transparent_geometry_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'LESS_THAN'
    # B
    compare.inputs[1].default_value = 0.0010000000474974513

    # Set locations
    transparent_geometry_1.nodes["Group Input"].location = (260.0, 60.0)
    transparent_geometry_1.nodes["Group Output"].location = (580.0, 60.0)
    transparent_geometry_1.nodes["Object Info"].location = (-60.0, -20.0)
    transparent_geometry_1.nodes["Delete Geometry"].location = (420.0, 60.0)
    transparent_geometry_1.nodes["Geometry Proximity"].location = (100.0, -20.0)
    transparent_geometry_1.nodes["Compare"].location = (260.0, -20.0)

    # Set dimensions
    transparent_geometry_1.nodes["Group Input"].width  = 140.0
    transparent_geometry_1.nodes["Group Input"].height = 100.0

    transparent_geometry_1.nodes["Group Output"].width  = 140.0
    transparent_geometry_1.nodes["Group Output"].height = 100.0

    transparent_geometry_1.nodes["Object Info"].width  = 140.0
    transparent_geometry_1.nodes["Object Info"].height = 100.0

    transparent_geometry_1.nodes["Delete Geometry"].width  = 140.0
    transparent_geometry_1.nodes["Delete Geometry"].height = 100.0

    transparent_geometry_1.nodes["Geometry Proximity"].width  = 140.0
    transparent_geometry_1.nodes["Geometry Proximity"].height = 100.0

    transparent_geometry_1.nodes["Compare"].width  = 140.0
    transparent_geometry_1.nodes["Compare"].height = 100.0


    # Initialize transparent_geometry_1 links

    # delete_geometry.Geometry -> group_output.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Delete Geometry"].outputs[0],
        transparent_geometry_1.nodes["Group Output"].inputs[0]
    )
    # geometry_proximity.Distance -> compare.A
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Geometry Proximity"].outputs[1],
        transparent_geometry_1.nodes["Compare"].inputs[0]
    )
    # compare.Result -> delete_geometry.Selection
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Compare"].outputs[0],
        transparent_geometry_1.nodes["Delete Geometry"].inputs[1]
    )
    # object_info.Geometry -> geometry_proximity.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Object Info"].outputs[4],
        transparent_geometry_1.nodes["Geometry Proximity"].inputs[0]
    )
    # group_input.Geometry -> delete_geometry.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Group Input"].outputs[0],
        transparent_geometry_1.nodes["Delete Geometry"].inputs[0]
    )

    return transparent_geometry_1

# R_DrawSegs
def beamsegs_1_node_group():
    """Initialize BeamSegs node group"""
    beamsegs_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="BeamSegs")

    beamsegs_1.color_tag = 'NONE'
    beamsegs_1.description = ""
    beamsegs_1.default_group_node_width = 140
    beamsegs_1.show_modifier_manage_panel = True

    # beamsegs_1 interface

    # Socket Geometry
    geometry_socket = beamsegs_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Material
    material_socket = beamsegs_1.interface.new_socket(name="Material", in_out='INPUT', socket_type='NodeSocketMaterial')
    material_socket.attribute_domain = 'POINT'
    material_socket.default_input = 'VALUE'
    material_socket.structure_type = 'AUTO'

    # Socket source
    source_socket = beamsegs_1.interface.new_socket(name="source", in_out='INPUT', socket_type='NodeSocketVector')
    source_socket.default_value = (0.0, 0.0, 0.0)
    source_socket.min_value = -3.4028234663852886e+38
    source_socket.max_value = 3.4028234663852886e+38
    source_socket.subtype = 'XYZ'
    source_socket.attribute_domain = 'POINT'
    source_socket.default_input = 'VALUE'
    source_socket.structure_type = 'AUTO'

    # Socket delta
    delta_socket = beamsegs_1.interface.new_socket(name="delta", in_out='INPUT', socket_type='NodeSocketVector')
    delta_socket.default_value = (0.0, 0.0, 0.0)
    delta_socket.min_value = -3.4028234663852886e+38
    delta_socket.max_value = 3.4028234663852886e+38
    delta_socket.subtype = 'XYZ'
    delta_socket.attribute_domain = 'POINT'
    delta_socket.default_input = 'VALUE'
    delta_socket.structure_type = 'AUTO'

    # Socket segments
    segments_socket = beamsegs_1.interface.new_socket(name="segments", in_out='INPUT', socket_type='NodeSocketInt')
    segments_socket.default_value = 0
    segments_socket.min_value = -2147483648
    segments_socket.max_value = 2147483647
    segments_socket.subtype = 'NONE'
    segments_socket.attribute_domain = 'POINT'
    segments_socket.default_input = 'VALUE'
    segments_socket.structure_type = 'AUTO'

    # Socket width
    width_socket = beamsegs_1.interface.new_socket(name="width", in_out='INPUT', socket_type='NodeSocketFloat')
    width_socket.default_value = 0.0
    width_socket.min_value = -3.4028234663852886e+38
    width_socket.max_value = 3.4028234663852886e+38
    width_socket.subtype = 'NONE'
    width_socket.attribute_domain = 'POINT'
    width_socket.default_input = 'VALUE'
    width_socket.structure_type = 'AUTO'

    # Socket freq
    freq_socket = beamsegs_1.interface.new_socket(name="freq", in_out='INPUT', socket_type='NodeSocketFloat')
    freq_socket.default_value = 0.0
    freq_socket.min_value = -3.4028234663852886e+38
    freq_socket.max_value = 3.4028234663852886e+38
    freq_socket.subtype = 'NONE'
    freq_socket.attribute_domain = 'POINT'
    freq_socket.default_input = 'VALUE'
    freq_socket.structure_type = 'AUTO'

    # Socket speed
    speed_socket = beamsegs_1.interface.new_socket(name="speed", in_out='INPUT', socket_type='NodeSocketFloat')
    speed_socket.default_value = 0.0
    speed_socket.min_value = -3.4028234663852886e+38
    speed_socket.max_value = 3.4028234663852886e+38
    speed_socket.subtype = 'NONE'
    speed_socket.attribute_domain = 'POINT'
    speed_socket.default_input = 'VALUE'
    speed_socket.structure_type = 'AUTO'

    # Initialize beamsegs_1 nodes

    # Node Grid.001
    grid_001 = beamsegs_1.nodes.new("GeometryNodeMeshGrid")
    grid_001.name = "Grid.001"
    # Size X
    grid_001.inputs[0].default_value = 1.0
    # Size Y
    grid_001.inputs[1].default_value = 1.0
    # Vertices Y
    grid_001.inputs[3].default_value = 2

    # Node Group Input.006
    group_input_006 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[0].hide = True
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[6].hide = True
    group_input_006.outputs[7].hide = True

    # Node Set Position.001
    set_position_001 = beamsegs_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node VectorMA
    vectorma = beamsegs_1.nodes.new("GeometryNodeGroup")
    vectorma.name = "VectorMA"
    vectorma.node_tree = ensure_group("VectorMA")

    # Node Group Input.008
    group_input_008 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_008.name = "Group Input.008"
    group_input_008.outputs[0].hide = True
    group_input_008.outputs[1].hide = True
    group_input_008.outputs[2].hide = True
    group_input_008.outputs[3].hide = True
    group_input_008.outputs[5].hide = True
    group_input_008.outputs[6].hide = True
    group_input_008.outputs[7].hide = True

    # Node Index
    index = beamsegs_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Integer Math
    integer_math = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.operation = 'FLOORED_MODULO'
    # Value_001
    integer_math.inputs[1].default_value = 2

    # Node Switch
    switch = beamsegs_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'FLOAT'
    # False
    switch.inputs[1].default_value = 1.0
    # True
    switch.inputs[2].default_value = -1.0

    # Node Math.013
    math_013 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.operation = 'MULTIPLY'
    math_013.use_clamp = False

    # Node VectorMA.001
    vectorma_001 = beamsegs_1.nodes.new("GeometryNodeGroup")
    vectorma_001.name = "VectorMA.001"
    vectorma_001.node_tree = ensure_group("VectorMA")

    # Node Camera Basis
    camera_basis = beamsegs_1.nodes.new("GeometryNodeGroup")
    camera_basis.name = "Camera Basis"
    camera_basis.node_tree = ensure_group("Camera Basis")
    camera_basis.outputs[1].hide = True

    # Node Vector Math.004
    vector_math_004 = beamsegs_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'SCALE'

    # Node Camera Basis.001
    camera_basis_001 = beamsegs_1.nodes.new("GeometryNodeGroup")
    camera_basis_001.name = "Camera Basis.001"
    camera_basis_001.node_tree = ensure_group("Camera Basis")
    camera_basis_001.outputs[0].hide = True

    # Node Math.014
    math_014 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'MULTIPLY'
    math_014.use_clamp = False
    # Value_001
    math_014.inputs[1].default_value = -1.0

    # Node Separate XYZ.004
    separate_xyz_004 = beamsegs_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_004.name = "Separate XYZ.004"

    # Node Vector Math.007
    vector_math_007 = beamsegs_1.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'NORMALIZE'

    # Node Combine XYZ.003
    combine_xyz_003 = beamsegs_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.name = "Combine XYZ.003"
    # Z
    combine_xyz_003.inputs[2].default_value = 0.0

    # Node Separate XYZ.005
    separate_xyz_005 = beamsegs_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_005.name = "Separate XYZ.005"

    # Node Vector Math.014
    vector_math_014 = beamsegs_1.nodes.new("ShaderNodeVectorMath")
    vector_math_014.name = "Vector Math.014"
    vector_math_014.operation = 'SUBTRACT'

    # Node ScreenTransform
    screentransform = beamsegs_1.nodes.new("GeometryNodeGroup")
    screentransform.name = "ScreenTransform"
    screentransform.node_tree = ensure_group("ScreenTransform")

    # Node ScreenTransform.001
    screentransform_001 = beamsegs_1.nodes.new("GeometryNodeGroup")
    screentransform_001.name = "ScreenTransform.001"
    screentransform_001.node_tree = ensure_group("ScreenTransform")

    # Node VectorMA.002
    vectorma_002 = beamsegs_1.nodes.new("GeometryNodeGroup")
    vectorma_002.name = "VectorMA.002"
    vectorma_002.node_tree = ensure_group("VectorMA")

    # Node Index.001
    index_001 = beamsegs_1.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    # Node Integer Math.001
    integer_math_001 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.operation = 'DIVIDE'
    # Value_001
    integer_math_001.inputs[1].default_value = 2

    # Node Integer Math.002
    integer_math_002 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.operation = 'SUBTRACT'
    # Value_001
    integer_math_002.inputs[1].default_value = 1

    # Node Group Input.010
    group_input_010 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_010.name = "Group Input.010"
    group_input_010.outputs[0].hide = True
    group_input_010.outputs[1].hide = True
    group_input_010.outputs[2].hide = True
    group_input_010.outputs[4].hide = True
    group_input_010.outputs[5].hide = True
    group_input_010.outputs[6].hide = True
    group_input_010.outputs[7].hide = True

    # Node Math.015
    math_015 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.operation = 'DIVIDE'
    math_015.use_clamp = False
    # Value
    math_015.inputs[0].default_value = 1.0

    # Node Integer Math.003
    integer_math_003 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.operation = 'SUBTRACT'
    # Value_001
    integer_math_003.inputs[1].default_value = 1

    # Node Math.016
    math_016 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.operation = 'MULTIPLY'
    math_016.use_clamp = False

    # Node Group Output.001
    group_output_001 = beamsegs_1.nodes.new("NodeGroupOutput")
    group_output_001.name = "Group Output.001"
    group_output_001.is_active_output = True

    # Node VectorMA.003
    vectorma_003 = beamsegs_1.nodes.new("GeometryNodeGroup")
    vectorma_003.name = "VectorMA.003"
    vectorma_003.node_tree = ensure_group("VectorMA")

    # Node Group Input.012
    group_input_012 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_012.name = "Group Input.012"
    group_input_012.outputs[0].hide = True
    group_input_012.outputs[3].hide = True
    group_input_012.outputs[4].hide = True
    group_input_012.outputs[5].hide = True
    group_input_012.outputs[6].hide = True
    group_input_012.outputs[7].hide = True

    # Node Math.017
    math_017 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'MULTIPLY'
    math_017.use_clamp = False

    # Node Set Material.001
    set_material_001 = beamsegs_1.nodes.new("GeometryNodeSetMaterial")
    set_material_001.name = "Set Material.001"
    # Selection
    set_material_001.inputs[1].default_value = True

    # Node Store Named Attribute.001
    store_named_attribute_001 = beamsegs_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT2'
    store_named_attribute_001.domain = 'CORNER'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "UVMap"

    # Node Group Input.007
    group_input_007 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[1].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True
    group_input_007.outputs[6].hide = True
    group_input_007.outputs[7].hide = True

    # Node Combine XYZ.004
    combine_xyz_004 = beamsegs_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"
    # Z
    combine_xyz_004.inputs[2].default_value = 0.0

    # Node Integer Math.004
    integer_math_004 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.operation = 'FLOORED_MODULO'
    # Value_001
    integer_math_004.inputs[1].default_value = 2

    # Node Math.018
    math_018 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'FLOORED_MODULO'
    math_018.use_clamp = False
    # Value_001
    math_018.inputs[1].default_value = 1.0

    # Node Math.019
    math_019 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'ADD'
    math_019.use_clamp = False

    # Node Index.003
    index_003 = beamsegs_1.nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"

    # Node Integer Math.005
    integer_math_005 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_005.name = "Integer Math.005"
    integer_math_005.operation = 'DIVIDE'
    # Value_001
    integer_math_005.inputs[1].default_value = 2

    # Node Group Input.009
    group_input_009 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    group_input_009.outputs[0].hide = True
    group_input_009.outputs[1].hide = True
    group_input_009.outputs[2].hide = True
    group_input_009.outputs[4].hide = True
    group_input_009.outputs[5].hide = True
    group_input_009.outputs[6].hide = True
    group_input_009.outputs[7].hide = True

    # Node Integer Math.006
    integer_math_006 = beamsegs_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_006.name = "Integer Math.006"
    integer_math_006.operation = 'SUBTRACT'
    # Value_001
    integer_math_006.inputs[1].default_value = 1

    # Node Math.021
    math_021 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.operation = 'MULTIPLY'
    math_021.use_clamp = False

    # Node Group Input.014
    group_input_014 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_014.name = "Group Input.014"
    group_input_014.outputs[0].hide = True
    group_input_014.outputs[1].hide = True
    group_input_014.outputs[2].hide = True
    group_input_014.outputs[3].hide = True
    group_input_014.outputs[4].hide = True
    group_input_014.outputs[7].hide = True

    # Node Math.022
    math_022 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.operation = 'MULTIPLY'
    math_022.use_clamp = False

    # Node Vertex of Corner.001
    vertex_of_corner_001 = beamsegs_1.nodes.new("GeometryNodeVertexOfCorner")
    vertex_of_corner_001.name = "Vertex of Corner.001"

    # Node Math.026
    math_026 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_026.name = "Math.026"
    math_026.operation = 'FLOORED_MODULO'
    math_026.use_clamp = False
    # Value_001
    math_026.inputs[1].default_value = 1.0

    # Node Math.028
    math_028 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_028.name = "Math.028"
    math_028.operation = 'SUBTRACT'
    math_028.use_clamp = False
    # Value
    math_028.inputs[0].default_value = 1.0

    # Node Math.029
    math_029 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_029.name = "Math.029"
    math_029.operation = 'DIVIDE'
    math_029.use_clamp = False

    # Node Group Input.026
    group_input_026 = beamsegs_1.nodes.new("NodeGroupInput")
    group_input_026.name = "Group Input.026"
    group_input_026.outputs[0].hide = True
    group_input_026.outputs[1].hide = True
    group_input_026.outputs[3].hide = True
    group_input_026.outputs[4].hide = True
    group_input_026.outputs[5].hide = True
    group_input_026.outputs[6].hide = True
    group_input_026.outputs[7].hide = True

    # Node Vector Math.002
    vector_math_002 = beamsegs_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'LENGTH'

    # Node Math.031
    math_031 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_031.name = "Math.031"
    math_031.operation = 'MULTIPLY'
    math_031.use_clamp = False
    # Value_001
    math_031.inputs[1].default_value = 0.009999999776482582

    # Node Math.032
    math_032 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_032.name = "Math.032"
    math_032.operation = 'MAXIMUM'
    math_032.use_clamp = False
    # Value_001
    math_032.inputs[1].default_value = 0.5

    # Node Math.033
    math_033 = beamsegs_1.nodes.new("ShaderNodeMath")
    math_033.name = "Math.033"
    math_033.operation = 'MULTIPLY'
    math_033.use_clamp = False
    # Value_001
    math_033.inputs[1].default_value = 100.0

    # Set locations
    beamsegs_1.nodes["Grid.001"].location = (0.0, 0.0)
    beamsegs_1.nodes["Group Input.006"].location = (-160.0, 0.0)
    beamsegs_1.nodes["Set Position.001"].location = (160.0, 0.0)
    beamsegs_1.nodes["VectorMA"].location = (0.0, -180.0)
    beamsegs_1.nodes["Group Input.008"].location = (-320.0, -160.0)
    beamsegs_1.nodes["Index"].location = (-640.0, -220.0)
    beamsegs_1.nodes["Integer Math"].location = (-480.0, -220.0)
    beamsegs_1.nodes["Switch"].location = (-320.0, -220.0)
    beamsegs_1.nodes["Math.013"].location = (-160.0, -220.0)
    beamsegs_1.nodes["VectorMA.001"].location = (-160.0, -380.0)
    beamsegs_1.nodes["Camera Basis"].location = (-320.0, -680.0)
    beamsegs_1.nodes["Vector Math.004"].location = (-320.0, -380.0)
    beamsegs_1.nodes["Camera Basis.001"].location = (-480.0, -380.0)
    beamsegs_1.nodes["Math.014"].location = (-320.0, -520.0)
    beamsegs_1.nodes["Separate XYZ.004"].location = (-480.0, -440.0)
    beamsegs_1.nodes["Vector Math.007"].location = (-640.0, -380.0)
    beamsegs_1.nodes["Combine XYZ.003"].location = (-800.0, -380.0)
    beamsegs_1.nodes["Separate XYZ.005"].location = (-960.0, -380.0)
    beamsegs_1.nodes["Vector Math.014"].location = (-1120.0, -380.0)
    beamsegs_1.nodes["ScreenTransform"].location = (-1280.0, -380.0)
    beamsegs_1.nodes["ScreenTransform.001"].location = (-1280.0, -460.0)
    beamsegs_1.nodes["VectorMA.002"].location = (-1440.0, -380.0)
    beamsegs_1.nodes["Index.001"].location = (-2080.0, -540.0)
    beamsegs_1.nodes["Integer Math.001"].location = (-1920.0, -540.0)
    beamsegs_1.nodes["Integer Math.002"].location = (-1760.0, -540.0)
    beamsegs_1.nodes["Group Input.010"].location = (-2080.0, -380.0)
    beamsegs_1.nodes["Math.015"].location = (-1760.0, -380.0)
    beamsegs_1.nodes["Integer Math.003"].location = (-1920.0, -380.0)
    beamsegs_1.nodes["Math.016"].location = (-1600.0, -380.0)
    beamsegs_1.nodes["Group Output.001"].location = (640.0, 0.0)
    beamsegs_1.nodes["VectorMA.003"].location = (-1440.0, -540.0)
    beamsegs_1.nodes["Group Input.012"].location = (-1600.0, -540.0)
    beamsegs_1.nodes["Math.017"].location = (-1600.0, -620.0)
    beamsegs_1.nodes["Set Material.001"].location = (480.0, 0.0)
    beamsegs_1.nodes["Store Named Attribute.001"].location = (320.0, 0.0)
    beamsegs_1.nodes["Group Input.007"].location = (320.0, -180.0)
    beamsegs_1.nodes["Combine XYZ.004"].location = (160.0, -640.0)
    beamsegs_1.nodes["Integer Math.004"].location = (0.0, -640.0)
    beamsegs_1.nodes["Math.018"].location = (-480.0, -1080.0)
    beamsegs_1.nodes["Math.019"].location = (-320.0, -780.0)
    beamsegs_1.nodes["Index.003"].location = (-960.0, -700.0)
    beamsegs_1.nodes["Integer Math.005"].location = (-640.0, -780.0)
    beamsegs_1.nodes["Group Input.009"].location = (-960.0, -780.0)
    beamsegs_1.nodes["Integer Math.006"].location = (-800.0, -780.0)
    beamsegs_1.nodes["Math.021"].location = (-480.0, -780.0)
    beamsegs_1.nodes["Group Input.014"].location = (-800.0, -1080.0)
    beamsegs_1.nodes["Math.022"].location = (-640.0, -1080.0)
    beamsegs_1.nodes["Vertex of Corner.001"].location = (-800.0, -700.0)
    beamsegs_1.nodes["Math.026"].location = (-160.0, -780.0)
    beamsegs_1.nodes["Math.028"].location = (0.0, -780.0)
    beamsegs_1.nodes["Math.029"].location = (-640.0, -920.0)
    beamsegs_1.nodes["Group Input.026"].location = (-1440.0, -920.0)
    beamsegs_1.nodes["Vector Math.002"].location = (-1280.0, -920.0)
    beamsegs_1.nodes["Math.031"].location = (-960.0, -920.0)
    beamsegs_1.nodes["Math.032"].location = (-800.0, -920.0)
    beamsegs_1.nodes["Math.033"].location = (-1120.0, -920.0)

    # Set dimensions
    beamsegs_1.nodes["Grid.001"].width  = 140.0
    beamsegs_1.nodes["Grid.001"].height = 100.0

    beamsegs_1.nodes["Group Input.006"].width  = 140.0
    beamsegs_1.nodes["Group Input.006"].height = 100.0

    beamsegs_1.nodes["Set Position.001"].width  = 140.0
    beamsegs_1.nodes["Set Position.001"].height = 100.0

    beamsegs_1.nodes["VectorMA"].width  = 140.0
    beamsegs_1.nodes["VectorMA"].height = 100.0

    beamsegs_1.nodes["Group Input.008"].width  = 140.0
    beamsegs_1.nodes["Group Input.008"].height = 100.0

    beamsegs_1.nodes["Index"].width  = 140.0
    beamsegs_1.nodes["Index"].height = 100.0

    beamsegs_1.nodes["Integer Math"].width  = 140.0
    beamsegs_1.nodes["Integer Math"].height = 100.0

    beamsegs_1.nodes["Switch"].width  = 140.0
    beamsegs_1.nodes["Switch"].height = 100.0

    beamsegs_1.nodes["Math.013"].width  = 140.0
    beamsegs_1.nodes["Math.013"].height = 100.0

    beamsegs_1.nodes["VectorMA.001"].width  = 140.0
    beamsegs_1.nodes["VectorMA.001"].height = 100.0

    beamsegs_1.nodes["Camera Basis"].width  = 140.0
    beamsegs_1.nodes["Camera Basis"].height = 100.0

    beamsegs_1.nodes["Vector Math.004"].width  = 140.0
    beamsegs_1.nodes["Vector Math.004"].height = 100.0

    beamsegs_1.nodes["Camera Basis.001"].width  = 140.0
    beamsegs_1.nodes["Camera Basis.001"].height = 100.0

    beamsegs_1.nodes["Math.014"].width  = 140.0
    beamsegs_1.nodes["Math.014"].height = 100.0

    beamsegs_1.nodes["Separate XYZ.004"].width  = 140.0
    beamsegs_1.nodes["Separate XYZ.004"].height = 100.0

    beamsegs_1.nodes["Vector Math.007"].width  = 140.0
    beamsegs_1.nodes["Vector Math.007"].height = 100.0

    beamsegs_1.nodes["Combine XYZ.003"].width  = 140.0
    beamsegs_1.nodes["Combine XYZ.003"].height = 100.0

    beamsegs_1.nodes["Separate XYZ.005"].width  = 140.0
    beamsegs_1.nodes["Separate XYZ.005"].height = 100.0

    beamsegs_1.nodes["Vector Math.014"].width  = 140.0
    beamsegs_1.nodes["Vector Math.014"].height = 100.0

    beamsegs_1.nodes["ScreenTransform"].width  = 140.0
    beamsegs_1.nodes["ScreenTransform"].height = 100.0

    beamsegs_1.nodes["ScreenTransform.001"].width  = 140.0
    beamsegs_1.nodes["ScreenTransform.001"].height = 100.0

    beamsegs_1.nodes["VectorMA.002"].width  = 140.0
    beamsegs_1.nodes["VectorMA.002"].height = 100.0

    beamsegs_1.nodes["Index.001"].width  = 140.0
    beamsegs_1.nodes["Index.001"].height = 100.0

    beamsegs_1.nodes["Integer Math.001"].width  = 140.0
    beamsegs_1.nodes["Integer Math.001"].height = 100.0

    beamsegs_1.nodes["Integer Math.002"].width  = 140.0
    beamsegs_1.nodes["Integer Math.002"].height = 100.0

    beamsegs_1.nodes["Group Input.010"].width  = 140.0
    beamsegs_1.nodes["Group Input.010"].height = 100.0

    beamsegs_1.nodes["Math.015"].width  = 140.0
    beamsegs_1.nodes["Math.015"].height = 100.0

    beamsegs_1.nodes["Integer Math.003"].width  = 140.0
    beamsegs_1.nodes["Integer Math.003"].height = 100.0

    beamsegs_1.nodes["Math.016"].width  = 140.0
    beamsegs_1.nodes["Math.016"].height = 100.0

    beamsegs_1.nodes["Group Output.001"].width  = 140.0
    beamsegs_1.nodes["Group Output.001"].height = 100.0

    beamsegs_1.nodes["VectorMA.003"].width  = 140.0
    beamsegs_1.nodes["VectorMA.003"].height = 100.0

    beamsegs_1.nodes["Group Input.012"].width  = 140.0
    beamsegs_1.nodes["Group Input.012"].height = 100.0

    beamsegs_1.nodes["Math.017"].width  = 140.0
    beamsegs_1.nodes["Math.017"].height = 100.0

    beamsegs_1.nodes["Set Material.001"].width  = 140.0
    beamsegs_1.nodes["Set Material.001"].height = 100.0

    beamsegs_1.nodes["Store Named Attribute.001"].width  = 140.0
    beamsegs_1.nodes["Store Named Attribute.001"].height = 100.0

    beamsegs_1.nodes["Group Input.007"].width  = 140.0
    beamsegs_1.nodes["Group Input.007"].height = 100.0

    beamsegs_1.nodes["Combine XYZ.004"].width  = 140.0
    beamsegs_1.nodes["Combine XYZ.004"].height = 100.0

    beamsegs_1.nodes["Integer Math.004"].width  = 140.0
    beamsegs_1.nodes["Integer Math.004"].height = 100.0

    beamsegs_1.nodes["Math.018"].width  = 140.0
    beamsegs_1.nodes["Math.018"].height = 100.0

    beamsegs_1.nodes["Math.019"].width  = 140.0
    beamsegs_1.nodes["Math.019"].height = 100.0

    beamsegs_1.nodes["Index.003"].width  = 140.0
    beamsegs_1.nodes["Index.003"].height = 100.0

    beamsegs_1.nodes["Integer Math.005"].width  = 140.0
    beamsegs_1.nodes["Integer Math.005"].height = 100.0

    beamsegs_1.nodes["Group Input.009"].width  = 140.0
    beamsegs_1.nodes["Group Input.009"].height = 100.0

    beamsegs_1.nodes["Integer Math.006"].width  = 140.0
    beamsegs_1.nodes["Integer Math.006"].height = 100.0

    beamsegs_1.nodes["Math.021"].width  = 140.0
    beamsegs_1.nodes["Math.021"].height = 100.0

    beamsegs_1.nodes["Group Input.014"].width  = 140.0
    beamsegs_1.nodes["Group Input.014"].height = 100.0

    beamsegs_1.nodes["Math.022"].width  = 140.0
    beamsegs_1.nodes["Math.022"].height = 100.0

    beamsegs_1.nodes["Vertex of Corner.001"].width  = 140.0
    beamsegs_1.nodes["Vertex of Corner.001"].height = 100.0

    beamsegs_1.nodes["Math.026"].width  = 140.0
    beamsegs_1.nodes["Math.026"].height = 100.0

    beamsegs_1.nodes["Math.028"].width  = 140.0
    beamsegs_1.nodes["Math.028"].height = 100.0

    beamsegs_1.nodes["Math.029"].width  = 140.0
    beamsegs_1.nodes["Math.029"].height = 100.0

    beamsegs_1.nodes["Group Input.026"].width  = 140.0
    beamsegs_1.nodes["Group Input.026"].height = 100.0

    beamsegs_1.nodes["Vector Math.002"].width  = 140.0
    beamsegs_1.nodes["Vector Math.002"].height = 100.0

    beamsegs_1.nodes["Math.031"].width  = 140.0
    beamsegs_1.nodes["Math.031"].height = 100.0

    beamsegs_1.nodes["Math.032"].width  = 140.0
    beamsegs_1.nodes["Math.032"].height = 100.0

    beamsegs_1.nodes["Math.033"].width  = 140.0
    beamsegs_1.nodes["Math.033"].height = 100.0


    # Initialize beamsegs_1 links

    # group_input_006.segments -> grid_001.Vertices X
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.006"].outputs[3],
        beamsegs_1.nodes["Grid.001"].inputs[2]
    )
    # grid_001.Mesh -> set_position_001.Geometry
    beamsegs_1.links.new(
        beamsegs_1.nodes["Grid.001"].outputs[0],
        beamsegs_1.nodes["Set Position.001"].inputs[0]
    )
    # vectorma.Vector -> set_position_001.Position
    beamsegs_1.links.new(
        beamsegs_1.nodes["VectorMA"].outputs[0],
        beamsegs_1.nodes["Set Position.001"].inputs[2]
    )
    # index.Index -> integer_math.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Index"].outputs[0],
        beamsegs_1.nodes["Integer Math"].inputs[0]
    )
    # integer_math.Value -> switch.Switch
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math"].outputs[0],
        beamsegs_1.nodes["Switch"].inputs[0]
    )
    # group_input_008.width -> math_013.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.008"].outputs[4],
        beamsegs_1.nodes["Math.013"].inputs[0]
    )
    # switch.Output -> math_013.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Switch"].outputs[0],
        beamsegs_1.nodes["Math.013"].inputs[1]
    )
    # math_013.Value -> vectorma.Scale
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.013"].outputs[0],
        beamsegs_1.nodes["VectorMA"].inputs[1]
    )
    # vectorma_001.Vector -> vectorma.Direction
    beamsegs_1.links.new(
        beamsegs_1.nodes["VectorMA.001"].outputs[0],
        beamsegs_1.nodes["VectorMA"].inputs[2]
    )
    # vector_math_004.Vector -> vectorma_001.Start
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vector Math.004"].outputs[0],
        beamsegs_1.nodes["VectorMA.001"].inputs[0]
    )
    # camera_basis_001.vup -> vector_math_004.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["Camera Basis.001"].outputs[1],
        beamsegs_1.nodes["Vector Math.004"].inputs[0]
    )
    # math_014.Value -> vectorma_001.Scale
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.014"].outputs[0],
        beamsegs_1.nodes["VectorMA.001"].inputs[1]
    )
    # separate_xyz_004.X -> vector_math_004.Scale
    beamsegs_1.links.new(
        beamsegs_1.nodes["Separate XYZ.004"].outputs[0],
        beamsegs_1.nodes["Vector Math.004"].inputs[3]
    )
    # separate_xyz_004.Y -> math_014.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Separate XYZ.004"].outputs[1],
        beamsegs_1.nodes["Math.014"].inputs[0]
    )
    # vector_math_007.Vector -> separate_xyz_004.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vector Math.007"].outputs[0],
        beamsegs_1.nodes["Separate XYZ.004"].inputs[0]
    )
    # combine_xyz_003.Vector -> vector_math_007.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["Combine XYZ.003"].outputs[0],
        beamsegs_1.nodes["Vector Math.007"].inputs[0]
    )
    # separate_xyz_005.X -> combine_xyz_003.X
    beamsegs_1.links.new(
        beamsegs_1.nodes["Separate XYZ.005"].outputs[0],
        beamsegs_1.nodes["Combine XYZ.003"].inputs[0]
    )
    # separate_xyz_005.Y -> combine_xyz_003.Y
    beamsegs_1.links.new(
        beamsegs_1.nodes["Separate XYZ.005"].outputs[1],
        beamsegs_1.nodes["Combine XYZ.003"].inputs[1]
    )
    # vector_math_014.Vector -> separate_xyz_005.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vector Math.014"].outputs[0],
        beamsegs_1.nodes["Separate XYZ.005"].inputs[0]
    )
    # screentransform.Vector -> vector_math_014.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["ScreenTransform"].outputs[0],
        beamsegs_1.nodes["Vector Math.014"].inputs[0]
    )
    # screentransform_001.Vector -> vector_math_014.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["ScreenTransform.001"].outputs[0],
        beamsegs_1.nodes["Vector Math.014"].inputs[1]
    )
    # index_001.Index -> integer_math_001.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Index.001"].outputs[0],
        beamsegs_1.nodes["Integer Math.001"].inputs[0]
    )
    # integer_math_001.Value -> integer_math_002.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.001"].outputs[0],
        beamsegs_1.nodes["Integer Math.002"].inputs[0]
    )
    # group_input_010.segments -> integer_math_003.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.010"].outputs[3],
        beamsegs_1.nodes["Integer Math.003"].inputs[0]
    )
    # integer_math_003.Value -> math_015.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.003"].outputs[0],
        beamsegs_1.nodes["Math.015"].inputs[1]
    )
    # math_015.Value -> math_016.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.015"].outputs[0],
        beamsegs_1.nodes["Math.016"].inputs[0]
    )
    # group_input_012.source -> vectorma_003.Start
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.012"].outputs[1],
        beamsegs_1.nodes["VectorMA.003"].inputs[0]
    )
    # math_017.Value -> vectorma_003.Scale
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.017"].outputs[0],
        beamsegs_1.nodes["VectorMA.003"].inputs[1]
    )
    # math_015.Value -> math_017.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.015"].outputs[0],
        beamsegs_1.nodes["Math.017"].inputs[0]
    )
    # group_input_012.source -> vectorma_002.Start
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.012"].outputs[1],
        beamsegs_1.nodes["VectorMA.002"].inputs[0]
    )
    # vectorma_002.Vector -> screentransform.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["VectorMA.002"].outputs[0],
        beamsegs_1.nodes["ScreenTransform"].inputs[0]
    )
    # camera_basis.vright -> vectorma_001.Direction
    beamsegs_1.links.new(
        beamsegs_1.nodes["Camera Basis"].outputs[0],
        beamsegs_1.nodes["VectorMA.001"].inputs[2]
    )
    # math_016.Value -> vectorma_002.Scale
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.016"].outputs[0],
        beamsegs_1.nodes["VectorMA.002"].inputs[1]
    )
    # group_input_012.delta -> vectorma_003.Direction
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.012"].outputs[2],
        beamsegs_1.nodes["VectorMA.003"].inputs[2]
    )
    # group_input_012.delta -> vectorma_002.Direction
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.012"].outputs[2],
        beamsegs_1.nodes["VectorMA.002"].inputs[2]
    )
    # vectorma_003.Vector -> screentransform_001.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["VectorMA.003"].outputs[0],
        beamsegs_1.nodes["ScreenTransform.001"].inputs[0]
    )
    # group_input_007.Material -> set_material_001.Material
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.007"].outputs[0],
        beamsegs_1.nodes["Set Material.001"].inputs[2]
    )
    # store_named_attribute_001.Geometry -> set_material_001.Geometry
    beamsegs_1.links.new(
        beamsegs_1.nodes["Store Named Attribute.001"].outputs[0],
        beamsegs_1.nodes["Set Material.001"].inputs[0]
    )
    # set_material_001.Geometry -> group_output_001.Geometry
    beamsegs_1.links.new(
        beamsegs_1.nodes["Set Material.001"].outputs[0],
        beamsegs_1.nodes["Group Output.001"].inputs[0]
    )
    # set_position_001.Geometry -> store_named_attribute_001.Geometry
    beamsegs_1.links.new(
        beamsegs_1.nodes["Set Position.001"].outputs[0],
        beamsegs_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # combine_xyz_004.Vector -> store_named_attribute_001.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Combine XYZ.004"].outputs[0],
        beamsegs_1.nodes["Store Named Attribute.001"].inputs[3]
    )
    # vertex_of_corner_001.Vertex Index -> integer_math_005.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vertex of Corner.001"].outputs[0],
        beamsegs_1.nodes["Integer Math.005"].inputs[0]
    )
    # group_input_009.segments -> integer_math_006.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.009"].outputs[3],
        beamsegs_1.nodes["Integer Math.006"].inputs[0]
    )
    # group_input_014.freq -> math_022.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.014"].outputs[5],
        beamsegs_1.nodes["Math.022"].inputs[0]
    )
    # group_input_014.speed -> math_022.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.014"].outputs[6],
        beamsegs_1.nodes["Math.022"].inputs[1]
    )
    # math_021.Value -> math_019.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.021"].outputs[0],
        beamsegs_1.nodes["Math.019"].inputs[0]
    )
    # index_003.Index -> vertex_of_corner_001.Corner Index
    beamsegs_1.links.new(
        beamsegs_1.nodes["Index.003"].outputs[0],
        beamsegs_1.nodes["Vertex of Corner.001"].inputs[0]
    )
    # integer_math_004.Value -> combine_xyz_004.X
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.004"].outputs[0],
        beamsegs_1.nodes["Combine XYZ.004"].inputs[0]
    )
    # math_022.Value -> math_018.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.022"].outputs[0],
        beamsegs_1.nodes["Math.018"].inputs[0]
    )
    # math_018.Value -> math_019.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.018"].outputs[0],
        beamsegs_1.nodes["Math.019"].inputs[1]
    )
    # vertex_of_corner_001.Vertex Index -> integer_math_004.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vertex of Corner.001"].outputs[0],
        beamsegs_1.nodes["Integer Math.004"].inputs[0]
    )
    # integer_math_001.Value -> math_016.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.001"].outputs[0],
        beamsegs_1.nodes["Math.016"].inputs[1]
    )
    # integer_math_002.Value -> math_017.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.002"].outputs[0],
        beamsegs_1.nodes["Math.017"].inputs[1]
    )
    # vectorma_002.Vector -> vectorma.Start
    beamsegs_1.links.new(
        beamsegs_1.nodes["VectorMA.002"].outputs[0],
        beamsegs_1.nodes["VectorMA"].inputs[0]
    )
    # math_019.Value -> math_026.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.019"].outputs[0],
        beamsegs_1.nodes["Math.026"].inputs[0]
    )
    # math_026.Value -> math_028.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.026"].outputs[0],
        beamsegs_1.nodes["Math.028"].inputs[1]
    )
    # math_029.Value -> math_021.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.029"].outputs[0],
        beamsegs_1.nodes["Math.021"].inputs[1]
    )
    # group_input_026.delta -> vector_math_002.Vector
    beamsegs_1.links.new(
        beamsegs_1.nodes["Group Input.026"].outputs[2],
        beamsegs_1.nodes["Vector Math.002"].inputs[0]
    )
    # math_031.Value -> math_032.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.031"].outputs[0],
        beamsegs_1.nodes["Math.032"].inputs[0]
    )
    # vector_math_002.Value -> math_033.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Vector Math.002"].outputs[1],
        beamsegs_1.nodes["Math.033"].inputs[0]
    )
    # math_033.Value -> math_031.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.033"].outputs[0],
        beamsegs_1.nodes["Math.031"].inputs[0]
    )
    # math_032.Value -> math_029.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.032"].outputs[0],
        beamsegs_1.nodes["Math.029"].inputs[0]
    )
    # integer_math_006.Value -> math_029.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.006"].outputs[0],
        beamsegs_1.nodes["Math.029"].inputs[1]
    )
    # math_028.Value -> combine_xyz_004.Y
    beamsegs_1.links.new(
        beamsegs_1.nodes["Math.028"].outputs[0],
        beamsegs_1.nodes["Combine XYZ.004"].inputs[1]
    )
    # integer_math_005.Value -> math_021.Value
    beamsegs_1.links.new(
        beamsegs_1.nodes["Integer Math.005"].outputs[0],
        beamsegs_1.nodes["Math.021"].inputs[0]
    )

    return beamsegs_1

# R_TextureAnimation
def animated_texture_1_node_group():
    """Initialize Animated Texture node group"""
    animated_texture_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Animated Texture")

    animated_texture_1.color_tag = 'NONE'
    animated_texture_1.description = ""
    animated_texture_1.default_group_node_width = 140
    # animated_texture_1 interface

    # Socket Vector
    vector_socket = animated_texture_1.interface.new_socket(name="Vector", in_out='OUTPUT', socket_type='NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'
    vector_socket.default_input = 'VALUE'
    vector_socket.structure_type = 'AUTO'

    # Socket Main Frames
    main_frames_socket = animated_texture_1.interface.new_socket(name="Main Frames", in_out='INPUT', socket_type='NodeSocketInt')
    main_frames_socket.default_value = 0
    main_frames_socket.min_value = -2147483648
    main_frames_socket.max_value = 2147483647
    main_frames_socket.subtype = 'NONE'
    main_frames_socket.attribute_domain = 'POINT'
    main_frames_socket.default_input = 'VALUE'
    main_frames_socket.structure_type = 'AUTO'

    # Socket Alt Frames
    alt_frames_socket = animated_texture_1.interface.new_socket(name="Alt Frames", in_out='INPUT', socket_type='NodeSocketInt')
    alt_frames_socket.default_value = 0
    alt_frames_socket.min_value = -2147483648
    alt_frames_socket.max_value = 2147483647
    alt_frames_socket.subtype = 'NONE'
    alt_frames_socket.attribute_domain = 'POINT'
    alt_frames_socket.default_input = 'VALUE'
    alt_frames_socket.structure_type = 'AUTO'

    # Initialize animated_texture_1 nodes

    # Node Group Output
    group_output = animated_texture_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Node Group Input
    group_input = animated_texture_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[2].hide = True

    # Node Math
    math = animated_texture_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MODULO'
    math.use_clamp = False

    # Node Separate XYZ.001
    separate_xyz_001 = animated_texture_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    # Node Combine XYZ
    combine_xyz = animated_texture_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Math.002
    math_002 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'FRACT'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'ADD'
    math_003.use_clamp = False

    # Node Math.004
    math_004 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False

    # Node Attribute.002
    attribute_002 = animated_texture_1.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "frame"
    attribute_002.attribute_type = 'OBJECT'

    # Node Math.001
    math_001 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'COMPARE'
    math_001.use_clamp = True
    # Value_001
    math_001.inputs[1].default_value = 0.0
    # Value_002
    math_001.inputs[2].default_value = 0.0

    # Node Math.005
    math_005 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MODULO'
    math_005.use_clamp = False

    # Node Math.006
    math_006 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'ADD'
    math_006.use_clamp = False

    # Node Mix
    mix = animated_texture_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'FLOAT'
    mix.factor_mode = 'UNIFORM'

    # Node Math.007
    math_007 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'ADD'
    math_007.use_clamp = False

    # Node Math.008
    math_008 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = False
    # Value_001
    math_008.inputs[1].default_value = 10.0

    # Node Math.009
    math_009 = animated_texture_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'TRUNC'
    math_009.use_clamp = False

    # Node Texture Coordinate.001
    texture_coordinate_001 = animated_texture_1.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.name = "Texture Coordinate.001"
    texture_coordinate_001.from_instancer = False
    texture_coordinate_001.outputs[0].hide = True
    texture_coordinate_001.outputs[1].hide = True
    texture_coordinate_001.outputs[3].hide = True
    texture_coordinate_001.outputs[4].hide = True
    texture_coordinate_001.outputs[5].hide = True
    texture_coordinate_001.outputs[6].hide = True

    # Node Value
    value = animated_texture_1.nodes.new("ShaderNodeGroup")
    value.name = "Value"
    value.node_tree = ensure_group("Shader Engine State")
    value.show_options = False

    # Set locations
    animated_texture_1.nodes["Group Output"].location = (720.0, -120.0)
    animated_texture_1.nodes["Group Input"].location = (-560.0, 40.0)
    animated_texture_1.nodes["Math"].location = (-400.0, -120.0)
    animated_texture_1.nodes["Separate XYZ.001"].location = (-80.0, -140.0)
    animated_texture_1.nodes["Combine XYZ"].location = (560.0, -120.0)
    animated_texture_1.nodes["Math.002"].location = (80.0, -20.0)
    animated_texture_1.nodes["Math.003"].location = (240.0, 120.0)
    animated_texture_1.nodes["Math.004"].location = (400.0, 60.0)
    animated_texture_1.nodes["Attribute.002"].location = (-400.0, 220.0)
    animated_texture_1.nodes["Math.001"].location = (-240.0, 220.0)
    animated_texture_1.nodes["Math.005"].location = (-400.0, 40.0)
    animated_texture_1.nodes["Math.006"].location = (-240.0, 40.0)
    animated_texture_1.nodes["Mix"].location = (-80.0, 40.0)
    animated_texture_1.nodes["Math.007"].location = (240.0, -40.0)
    animated_texture_1.nodes["Math.008"].location = (-720.0, -120.0)
    animated_texture_1.nodes["Math.009"].location = (-560.0, -120.0)
    animated_texture_1.nodes["Texture Coordinate.001"].location = (-240.0, -160.0)
    animated_texture_1.nodes["Value"].location = (-880.0, -180.0)

    # Set dimensions
    animated_texture_1.nodes["Group Output"].width  = 140.0
    animated_texture_1.nodes["Group Output"].height = 100.0

    animated_texture_1.nodes["Group Input"].width  = 140.0
    animated_texture_1.nodes["Group Input"].height = 100.0

    animated_texture_1.nodes["Math"].width  = 140.0
    animated_texture_1.nodes["Math"].height = 100.0

    animated_texture_1.nodes["Separate XYZ.001"].width  = 140.0
    animated_texture_1.nodes["Separate XYZ.001"].height = 100.0

    animated_texture_1.nodes["Combine XYZ"].width  = 140.0
    animated_texture_1.nodes["Combine XYZ"].height = 100.0

    animated_texture_1.nodes["Math.002"].width  = 140.0
    animated_texture_1.nodes["Math.002"].height = 100.0

    animated_texture_1.nodes["Math.003"].width  = 140.0
    animated_texture_1.nodes["Math.003"].height = 100.0

    animated_texture_1.nodes["Math.004"].width  = 140.0
    animated_texture_1.nodes["Math.004"].height = 100.0

    animated_texture_1.nodes["Attribute.002"].width  = 140.0
    animated_texture_1.nodes["Attribute.002"].height = 100.0

    animated_texture_1.nodes["Math.001"].width  = 140.0
    animated_texture_1.nodes["Math.001"].height = 100.0

    animated_texture_1.nodes["Math.005"].width  = 140.0
    animated_texture_1.nodes["Math.005"].height = 100.0

    animated_texture_1.nodes["Math.006"].width  = 140.0
    animated_texture_1.nodes["Math.006"].height = 100.0

    animated_texture_1.nodes["Mix"].width  = 140.0
    animated_texture_1.nodes["Mix"].height = 100.0

    animated_texture_1.nodes["Math.007"].width  = 140.0
    animated_texture_1.nodes["Math.007"].height = 100.0

    animated_texture_1.nodes["Math.008"].width  = 140.0
    animated_texture_1.nodes["Math.008"].height = 100.0

    animated_texture_1.nodes["Math.009"].width  = 140.0
    animated_texture_1.nodes["Math.009"].height = 100.0

    animated_texture_1.nodes["Texture Coordinate.001"].width  = 140.0
    animated_texture_1.nodes["Texture Coordinate.001"].height = 100.0

    animated_texture_1.nodes["Value"].width  = 140.0
    animated_texture_1.nodes["Value"].height = 100.0


    # Initialize animated_texture_1 links

    # mix.Result -> math_003.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Mix"].outputs[0],
        animated_texture_1.nodes["Math.003"].inputs[0]
    )
    # math_001.Value -> mix.Factor
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.001"].outputs[0],
        animated_texture_1.nodes["Mix"].inputs[0]
    )
    # attribute_002.Factor -> math_001.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Attribute.002"].outputs[2],
        animated_texture_1.nodes["Math.001"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.002"].outputs[0],
        animated_texture_1.nodes["Math.003"].inputs[1]
    )
    # separate_xyz_001.Y -> combine_xyz.Y
    animated_texture_1.links.new(
        animated_texture_1.nodes["Separate XYZ.001"].outputs[1],
        animated_texture_1.nodes["Combine XYZ"].inputs[1]
    )
    # math_005.Value -> math_006.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.005"].outputs[0],
        animated_texture_1.nodes["Math.006"].inputs[0]
    )
    # math_004.Value -> combine_xyz.X
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.004"].outputs[0],
        animated_texture_1.nodes["Combine XYZ"].inputs[0]
    )
    # math_003.Value -> math_004.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.003"].outputs[0],
        animated_texture_1.nodes["Math.004"].inputs[0]
    )
    # separate_xyz_001.X -> math_002.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Separate XYZ.001"].outputs[0],
        animated_texture_1.nodes["Math.002"].inputs[0]
    )
    # combine_xyz.Vector -> group_output.Vector
    animated_texture_1.links.new(
        animated_texture_1.nodes["Combine XYZ"].outputs[0],
        animated_texture_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Main Frames -> math.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Group Input"].outputs[0],
        animated_texture_1.nodes["Math"].inputs[1]
    )
    # group_input.Alt Frames -> math_005.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Group Input"].outputs[1],
        animated_texture_1.nodes["Math.005"].inputs[1]
    )
    # group_input.Main Frames -> math_006.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Group Input"].outputs[0],
        animated_texture_1.nodes["Math.006"].inputs[1]
    )
    # group_input.Main Frames -> math_007.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Group Input"].outputs[0],
        animated_texture_1.nodes["Math.007"].inputs[0]
    )
    # group_input.Alt Frames -> math_007.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Group Input"].outputs[1],
        animated_texture_1.nodes["Math.007"].inputs[1]
    )
    # math_007.Value -> math_004.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.007"].outputs[0],
        animated_texture_1.nodes["Math.004"].inputs[1]
    )
    # math_006.Value -> mix.A
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.006"].outputs[0],
        animated_texture_1.nodes["Mix"].inputs[2]
    )
    # math.Value -> mix.B
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math"].outputs[0],
        animated_texture_1.nodes["Mix"].inputs[3]
    )
    # math_008.Value -> math_009.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.008"].outputs[0],
        animated_texture_1.nodes["Math.009"].inputs[0]
    )
    # math_009.Value -> math_005.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.009"].outputs[0],
        animated_texture_1.nodes["Math.005"].inputs[0]
    )
    # math_009.Value -> math.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Math.009"].outputs[0],
        animated_texture_1.nodes["Math"].inputs[0]
    )
    # texture_coordinate_001.UV -> separate_xyz_001.Vector
    animated_texture_1.links.new(
        animated_texture_1.nodes["Texture Coordinate.001"].outputs[2],
        animated_texture_1.nodes["Separate XYZ.001"].inputs[0]
    )
    # value.Time -> math_008.Value
    animated_texture_1.links.new(
        animated_texture_1.nodes["Value"].outputs[0],
        animated_texture_1.nodes["Math.008"].inputs[0]
    )

    return animated_texture_1

def glow_sprite_1_node_group():
    """Initialize Glow Sprite node group"""
    glow_sprite_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Glow Sprite")

    glow_sprite_1.color_tag = 'NONE'
    glow_sprite_1.description = ""
    glow_sprite_1.default_group_node_width = 140
    glow_sprite_1.is_modifier = True
    glow_sprite_1.show_modifier_manage_panel = True

    # glow_sprite_1 interface

    # Socket Geometry
    geometry_socket = glow_sprite_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = glow_sprite_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket Image
    image_socket = glow_sprite_1.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketImage')
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'

    # Socket Frame
    frame_socket = glow_sprite_1.interface.new_socket(name="Frame", in_out='INPUT', socket_type='NodeSocketInt')
    frame_socket.default_value = 0
    frame_socket.min_value = -2147483648
    frame_socket.max_value = 2147483647
    frame_socket.subtype = 'NONE'
    frame_socket.attribute_domain = 'POINT'
    frame_socket.default_input = 'VALUE'
    frame_socket.structure_type = 'AUTO'

    # Initialize glow_sprite_1 nodes

    # Node Group Input
    group_input = glow_sprite_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True

    # Node Group Output
    group_output = glow_sprite_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Node Raycast
    raycast = glow_sprite_1.nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.data_type = 'FLOAT'
    # Attribute
    raycast.inputs[1].default_value = 0.0
    # Interpolation
    raycast.inputs[2].default_value = 'Interpolated'

    # Node Active Camera
    active_camera = glow_sprite_1.nodes.new("GeometryNodeInputActiveCamera")
    active_camera.name = "Active Camera"

    # Node Object Info
    object_info = glow_sprite_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    object_info.inputs[1].hide = True
    object_info.outputs[0].hide = True
    object_info.outputs[2].hide = True
    object_info.outputs[3].hide = True
    object_info.outputs[4].hide = True
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Self Object
    self_object = glow_sprite_1.nodes.new("GeometryNodeSelfObject")
    self_object.name = "Self Object"

    # Node Object Info.001
    object_info_001 = glow_sprite_1.nodes.new("GeometryNodeObjectInfo")
    object_info_001.name = "Object Info.001"
    object_info_001.transform_space = 'ORIGINAL'
    object_info_001.inputs[1].hide = True
    object_info_001.outputs[0].hide = True
    object_info_001.outputs[2].hide = True
    object_info_001.outputs[3].hide = True
    object_info_001.outputs[4].hide = True
    # As Instance
    object_info_001.inputs[1].default_value = False

    # Node Vector Math
    vector_math = glow_sprite_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'SUBTRACT'

    # Node Vector Math.001
    vector_math_001 = glow_sprite_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'NORMALIZE'

    # Node Vector Math.002
    vector_math_002 = glow_sprite_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'LENGTH'

    # Node Store Named Attribute
    store_named_attribute = glow_sprite_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "visible"

    # Node Join Geometry
    join_geometry = glow_sprite_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # Node Object Info.002
    object_info_002 = glow_sprite_1.nodes.new("GeometryNodeObjectInfo")
    object_info_002.name = "Object Info.002"
    object_info_002.transform_space = 'ORIGINAL'
    if "model_0" in bpy.data.objects:
        object_info_002.inputs[0].default_value = bpy.data.objects["model_0"]
    # As Instance
    object_info_002.inputs[1].default_value = False

    # Node Math.002
    math_002 = glow_sprite_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'SUBTRACT'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = glow_sprite_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'LESS_THAN'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 0.07999999821186066

    # Node Join Geometry.001
    join_geometry_001 = glow_sprite_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    # Node Object Info.003
    object_info_003 = glow_sprite_1.nodes.new("GeometryNodeObjectInfo")
    object_info_003.name = "Object Info.003"
    object_info_003.transform_space = 'ORIGINAL'
    if "Point" in bpy.data.objects:
        object_info_003.inputs[0].default_value = bpy.data.objects["Point"]
    # As Instance
    object_info_003.inputs[1].default_value = True

    # Node Store Named Attribute.001
    store_named_attribute_001 = glow_sprite_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT_COLOR'
    store_named_attribute_001.domain = 'INSTANCE'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "light_color"

    # Node Geometry to Instance
    geometry_to_instance = glow_sprite_1.nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"

    # Node Image Texture
    image_texture = glow_sprite_1.nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.extension = 'CLIP'
    image_texture.interpolation = 'Closest'
    image_texture.inputs[2].hide = True
    image_texture.outputs[1].hide = True
    # Frame
    image_texture.inputs[2].default_value = 0

    # Node Combine XYZ
    combine_xyz = glow_sprite_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    combine_xyz.inputs[1].hide = True
    combine_xyz.inputs[2].hide = True
    # Y
    combine_xyz.inputs[1].default_value = 0.0
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Group Input.001
    group_input_001 = glow_sprite_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True

    # Node Bounding Box
    bounding_box = glow_sprite_1.nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True

    # Node Store Named Attribute.002
    store_named_attribute_002 = glow_sprite_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'FLOAT'
    store_named_attribute_002.domain = 'INSTANCE'
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "size"

    # Node Separate XYZ
    separate_xyz = glow_sprite_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"
    separate_xyz.outputs[1].hide = True
    separate_xyz.outputs[2].hide = True

    # Node Image Info
    image_info = glow_sprite_1.nodes.new("GeometryNodeImageInfo")
    image_info.name = "Image Info"
    image_info.inputs[1].hide = True
    image_info.outputs[1].hide = True
    image_info.outputs[2].hide = True
    image_info.outputs[3].hide = True
    image_info.outputs[4].hide = True
    # Frame
    image_info.inputs[1].default_value = 0

    # Node Math
    math = glow_sprite_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'DIVIDE'
    math.use_clamp = False

    # Node Group Input.002
    group_input_002 = glow_sprite_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True

    # Node Group Input.003
    group_input_003 = glow_sprite_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[3].hide = True

    # Set locations
    glow_sprite_1.nodes["Group Input"].location = (-340.0, 140.0)
    glow_sprite_1.nodes["Group Output"].location = (940.0, 140.0)
    glow_sprite_1.nodes["Raycast"].location = (-20.0, 80.0)
    glow_sprite_1.nodes["Active Camera"].location = (-660.0, -140.0)
    glow_sprite_1.nodes["Object Info"].location = (-500.0, -100.0)
    glow_sprite_1.nodes["Self Object"].location = (-660.0, -260.0)
    glow_sprite_1.nodes["Object Info.001"].location = (-500.0, -220.0)
    glow_sprite_1.nodes["Vector Math"].location = (-340.0, -160.0)
    glow_sprite_1.nodes["Vector Math.001"].location = (-180.0, -40.0)
    glow_sprite_1.nodes["Vector Math.002"].location = (-180.0, -180.0)
    glow_sprite_1.nodes["Store Named Attribute"].location = (460.0, 140.0)
    glow_sprite_1.nodes["Join Geometry"].location = (-180.0, 80.0)
    glow_sprite_1.nodes["Object Info.002"].location = (-340.0, 80.0)
    glow_sprite_1.nodes["Math.002"].location = (140.0, 80.0)
    glow_sprite_1.nodes["Math.003"].location = (300.0, 80.0)
    glow_sprite_1.nodes["Join Geometry.001"].location = (300.0, 140.0)
    glow_sprite_1.nodes["Object Info.003"].location = (-20.0, 340.0)
    glow_sprite_1.nodes["Store Named Attribute.001"].location = (620.0, 140.0)
    glow_sprite_1.nodes["Geometry to Instance"].location = (140.0, 200.0)
    glow_sprite_1.nodes["Image Texture"].location = (460.0, -40.0)
    glow_sprite_1.nodes["Combine XYZ"].location = (300.0, -140.0)
    glow_sprite_1.nodes["Group Input.001"].location = (-180.0, -300.0)
    glow_sprite_1.nodes["Bounding Box"].location = (460.0, 300.0)
    glow_sprite_1.nodes["Store Named Attribute.002"].location = (780.0, 140.0)
    glow_sprite_1.nodes["Separate XYZ"].location = (620.0, 240.0)
    glow_sprite_1.nodes["Image Info"].location = (-20.0, -300.0)
    glow_sprite_1.nodes["Math"].location = (140.0, -140.0)
    glow_sprite_1.nodes["Group Input.002"].location = (300.0, -80.0)
    glow_sprite_1.nodes["Group Input.003"].location = (-20.0, -240.0)

    # Set dimensions
    glow_sprite_1.nodes["Group Input"].width  = 140.0
    glow_sprite_1.nodes["Group Input"].height = 100.0

    glow_sprite_1.nodes["Group Output"].width  = 140.0
    glow_sprite_1.nodes["Group Output"].height = 100.0

    glow_sprite_1.nodes["Raycast"].width  = 140.0
    glow_sprite_1.nodes["Raycast"].height = 100.0

    glow_sprite_1.nodes["Active Camera"].width  = 140.0
    glow_sprite_1.nodes["Active Camera"].height = 100.0

    glow_sprite_1.nodes["Object Info"].width  = 140.0
    glow_sprite_1.nodes["Object Info"].height = 100.0

    glow_sprite_1.nodes["Self Object"].width  = 140.0
    glow_sprite_1.nodes["Self Object"].height = 100.0

    glow_sprite_1.nodes["Object Info.001"].width  = 140.0
    glow_sprite_1.nodes["Object Info.001"].height = 100.0

    glow_sprite_1.nodes["Vector Math"].width  = 140.0
    glow_sprite_1.nodes["Vector Math"].height = 100.0

    glow_sprite_1.nodes["Vector Math.001"].width  = 140.0
    glow_sprite_1.nodes["Vector Math.001"].height = 100.0

    glow_sprite_1.nodes["Vector Math.002"].width  = 140.0
    glow_sprite_1.nodes["Vector Math.002"].height = 100.0

    glow_sprite_1.nodes["Store Named Attribute"].width  = 140.0
    glow_sprite_1.nodes["Store Named Attribute"].height = 100.0

    glow_sprite_1.nodes["Join Geometry"].width  = 140.0
    glow_sprite_1.nodes["Join Geometry"].height = 100.0

    glow_sprite_1.nodes["Object Info.002"].width  = 140.0
    glow_sprite_1.nodes["Object Info.002"].height = 100.0

    glow_sprite_1.nodes["Math.002"].width  = 140.0
    glow_sprite_1.nodes["Math.002"].height = 100.0

    glow_sprite_1.nodes["Math.003"].width  = 140.0
    glow_sprite_1.nodes["Math.003"].height = 100.0

    glow_sprite_1.nodes["Join Geometry.001"].width  = 140.0
    glow_sprite_1.nodes["Join Geometry.001"].height = 100.0

    glow_sprite_1.nodes["Object Info.003"].width  = 140.0
    glow_sprite_1.nodes["Object Info.003"].height = 100.0

    glow_sprite_1.nodes["Store Named Attribute.001"].width  = 140.0
    glow_sprite_1.nodes["Store Named Attribute.001"].height = 100.0

    glow_sprite_1.nodes["Geometry to Instance"].width  = 140.0
    glow_sprite_1.nodes["Geometry to Instance"].height = 100.0

    glow_sprite_1.nodes["Image Texture"].width  = 140.0
    glow_sprite_1.nodes["Image Texture"].height = 100.0

    glow_sprite_1.nodes["Combine XYZ"].width  = 140.0
    glow_sprite_1.nodes["Combine XYZ"].height = 100.0

    glow_sprite_1.nodes["Group Input.001"].width  = 140.0
    glow_sprite_1.nodes["Group Input.001"].height = 100.0

    glow_sprite_1.nodes["Bounding Box"].width  = 140.0
    glow_sprite_1.nodes["Bounding Box"].height = 100.0

    glow_sprite_1.nodes["Store Named Attribute.002"].width  = 140.0
    glow_sprite_1.nodes["Store Named Attribute.002"].height = 100.0

    glow_sprite_1.nodes["Separate XYZ"].width  = 140.0
    glow_sprite_1.nodes["Separate XYZ"].height = 100.0

    glow_sprite_1.nodes["Image Info"].width  = 140.0
    glow_sprite_1.nodes["Image Info"].height = 100.0

    glow_sprite_1.nodes["Math"].width  = 140.0
    glow_sprite_1.nodes["Math"].height = 100.0

    glow_sprite_1.nodes["Group Input.002"].width  = 140.0
    glow_sprite_1.nodes["Group Input.002"].height = 100.0

    glow_sprite_1.nodes["Group Input.003"].width  = 140.0
    glow_sprite_1.nodes["Group Input.003"].height = 100.0


    # Initialize glow_sprite_1 links

    # active_camera.Active Camera -> object_info.Object
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Active Camera"].outputs[0],
        glow_sprite_1.nodes["Object Info"].inputs[0]
    )
    # object_info.Location -> raycast.Source Position
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Object Info"].outputs[1],
        glow_sprite_1.nodes["Raycast"].inputs[3]
    )
    # self_object.Self Object -> object_info_001.Object
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Self Object"].outputs[0],
        glow_sprite_1.nodes["Object Info.001"].inputs[0]
    )
    # object_info_001.Location -> vector_math.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Object Info.001"].outputs[1],
        glow_sprite_1.nodes["Vector Math"].inputs[0]
    )
    # object_info.Location -> vector_math.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Object Info"].outputs[1],
        glow_sprite_1.nodes["Vector Math"].inputs[1]
    )
    # vector_math.Vector -> vector_math_001.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Vector Math"].outputs[0],
        glow_sprite_1.nodes["Vector Math.001"].inputs[0]
    )
    # vector_math_001.Vector -> raycast.Ray Direction
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Vector Math.001"].outputs[0],
        glow_sprite_1.nodes["Raycast"].inputs[4]
    )
    # vector_math.Vector -> vector_math_002.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Vector Math"].outputs[0],
        glow_sprite_1.nodes["Vector Math.002"].inputs[0]
    )
    # vector_math_002.Value -> raycast.Ray Length
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Vector Math.002"].outputs[1],
        glow_sprite_1.nodes["Raycast"].inputs[5]
    )
    # object_info_002.Geometry -> join_geometry.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Object Info.002"].outputs[4],
        glow_sprite_1.nodes["Join Geometry"].inputs[0]
    )
    # join_geometry.Geometry -> raycast.Target Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Join Geometry"].outputs[0],
        glow_sprite_1.nodes["Raycast"].inputs[0]
    )
    # vector_math_002.Value -> math_002.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Vector Math.002"].outputs[1],
        glow_sprite_1.nodes["Math.002"].inputs[0]
    )
    # raycast.Hit Distance -> math_002.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Raycast"].outputs[3],
        glow_sprite_1.nodes["Math.002"].inputs[1]
    )
    # math_002.Value -> math_003.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Math.002"].outputs[0],
        glow_sprite_1.nodes["Math.003"].inputs[0]
    )
    # math_003.Value -> store_named_attribute.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Math.003"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute"].inputs[3]
    )
    # group_input.Geometry -> join_geometry_001.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Group Input"].outputs[0],
        glow_sprite_1.nodes["Join Geometry.001"].inputs[0]
    )
    # join_geometry_001.Geometry -> store_named_attribute.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Join Geometry.001"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute"].inputs[0]
    )
    # object_info_003.Geometry -> geometry_to_instance.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Object Info.003"].outputs[4],
        glow_sprite_1.nodes["Geometry to Instance"].inputs[0]
    )
    # combine_xyz.Vector -> image_texture.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Combine XYZ"].outputs[0],
        glow_sprite_1.nodes["Image Texture"].inputs[1]
    )
    # image_texture.Color -> store_named_attribute_001.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Image Texture"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute.001"].inputs[3]
    )
    # store_named_attribute.Geometry -> store_named_attribute_001.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Store Named Attribute"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # bounding_box.Max -> separate_xyz.Vector
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Bounding Box"].outputs[2],
        glow_sprite_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> store_named_attribute_002.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Separate XYZ"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute.002"].inputs[3]
    )
    # join_geometry_001.Geometry -> bounding_box.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Join Geometry.001"].outputs[0],
        glow_sprite_1.nodes["Bounding Box"].inputs[0]
    )
    # store_named_attribute_002.Geometry -> group_output.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Store Named Attribute.002"].outputs[0],
        glow_sprite_1.nodes["Group Output"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> store_named_attribute_002.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Store Named Attribute.001"].outputs[0],
        glow_sprite_1.nodes["Store Named Attribute.002"].inputs[0]
    )
    # group_input_001.Image -> image_info.Image
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Group Input.001"].outputs[1],
        glow_sprite_1.nodes["Image Info"].inputs[0]
    )
    # image_info.Width -> math.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Image Info"].outputs[0],
        glow_sprite_1.nodes["Math"].inputs[1]
    )
    # math.Value -> combine_xyz.X
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Math"].outputs[0],
        glow_sprite_1.nodes["Combine XYZ"].inputs[0]
    )
    # group_input_002.Image -> image_texture.Image
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Group Input.002"].outputs[1],
        glow_sprite_1.nodes["Image Texture"].inputs[0]
    )
    # group_input_003.Frame -> math.Value
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Group Input.003"].outputs[2],
        glow_sprite_1.nodes["Math"].inputs[0]
    )
    # group_input.Geometry -> join_geometry.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Group Input"].outputs[0],
        glow_sprite_1.nodes["Join Geometry"].inputs[0]
    )
    # geometry_to_instance.Instances -> join_geometry_001.Geometry
    glow_sprite_1.links.new(
        glow_sprite_1.nodes["Geometry to Instance"].outputs[0],
        glow_sprite_1.nodes["Join Geometry.001"].inputs[0]
    )

    return glow_sprite_1

# CL_FxBlend
def fxblend_1_node_group():
    """Initialize FxBlend node group"""
    fxblend_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "FxBlend")

    fxblend_1.color_tag = 'NONE'
    fxblend_1.description = ""
    fxblend_1.default_group_node_width = 140
    # fxblend_1 interface

    # Socket Value
    value_socket = fxblend_1.interface.new_socket(name="Value", in_out='OUTPUT', socket_type='NodeSocketFloat')
    value_socket.default_value = 0.0
    value_socket.min_value = -3.4028234663852886e+38
    value_socket.max_value = 3.4028234663852886e+38
    value_socket.subtype = 'NONE'
    value_socket.attribute_domain = 'POINT'
    value_socket.default_input = 'VALUE'
    value_socket.structure_type = 'AUTO'

    # Initialize fxblend_1 nodes

    # Node Object Info.001
    object_info_001 = fxblend_1.nodes.new("ShaderNodeObjectInfo")
    object_info_001.name = "Object Info.001"

    # Node Math.001
    math_001 = fxblend_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 900.0

    # Node Math.002
    math_002 = fxblend_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'FLOOR'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = fxblend_1.nodes.new("ShaderNodeMath")
    math_003.label = "offset"
    math_003.name = "Math.003"
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 363.0

    # Node Attribute.005
    attribute_005 = fxblend_1.nodes.new("ShaderNodeAttribute")
    attribute_005.label = "renderfx"
    attribute_005.name = "Attribute.005"
    attribute_005.attribute_name = "renderfx"
    attribute_005.attribute_type = 'INSTANCER'

    # Node Math.004
    math_004 = fxblend_1.nodes.new("ShaderNodeMath")
    math_004.label = "PulseSlow"
    math_004.name = "Math.004"
    math_004.operation = 'COMPARE'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 1.0
    # Value_002
    math_004.inputs[2].default_value = 0.0

    # Node Attribute.006
    attribute_006 = fxblend_1.nodes.new("ShaderNodeAttribute")
    attribute_006.label = "renderamt"
    attribute_006.name = "Attribute.006"
    attribute_006.attribute_name = "renderamt"
    attribute_006.attribute_type = 'INSTANCER'

    # Node Math.010
    math_010 = fxblend_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'SINE'
    math_010.use_clamp = False

    # Node Math.011
    math_011 = fxblend_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'MULTIPLY'
    math_011.use_clamp = False
    # Value_001
    math_011.inputs[1].default_value = 2.0

    # Node Math.012
    math_012 = fxblend_1.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.operation = 'ADD'
    math_012.use_clamp = False

    # Node Math.013
    math_013 = fxblend_1.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.operation = 'MULTIPLY'
    math_013.use_clamp = False
    # Value_001
    math_013.inputs[1].default_value = 16.0

    # Node Math.014
    math_014 = fxblend_1.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'ADD'
    math_014.use_clamp = False

    # Node Reroute
    reroute = fxblend_1.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    # Node Reroute.001
    reroute_001 = fxblend_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketFloat"
    # Node Reroute.002
    reroute_002 = fxblend_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketFloat"
    # Node Reroute.003
    reroute_003 = fxblend_1.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketFloat"
    # Node Reroute.004
    reroute_004 = fxblend_1.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketFloat"
    # Node Reroute.005
    reroute_005 = fxblend_1.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.socket_idname = "NodeSocketFloat"
    # Node Reroute.006
    reroute_006 = fxblend_1.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.socket_idname = "NodeSocketFloat"
    # Node Reroute.007
    reroute_007 = fxblend_1.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.socket_idname = "NodeSocketFloat"
    # Node Reroute.008
    reroute_008 = fxblend_1.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketFloat"
    # Node Reroute.009
    reroute_009 = fxblend_1.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketFloat"
    # Node Reroute.010
    reroute_010 = fxblend_1.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketFloat"
    # Node Reroute.011
    reroute_011 = fxblend_1.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketFloat"
    # Node Reroute.012
    reroute_012 = fxblend_1.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.socket_idname = "NodeSocketFloat"
    # Node Reroute.013
    reroute_013 = fxblend_1.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.socket_idname = "NodeSocketFloat"
    # Node Reroute.014
    reroute_014 = fxblend_1.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.socket_idname = "NodeSocketFloat"
    # Node Reroute.015
    reroute_015 = fxblend_1.nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.socket_idname = "NodeSocketFloat"
    # Node Reroute.016
    reroute_016 = fxblend_1.nodes.new("NodeReroute")
    reroute_016.name = "Reroute.016"
    reroute_016.socket_idname = "NodeSocketFloat"
    # Node Reroute.017
    reroute_017 = fxblend_1.nodes.new("NodeReroute")
    reroute_017.name = "Reroute.017"
    reroute_017.socket_idname = "NodeSocketFloat"
    # Node Reroute.018
    reroute_018 = fxblend_1.nodes.new("NodeReroute")
    reroute_018.name = "Reroute.018"
    reroute_018.socket_idname = "NodeSocketFloat"
    # Node Reroute.019
    reroute_019 = fxblend_1.nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.socket_idname = "NodeSocketFloat"
    # Node Reroute.020
    reroute_020 = fxblend_1.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.socket_idname = "NodeSocketFloat"
    # Node Math.015
    math_015 = fxblend_1.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.operation = 'SINE'
    math_015.use_clamp = False

    # Node Math.016
    math_016 = fxblend_1.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.operation = 'MULTIPLY'
    math_016.use_clamp = False
    # Value_001
    math_016.inputs[1].default_value = 8.0

    # Node Math.017
    math_017 = fxblend_1.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'ADD'
    math_017.use_clamp = False

    # Node Math.018
    math_018 = fxblend_1.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'MULTIPLY'
    math_018.use_clamp = False
    # Value_001
    math_018.inputs[1].default_value = 16.0

    # Node Math.019
    math_019 = fxblend_1.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'ADD'
    math_019.use_clamp = False

    # Node Math.020
    math_020 = fxblend_1.nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.operation = 'SINE'
    math_020.use_clamp = False

    # Node Math.021
    math_021 = fxblend_1.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.operation = 'MULTIPLY'
    math_021.use_clamp = False
    # Value_001
    math_021.inputs[1].default_value = 2.0

    # Node Math.022
    math_022 = fxblend_1.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.operation = 'ADD'
    math_022.use_clamp = False

    # Node Math.023
    math_023 = fxblend_1.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.operation = 'MULTIPLY'
    math_023.use_clamp = False
    # Value_001
    math_023.inputs[1].default_value = 64.0

    # Node Math.024
    math_024 = fxblend_1.nodes.new("ShaderNodeMath")
    math_024.name = "Math.024"
    math_024.operation = 'ADD'
    math_024.use_clamp = False

    # Node Math.025
    math_025 = fxblend_1.nodes.new("ShaderNodeMath")
    math_025.name = "Math.025"
    math_025.operation = 'SINE'
    math_025.use_clamp = False

    # Node Math.026
    math_026 = fxblend_1.nodes.new("ShaderNodeMath")
    math_026.name = "Math.026"
    math_026.operation = 'MULTIPLY'
    math_026.use_clamp = False
    # Value_001
    math_026.inputs[1].default_value = 8.0

    # Node Math.027
    math_027 = fxblend_1.nodes.new("ShaderNodeMath")
    math_027.name = "Math.027"
    math_027.operation = 'ADD'
    math_027.use_clamp = False

    # Node Math.028
    math_028 = fxblend_1.nodes.new("ShaderNodeMath")
    math_028.name = "Math.028"
    math_028.operation = 'MULTIPLY'
    math_028.use_clamp = False
    # Value_001
    math_028.inputs[1].default_value = 64.0

    # Node Math.029
    math_029 = fxblend_1.nodes.new("ShaderNodeMath")
    math_029.name = "Math.029"
    math_029.operation = 'ADD'
    math_029.use_clamp = False

    # Node Math.030
    math_030 = fxblend_1.nodes.new("ShaderNodeMath")
    math_030.name = "Math.030"
    math_030.operation = 'MULTIPLY'
    math_030.use_clamp = False
    # Value_001
    math_030.inputs[1].default_value = 4.0

    # Node Math.031
    math_031 = fxblend_1.nodes.new("ShaderNodeMath")
    math_031.name = "Math.031"
    math_031.operation = 'ADD'
    math_031.use_clamp = False

    # Node Math.032
    math_032 = fxblend_1.nodes.new("ShaderNodeMath")
    math_032.name = "Math.032"
    math_032.operation = 'SINE'
    math_032.use_clamp = False

    # Node Math.033
    math_033 = fxblend_1.nodes.new("ShaderNodeMath")
    math_033.name = "Math.033"
    math_033.operation = 'MULTIPLY'
    math_033.use_clamp = False
    # Value_001
    math_033.inputs[1].default_value = 20.0

    # Node Mix.001
    mix_001 = fxblend_1.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.data_type = 'FLOAT'
    mix_001.factor_mode = 'UNIFORM'

    # Node Math.034
    math_034 = fxblend_1.nodes.new("ShaderNodeMath")
    math_034.label = "PulseFast"
    math_034.name = "Math.034"
    math_034.operation = 'COMPARE'
    math_034.use_clamp = False
    # Value_001
    math_034.inputs[1].default_value = 2.0
    # Value_002
    math_034.inputs[2].default_value = 0.0

    # Node Math.035
    math_035 = fxblend_1.nodes.new("ShaderNodeMath")
    math_035.label = "PulseSlowWide"
    math_035.name = "Math.035"
    math_035.operation = 'COMPARE'
    math_035.use_clamp = False
    # Value_001
    math_035.inputs[1].default_value = 3.0
    # Value_002
    math_035.inputs[2].default_value = 0.0

    # Node Math.036
    math_036 = fxblend_1.nodes.new("ShaderNodeMath")
    math_036.label = "PulseFastWide"
    math_036.name = "Math.036"
    math_036.operation = 'COMPARE'
    math_036.use_clamp = False
    # Value_001
    math_036.inputs[1].default_value = 4.0
    # Value_002
    math_036.inputs[2].default_value = 0.0

    # Node Mix.002
    mix_002 = fxblend_1.nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.data_type = 'FLOAT'
    mix_002.factor_mode = 'UNIFORM'

    # Node Mix.003
    mix_003 = fxblend_1.nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.data_type = 'FLOAT'
    mix_003.factor_mode = 'UNIFORM'

    # Node Mix.004
    mix_004 = fxblend_1.nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.data_type = 'FLOAT'
    mix_004.factor_mode = 'UNIFORM'

    # Node Group Output
    group_output = fxblend_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Engine State
    engine_state = fxblend_1.nodes.new("ShaderNodeGroup")
    engine_state.name = "Engine State"
    engine_state.node_tree = ensure_group("Shader Engine State")
    engine_state.show_options = False

    # Set locations
    fxblend_1.nodes["Object Info.001"].location = (-1060.0, 320.0)
    fxblend_1.nodes["Math.001"].location = (-900.0, 320.0)
    fxblend_1.nodes["Math.002"].location = (-740.0, 320.0)
    fxblend_1.nodes["Math.003"].location = (-580.0, 320.0)
    fxblend_1.nodes["Attribute.005"].location = (260.0, 500.0)
    fxblend_1.nodes["Math.004"].location = (420.0, 220.0)
    fxblend_1.nodes["Attribute.006"].location = (-580.0, 160.0)
    fxblend_1.nodes["Math.010"].location = (-60.0, 220.0)
    fxblend_1.nodes["Math.011"].location = (-380.0, 220.0)
    fxblend_1.nodes["Math.012"].location = (-220.0, 220.0)
    fxblend_1.nodes["Math.013"].location = (100.0, 220.0)
    fxblend_1.nodes["Math.014"].location = (260.0, 220.0)
    fxblend_1.nodes["Reroute"].location = (-420.0, 300.0)
    fxblend_1.nodes["Reroute.001"].location = (-420.0, 280.0)
    fxblend_1.nodes["Reroute.002"].location = (-420.0, 260.0)
    fxblend_1.nodes["Reroute.003"].location = (-400.0, 300.0)
    fxblend_1.nodes["Reroute.004"].location = (-240.0, 300.0)
    fxblend_1.nodes["Reroute.005"].location = (-80.0, 300.0)
    fxblend_1.nodes["Reroute.006"].location = (80.0, 300.0)
    fxblend_1.nodes["Reroute.007"].location = (-400.0, 280.0)
    fxblend_1.nodes["Reroute.008"].location = (-240.0, 280.0)
    fxblend_1.nodes["Reroute.009"].location = (-80.0, 280.0)
    fxblend_1.nodes["Reroute.010"].location = (80.0, 280.0)
    fxblend_1.nodes["Reroute.011"].location = (-400.0, 260.0)
    fxblend_1.nodes["Reroute.012"].location = (-240.0, 260.0)
    fxblend_1.nodes["Reroute.013"].location = (-80.0, 260.0)
    fxblend_1.nodes["Reroute.014"].location = (80.0, 260.0)
    fxblend_1.nodes["Reroute.015"].location = (240.0, 300.0)
    fxblend_1.nodes["Reroute.016"].location = (400.0, 300.0)
    fxblend_1.nodes["Reroute.017"].location = (240.0, 280.0)
    fxblend_1.nodes["Reroute.018"].location = (400.0, 280.0)
    fxblend_1.nodes["Reroute.019"].location = (240.0, 260.0)
    fxblend_1.nodes["Reroute.020"].location = (560.0, 260.0)
    fxblend_1.nodes["Math.015"].location = (-60.0, 40.0)
    fxblend_1.nodes["Math.016"].location = (-380.0, 40.0)
    fxblend_1.nodes["Math.017"].location = (-220.0, 40.0)
    fxblend_1.nodes["Math.018"].location = (100.0, 40.0)
    fxblend_1.nodes["Math.019"].location = (260.0, 40.0)
    fxblend_1.nodes["Math.020"].location = (-60.0, -140.0)
    fxblend_1.nodes["Math.021"].location = (-380.0, -140.0)
    fxblend_1.nodes["Math.022"].location = (-220.0, -140.0)
    fxblend_1.nodes["Math.023"].location = (100.0, -140.0)
    fxblend_1.nodes["Math.024"].location = (260.0, -140.0)
    fxblend_1.nodes["Math.025"].location = (-60.0, -320.0)
    fxblend_1.nodes["Math.026"].location = (-380.0, -320.0)
    fxblend_1.nodes["Math.027"].location = (-220.0, -320.0)
    fxblend_1.nodes["Math.028"].location = (100.0, -320.0)
    fxblend_1.nodes["Math.029"].location = (260.0, -320.0)
    fxblend_1.nodes["Math.030"].location = (-380.0, -500.0)
    fxblend_1.nodes["Math.031"].location = (-220.0, -500.0)
    fxblend_1.nodes["Math.032"].location = (-60.0, -500.0)
    fxblend_1.nodes["Math.033"].location = (100.0, -500.0)
    fxblend_1.nodes["Mix.001"].location = (580.0, 220.0)
    fxblend_1.nodes["Math.034"].location = (420.0, 40.0)
    fxblend_1.nodes["Math.035"].location = (420.0, -140.0)
    fxblend_1.nodes["Math.036"].location = (420.0, -320.0)
    fxblend_1.nodes["Mix.002"].location = (740.0, 40.0)
    fxblend_1.nodes["Mix.003"].location = (900.0, -140.0)
    fxblend_1.nodes["Mix.004"].location = (1060.0, -320.0)
    fxblend_1.nodes["Group Output"].location = (1220.0, -320.0)
    fxblend_1.nodes["Engine State"].location = (-580.0, 380.0)

    # Set dimensions
    fxblend_1.nodes["Object Info.001"].width  = 140.0
    fxblend_1.nodes["Object Info.001"].height = 100.0

    fxblend_1.nodes["Math.001"].width  = 140.0
    fxblend_1.nodes["Math.001"].height = 100.0

    fxblend_1.nodes["Math.002"].width  = 140.0
    fxblend_1.nodes["Math.002"].height = 100.0

    fxblend_1.nodes["Math.003"].width  = 140.0
    fxblend_1.nodes["Math.003"].height = 100.0

    fxblend_1.nodes["Attribute.005"].width  = 140.0
    fxblend_1.nodes["Attribute.005"].height = 100.0

    fxblend_1.nodes["Math.004"].width  = 140.0
    fxblend_1.nodes["Math.004"].height = 100.0

    fxblend_1.nodes["Attribute.006"].width  = 140.0
    fxblend_1.nodes["Attribute.006"].height = 100.0

    fxblend_1.nodes["Math.010"].width  = 140.0
    fxblend_1.nodes["Math.010"].height = 100.0

    fxblend_1.nodes["Math.011"].width  = 140.0
    fxblend_1.nodes["Math.011"].height = 100.0

    fxblend_1.nodes["Math.012"].width  = 140.0
    fxblend_1.nodes["Math.012"].height = 100.0

    fxblend_1.nodes["Math.013"].width  = 140.0
    fxblend_1.nodes["Math.013"].height = 100.0

    fxblend_1.nodes["Math.014"].width  = 140.0
    fxblend_1.nodes["Math.014"].height = 100.0

    fxblend_1.nodes["Reroute"].width  = 10.0
    fxblend_1.nodes["Reroute"].height = 100.0

    fxblend_1.nodes["Reroute.001"].width  = 10.0
    fxblend_1.nodes["Reroute.001"].height = 100.0

    fxblend_1.nodes["Reroute.002"].width  = 10.0
    fxblend_1.nodes["Reroute.002"].height = 100.0

    fxblend_1.nodes["Reroute.003"].width  = 10.0
    fxblend_1.nodes["Reroute.003"].height = 100.0

    fxblend_1.nodes["Reroute.004"].width  = 10.0
    fxblend_1.nodes["Reroute.004"].height = 100.0

    fxblend_1.nodes["Reroute.005"].width  = 10.0
    fxblend_1.nodes["Reroute.005"].height = 100.0

    fxblend_1.nodes["Reroute.006"].width  = 10.0
    fxblend_1.nodes["Reroute.006"].height = 100.0

    fxblend_1.nodes["Reroute.007"].width  = 10.0
    fxblend_1.nodes["Reroute.007"].height = 100.0

    fxblend_1.nodes["Reroute.008"].width  = 10.0
    fxblend_1.nodes["Reroute.008"].height = 100.0

    fxblend_1.nodes["Reroute.009"].width  = 10.0
    fxblend_1.nodes["Reroute.009"].height = 100.0

    fxblend_1.nodes["Reroute.010"].width  = 10.0
    fxblend_1.nodes["Reroute.010"].height = 100.0

    fxblend_1.nodes["Reroute.011"].width  = 10.0
    fxblend_1.nodes["Reroute.011"].height = 100.0

    fxblend_1.nodes["Reroute.012"].width  = 10.0
    fxblend_1.nodes["Reroute.012"].height = 100.0

    fxblend_1.nodes["Reroute.013"].width  = 10.0
    fxblend_1.nodes["Reroute.013"].height = 100.0

    fxblend_1.nodes["Reroute.014"].width  = 10.0
    fxblend_1.nodes["Reroute.014"].height = 100.0

    fxblend_1.nodes["Reroute.015"].width  = 10.0
    fxblend_1.nodes["Reroute.015"].height = 100.0

    fxblend_1.nodes["Reroute.016"].width  = 10.0
    fxblend_1.nodes["Reroute.016"].height = 100.0

    fxblend_1.nodes["Reroute.017"].width  = 10.0
    fxblend_1.nodes["Reroute.017"].height = 100.0

    fxblend_1.nodes["Reroute.018"].width  = 10.0
    fxblend_1.nodes["Reroute.018"].height = 100.0

    fxblend_1.nodes["Reroute.019"].width  = 10.0
    fxblend_1.nodes["Reroute.019"].height = 100.0

    fxblend_1.nodes["Reroute.020"].width  = 10.0
    fxblend_1.nodes["Reroute.020"].height = 100.0

    fxblend_1.nodes["Math.015"].width  = 140.0
    fxblend_1.nodes["Math.015"].height = 100.0

    fxblend_1.nodes["Math.016"].width  = 140.0
    fxblend_1.nodes["Math.016"].height = 100.0

    fxblend_1.nodes["Math.017"].width  = 140.0
    fxblend_1.nodes["Math.017"].height = 100.0

    fxblend_1.nodes["Math.018"].width  = 140.0
    fxblend_1.nodes["Math.018"].height = 100.0

    fxblend_1.nodes["Math.019"].width  = 140.0
    fxblend_1.nodes["Math.019"].height = 100.0

    fxblend_1.nodes["Math.020"].width  = 140.0
    fxblend_1.nodes["Math.020"].height = 100.0

    fxblend_1.nodes["Math.021"].width  = 140.0
    fxblend_1.nodes["Math.021"].height = 100.0

    fxblend_1.nodes["Math.022"].width  = 140.0
    fxblend_1.nodes["Math.022"].height = 100.0

    fxblend_1.nodes["Math.023"].width  = 140.0
    fxblend_1.nodes["Math.023"].height = 100.0

    fxblend_1.nodes["Math.024"].width  = 140.0
    fxblend_1.nodes["Math.024"].height = 100.0

    fxblend_1.nodes["Math.025"].width  = 140.0
    fxblend_1.nodes["Math.025"].height = 100.0

    fxblend_1.nodes["Math.026"].width  = 140.0
    fxblend_1.nodes["Math.026"].height = 100.0

    fxblend_1.nodes["Math.027"].width  = 140.0
    fxblend_1.nodes["Math.027"].height = 100.0

    fxblend_1.nodes["Math.028"].width  = 140.0
    fxblend_1.nodes["Math.028"].height = 100.0

    fxblend_1.nodes["Math.029"].width  = 140.0
    fxblend_1.nodes["Math.029"].height = 100.0

    fxblend_1.nodes["Math.030"].width  = 140.0
    fxblend_1.nodes["Math.030"].height = 100.0

    fxblend_1.nodes["Math.031"].width  = 140.0
    fxblend_1.nodes["Math.031"].height = 100.0

    fxblend_1.nodes["Math.032"].width  = 140.0
    fxblend_1.nodes["Math.032"].height = 100.0

    fxblend_1.nodes["Math.033"].width  = 140.0
    fxblend_1.nodes["Math.033"].height = 100.0

    fxblend_1.nodes["Mix.001"].width  = 140.0
    fxblend_1.nodes["Mix.001"].height = 100.0

    fxblend_1.nodes["Math.034"].width  = 140.0
    fxblend_1.nodes["Math.034"].height = 100.0

    fxblend_1.nodes["Math.035"].width  = 140.0
    fxblend_1.nodes["Math.035"].height = 100.0

    fxblend_1.nodes["Math.036"].width  = 140.0
    fxblend_1.nodes["Math.036"].height = 100.0

    fxblend_1.nodes["Mix.002"].width  = 140.0
    fxblend_1.nodes["Mix.002"].height = 100.0

    fxblend_1.nodes["Mix.003"].width  = 140.0
    fxblend_1.nodes["Mix.003"].height = 100.0

    fxblend_1.nodes["Mix.004"].width  = 140.0
    fxblend_1.nodes["Mix.004"].height = 100.0

    fxblend_1.nodes["Group Output"].width  = 140.0
    fxblend_1.nodes["Group Output"].height = 100.0

    fxblend_1.nodes["Engine State"].width  = 140.0
    fxblend_1.nodes["Engine State"].height = 100.0


    # Initialize fxblend_1 links

    # object_info_001.Random -> math_001.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Object Info.001"].outputs[5],
        fxblend_1.nodes["Math.001"].inputs[0]
    )
    # math_001.Value -> math_002.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.001"].outputs[0],
        fxblend_1.nodes["Math.002"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.002"].outputs[0],
        fxblend_1.nodes["Math.003"].inputs[0]
    )
    # attribute_005.Factor -> math_004.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Attribute.005"].outputs[2],
        fxblend_1.nodes["Math.004"].inputs[0]
    )
    # math_011.Value -> math_012.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.011"].outputs[0],
        fxblend_1.nodes["Math.012"].inputs[0]
    )
    # math_012.Value -> math_010.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.012"].outputs[0],
        fxblend_1.nodes["Math.010"].inputs[0]
    )
    # math_010.Value -> math_013.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.010"].outputs[0],
        fxblend_1.nodes["Math.013"].inputs[0]
    )
    # math_013.Value -> math_014.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.013"].outputs[0],
        fxblend_1.nodes["Math.014"].inputs[0]
    )
    # math_003.Value -> reroute_001.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Math.003"].outputs[0],
        fxblend_1.nodes["Reroute.001"].inputs[0]
    )
    # attribute_006.Factor -> reroute_002.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Attribute.006"].outputs[2],
        fxblend_1.nodes["Reroute.002"].inputs[0]
    )
    # reroute.Output -> reroute_003.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute"].outputs[0],
        fxblend_1.nodes["Reroute.003"].inputs[0]
    )
    # reroute_003.Output -> reroute_004.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.003"].outputs[0],
        fxblend_1.nodes["Reroute.004"].inputs[0]
    )
    # reroute_004.Output -> reroute_005.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.004"].outputs[0],
        fxblend_1.nodes["Reroute.005"].inputs[0]
    )
    # reroute_005.Output -> reroute_006.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.005"].outputs[0],
        fxblend_1.nodes["Reroute.006"].inputs[0]
    )
    # reroute_001.Output -> reroute_007.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.001"].outputs[0],
        fxblend_1.nodes["Reroute.007"].inputs[0]
    )
    # reroute_007.Output -> reroute_008.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.007"].outputs[0],
        fxblend_1.nodes["Reroute.008"].inputs[0]
    )
    # reroute_008.Output -> reroute_009.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Reroute.009"].inputs[0]
    )
    # reroute_009.Output -> reroute_010.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.009"].outputs[0],
        fxblend_1.nodes["Reroute.010"].inputs[0]
    )
    # reroute_002.Output -> reroute_011.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.002"].outputs[0],
        fxblend_1.nodes["Reroute.011"].inputs[0]
    )
    # reroute_011.Output -> reroute_012.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.011"].outputs[0],
        fxblend_1.nodes["Reroute.012"].inputs[0]
    )
    # reroute_012.Output -> reroute_013.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.012"].outputs[0],
        fxblend_1.nodes["Reroute.013"].inputs[0]
    )
    # reroute_013.Output -> reroute_014.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.013"].outputs[0],
        fxblend_1.nodes["Reroute.014"].inputs[0]
    )
    # reroute_008.Output -> math_012.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Math.012"].inputs[1]
    )
    # reroute_015.Output -> reroute_016.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.015"].outputs[0],
        fxblend_1.nodes["Reroute.016"].inputs[0]
    )
    # reroute_017.Output -> reroute_018.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.017"].outputs[0],
        fxblend_1.nodes["Reroute.018"].inputs[0]
    )
    # reroute_019.Output -> reroute_020.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.019"].outputs[0],
        fxblend_1.nodes["Reroute.020"].inputs[0]
    )
    # reroute_006.Output -> reroute_015.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.006"].outputs[0],
        fxblend_1.nodes["Reroute.015"].inputs[0]
    )
    # reroute_010.Output -> reroute_017.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.010"].outputs[0],
        fxblend_1.nodes["Reroute.017"].inputs[0]
    )
    # reroute_014.Output -> reroute_019.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.014"].outputs[0],
        fxblend_1.nodes["Reroute.019"].inputs[0]
    )
    # reroute_019.Output -> math_014.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.019"].outputs[0],
        fxblend_1.nodes["Math.014"].inputs[1]
    )
    # reroute_003.Output -> math_011.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.003"].outputs[0],
        fxblend_1.nodes["Math.011"].inputs[0]
    )
    # math_016.Value -> math_017.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.016"].outputs[0],
        fxblend_1.nodes["Math.017"].inputs[0]
    )
    # math_017.Value -> math_015.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.017"].outputs[0],
        fxblend_1.nodes["Math.015"].inputs[0]
    )
    # math_015.Value -> math_018.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.015"].outputs[0],
        fxblend_1.nodes["Math.018"].inputs[0]
    )
    # math_018.Value -> math_019.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.018"].outputs[0],
        fxblend_1.nodes["Math.019"].inputs[0]
    )
    # reroute_003.Output -> math_016.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.003"].outputs[0],
        fxblend_1.nodes["Math.016"].inputs[0]
    )
    # reroute_008.Output -> math_017.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Math.017"].inputs[1]
    )
    # reroute_019.Output -> math_019.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.019"].outputs[0],
        fxblend_1.nodes["Math.019"].inputs[1]
    )
    # math_021.Value -> math_022.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.021"].outputs[0],
        fxblend_1.nodes["Math.022"].inputs[0]
    )
    # math_022.Value -> math_020.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.022"].outputs[0],
        fxblend_1.nodes["Math.020"].inputs[0]
    )
    # math_020.Value -> math_023.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.020"].outputs[0],
        fxblend_1.nodes["Math.023"].inputs[0]
    )
    # math_023.Value -> math_024.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.023"].outputs[0],
        fxblend_1.nodes["Math.024"].inputs[0]
    )
    # reroute_003.Output -> math_021.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.003"].outputs[0],
        fxblend_1.nodes["Math.021"].inputs[0]
    )
    # reroute_008.Output -> math_022.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Math.022"].inputs[1]
    )
    # reroute_019.Output -> math_024.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.019"].outputs[0],
        fxblend_1.nodes["Math.024"].inputs[1]
    )
    # math_026.Value -> math_027.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.026"].outputs[0],
        fxblend_1.nodes["Math.027"].inputs[0]
    )
    # math_027.Value -> math_025.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.027"].outputs[0],
        fxblend_1.nodes["Math.025"].inputs[0]
    )
    # math_025.Value -> math_028.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.025"].outputs[0],
        fxblend_1.nodes["Math.028"].inputs[0]
    )
    # math_028.Value -> math_029.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.028"].outputs[0],
        fxblend_1.nodes["Math.029"].inputs[0]
    )
    # reroute_003.Output -> math_026.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.003"].outputs[0],
        fxblend_1.nodes["Math.026"].inputs[0]
    )
    # reroute_008.Output -> math_027.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Math.027"].inputs[1]
    )
    # reroute_019.Output -> math_029.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.019"].outputs[0],
        fxblend_1.nodes["Math.029"].inputs[1]
    )
    # reroute_011.Output -> math_030.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.011"].outputs[0],
        fxblend_1.nodes["Math.030"].inputs[0]
    )
    # math_030.Value -> math_031.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.030"].outputs[0],
        fxblend_1.nodes["Math.031"].inputs[0]
    )
    # reroute_008.Output -> math_031.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.008"].outputs[0],
        fxblend_1.nodes["Math.031"].inputs[1]
    )
    # math_031.Value -> math_032.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.031"].outputs[0],
        fxblend_1.nodes["Math.032"].inputs[0]
    )
    # math_032.Value -> math_033.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Math.032"].outputs[0],
        fxblend_1.nodes["Math.033"].inputs[0]
    )
    # math_004.Value -> mix_001.Factor
    fxblend_1.links.new(
        fxblend_1.nodes["Math.004"].outputs[0],
        fxblend_1.nodes["Mix.001"].inputs[0]
    )
    # reroute_020.Output -> mix_001.A
    fxblend_1.links.new(
        fxblend_1.nodes["Reroute.020"].outputs[0],
        fxblend_1.nodes["Mix.001"].inputs[2]
    )
    # math_014.Value -> mix_001.B
    fxblend_1.links.new(
        fxblend_1.nodes["Math.014"].outputs[0],
        fxblend_1.nodes["Mix.001"].inputs[3]
    )
    # attribute_005.Factor -> math_034.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Attribute.005"].outputs[2],
        fxblend_1.nodes["Math.034"].inputs[0]
    )
    # attribute_005.Factor -> math_035.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Attribute.005"].outputs[2],
        fxblend_1.nodes["Math.035"].inputs[0]
    )
    # attribute_005.Factor -> math_036.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Attribute.005"].outputs[2],
        fxblend_1.nodes["Math.036"].inputs[0]
    )
    # math_034.Value -> mix_002.Factor
    fxblend_1.links.new(
        fxblend_1.nodes["Math.034"].outputs[0],
        fxblend_1.nodes["Mix.002"].inputs[0]
    )
    # mix_001.Result -> mix_002.A
    fxblend_1.links.new(
        fxblend_1.nodes["Mix.001"].outputs[0],
        fxblend_1.nodes["Mix.002"].inputs[2]
    )
    # math_019.Value -> mix_002.B
    fxblend_1.links.new(
        fxblend_1.nodes["Math.019"].outputs[0],
        fxblend_1.nodes["Mix.002"].inputs[3]
    )
    # math_035.Value -> mix_003.Factor
    fxblend_1.links.new(
        fxblend_1.nodes["Math.035"].outputs[0],
        fxblend_1.nodes["Mix.003"].inputs[0]
    )
    # mix_002.Result -> mix_003.A
    fxblend_1.links.new(
        fxblend_1.nodes["Mix.002"].outputs[0],
        fxblend_1.nodes["Mix.003"].inputs[2]
    )
    # math_024.Value -> mix_003.B
    fxblend_1.links.new(
        fxblend_1.nodes["Math.024"].outputs[0],
        fxblend_1.nodes["Mix.003"].inputs[3]
    )
    # mix_003.Result -> mix_004.A
    fxblend_1.links.new(
        fxblend_1.nodes["Mix.003"].outputs[0],
        fxblend_1.nodes["Mix.004"].inputs[2]
    )
    # math_036.Value -> mix_004.Factor
    fxblend_1.links.new(
        fxblend_1.nodes["Math.036"].outputs[0],
        fxblend_1.nodes["Mix.004"].inputs[0]
    )
    # math_029.Value -> mix_004.B
    fxblend_1.links.new(
        fxblend_1.nodes["Math.029"].outputs[0],
        fxblend_1.nodes["Mix.004"].inputs[3]
    )
    # mix_004.Result -> group_output.Value
    fxblend_1.links.new(
        fxblend_1.nodes["Mix.004"].outputs[0],
        fxblend_1.nodes["Group Output"].inputs[0]
    )
    # engine_state.Time -> reroute.Input
    fxblend_1.links.new(
        fxblend_1.nodes["Engine State"].outputs[0],
        fxblend_1.nodes["Reroute"].inputs[0]
    )

    return fxblend_1

# GlowBlend
def glowblend_1_node_group():
    """Initialize GlowBlend node group"""
    glowblend_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "GlowBlend")

    glowblend_1.color_tag = 'NONE'
    glowblend_1.description = ""
    glowblend_1.default_group_node_width = 140
    # glowblend_1 interface

    # Socket Value
    value_socket = glowblend_1.interface.new_socket(name="Value", in_out='OUTPUT', socket_type='NodeSocketFloat')
    value_socket.default_value = 0.0
    value_socket.min_value = -3.4028234663852886e+38
    value_socket.max_value = 3.4028234663852886e+38
    value_socket.subtype = 'NONE'
    value_socket.attribute_domain = 'POINT'
    value_socket.default_input = 'VALUE'
    value_socket.structure_type = 'AUTO'

    # Initialize glowblend_1 nodes

    # Node Attribute.003
    attribute_003 = glowblend_1.nodes.new("ShaderNodeAttribute")
    attribute_003.label = "PM_PlayerTrace"
    attribute_003.name = "Attribute.003"
    attribute_003.attribute_name = "visible"
    attribute_003.attribute_type = 'GEOMETRY'

    # Node Math.001
    math_001 = glowblend_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False

    # Node Attribute.006
    attribute_006 = glowblend_1.nodes.new("ShaderNodeAttribute")
    attribute_006.label = "renderamt"
    attribute_006.name = "Attribute.006"
    attribute_006.attribute_name = "renderamt"
    attribute_006.attribute_type = 'OBJECT'

    # Node Math.004
    math_004 = glowblend_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 255.0

    # Node Group Output
    group_output = glowblend_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Set locations
    glowblend_1.nodes["Attribute.003"].location = (0.0, 80.0)
    glowblend_1.nodes["Math.001"].location = (160.0, 80.0)
    glowblend_1.nodes["Attribute.006"].location = (-160.0, -100.0)
    glowblend_1.nodes["Math.004"].location = (0.0, -100.0)
    glowblend_1.nodes["Group Output"].location = (320.0, 80.0)

    # Set dimensions
    glowblend_1.nodes["Attribute.003"].width  = 140.0
    glowblend_1.nodes["Attribute.003"].height = 100.0

    glowblend_1.nodes["Math.001"].width  = 140.0
    glowblend_1.nodes["Math.001"].height = 100.0

    glowblend_1.nodes["Attribute.006"].width  = 140.0
    glowblend_1.nodes["Attribute.006"].height = 100.0

    glowblend_1.nodes["Math.004"].width  = 140.0
    glowblend_1.nodes["Math.004"].height = 100.0

    glowblend_1.nodes["Group Output"].width  = 140.0
    glowblend_1.nodes["Group Output"].height = 100.0


    # Initialize glowblend_1 links

    # attribute_006.Factor -> math_004.Value
    glowblend_1.links.new(
        glowblend_1.nodes["Attribute.006"].outputs[2],
        glowblend_1.nodes["Math.004"].inputs[0]
    )
    # attribute_003.Factor -> math_001.Value
    glowblend_1.links.new(
        glowblend_1.nodes["Attribute.003"].outputs[2],
        glowblend_1.nodes["Math.001"].inputs[0]
    )
    # math_004.Value -> math_001.Value
    glowblend_1.links.new(
        glowblend_1.nodes["Math.004"].outputs[0],
        glowblend_1.nodes["Math.001"].inputs[1]
    )
    # math_001.Value -> group_output.Value
    glowblend_1.links.new(
        glowblend_1.nodes["Math.001"].outputs[0],
        glowblend_1.nodes["Group Output"].inputs[0]
    )

    return glowblend_1

def _8_value_maximum_1_node_group():
    """Initialize 8-Value Maximum node group"""
    _8_value_maximum_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "8-Value Maximum")

    _8_value_maximum_1.color_tag = 'CONVERTER'
    _8_value_maximum_1.description = ""
    _8_value_maximum_1.default_group_node_width = 140
    # _8_value_maximum_1 interface

    # Socket Value
    value_socket = _8_value_maximum_1.interface.new_socket(name="Value", in_out='OUTPUT', socket_type='NodeSocketFloat')
    value_socket.default_value = 0.0
    value_socket.min_value = -3.4028234663852886e+38
    value_socket.max_value = 3.4028234663852886e+38
    value_socket.subtype = 'NONE'
    value_socket.attribute_domain = 'POINT'
    value_socket.default_input = 'VALUE'
    value_socket.structure_type = 'AUTO'

    # Socket Value
    value_socket_1 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_1.default_value = 0.0
    value_socket_1.min_value = -10000.0
    value_socket_1.max_value = 10000.0
    value_socket_1.subtype = 'NONE'
    value_socket_1.attribute_domain = 'POINT'
    value_socket_1.default_input = 'VALUE'
    value_socket_1.structure_type = 'AUTO'

    # Socket Value
    value_socket_2 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_2.default_value = 0.0
    value_socket_2.min_value = -10000.0
    value_socket_2.max_value = 10000.0
    value_socket_2.subtype = 'NONE'
    value_socket_2.attribute_domain = 'POINT'
    value_socket_2.default_input = 'VALUE'
    value_socket_2.structure_type = 'AUTO'

    # Socket Value
    value_socket_3 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_3.default_value = 0.0
    value_socket_3.min_value = -10000.0
    value_socket_3.max_value = 10000.0
    value_socket_3.subtype = 'NONE'
    value_socket_3.attribute_domain = 'POINT'
    value_socket_3.default_input = 'VALUE'
    value_socket_3.structure_type = 'AUTO'

    # Socket Value
    value_socket_4 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_4.default_value = 0.0
    value_socket_4.min_value = -10000.0
    value_socket_4.max_value = 10000.0
    value_socket_4.subtype = 'NONE'
    value_socket_4.attribute_domain = 'POINT'
    value_socket_4.default_input = 'VALUE'
    value_socket_4.structure_type = 'AUTO'

    # Socket Value
    value_socket_5 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_5.default_value = 0.0
    value_socket_5.min_value = -10000.0
    value_socket_5.max_value = 10000.0
    value_socket_5.subtype = 'NONE'
    value_socket_5.attribute_domain = 'POINT'
    value_socket_5.default_input = 'VALUE'
    value_socket_5.structure_type = 'AUTO'

    # Socket Value
    value_socket_6 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_6.default_value = 0.0
    value_socket_6.min_value = -10000.0
    value_socket_6.max_value = 10000.0
    value_socket_6.subtype = 'NONE'
    value_socket_6.attribute_domain = 'POINT'
    value_socket_6.default_input = 'VALUE'
    value_socket_6.structure_type = 'AUTO'

    # Socket Value
    value_socket_7 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_7.default_value = 0.0
    value_socket_7.min_value = -10000.0
    value_socket_7.max_value = 10000.0
    value_socket_7.subtype = 'NONE'
    value_socket_7.attribute_domain = 'POINT'
    value_socket_7.default_input = 'VALUE'
    value_socket_7.structure_type = 'AUTO'

    # Socket Value
    value_socket_8 = _8_value_maximum_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
    value_socket_8.default_value = 0.0
    value_socket_8.min_value = -10000.0
    value_socket_8.max_value = 10000.0
    value_socket_8.subtype = 'NONE'
    value_socket_8.attribute_domain = 'POINT'
    value_socket_8.default_input = 'VALUE'
    value_socket_8.structure_type = 'AUTO'

    # Initialize _8_value_maximum_1 nodes

    # Node Math.004
    math_004 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'MAXIMUM'
    math_004.use_clamp = False

    # Node Group Output
    group_output = _8_value_maximum_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = _8_value_maximum_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Math
    math = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MAXIMUM'
    math.use_clamp = False

    # Node Math.001
    math_001 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MAXIMUM'
    math_001.use_clamp = False

    # Node Math.005
    math_005 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MAXIMUM'
    math_005.use_clamp = False

    # Node Math.002
    math_002 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MAXIMUM'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MAXIMUM'
    math_003.use_clamp = False

    # Node Math.006
    math_006 = _8_value_maximum_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'MAXIMUM'
    math_006.use_clamp = False

    # Set locations
    _8_value_maximum_1.nodes["Math.004"].location = (0.0, 0.0)
    _8_value_maximum_1.nodes["Group Output"].location = (1120.0, -120.0)
    _8_value_maximum_1.nodes["Group Input"].location = (-160.0, -80.0)
    _8_value_maximum_1.nodes["Math"].location = (160.0, -20.0)
    _8_value_maximum_1.nodes["Math.001"].location = (320.0, -40.0)
    _8_value_maximum_1.nodes["Math.005"].location = (480.0, -60.0)
    _8_value_maximum_1.nodes["Math.002"].location = (640.0, -80.0)
    _8_value_maximum_1.nodes["Math.003"].location = (800.0, -100.0)
    _8_value_maximum_1.nodes["Math.006"].location = (960.0, -120.0)

    # Set dimensions
    _8_value_maximum_1.nodes["Math.004"].width  = 140.0
    _8_value_maximum_1.nodes["Math.004"].height = 100.0

    _8_value_maximum_1.nodes["Group Output"].width  = 140.0
    _8_value_maximum_1.nodes["Group Output"].height = 100.0

    _8_value_maximum_1.nodes["Group Input"].width  = 140.0
    _8_value_maximum_1.nodes["Group Input"].height = 100.0

    _8_value_maximum_1.nodes["Math"].width  = 140.0
    _8_value_maximum_1.nodes["Math"].height = 100.0

    _8_value_maximum_1.nodes["Math.001"].width  = 140.0
    _8_value_maximum_1.nodes["Math.001"].height = 100.0

    _8_value_maximum_1.nodes["Math.005"].width  = 140.0
    _8_value_maximum_1.nodes["Math.005"].height = 100.0

    _8_value_maximum_1.nodes["Math.002"].width  = 140.0
    _8_value_maximum_1.nodes["Math.002"].height = 100.0

    _8_value_maximum_1.nodes["Math.003"].width  = 140.0
    _8_value_maximum_1.nodes["Math.003"].height = 100.0

    _8_value_maximum_1.nodes["Math.006"].width  = 140.0
    _8_value_maximum_1.nodes["Math.006"].height = 100.0


    # Initialize _8_value_maximum_1 links

    # group_input.Value -> math_004.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[0],
        _8_value_maximum_1.nodes["Math.004"].inputs[0]
    )
    # group_input.Value -> math_004.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[1],
        _8_value_maximum_1.nodes["Math.004"].inputs[1]
    )
    # group_input.Value -> math.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[2],
        _8_value_maximum_1.nodes["Math"].inputs[1]
    )
    # math_004.Value -> math.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.004"].outputs[0],
        _8_value_maximum_1.nodes["Math"].inputs[0]
    )
    # math.Value -> math_001.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math"].outputs[0],
        _8_value_maximum_1.nodes["Math.001"].inputs[0]
    )
    # group_input.Value -> math_001.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[3],
        _8_value_maximum_1.nodes["Math.001"].inputs[1]
    )
    # math_005.Value -> math_002.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.005"].outputs[0],
        _8_value_maximum_1.nodes["Math.002"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.002"].outputs[0],
        _8_value_maximum_1.nodes["Math.003"].inputs[0]
    )
    # math_001.Value -> math_005.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.001"].outputs[0],
        _8_value_maximum_1.nodes["Math.005"].inputs[0]
    )
    # group_input.Value -> math_005.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[4],
        _8_value_maximum_1.nodes["Math.005"].inputs[1]
    )
    # group_input.Value -> math_002.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[5],
        _8_value_maximum_1.nodes["Math.002"].inputs[1]
    )
    # group_input.Value -> math_003.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[6],
        _8_value_maximum_1.nodes["Math.003"].inputs[1]
    )
    # math_003.Value -> math_006.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.003"].outputs[0],
        _8_value_maximum_1.nodes["Math.006"].inputs[0]
    )
    # group_input.Value -> math_006.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Group Input"].outputs[7],
        _8_value_maximum_1.nodes["Math.006"].inputs[1]
    )
    # math_006.Value -> group_output.Value
    _8_value_maximum_1.links.new(
        _8_value_maximum_1.nodes["Math.006"].outputs[0],
        _8_value_maximum_1.nodes["Group Output"].inputs[0]
    )

    return _8_value_maximum_1

def viewent_modifier_1_node_group(options):
    """Initialize Viewent Modifier node group"""
    viewent_modifier_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Viewent Modifier")

    viewent_modifier_1.color_tag = 'NONE'
    viewent_modifier_1.description = ""
    viewent_modifier_1.default_group_node_width = 140
    # viewent_modifier_1 interface

    # Socket Shader
    shader_socket = viewent_modifier_1.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket Shader
    shader_socket_1 = viewent_modifier_1.interface.new_socket(name="Shader", in_out='INPUT', socket_type='NodeSocketShader')
    shader_socket_1.attribute_domain = 'POINT'
    shader_socket_1.default_input = 'VALUE'
    shader_socket_1.structure_type = 'AUTO'

    # Initialize viewent_modifier_1 nodes

    # Node Attribute
    attribute = viewent_modifier_1.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "draw_viewent"
    attribute.attribute_type = 'VIEW_LAYER'

    # Node Math.001
    math_001 = viewent_modifier_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MAXIMUM'
    math_001.use_clamp = False

    # Node Transparent BSDF
    transparent_bsdf = viewent_modifier_1.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Mix Shader
    mix_shader = viewent_modifier_1.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Light Path.001
    light_path_001 = viewent_modifier_1.nodes.new("ShaderNodeLightPath")
    light_path_001.name = "Light Path.001"
    light_path_001.outputs[8].hide = True
    light_path_001.outputs[9].hide = True
    light_path_001.outputs[10].hide = True
    light_path_001.outputs[11].hide = True
    light_path_001.outputs[12].hide = True
    light_path_001.outputs[13].hide = True
    light_path_001.outputs[14].hide = True

    # Node Math.004
    math_004 = viewent_modifier_1.nodes.new("ShaderNodeGroup")
    math_004.name = "Math.004"
    math_004.node_tree = ensure_group("8-Value Maximum")

    # Node Group Output
    group_output = viewent_modifier_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = viewent_modifier_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Set locations
    viewent_modifier_1.nodes["Attribute"].location = (-80.0, 340.0)
    viewent_modifier_1.nodes["Math.001"].location = (80.0, 280.0)
    viewent_modifier_1.nodes["Transparent BSDF"].location = (80.0, 120.0)
    viewent_modifier_1.nodes["Mix Shader"].location = (240.0, 120.0)
    viewent_modifier_1.nodes["Light Path.001"].location = (-240.0, 120.0)
    viewent_modifier_1.nodes["Math.004"].location = (-80.0, 160.0)
    viewent_modifier_1.nodes["Group Output"].location = (400.0, 120.0)
    viewent_modifier_1.nodes["Group Input"].location = (80.0, 20.0)

    # Set dimensions
    viewent_modifier_1.nodes["Attribute"].width  = 140.0
    viewent_modifier_1.nodes["Attribute"].height = 100.0

    viewent_modifier_1.nodes["Math.001"].width  = 140.0
    viewent_modifier_1.nodes["Math.001"].height = 100.0

    viewent_modifier_1.nodes["Transparent BSDF"].width  = 140.0
    viewent_modifier_1.nodes["Transparent BSDF"].height = 100.0

    viewent_modifier_1.nodes["Mix Shader"].width  = 140.0
    viewent_modifier_1.nodes["Mix Shader"].height = 100.0

    viewent_modifier_1.nodes["Light Path.001"].width  = 140.0
    viewent_modifier_1.nodes["Light Path.001"].height = 100.0

    viewent_modifier_1.nodes["Math.004"].width  = 140.0
    viewent_modifier_1.nodes["Math.004"].height = 100.0

    viewent_modifier_1.nodes["Group Output"].width  = 140.0
    viewent_modifier_1.nodes["Group Output"].height = 100.0

    viewent_modifier_1.nodes["Group Input"].width  = 140.0
    viewent_modifier_1.nodes["Group Input"].height = 100.0


    # Initialize viewent_modifier_1 links

    # math_001.Value -> mix_shader.Factor
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Math.001"].outputs[0],
        viewent_modifier_1.nodes["Mix Shader"].inputs[0]
    )
    # attribute.Factor -> math_001.Value
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Attribute"].outputs[2],
        viewent_modifier_1.nodes["Math.001"].inputs[0]
    )
    # math_004.Value -> math_001.Value
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Math.004"].outputs[0],
        viewent_modifier_1.nodes["Math.001"].inputs[1]
    )
    # mix_shader.Shader -> group_output.Shader
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Mix Shader"].outputs[0],
        viewent_modifier_1.nodes["Group Output"].inputs[0]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Transparent BSDF"].outputs[0],
        viewent_modifier_1.nodes["Mix Shader"].inputs[1]
    )
    # group_input.Shader -> mix_shader.Shader
    viewent_modifier_1.links.new(
        viewent_modifier_1.nodes["Group Input"].outputs[0],
        viewent_modifier_1.nodes["Mix Shader"].inputs[2]
    )
    if options.viewent_camera_rays:
        # light_path_001.Is Camera Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[0],
            viewent_modifier_1.nodes["Math.004"].inputs[0]
        )
    if options.viewent_shadow_rays:
        # light_path_001.Is Shadow Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[1],
            viewent_modifier_1.nodes["Math.004"].inputs[1]
        )
    if options.viewent_diffuse_rays:
        # light_path_001.Is Diffuse Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[2],
            viewent_modifier_1.nodes["Math.004"].inputs[2]
        )
    if options.viewent_glossy_rays:
        # light_path_001.Is Glossy Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[3],
            viewent_modifier_1.nodes["Math.004"].inputs[3]
        )
    if options.viewent_reflection_rays:
        # light_path_001.Is Reflection Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[5],
            viewent_modifier_1.nodes["Math.004"].inputs[5]
        )
    if options.viewent_singular_rays:
        # light_path_001.Is Singular Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[4],
            viewent_modifier_1.nodes["Math.004"].inputs[4]
        )
    if options.viewent_transmission_rays:
        # light_path_001.Is Transmission Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[6],
            viewent_modifier_1.nodes["Math.004"].inputs[6]
        )
    if options.viewent_volume_scatter_rays:
        # light_path_001.Is Volume Scatter Ray -> math_004.Value
        viewent_modifier_1.links.new(
            viewent_modifier_1.nodes["Light Path.001"].outputs[7],
            viewent_modifier_1.nodes["Math.004"].inputs[7]
        )

    return viewent_modifier_1

def screentransform_1_node_group():
    """Initialize ScreenTransform node group"""
    screentransform_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="ScreenTransform")

    screentransform_1.color_tag = 'VECTOR'
    screentransform_1.description = ""
    screentransform_1.default_group_node_width = 140
    screentransform_1.show_modifier_manage_panel = True

    # screentransform_1 interface

    # Socket Vector
    vector_socket = screentransform_1.interface.new_socket(name="Vector", in_out='OUTPUT', socket_type='NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'
    vector_socket.default_input = 'VALUE'
    vector_socket.structure_type = 'AUTO'

    # Socket Vector
    vector_socket_1 = screentransform_1.interface.new_socket(name="Vector", in_out='INPUT', socket_type='NodeSocketVector')
    vector_socket_1.default_value = (0.0, 0.0, 0.0)
    vector_socket_1.min_value = -10000.0
    vector_socket_1.max_value = 10000.0
    vector_socket_1.subtype = 'NONE'
    vector_socket_1.attribute_domain = 'POINT'
    vector_socket_1.default_input = 'VALUE'
    vector_socket_1.structure_type = 'AUTO'

    # Initialize screentransform_1 nodes

    # Node Camera Info
    camera_info = screentransform_1.nodes.new("GeometryNodeCameraInfo")
    camera_info.name = "Camera Info"
    camera_info.outputs[1].hide = True
    camera_info.outputs[2].hide = True
    camera_info.outputs[3].hide = True
    camera_info.outputs[4].hide = True
    camera_info.outputs[5].hide = True
    camera_info.outputs[6].hide = True
    camera_info.outputs[7].hide = True
    camera_info.outputs[8].hide = True

    # Node Object Info
    object_info = screentransform_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    object_info.inputs[1].hide = True
    object_info.outputs[1].hide = True
    object_info.outputs[2].hide = True
    object_info.outputs[3].hide = True
    object_info.outputs[4].hide = True
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Active Camera
    active_camera = screentransform_1.nodes.new("GeometryNodeInputActiveCamera")
    active_camera.name = "Active Camera"

    # Node Multiply Matrices
    multiply_matrices = screentransform_1.nodes.new("FunctionNodeMatrixMultiply")
    multiply_matrices.name = "Multiply Matrices"

    # Node Invert Matrix
    invert_matrix = screentransform_1.nodes.new("FunctionNodeInvertMatrix")
    invert_matrix.name = "Invert Matrix"

    # Node Group Input.001
    group_input_001 = screentransform_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True

    # Node Separate Matrix.001
    separate_matrix_001 = screentransform_1.nodes.new("FunctionNodeSeparateMatrix")
    separate_matrix_001.name = "Separate Matrix.001"

    # Node Separate XYZ
    separate_xyz = screentransform_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Math.005
    math_005 = screentransform_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False

    # Node Math.006
    math_006 = screentransform_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False

    # Node Math.007
    math_007 = screentransform_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = False

    # Node Math.008
    math_008 = screentransform_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'ADD'
    math_008.use_clamp = False

    # Node Math.009
    math_009 = screentransform_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False

    # Node Math.010
    math_010 = screentransform_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False

    # Node Math.011
    math_011 = screentransform_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'ADD'
    math_011.use_clamp = False

    # Node Math.012
    math_012 = screentransform_1.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.operation = 'ADD'
    math_012.use_clamp = False

    # Node Math.013
    math_013 = screentransform_1.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.operation = 'MULTIPLY'
    math_013.use_clamp = False

    # Node Math.014
    math_014 = screentransform_1.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'ADD'
    math_014.use_clamp = False

    # Node Math.015
    math_015 = screentransform_1.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.operation = 'ADD'
    math_015.use_clamp = False

    # Node Math.016
    math_016 = screentransform_1.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.operation = 'ADD'
    math_016.use_clamp = False

    # Node Math.017
    math_017 = screentransform_1.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'MULTIPLY'
    math_017.use_clamp = False

    # Node Math.018
    math_018 = screentransform_1.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'MULTIPLY'
    math_018.use_clamp = False

    # Node Math.019
    math_019 = screentransform_1.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'ADD'
    math_019.use_clamp = False

    # Node Math.020
    math_020 = screentransform_1.nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.operation = 'ADD'
    math_020.use_clamp = False

    # Node Math.021
    math_021 = screentransform_1.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.operation = 'MULTIPLY'
    math_021.use_clamp = False

    # Node Math.022
    math_022 = screentransform_1.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.operation = 'ADD'
    math_022.use_clamp = False

    # Node Math.023
    math_023 = screentransform_1.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.operation = 'DIVIDE'
    math_023.use_clamp = False
    # Value
    math_023.inputs[0].default_value = 1.0

    # Node Math.024
    math_024 = screentransform_1.nodes.new("ShaderNodeMath")
    math_024.name = "Math.024"
    math_024.operation = 'MULTIPLY'
    math_024.use_clamp = False

    # Node Math.025
    math_025 = screentransform_1.nodes.new("ShaderNodeMath")
    math_025.name = "Math.025"
    math_025.operation = 'MULTIPLY'
    math_025.use_clamp = False

    # Node Combine XYZ.004
    combine_xyz_004 = screentransform_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"
    # Z
    combine_xyz_004.inputs[2].default_value = 0.0

    # Node Group Output.001
    group_output_001 = screentransform_1.nodes.new("NodeGroupOutput")
    group_output_001.name = "Group Output.001"
    group_output_001.is_active_output = True
    group_output_001.inputs[1].hide = True

    # Set locations
    screentransform_1.nodes["Camera Info"].location = (-320.0, -260.0)
    screentransform_1.nodes["Object Info"].location = (-320.0, -340.0)
    screentransform_1.nodes["Active Camera"].location = (-480.0, -260.0)
    screentransform_1.nodes["Multiply Matrices"].location = (0.0, -260.0)
    screentransform_1.nodes["Invert Matrix"].location = (-160.0, -340.0)
    screentransform_1.nodes["Group Input.001"].location = (0.0, -200.0)
    screentransform_1.nodes["Separate Matrix.001"].location = (160.0, -400.0)
    screentransform_1.nodes["Separate XYZ"].location = (160.0, -260.0)
    screentransform_1.nodes["Math.005"].location = (320.0, -260.0)
    screentransform_1.nodes["Math.006"].location = (480.0, -580.0)
    screentransform_1.nodes["Math.007"].location = (480.0, -420.0)
    screentransform_1.nodes["Math.008"].location = (480.0, -260.0)
    screentransform_1.nodes["Math.009"].location = (320.0, -580.0)
    screentransform_1.nodes["Math.010"].location = (320.0, -420.0)
    screentransform_1.nodes["Math.011"].location = (640.0, -260.0)
    screentransform_1.nodes["Math.012"].location = (640.0, -420.0)
    screentransform_1.nodes["Math.013"].location = (480.0, -740.0)
    screentransform_1.nodes["Math.014"].location = (800.0, -420.0)
    screentransform_1.nodes["Math.015"].location = (800.0, -260.0)
    screentransform_1.nodes["Math.016"].location = (960.0, -420.0)
    screentransform_1.nodes["Math.017"].location = (640.0, -580.0)
    screentransform_1.nodes["Math.018"].location = (640.0, -740.0)
    screentransform_1.nodes["Math.019"].location = (800.0, -580.0)
    screentransform_1.nodes["Math.020"].location = (960.0, -580.0)
    screentransform_1.nodes["Math.021"].location = (640.0, -900.0)
    screentransform_1.nodes["Math.022"].location = (1120.0, -580.0)
    screentransform_1.nodes["Math.023"].location = (1280.0, -580.0)
    screentransform_1.nodes["Math.024"].location = (1440.0, -420.0)
    screentransform_1.nodes["Math.025"].location = (1440.0, -260.0)
    screentransform_1.nodes["Combine XYZ.004"].location = (1600.0, -260.0)
    screentransform_1.nodes["Group Output.001"].location = (1760.0, -260.0)

    # Set dimensions
    screentransform_1.nodes["Camera Info"].width  = 140.0
    screentransform_1.nodes["Camera Info"].height = 100.0

    screentransform_1.nodes["Object Info"].width  = 140.0
    screentransform_1.nodes["Object Info"].height = 100.0

    screentransform_1.nodes["Active Camera"].width  = 140.0
    screentransform_1.nodes["Active Camera"].height = 100.0

    screentransform_1.nodes["Multiply Matrices"].width  = 140.0
    screentransform_1.nodes["Multiply Matrices"].height = 100.0

    screentransform_1.nodes["Invert Matrix"].width  = 140.0
    screentransform_1.nodes["Invert Matrix"].height = 100.0

    screentransform_1.nodes["Group Input.001"].width  = 140.0
    screentransform_1.nodes["Group Input.001"].height = 100.0

    screentransform_1.nodes["Separate Matrix.001"].width  = 140.0
    screentransform_1.nodes["Separate Matrix.001"].height = 100.0

    screentransform_1.nodes["Separate XYZ"].width  = 140.0
    screentransform_1.nodes["Separate XYZ"].height = 100.0

    screentransform_1.nodes["Math.005"].width  = 140.0
    screentransform_1.nodes["Math.005"].height = 100.0

    screentransform_1.nodes["Math.006"].width  = 140.0
    screentransform_1.nodes["Math.006"].height = 100.0

    screentransform_1.nodes["Math.007"].width  = 140.0
    screentransform_1.nodes["Math.007"].height = 100.0

    screentransform_1.nodes["Math.008"].width  = 140.0
    screentransform_1.nodes["Math.008"].height = 100.0

    screentransform_1.nodes["Math.009"].width  = 140.0
    screentransform_1.nodes["Math.009"].height = 100.0

    screentransform_1.nodes["Math.010"].width  = 140.0
    screentransform_1.nodes["Math.010"].height = 100.0

    screentransform_1.nodes["Math.011"].width  = 140.0
    screentransform_1.nodes["Math.011"].height = 100.0

    screentransform_1.nodes["Math.012"].width  = 140.0
    screentransform_1.nodes["Math.012"].height = 100.0

    screentransform_1.nodes["Math.013"].width  = 140.0
    screentransform_1.nodes["Math.013"].height = 100.0

    screentransform_1.nodes["Math.014"].width  = 140.0
    screentransform_1.nodes["Math.014"].height = 100.0

    screentransform_1.nodes["Math.015"].width  = 140.0
    screentransform_1.nodes["Math.015"].height = 100.0

    screentransform_1.nodes["Math.016"].width  = 140.0
    screentransform_1.nodes["Math.016"].height = 100.0

    screentransform_1.nodes["Math.017"].width  = 140.0
    screentransform_1.nodes["Math.017"].height = 100.0

    screentransform_1.nodes["Math.018"].width  = 140.0
    screentransform_1.nodes["Math.018"].height = 100.0

    screentransform_1.nodes["Math.019"].width  = 140.0
    screentransform_1.nodes["Math.019"].height = 100.0

    screentransform_1.nodes["Math.020"].width  = 140.0
    screentransform_1.nodes["Math.020"].height = 100.0

    screentransform_1.nodes["Math.021"].width  = 140.0
    screentransform_1.nodes["Math.021"].height = 100.0

    screentransform_1.nodes["Math.022"].width  = 140.0
    screentransform_1.nodes["Math.022"].height = 100.0

    screentransform_1.nodes["Math.023"].width  = 140.0
    screentransform_1.nodes["Math.023"].height = 100.0

    screentransform_1.nodes["Math.024"].width  = 140.0
    screentransform_1.nodes["Math.024"].height = 100.0

    screentransform_1.nodes["Math.025"].width  = 140.0
    screentransform_1.nodes["Math.025"].height = 100.0

    screentransform_1.nodes["Combine XYZ.004"].width  = 140.0
    screentransform_1.nodes["Combine XYZ.004"].height = 100.0

    screentransform_1.nodes["Group Output.001"].width  = 140.0
    screentransform_1.nodes["Group Output.001"].height = 100.0


    # Initialize screentransform_1 links

    # active_camera.Active Camera -> camera_info.Camera
    screentransform_1.links.new(
        screentransform_1.nodes["Active Camera"].outputs[0],
        screentransform_1.nodes["Camera Info"].inputs[0]
    )
    # active_camera.Active Camera -> object_info.Object
    screentransform_1.links.new(
        screentransform_1.nodes["Active Camera"].outputs[0],
        screentransform_1.nodes["Object Info"].inputs[0]
    )
    # object_info.Transform -> invert_matrix.Matrix
    screentransform_1.links.new(
        screentransform_1.nodes["Object Info"].outputs[0],
        screentransform_1.nodes["Invert Matrix"].inputs[0]
    )
    # multiply_matrices.Matrix -> separate_matrix_001.Matrix
    screentransform_1.links.new(
        screentransform_1.nodes["Multiply Matrices"].outputs[0],
        screentransform_1.nodes["Separate Matrix.001"].inputs[0]
    )
    # group_input_001.Vector -> separate_xyz.Vector
    screentransform_1.links.new(
        screentransform_1.nodes["Group Input.001"].outputs[0],
        screentransform_1.nodes["Separate XYZ"].inputs[0]
    )
    # math_005.Value -> math_008.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.005"].outputs[0],
        screentransform_1.nodes["Math.008"].inputs[0]
    )
    # math_010.Value -> math_008.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.010"].outputs[0],
        screentransform_1.nodes["Math.008"].inputs[1]
    )
    # math_008.Value -> math_011.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.008"].outputs[0],
        screentransform_1.nodes["Math.011"].inputs[0]
    )
    # math_009.Value -> math_011.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.009"].outputs[0],
        screentransform_1.nodes["Math.011"].inputs[1]
    )
    # separate_matrix_001.Column 1 Row 2 -> math_007.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[1],
        screentransform_1.nodes["Math.007"].inputs[0]
    )
    # separate_matrix_001.Column 1 Row 1 -> math_005.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[0],
        screentransform_1.nodes["Math.005"].inputs[0]
    )
    # separate_xyz.X -> math_005.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[0],
        screentransform_1.nodes["Math.005"].inputs[1]
    )
    # separate_matrix_001.Column 2 Row 1 -> math_010.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[4],
        screentransform_1.nodes["Math.010"].inputs[0]
    )
    # separate_xyz.Y -> math_010.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[1],
        screentransform_1.nodes["Math.010"].inputs[1]
    )
    # separate_xyz.Z -> math_009.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[2],
        screentransform_1.nodes["Math.009"].inputs[1]
    )
    # separate_xyz.X -> math_007.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[0],
        screentransform_1.nodes["Math.007"].inputs[1]
    )
    # math_007.Value -> math_012.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.007"].outputs[0],
        screentransform_1.nodes["Math.012"].inputs[0]
    )
    # math_006.Value -> math_012.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.006"].outputs[0],
        screentransform_1.nodes["Math.012"].inputs[1]
    )
    # separate_matrix_001.Column 2 Row 2 -> math_006.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[5],
        screentransform_1.nodes["Math.006"].inputs[0]
    )
    # separate_xyz.Y -> math_006.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[1],
        screentransform_1.nodes["Math.006"].inputs[1]
    )
    # math_012.Value -> math_014.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.012"].outputs[0],
        screentransform_1.nodes["Math.014"].inputs[0]
    )
    # math_013.Value -> math_014.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.013"].outputs[0],
        screentransform_1.nodes["Math.014"].inputs[1]
    )
    # separate_matrix_001.Column 3 Row 1 -> math_009.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[8],
        screentransform_1.nodes["Math.009"].inputs[0]
    )
    # math_011.Value -> math_015.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.011"].outputs[0],
        screentransform_1.nodes["Math.015"].inputs[0]
    )
    # separate_matrix_001.Column 4 Row 1 -> math_015.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[12],
        screentransform_1.nodes["Math.015"].inputs[1]
    )
    # separate_matrix_001.Column 3 Row 2 -> math_013.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[9],
        screentransform_1.nodes["Math.013"].inputs[0]
    )
    # separate_xyz.Z -> math_013.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[2],
        screentransform_1.nodes["Math.013"].inputs[1]
    )
    # math_014.Value -> math_016.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.014"].outputs[0],
        screentransform_1.nodes["Math.016"].inputs[0]
    )
    # separate_matrix_001.Column 4 Row 2 -> math_016.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[13],
        screentransform_1.nodes["Math.016"].inputs[1]
    )
    # separate_matrix_001.Column 1 Row 4 -> math_017.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[3],
        screentransform_1.nodes["Math.017"].inputs[0]
    )
    # separate_xyz.X -> math_017.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[0],
        screentransform_1.nodes["Math.017"].inputs[1]
    )
    # math_017.Value -> math_019.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.017"].outputs[0],
        screentransform_1.nodes["Math.019"].inputs[0]
    )
    # math_018.Value -> math_019.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.018"].outputs[0],
        screentransform_1.nodes["Math.019"].inputs[1]
    )
    # math_019.Value -> math_020.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.019"].outputs[0],
        screentransform_1.nodes["Math.020"].inputs[0]
    )
    # math_021.Value -> math_020.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.021"].outputs[0],
        screentransform_1.nodes["Math.020"].inputs[1]
    )
    # separate_matrix_001.Column 2 Row 4 -> math_018.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[7],
        screentransform_1.nodes["Math.018"].inputs[0]
    )
    # separate_xyz.Y -> math_018.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[1],
        screentransform_1.nodes["Math.018"].inputs[1]
    )
    # separate_matrix_001.Column 3 Row 4 -> math_021.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[11],
        screentransform_1.nodes["Math.021"].inputs[0]
    )
    # separate_xyz.Z -> math_021.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate XYZ"].outputs[2],
        screentransform_1.nodes["Math.021"].inputs[1]
    )
    # math_020.Value -> math_022.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.020"].outputs[0],
        screentransform_1.nodes["Math.022"].inputs[0]
    )
    # separate_matrix_001.Column 4 Row 4 -> math_022.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Separate Matrix.001"].outputs[15],
        screentransform_1.nodes["Math.022"].inputs[1]
    )
    # math_022.Value -> math_023.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.022"].outputs[0],
        screentransform_1.nodes["Math.023"].inputs[1]
    )
    # math_015.Value -> math_025.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.015"].outputs[0],
        screentransform_1.nodes["Math.025"].inputs[0]
    )
    # math_023.Value -> math_025.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.023"].outputs[0],
        screentransform_1.nodes["Math.025"].inputs[1]
    )
    # math_016.Value -> math_024.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.016"].outputs[0],
        screentransform_1.nodes["Math.024"].inputs[0]
    )
    # math_023.Value -> math_024.Value
    screentransform_1.links.new(
        screentransform_1.nodes["Math.023"].outputs[0],
        screentransform_1.nodes["Math.024"].inputs[1]
    )
    # math_025.Value -> combine_xyz_004.X
    screentransform_1.links.new(
        screentransform_1.nodes["Math.025"].outputs[0],
        screentransform_1.nodes["Combine XYZ.004"].inputs[0]
    )
    # math_024.Value -> combine_xyz_004.Y
    screentransform_1.links.new(
        screentransform_1.nodes["Math.024"].outputs[0],
        screentransform_1.nodes["Combine XYZ.004"].inputs[1]
    )
    # combine_xyz_004.Vector -> group_output_001.Vector
    screentransform_1.links.new(
        screentransform_1.nodes["Combine XYZ.004"].outputs[0],
        screentransform_1.nodes["Group Output.001"].inputs[0]
    )
    # camera_info.Projection Matrix -> multiply_matrices.Matrix
    screentransform_1.links.new(
        screentransform_1.nodes["Camera Info"].outputs[0],
        screentransform_1.nodes["Multiply Matrices"].inputs[0]
    )
    # invert_matrix.Matrix -> multiply_matrices.Matrix
    screentransform_1.links.new(
        screentransform_1.nodes["Invert Matrix"].outputs[0],
        screentransform_1.nodes["Multiply Matrices"].inputs[1]
    )

    return screentransform_1

def camera_basis_1_node_group():
    """Initialize Camera Basis node group"""
    camera_basis_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Camera Basis")

    camera_basis_1.color_tag = 'INPUT'
    camera_basis_1.description = ""
    camera_basis_1.default_group_node_width = 140
    camera_basis_1.show_modifier_manage_panel = True

    # camera_basis_1 interface

    # Socket vright
    vright_socket = camera_basis_1.interface.new_socket(name="vright", in_out='OUTPUT', socket_type='NodeSocketVector')
    vright_socket.default_value = (0.0, 0.0, 0.0)
    vright_socket.min_value = -3.4028234663852886e+38
    vright_socket.max_value = 3.4028234663852886e+38
    vright_socket.subtype = 'NONE'
    vright_socket.attribute_domain = 'POINT'
    vright_socket.default_input = 'VALUE'
    vright_socket.structure_type = 'AUTO'

    # Socket vup
    vup_socket = camera_basis_1.interface.new_socket(name="vup", in_out='OUTPUT', socket_type='NodeSocketVector')
    vup_socket.default_value = (0.0, 0.0, 0.0)
    vup_socket.min_value = -3.4028234663852886e+38
    vup_socket.max_value = 3.4028234663852886e+38
    vup_socket.subtype = 'NONE'
    vup_socket.attribute_domain = 'POINT'
    vup_socket.default_input = 'VALUE'
    vup_socket.structure_type = 'AUTO'

    # Initialize camera_basis_1 nodes

    # Node Active Camera.001
    active_camera_001 = camera_basis_1.nodes.new("GeometryNodeInputActiveCamera")
    active_camera_001.name = "Active Camera.001"

    # Node Separate Matrix
    separate_matrix = camera_basis_1.nodes.new("FunctionNodeSeparateMatrix")
    separate_matrix.name = "Separate Matrix"
    separate_matrix.outputs[3].hide = True
    separate_matrix.outputs[7].hide = True
    separate_matrix.outputs[8].hide = True
    separate_matrix.outputs[9].hide = True
    separate_matrix.outputs[10].hide = True
    separate_matrix.outputs[11].hide = True
    separate_matrix.outputs[12].hide = True
    separate_matrix.outputs[13].hide = True
    separate_matrix.outputs[14].hide = True
    separate_matrix.outputs[15].hide = True

    # Node Combine XYZ.003
    combine_xyz_003 = camera_basis_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.name = "Combine XYZ.003"

    # Node Group Output
    group_output = camera_basis_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[2].hide = True

    # Node Combine XYZ.004
    combine_xyz_004 = camera_basis_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"

    # Node Object Info
    object_info = camera_basis_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    object_info.inputs[1].hide = True
    object_info.outputs[1].hide = True
    object_info.outputs[2].hide = True
    object_info.outputs[3].hide = True
    object_info.outputs[4].hide = True
    # As Instance
    object_info.inputs[1].default_value = False

    # Set locations
    camera_basis_1.nodes["Active Camera.001"].location = (-240.0, 0.0)
    camera_basis_1.nodes["Separate Matrix"].location = (80.0, 0.0)
    camera_basis_1.nodes["Combine XYZ.003"].location = (240.0, 0.0)
    camera_basis_1.nodes["Group Output"].location = (400.0, 0.0)
    camera_basis_1.nodes["Combine XYZ.004"].location = (240.0, -140.0)
    camera_basis_1.nodes["Object Info"].location = (-80.0, 0.0)

    # Set dimensions
    camera_basis_1.nodes["Active Camera.001"].width  = 140.0
    camera_basis_1.nodes["Active Camera.001"].height = 100.0

    camera_basis_1.nodes["Separate Matrix"].width  = 140.0
    camera_basis_1.nodes["Separate Matrix"].height = 100.0

    camera_basis_1.nodes["Combine XYZ.003"].width  = 140.0
    camera_basis_1.nodes["Combine XYZ.003"].height = 100.0

    camera_basis_1.nodes["Group Output"].width  = 140.0
    camera_basis_1.nodes["Group Output"].height = 100.0

    camera_basis_1.nodes["Combine XYZ.004"].width  = 140.0
    camera_basis_1.nodes["Combine XYZ.004"].height = 100.0

    camera_basis_1.nodes["Object Info"].width  = 140.0
    camera_basis_1.nodes["Object Info"].height = 100.0


    # Initialize camera_basis_1 links

    # separate_matrix.Column 1 Row 1 -> combine_xyz_003.X
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[0],
        camera_basis_1.nodes["Combine XYZ.003"].inputs[0]
    )
    # separate_matrix.Column 1 Row 2 -> combine_xyz_003.Y
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[1],
        camera_basis_1.nodes["Combine XYZ.003"].inputs[1]
    )
    # separate_matrix.Column 1 Row 3 -> combine_xyz_003.Z
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[2],
        camera_basis_1.nodes["Combine XYZ.003"].inputs[2]
    )
    # combine_xyz_003.Vector -> group_output.vright
    camera_basis_1.links.new(
        camera_basis_1.nodes["Combine XYZ.003"].outputs[0],
        camera_basis_1.nodes["Group Output"].inputs[0]
    )
    # combine_xyz_004.Vector -> group_output.vup
    camera_basis_1.links.new(
        camera_basis_1.nodes["Combine XYZ.004"].outputs[0],
        camera_basis_1.nodes["Group Output"].inputs[1]
    )
    # separate_matrix.Column 2 Row 1 -> combine_xyz_004.X
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[4],
        camera_basis_1.nodes["Combine XYZ.004"].inputs[0]
    )
    # separate_matrix.Column 2 Row 2 -> combine_xyz_004.Y
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[5],
        camera_basis_1.nodes["Combine XYZ.004"].inputs[1]
    )
    # separate_matrix.Column 2 Row 3 -> combine_xyz_004.Z
    camera_basis_1.links.new(
        camera_basis_1.nodes["Separate Matrix"].outputs[6],
        camera_basis_1.nodes["Combine XYZ.004"].inputs[2]
    )
    # active_camera_001.Active Camera -> object_info.Object
    camera_basis_1.links.new(
        camera_basis_1.nodes["Active Camera.001"].outputs[0],
        camera_basis_1.nodes["Object Info"].inputs[0]
    )
    # object_info.Transform -> separate_matrix.Matrix
    camera_basis_1.links.new(
        camera_basis_1.nodes["Object Info"].outputs[0],
        camera_basis_1.nodes["Separate Matrix"].inputs[0]
    )

    return camera_basis_1

def engine_state_1_node_group_geometry():
    """Initialize Engine State node group"""
    engine_state_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Engine State")

    engine_state_1.color_tag = 'INPUT'
    engine_state_1.description = ""
    engine_state_1.default_group_node_width = 140
    engine_state_1.show_modifier_manage_panel = True

    # engine_state_1 interface

    # Socket Time
    time_socket = engine_state_1.interface.new_socket(name="Time", in_out='OUTPUT', socket_type='NodeSocketFloat')
    time_socket.default_value = 0.0
    time_socket.min_value = -3.4028234663852886e+38
    time_socket.max_value = 3.4028234663852886e+38
    time_socket.subtype = 'NONE'
    time_socket.attribute_domain = 'POINT'
    time_socket.default_input = 'VALUE'
    time_socket.structure_type = 'AUTO'

    # Initialize engine_state_1 nodes

    # Node Value
    value = engine_state_1.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0

    time_driver = value.outputs[0].driver_add("default_value").driver
    time_driver.type = "SCRIPTED"

    time_driver_var = time_driver.variables.new()
    time_driver_var.name = "time"
    time_driver_var.type = "SINGLE_PROP"
    time_driver_var.targets[0].id_type = "SCENE"
    time_driver_var.targets[0].id = bpy.context.scene
    time_driver_var.targets[0].data_path = '["time"]'

    time_driver.expression = "time"

    # Node Group Output
    group_output = engine_state_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Set locations
    engine_state_1.nodes["Value"].location = (40.0, 0.0)
    engine_state_1.nodes["Group Output"].location = (200.0, 0.0)

    # Set dimensions
    engine_state_1.nodes["Value"].width  = 140.0
    engine_state_1.nodes["Value"].height = 100.0

    engine_state_1.nodes["Group Output"].width  = 140.0
    engine_state_1.nodes["Group Output"].height = 100.0


    # Initialize engine_state_1 links

    # value.Value -> group_output.Time
    engine_state_1.links.new(
        engine_state_1.nodes["Value"].outputs[0],
        engine_state_1.nodes["Group Output"].inputs[0]
    )

    return engine_state_1

def engine_state_1_node_group_shader():
    """Initialize Engine State node group"""
    engine_state_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Engine State")

    engine_state_1.color_tag = 'INPUT'
    engine_state_1.description = ""
    engine_state_1.default_group_node_width = 140
    # engine_state_1 interface

    # Socket Time
    time_socket = engine_state_1.interface.new_socket(name="Time", in_out='OUTPUT', socket_type='NodeSocketFloat')
    time_socket.default_value = 0.0
    time_socket.min_value = -3.4028234663852886e+38
    time_socket.max_value = 3.4028234663852886e+38
    time_socket.subtype = 'NONE'
    time_socket.attribute_domain = 'POINT'
    time_socket.default_input = 'VALUE'
    time_socket.structure_type = 'AUTO'

    # Initialize engine_state_1 nodes

    # Node Value
    value = engine_state_1.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0

    time_driver = value.outputs[0].driver_add("default_value").driver
    time_driver.type = "SCRIPTED"

    time_driver_var = time_driver.variables.new()
    time_driver_var.name = "time"
    time_driver_var.type = "SINGLE_PROP"
    time_driver_var.targets[0].id_type = "SCENE"
    time_driver_var.targets[0].id = bpy.context.scene
    time_driver_var.targets[0].data_path = '["time"]'

    time_driver.expression = "time"

    # Node Group Output
    group_output = engine_state_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Set locations
    engine_state_1.nodes["Value"].location = (40.0, 0.0)
    engine_state_1.nodes["Group Output"].location = (200.0, 0.0)

    # Set dimensions
    engine_state_1.nodes["Value"].width  = 140.0
    engine_state_1.nodes["Value"].height = 100.0

    engine_state_1.nodes["Group Output"].width  = 140.0
    engine_state_1.nodes["Group Output"].height = 100.0


    # Initialize engine_state_1 links

    # value.Value -> group_output.Time
    engine_state_1.links.new(
        engine_state_1.nodes["Value"].outputs[0],
        engine_state_1.nodes["Group Output"].inputs[0]
    )

    return engine_state_1


def vectorma_1_node_group():
    """Initialize VectorMA node group"""
    vectorma_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="VectorMA")

    vectorma_1.color_tag = 'VECTOR'
    vectorma_1.description = ""
    vectorma_1.default_group_node_width = 140
    vectorma_1.show_modifier_manage_panel = True

    # vectorma_1 interface

    # Socket Vector
    vector_socket = vectorma_1.interface.new_socket(name="Vector", in_out='OUTPUT', socket_type='NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'
    vector_socket.default_input = 'VALUE'
    vector_socket.structure_type = 'AUTO'

    # Socket Start
    start_socket = vectorma_1.interface.new_socket(name="Start", in_out='INPUT', socket_type='NodeSocketVector')
    start_socket.default_value = (0.0, 0.0, 0.0)
    start_socket.min_value = -10000.0
    start_socket.max_value = 10000.0
    start_socket.subtype = 'NONE'
    start_socket.attribute_domain = 'POINT'
    start_socket.default_input = 'VALUE'
    start_socket.structure_type = 'AUTO'

    # Socket Scale
    scale_socket = vectorma_1.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    scale_socket.default_value = 0.0
    scale_socket.min_value = -3.4028234663852886e+38
    scale_socket.max_value = 3.4028234663852886e+38
    scale_socket.subtype = 'NONE'
    scale_socket.attribute_domain = 'POINT'
    scale_socket.default_input = 'VALUE'
    scale_socket.structure_type = 'AUTO'

    # Socket Direction
    direction_socket = vectorma_1.interface.new_socket(name="Direction", in_out='INPUT', socket_type='NodeSocketVector')
    direction_socket.default_value = (0.0, 0.0, 0.0)
    direction_socket.min_value = -10000.0
    direction_socket.max_value = 10000.0
    direction_socket.subtype = 'NONE'
    direction_socket.attribute_domain = 'POINT'
    direction_socket.default_input = 'VALUE'
    direction_socket.structure_type = 'AUTO'

    # Initialize vectorma_1 nodes

    # Node Vector Math.008
    vector_math_008 = vectorma_1.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'ADD'

    # Node Group Output
    group_output = vectorma_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = vectorma_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[0].hide = True
    group_input.outputs[3].hide = True

    # Node Vector Math
    vector_math = vectorma_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'SCALE'

    # Node Group Input.001
    group_input_001 = vectorma_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True

    # Set locations
    vectorma_1.nodes["Vector Math.008"].location = (120.0, 0.0)
    vectorma_1.nodes["Group Output"].location = (280.0, 0.0)
    vectorma_1.nodes["Group Input"].location = (-200.0, 0.0)
    vectorma_1.nodes["Vector Math"].location = (-40.0, 0.0)
    vectorma_1.nodes["Group Input.001"].location = (-40.0, -140.0)

    # Set dimensions
    vectorma_1.nodes["Vector Math.008"].width  = 140.0
    vectorma_1.nodes["Vector Math.008"].height = 100.0

    vectorma_1.nodes["Group Output"].width  = 140.0
    vectorma_1.nodes["Group Output"].height = 100.0

    vectorma_1.nodes["Group Input"].width  = 140.0
    vectorma_1.nodes["Group Input"].height = 100.0

    vectorma_1.nodes["Vector Math"].width  = 140.0
    vectorma_1.nodes["Vector Math"].height = 100.0

    vectorma_1.nodes["Group Input.001"].width  = 140.0
    vectorma_1.nodes["Group Input.001"].height = 100.0


    # Initialize vectorma_1 links

    # vector_math_008.Vector -> group_output.Vector
    vectorma_1.links.new(
        vectorma_1.nodes["Vector Math.008"].outputs[0],
        vectorma_1.nodes["Group Output"].inputs[0]
    )
    # vector_math.Vector -> vector_math_008.Vector
    vectorma_1.links.new(
        vectorma_1.nodes["Vector Math"].outputs[0],
        vectorma_1.nodes["Vector Math.008"].inputs[0]
    )
    # group_input.Scale -> vector_math.Scale
    vectorma_1.links.new(
        vectorma_1.nodes["Group Input"].outputs[1],
        vectorma_1.nodes["Vector Math"].inputs[3]
    )
    # group_input.Direction -> vector_math.Vector
    vectorma_1.links.new(
        vectorma_1.nodes["Group Input"].outputs[2],
        vectorma_1.nodes["Vector Math"].inputs[0]
    )
    # group_input_001.Start -> vector_math_008.Vector
    vectorma_1.links.new(
        vectorma_1.nodes["Group Input.001"].outputs[0],
        vectorma_1.nodes["Vector Math.008"].inputs[1]
    )

    return vectorma_1

def beamfollow_1_node_group():
    """Initialize BeamFollow node group"""
    beamfollow_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="BeamFollow")

    beamfollow_1.color_tag = 'NONE'
    beamfollow_1.description = ""
    beamfollow_1.default_group_node_width = 140
    beamfollow_1.is_modifier = True
    beamfollow_1.show_modifier_manage_panel = True

    # beamfollow_1 interface

    # Socket Geometry
    geometry_socket = beamfollow_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = beamfollow_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket Material
    material_socket = beamfollow_1.interface.new_socket(name="Material", in_out='INPUT', socket_type='NodeSocketMaterial')
    material_socket.attribute_domain = 'POINT'
    material_socket.default_input = 'VALUE'
    material_socket.structure_type = 'AUTO'

    # Socket width
    width_socket = beamfollow_1.interface.new_socket(name="width", in_out='INPUT', socket_type='NodeSocketFloat')
    width_socket.default_value = 0.0
    width_socket.min_value = -3.4028234663852886e+38
    width_socket.max_value = 3.4028234663852886e+38
    width_socket.subtype = 'NONE'
    width_socket.attribute_domain = 'POINT'
    width_socket.default_input = 'VALUE'
    width_socket.structure_type = 'AUTO'

    # Socket amplitude
    amplitude_socket = beamfollow_1.interface.new_socket(name="amplitude", in_out='INPUT', socket_type='NodeSocketFloat')
    amplitude_socket.default_value = 0.0
    amplitude_socket.min_value = -3.4028234663852886e+38
    amplitude_socket.max_value = 3.4028234663852886e+38
    amplitude_socket.subtype = 'NONE'
    amplitude_socket.attribute_domain = 'POINT'
    amplitude_socket.default_input = 'VALUE'
    amplitude_socket.structure_type = 'AUTO'

    # Socket source
    source_socket = beamfollow_1.interface.new_socket(name="source", in_out='INPUT', socket_type='NodeSocketVector')
    source_socket.default_value = (0.0, 0.0, 0.0)
    source_socket.min_value = -3.4028234663852886e+38
    source_socket.max_value = 3.4028234663852886e+38
    source_socket.subtype = 'XYZ'
    source_socket.attribute_domain = 'POINT'
    source_socket.default_input = 'VALUE'
    source_socket.structure_type = 'AUTO'

    # Initialize beamfollow_1 nodes

    # Node Group Output.001
    group_output_001 = beamfollow_1.nodes.new("NodeGroupOutput")
    group_output_001.name = "Group Output.001"
    group_output_001.is_active_output = True

    # Node Grid.001
    grid_001 = beamfollow_1.nodes.new("GeometryNodeMeshGrid")
    grid_001.name = "Grid.001"
    # Size X
    grid_001.inputs[0].default_value = 1.0
    # Size Y
    grid_001.inputs[1].default_value = 1.0
    # Vertices Y
    grid_001.inputs[3].default_value = 2

    # Node Domain Size.001
    domain_size_001 = beamfollow_1.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.component = 'MESH'

    # Node Delete Geometry
    delete_geometry = beamfollow_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    # Node Named Attribute.001
    named_attribute_001 = beamfollow_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'FLOAT'
    # Name
    named_attribute_001.inputs[0].default_value = "die"

    # Node Compare
    compare = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_THAN'

    # Node Value.001
    value_001 = beamfollow_1.nodes.new("GeometryNodeGroup")
    value_001.name = "Value.001"
    value_001.node_tree = ensure_group("Geometry Engine State")
    value_001.show_options = False

    # Node Compare.001
    compare_001 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'LESS_THAN'

    # Node Boolean Math
    boolean_math = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'OR'

    # Node Group Input.007
    group_input_007 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[1].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True

    # Node Named Attribute.002
    named_attribute_002 = beamfollow_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.data_type = 'FLOAT'
    # Name
    named_attribute_002.inputs[0].default_value = "born"

    # Node Sample Index.004
    sample_index_004 = beamfollow_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.clamp = False
    sample_index_004.data_type = 'FLOAT_VECTOR'
    sample_index_004.domain = 'POINT'
    # Index
    sample_index_004.inputs[2].default_value = 0

    # Node Compare.005
    compare_005 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.data_type = 'VECTOR'
    compare_005.mode = 'ELEMENT'
    compare_005.operation = 'EQUAL'
    compare_005.inputs[0].hide = True
    compare_005.inputs[1].hide = True
    compare_005.inputs[2].hide = True
    compare_005.inputs[3].hide = True
    compare_005.inputs[6].hide = True
    compare_005.inputs[7].hide = True
    compare_005.inputs[8].hide = True
    compare_005.inputs[9].hide = True
    compare_005.inputs[10].hide = True
    compare_005.inputs[11].hide = True
    compare_005.inputs[12].hide = True
    # Epsilon
    compare_005.inputs[12].default_value = 0.0

    # Node Position.002
    position_002 = beamfollow_1.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    # Node Group Input.009
    group_input_009 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    group_input_009.outputs[0].hide = True
    group_input_009.outputs[1].hide = True
    group_input_009.outputs[2].hide = True
    group_input_009.outputs[3].hide = True
    group_input_009.outputs[5].hide = True

    # Node Join Geometry.001
    join_geometry_001 = beamfollow_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    # Node Group Input.010
    group_input_010 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_010.name = "Group Input.010"
    group_input_010.outputs[0].hide = True
    group_input_010.outputs[1].hide = True
    group_input_010.outputs[2].hide = True
    group_input_010.outputs[3].hide = True
    group_input_010.outputs[5].hide = True

    # Node Reroute.008
    reroute_008 = beamfollow_1.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketGeometry"
    # Node Reroute.009
    reroute_009 = beamfollow_1.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketGeometry"
    # Node Switch.004
    switch_004 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_004.name = "Switch.004"
    switch_004.input_type = 'INT'
    # False
    switch_004.inputs[1].default_value = 1
    # True
    switch_004.inputs[2].default_value = 0

    # Node Mesh Line
    mesh_line = beamfollow_1.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'OFFSET'
    mesh_line.inputs[1].hide = True
    mesh_line.inputs[3].hide = True
    # Offset
    mesh_line.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Integer Math
    integer_math = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.operation = 'SUBTRACT'
    # Value_001
    integer_math.inputs[1].default_value = 1

    # Node Integer Math.001
    integer_math_001 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.operation = 'MULTIPLY'
    # Value_001
    integer_math_001.inputs[1].default_value = 2

    # Node Delete Geometry.001
    delete_geometry_001 = beamfollow_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.domain = 'EDGE'
    delete_geometry_001.mode = 'ALL'

    # Node Index.005
    index_005 = beamfollow_1.nodes.new("GeometryNodeInputIndex")
    index_005.name = "Index.005"

    # Node Compare.004
    compare_004 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'INT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'GREATER_EQUAL'

    # Node Boolean Math.003
    boolean_math_003 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.operation = 'AND'

    # Node Integer Math.009
    integer_math_009 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_009.name = "Integer Math.009"
    integer_math_009.operation = 'MODULO'
    # Value_001
    integer_math_009.inputs[1].default_value = 2

    # Node Compare.006
    compare_006 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.data_type = 'INT'
    compare_006.mode = 'ELEMENT'
    compare_006.operation = 'GREATER_THAN'

    # Node Integer Math.011
    integer_math_011 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_011.name = "Integer Math.011"
    integer_math_011.operation = 'MULTIPLY'
    # Value_001
    integer_math_011.inputs[1].default_value = 2

    # Node Boolean Math.004
    boolean_math_004 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.operation = 'AND'

    # Node Boolean Math.005
    boolean_math_005 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.operation = 'NOT'

    # Node Boolean Math.006
    boolean_math_006 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.name = "Boolean Math.006"
    boolean_math_006.operation = 'AND'

    # Node Boolean Math.008
    boolean_math_008 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_008.name = "Boolean Math.008"
    boolean_math_008.operation = 'OR'

    # Node Compare.007
    compare_007 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.data_type = 'INT'
    compare_007.mode = 'ELEMENT'
    compare_007.operation = 'LESS_THAN'

    # Node Integer Math.012
    integer_math_012 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_012.name = "Integer Math.012"
    integer_math_012.operation = 'SUBTRACT'
    # Value_001
    integer_math_012.inputs[1].default_value = 1

    # Node Reroute.002
    reroute_002 = beamfollow_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Node Reroute.004
    reroute_004 = beamfollow_1.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Node Set Position
    set_position = beamfollow_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.008
    vector_math_008 = beamfollow_1.nodes.new("GeometryNodeGroup")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.node_tree = ensure_group("VectorMA")
    vector_math_008.show_options = False

    # Node Index.007
    index_007 = beamfollow_1.nodes.new("GeometryNodeInputIndex")
    index_007.name = "Index.007"

    # Node Integer Math.016
    integer_math_016 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_016.name = "Integer Math.016"
    integer_math_016.operation = 'FLOORED_MODULO'
    # Value_001
    integer_math_016.inputs[1].default_value = 2

    # Node Group Input.003
    group_input_003 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True

    # Node Math.008
    math_008 = beamfollow_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = False

    # Node Vector Math.009
    vector_math_009 = beamfollow_1.nodes.new("GeometryNodeGroup")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.node_tree = ensure_group("VectorMA")
    vector_math_009.show_options = False

    # Node Vector Math.010
    vector_math_010 = beamfollow_1.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'SCALE'

    # Node Group
    group = beamfollow_1.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = ensure_group("Camera Basis")
    group.outputs[1].hide = True
    group.show_options = False

    # Node Group.001
    group_001 = beamfollow_1.nodes.new("GeometryNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = ensure_group("Camera Basis")
    group_001.outputs[0].hide = True
    group_001.show_options = False

    # Node Vector Math.011
    vector_math_011 = beamfollow_1.nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.operation = 'NORMALIZE'

    # Node Separate XYZ.003
    separate_xyz_003 = beamfollow_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"

    # Node Math.009
    math_009 = beamfollow_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False
    # Value_001
    math_009.inputs[1].default_value = -1.0

    # Node Vector Math.012
    vector_math_012 = beamfollow_1.nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.operation = 'SUBTRACT'

    # Node Vector Math.013
    vector_math_013 = beamfollow_1.nodes.new("GeometryNodeGroup")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.node_tree = ensure_group("ScreenTransform")
    vector_math_013.show_options = False

    # Node Vector Math.014
    vector_math_014 = beamfollow_1.nodes.new("GeometryNodeGroup")
    vector_math_014.name = "Vector Math.014"
    vector_math_014.node_tree = ensure_group("ScreenTransform")
    vector_math_014.show_options = False

    # Node Separate XYZ.004
    separate_xyz_004 = beamfollow_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_004.name = "Separate XYZ.004"

    # Node Combine XYZ.003
    combine_xyz_003 = beamfollow_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.name = "Combine XYZ.003"
    # Z
    combine_xyz_003.inputs[2].default_value = 0.0

    # Node Sample Index.006
    sample_index_006 = beamfollow_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.clamp = False
    sample_index_006.data_type = 'FLOAT_VECTOR'
    sample_index_006.domain = 'POINT'

    # Node Position.004
    position_004 = beamfollow_1.nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"

    # Node Switch.002
    switch_002 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.input_type = 'FLOAT'
    # False
    switch_002.inputs[1].default_value = 1.0
    # True
    switch_002.inputs[2].default_value = -1.0

    # Node Reroute.010
    reroute_010 = beamfollow_1.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketVector"
    # Node Reroute.011
    reroute_011 = beamfollow_1.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketVector"
    # Node Sample Index.007
    sample_index_007 = beamfollow_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_007.name = "Sample Index.007"
    sample_index_007.clamp = False
    sample_index_007.data_type = 'FLOAT_VECTOR'
    sample_index_007.domain = 'POINT'

    # Node Position.005
    position_005 = beamfollow_1.nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"

    # Node Index.010
    index_010 = beamfollow_1.nodes.new("GeometryNodeInputIndex")
    index_010.name = "Index.010"

    # Node Integer Math.022
    integer_math_022 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_022.name = "Integer Math.022"
    integer_math_022.operation = 'DIVIDE'
    # Value_001
    integer_math_022.inputs[1].default_value = 2

    # Node Integer Math.018
    integer_math_018 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_018.name = "Integer Math.018"
    integer_math_018.operation = 'ADD'
    # Value_001
    integer_math_018.inputs[1].default_value = 1

    # Node Integer Math.023
    integer_math_023 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_023.name = "Integer Math.023"
    integer_math_023.operation = 'DIVIDE'
    # Value_001
    integer_math_023.inputs[1].default_value = 2

    # Node Sample Index.008
    sample_index_008 = beamfollow_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_008.name = "Sample Index.008"
    sample_index_008.clamp = False
    sample_index_008.data_type = 'FLOAT_VECTOR'
    sample_index_008.domain = 'POINT'

    # Node Integer Math.026
    integer_math_026 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_026.name = "Integer Math.026"
    integer_math_026.operation = 'SUBTRACT'
    # Value_001
    integer_math_026.inputs[1].default_value = 1

    # Node Compare.009
    compare_009 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.data_type = 'INT'
    compare_009.mode = 'ELEMENT'
    compare_009.operation = 'EQUAL'
    # B_INT
    compare_009.inputs[3].default_value = 0

    # Node Switch.006
    switch_006 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_006.name = "Switch.006"
    switch_006.input_type = 'INT'
    # True
    switch_006.inputs[2].default_value = 1

    # Node Switch.007
    switch_007 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_007.name = "Switch.007"
    switch_007.input_type = 'INT'
    # True
    switch_007.inputs[2].default_value = 0

    # Node Set Material.001
    set_material_001 = beamfollow_1.nodes.new("GeometryNodeSetMaterial")
    set_material_001.name = "Set Material.001"
    # Selection
    set_material_001.inputs[1].default_value = True

    # Node Group Input.005
    group_input_005 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[5].hide = True

    # Node Store Named Attribute.003
    store_named_attribute_003 = beamfollow_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'FLOAT2'
    store_named_attribute_003.domain = 'CORNER'
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "UVMap"

    # Node Index.008
    index_008 = beamfollow_1.nodes.new("GeometryNodeInputIndex")
    index_008.name = "Index.008"

    # Node Integer Math.017
    integer_math_017 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_017.name = "Integer Math.017"
    integer_math_017.operation = 'FLOORED_MODULO'
    # Value_001
    integer_math_017.inputs[1].default_value = 4

    # Node Index Switch.002
    index_switch_002 = beamfollow_1.nodes.new("GeometryNodeIndexSwitch")
    index_switch_002.name = "Index Switch.002"
    index_switch_002.data_type = 'VECTOR'
    index_switch_002.index_switch_items.clear()
    index_switch_002.index_switch_items.new()
    index_switch_002.index_switch_items.new()
    index_switch_002.index_switch_items.new()
    index_switch_002.index_switch_items.new()
    # Item_2
    index_switch_002.inputs[1].default_value = (0.0, 1.0, 0.0)
    # Item_3
    index_switch_002.inputs[2].default_value = (1.0, 1.0, 0.0)
    # Item_4
    index_switch_002.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Item_5
    index_switch_002.inputs[4].default_value = (1.0, 0.0, 0.0)

    # Node Store Named Attribute.004
    store_named_attribute_004 = beamfollow_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.data_type = 'FLOAT'
    store_named_attribute_004.domain = 'CORNER'
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "brightness"

    # Node Sample Index.009
    sample_index_009 = beamfollow_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_009.name = "Sample Index.009"
    sample_index_009.clamp = False
    sample_index_009.data_type = 'FLOAT'
    sample_index_009.domain = 'POINT'

    # Node Named Attribute.003
    named_attribute_003 = beamfollow_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.data_type = 'FLOAT'
    # Name
    named_attribute_003.inputs[0].default_value = "die"

    # Node Switch.005
    switch_005 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_005.name = "Switch.005"
    switch_005.input_type = 'FLOAT'
    # True
    switch_005.inputs[2].default_value = 0.0

    # Node Compare.008
    compare_008 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.data_type = 'INT'
    compare_008.mode = 'ELEMENT'
    compare_008.operation = 'EQUAL'

    # Node Value.003
    value_003 = beamfollow_1.nodes.new("GeometryNodeGroup")
    value_003.name = "Value.003"
    value_003.node_tree = ensure_group("Geometry Engine State")
    value_003.show_options = False

    # Node Math.010
    math_010 = beamfollow_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'SUBTRACT'
    math_010.use_clamp = False

    # Node Group Input.006
    group_input_006 = beamfollow_1.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[0].hide = True
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True

    # Node Math.011
    math_011 = beamfollow_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'DIVIDE'
    math_011.use_clamp = False

    # Node Compare.010
    compare_010 = beamfollow_1.nodes.new("FunctionNodeCompare")
    compare_010.name = "Compare.010"
    compare_010.data_type = 'INT'
    compare_010.mode = 'ELEMENT'
    compare_010.operation = 'EQUAL'
    # B_INT
    compare_010.inputs[3].default_value = 0

    # Node Index.011
    index_011 = beamfollow_1.nodes.new("GeometryNodeInputIndex")
    index_011.name = "Index.011"

    # Node Integer Math.024
    integer_math_024 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_024.name = "Integer Math.024"
    integer_math_024.operation = 'DIVIDE'
    # Value_001
    integer_math_024.inputs[1].default_value = 2

    # Node Integer Math.019
    integer_math_019 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_019.name = "Integer Math.019"
    integer_math_019.operation = 'ADD'
    # Value_001
    integer_math_019.inputs[1].default_value = 1

    # Node Integer Math.025
    integer_math_025 = beamfollow_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_025.name = "Integer Math.025"
    integer_math_025.operation = 'DIVIDE'
    # Value_001
    integer_math_025.inputs[1].default_value = 2

    # Node Boolean Math.007
    boolean_math_007 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.name = "Boolean Math.007"
    boolean_math_007.operation = 'AND'

    # Node Boolean Math.009
    boolean_math_009 = beamfollow_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_009.name = "Boolean Math.009"
    boolean_math_009.operation = 'NOT'

    # Node Switch.009
    switch_009 = beamfollow_1.nodes.new("GeometryNodeSwitch")
    switch_009.name = "Switch.009"
    switch_009.input_type = 'INT'
    # True
    switch_009.inputs[2].default_value = 1

    # Node Vertex of Corner.002
    vertex_of_corner_002 = beamfollow_1.nodes.new("GeometryNodeVertexOfCorner")
    vertex_of_corner_002.name = "Vertex of Corner.002"

    # Node Vertex of Corner.003
    vertex_of_corner_003 = beamfollow_1.nodes.new("GeometryNodeVertexOfCorner")
    vertex_of_corner_003.name = "Vertex of Corner.003"

    # Set locations
    beamfollow_1.nodes["Group Output.001"].location = (1600.0, 0.0)
    beamfollow_1.nodes["Grid.001"].location = (0.0, 0.0)
    beamfollow_1.nodes["Domain Size.001"].location = (-480.0, 0.0)
    beamfollow_1.nodes["Delete Geometry"].location = (-1600.0, 0.0)
    beamfollow_1.nodes["Named Attribute.001"].location = (-2080.0, -240.0)
    beamfollow_1.nodes["Compare"].location = (-1920.0, -200.0)
    beamfollow_1.nodes["Value.001"].location = (-2080.0, -40.0)
    beamfollow_1.nodes["Compare.001"].location = (-1920.0, -40.0)
    beamfollow_1.nodes["Boolean Math"].location = (-1760.0, -60.0)
    beamfollow_1.nodes["Group Input.007"].location = (-1760.0, 0.0)
    beamfollow_1.nodes["Named Attribute.002"].location = (-2080.0, -100.0)
    beamfollow_1.nodes["Sample Index.004"].location = (-1440.0, -40.0)
    beamfollow_1.nodes["Compare.005"].location = (-1280.0, -40.0)
    beamfollow_1.nodes["Position.002"].location = (-1600.0, -140.0)
    beamfollow_1.nodes["Group Input.009"].location = (-1440.0, -240.0)
    beamfollow_1.nodes["Join Geometry.001"].location = (-800.0, 0.0)
    beamfollow_1.nodes["Group Input.010"].location = (-1120.0, -200.0)
    beamfollow_1.nodes["Reroute.008"].location = (-1440.0, -20.0)
    beamfollow_1.nodes["Reroute.009"].location = (-820.0, -20.0)
    beamfollow_1.nodes["Switch.004"].location = (-1120.0, -40.0)
    beamfollow_1.nodes["Mesh Line"].location = (-960.0, -40.0)
    beamfollow_1.nodes["Integer Math"].location = (-320.0, 0.0)
    beamfollow_1.nodes["Integer Math.001"].location = (-160.0, 0.0)
    beamfollow_1.nodes["Delete Geometry.001"].location = (800.0, 0.0)
    beamfollow_1.nodes["Index.005"].location = (0.0, -240.0)
    beamfollow_1.nodes["Compare.004"].location = (160.0, -140.0)
    beamfollow_1.nodes["Boolean Math.003"].location = (320.0, 0.0)
    beamfollow_1.nodes["Integer Math.009"].location = (160.0, 0.0)
    beamfollow_1.nodes["Compare.006"].location = (320.0, -420.0)
    beamfollow_1.nodes["Integer Math.011"].location = (0.0, -300.0)
    beamfollow_1.nodes["Boolean Math.004"].location = (480.0, -300.0)
    beamfollow_1.nodes["Boolean Math.005"].location = (320.0, -300.0)
    beamfollow_1.nodes["Boolean Math.006"].location = (480.0, 0.0)
    beamfollow_1.nodes["Boolean Math.008"].location = (640.0, 0.0)
    beamfollow_1.nodes["Compare.007"].location = (320.0, -140.0)
    beamfollow_1.nodes["Integer Math.012"].location = (160.0, -300.0)
    beamfollow_1.nodes["Reroute.002"].location = (160.0, 20.0)
    beamfollow_1.nodes["Reroute.004"].location = (780.0, 20.0)
    beamfollow_1.nodes["Set Position"].location = (960.0, 0.0)
    beamfollow_1.nodes["Vector Math.008"].location = (800.0, -600.0)
    beamfollow_1.nodes["Index.007"].location = (160.0, -600.0)
    beamfollow_1.nodes["Integer Math.016"].location = (320.0, -600.0)
    beamfollow_1.nodes["Group Input.003"].location = (480.0, -600.0)
    beamfollow_1.nodes["Math.008"].location = (640.0, -600.0)
    beamfollow_1.nodes["Vector Math.009"].location = (640.0, -960.0)
    beamfollow_1.nodes["Vector Math.010"].location = (480.0, -820.0)
    beamfollow_1.nodes["Group"].location = (480.0, -1120.0)
    beamfollow_1.nodes["Group.001"].location = (320.0, -900.0)
    beamfollow_1.nodes["Vector Math.011"].location = (160.0, -960.0)
    beamfollow_1.nodes["Separate XYZ.003"].location = (320.0, -960.0)
    beamfollow_1.nodes["Math.009"].location = (480.0, -960.0)
    beamfollow_1.nodes["Vector Math.012"].location = (-320.0, -960.0)
    beamfollow_1.nodes["Vector Math.013"].location = (-480.0, -960.0)
    beamfollow_1.nodes["Vector Math.014"].location = (-480.0, -1040.0)
    beamfollow_1.nodes["Separate XYZ.004"].location = (-160.0, -960.0)
    beamfollow_1.nodes["Combine XYZ.003"].location = (0.0, -960.0)
    beamfollow_1.nodes["Sample Index.006"].location = (-640.0, -960.0)
    beamfollow_1.nodes["Position.004"].location = (-800.0, -1120.0)
    beamfollow_1.nodes["Switch.002"].location = (480.0, -660.0)
    beamfollow_1.nodes["Reroute.010"].location = (780.0, -580.0)
    beamfollow_1.nodes["Reroute.011"].location = (160.0, -580.0)
    beamfollow_1.nodes["Sample Index.007"].location = (0.0, -600.0)
    beamfollow_1.nodes["Position.005"].location = (-160.0, -720.0)
    beamfollow_1.nodes["Index.010"].location = (-1600.0, -960.0)
    beamfollow_1.nodes["Integer Math.022"].location = (-1440.0, -960.0)
    beamfollow_1.nodes["Integer Math.018"].location = (-1280.0, -960.0)
    beamfollow_1.nodes["Integer Math.023"].location = (-1120.0, -960.0)
    beamfollow_1.nodes["Sample Index.008"].location = (-640.0, -1160.0)
    beamfollow_1.nodes["Integer Math.026"].location = (-960.0, -1240.0)
    beamfollow_1.nodes["Compare.009"].location = (-960.0, -1080.0)
    beamfollow_1.nodes["Switch.006"].location = (-800.0, -960.0)
    beamfollow_1.nodes["Switch.007"].location = (-800.0, -1180.0)
    beamfollow_1.nodes["Set Material.001"].location = (1440.0, 0.0)
    beamfollow_1.nodes["Group Input.005"].location = (1280.0, -180.0)
    beamfollow_1.nodes["Store Named Attribute.003"].location = (1120.0, 0.0)
    beamfollow_1.nodes["Index.008"].location = (480.0, -200.0)
    beamfollow_1.nodes["Integer Math.017"].location = (800.0, -200.0)
    beamfollow_1.nodes["Index Switch.002"].location = (960.0, -200.0)
    beamfollow_1.nodes["Store Named Attribute.004"].location = (1280.0, 0.0)
    beamfollow_1.nodes["Sample Index.009"].location = (640.0, 280.0)
    beamfollow_1.nodes["Named Attribute.003"].location = (480.0, 320.0)
    beamfollow_1.nodes["Switch.005"].location = (1120.0, 320.0)
    beamfollow_1.nodes["Compare.008"].location = (640.0, 440.0)
    beamfollow_1.nodes["Value.003"].location = (640.0, 80.0)
    beamfollow_1.nodes["Math.010"].location = (800.0, 240.0)
    beamfollow_1.nodes["Group Input.006"].location = (800.0, 80.0)
    beamfollow_1.nodes["Math.011"].location = (960.0, 220.0)
    beamfollow_1.nodes["Compare.010"].location = (160.0, 300.0)
    beamfollow_1.nodes["Index.011"].location = (-640.0, 440.0)
    beamfollow_1.nodes["Integer Math.024"].location = (-320.0, 440.0)
    beamfollow_1.nodes["Integer Math.019"].location = (-160.0, 440.0)
    beamfollow_1.nodes["Integer Math.025"].location = (0.0, 440.0)
    beamfollow_1.nodes["Boolean Math.007"].location = (320.0, 180.0)
    beamfollow_1.nodes["Boolean Math.009"].location = (160.0, 140.0)
    beamfollow_1.nodes["Switch.009"].location = (480.0, 180.0)
    beamfollow_1.nodes["Vertex of Corner.002"].location = (-480.0, 440.0)
    beamfollow_1.nodes["Vertex of Corner.003"].location = (640.0, -200.0)

    # Set dimensions
    beamfollow_1.nodes["Group Output.001"].width  = 140.0
    beamfollow_1.nodes["Group Output.001"].height = 100.0

    beamfollow_1.nodes["Grid.001"].width  = 140.0
    beamfollow_1.nodes["Grid.001"].height = 100.0

    beamfollow_1.nodes["Domain Size.001"].width  = 140.0
    beamfollow_1.nodes["Domain Size.001"].height = 100.0

    beamfollow_1.nodes["Delete Geometry"].width  = 140.0
    beamfollow_1.nodes["Delete Geometry"].height = 100.0

    beamfollow_1.nodes["Named Attribute.001"].width  = 140.0
    beamfollow_1.nodes["Named Attribute.001"].height = 100.0

    beamfollow_1.nodes["Compare"].width  = 140.0
    beamfollow_1.nodes["Compare"].height = 100.0

    beamfollow_1.nodes["Value.001"].width  = 140.0
    beamfollow_1.nodes["Value.001"].height = 100.0

    beamfollow_1.nodes["Compare.001"].width  = 140.0
    beamfollow_1.nodes["Compare.001"].height = 100.0

    beamfollow_1.nodes["Boolean Math"].width  = 140.0
    beamfollow_1.nodes["Boolean Math"].height = 100.0

    beamfollow_1.nodes["Group Input.007"].width  = 140.0
    beamfollow_1.nodes["Group Input.007"].height = 100.0

    beamfollow_1.nodes["Named Attribute.002"].width  = 140.0
    beamfollow_1.nodes["Named Attribute.002"].height = 100.0

    beamfollow_1.nodes["Sample Index.004"].width  = 140.0
    beamfollow_1.nodes["Sample Index.004"].height = 100.0

    beamfollow_1.nodes["Compare.005"].width  = 140.0
    beamfollow_1.nodes["Compare.005"].height = 100.0

    beamfollow_1.nodes["Position.002"].width  = 140.0
    beamfollow_1.nodes["Position.002"].height = 100.0

    beamfollow_1.nodes["Group Input.009"].width  = 140.0
    beamfollow_1.nodes["Group Input.009"].height = 100.0

    beamfollow_1.nodes["Join Geometry.001"].width  = 140.0
    beamfollow_1.nodes["Join Geometry.001"].height = 100.0

    beamfollow_1.nodes["Group Input.010"].width  = 140.0
    beamfollow_1.nodes["Group Input.010"].height = 100.0

    beamfollow_1.nodes["Reroute.008"].width  = 10.0
    beamfollow_1.nodes["Reroute.008"].height = 100.0

    beamfollow_1.nodes["Reroute.009"].width  = 10.0
    beamfollow_1.nodes["Reroute.009"].height = 100.0

    beamfollow_1.nodes["Switch.004"].width  = 140.0
    beamfollow_1.nodes["Switch.004"].height = 100.0

    beamfollow_1.nodes["Mesh Line"].width  = 140.0
    beamfollow_1.nodes["Mesh Line"].height = 100.0

    beamfollow_1.nodes["Integer Math"].width  = 140.0
    beamfollow_1.nodes["Integer Math"].height = 100.0

    beamfollow_1.nodes["Integer Math.001"].width  = 140.0
    beamfollow_1.nodes["Integer Math.001"].height = 100.0

    beamfollow_1.nodes["Delete Geometry.001"].width  = 140.0
    beamfollow_1.nodes["Delete Geometry.001"].height = 100.0

    beamfollow_1.nodes["Index.005"].width  = 140.0
    beamfollow_1.nodes["Index.005"].height = 100.0

    beamfollow_1.nodes["Compare.004"].width  = 140.0
    beamfollow_1.nodes["Compare.004"].height = 100.0

    beamfollow_1.nodes["Boolean Math.003"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.003"].height = 100.0

    beamfollow_1.nodes["Integer Math.009"].width  = 140.0
    beamfollow_1.nodes["Integer Math.009"].height = 100.0

    beamfollow_1.nodes["Compare.006"].width  = 140.0
    beamfollow_1.nodes["Compare.006"].height = 100.0

    beamfollow_1.nodes["Integer Math.011"].width  = 140.0
    beamfollow_1.nodes["Integer Math.011"].height = 100.0

    beamfollow_1.nodes["Boolean Math.004"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.004"].height = 100.0

    beamfollow_1.nodes["Boolean Math.005"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.005"].height = 100.0

    beamfollow_1.nodes["Boolean Math.006"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.006"].height = 100.0

    beamfollow_1.nodes["Boolean Math.008"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.008"].height = 100.0

    beamfollow_1.nodes["Compare.007"].width  = 140.0
    beamfollow_1.nodes["Compare.007"].height = 100.0

    beamfollow_1.nodes["Integer Math.012"].width  = 140.0
    beamfollow_1.nodes["Integer Math.012"].height = 100.0

    beamfollow_1.nodes["Reroute.002"].width  = 10.0
    beamfollow_1.nodes["Reroute.002"].height = 100.0

    beamfollow_1.nodes["Reroute.004"].width  = 10.0
    beamfollow_1.nodes["Reroute.004"].height = 100.0

    beamfollow_1.nodes["Set Position"].width  = 140.0
    beamfollow_1.nodes["Set Position"].height = 100.0

    beamfollow_1.nodes["Vector Math.008"].width  = 140.0
    beamfollow_1.nodes["Vector Math.008"].height = 100.0

    beamfollow_1.nodes["Index.007"].width  = 140.0
    beamfollow_1.nodes["Index.007"].height = 100.0

    beamfollow_1.nodes["Integer Math.016"].width  = 140.0
    beamfollow_1.nodes["Integer Math.016"].height = 100.0

    beamfollow_1.nodes["Group Input.003"].width  = 140.0
    beamfollow_1.nodes["Group Input.003"].height = 100.0

    beamfollow_1.nodes["Math.008"].width  = 140.0
    beamfollow_1.nodes["Math.008"].height = 100.0

    beamfollow_1.nodes["Vector Math.009"].width  = 140.0
    beamfollow_1.nodes["Vector Math.009"].height = 100.0

    beamfollow_1.nodes["Vector Math.010"].width  = 140.0
    beamfollow_1.nodes["Vector Math.010"].height = 100.0

    beamfollow_1.nodes["Group"].width  = 140.0
    beamfollow_1.nodes["Group"].height = 100.0

    beamfollow_1.nodes["Group.001"].width  = 140.0
    beamfollow_1.nodes["Group.001"].height = 100.0

    beamfollow_1.nodes["Vector Math.011"].width  = 140.0
    beamfollow_1.nodes["Vector Math.011"].height = 100.0

    beamfollow_1.nodes["Separate XYZ.003"].width  = 140.0
    beamfollow_1.nodes["Separate XYZ.003"].height = 100.0

    beamfollow_1.nodes["Math.009"].width  = 140.0
    beamfollow_1.nodes["Math.009"].height = 100.0

    beamfollow_1.nodes["Vector Math.012"].width  = 140.0
    beamfollow_1.nodes["Vector Math.012"].height = 100.0

    beamfollow_1.nodes["Vector Math.013"].width  = 140.0
    beamfollow_1.nodes["Vector Math.013"].height = 100.0

    beamfollow_1.nodes["Vector Math.014"].width  = 140.0
    beamfollow_1.nodes["Vector Math.014"].height = 100.0

    beamfollow_1.nodes["Separate XYZ.004"].width  = 140.0
    beamfollow_1.nodes["Separate XYZ.004"].height = 100.0

    beamfollow_1.nodes["Combine XYZ.003"].width  = 140.0
    beamfollow_1.nodes["Combine XYZ.003"].height = 100.0

    beamfollow_1.nodes["Sample Index.006"].width  = 140.0
    beamfollow_1.nodes["Sample Index.006"].height = 100.0

    beamfollow_1.nodes["Position.004"].width  = 140.0
    beamfollow_1.nodes["Position.004"].height = 100.0

    beamfollow_1.nodes["Switch.002"].width  = 140.0
    beamfollow_1.nodes["Switch.002"].height = 100.0

    beamfollow_1.nodes["Reroute.010"].width  = 10.0
    beamfollow_1.nodes["Reroute.010"].height = 100.0

    beamfollow_1.nodes["Reroute.011"].width  = 10.0
    beamfollow_1.nodes["Reroute.011"].height = 100.0

    beamfollow_1.nodes["Sample Index.007"].width  = 140.0
    beamfollow_1.nodes["Sample Index.007"].height = 100.0

    beamfollow_1.nodes["Position.005"].width  = 140.0
    beamfollow_1.nodes["Position.005"].height = 100.0

    beamfollow_1.nodes["Index.010"].width  = 140.0
    beamfollow_1.nodes["Index.010"].height = 100.0

    beamfollow_1.nodes["Integer Math.022"].width  = 140.0
    beamfollow_1.nodes["Integer Math.022"].height = 100.0

    beamfollow_1.nodes["Integer Math.018"].width  = 140.0
    beamfollow_1.nodes["Integer Math.018"].height = 100.0

    beamfollow_1.nodes["Integer Math.023"].width  = 140.0
    beamfollow_1.nodes["Integer Math.023"].height = 100.0

    beamfollow_1.nodes["Sample Index.008"].width  = 140.0
    beamfollow_1.nodes["Sample Index.008"].height = 100.0

    beamfollow_1.nodes["Integer Math.026"].width  = 140.0
    beamfollow_1.nodes["Integer Math.026"].height = 100.0

    beamfollow_1.nodes["Compare.009"].width  = 140.0
    beamfollow_1.nodes["Compare.009"].height = 100.0

    beamfollow_1.nodes["Switch.006"].width  = 140.0
    beamfollow_1.nodes["Switch.006"].height = 100.0

    beamfollow_1.nodes["Switch.007"].width  = 140.0
    beamfollow_1.nodes["Switch.007"].height = 100.0

    beamfollow_1.nodes["Set Material.001"].width  = 140.0
    beamfollow_1.nodes["Set Material.001"].height = 100.0

    beamfollow_1.nodes["Group Input.005"].width  = 140.0
    beamfollow_1.nodes["Group Input.005"].height = 100.0

    beamfollow_1.nodes["Store Named Attribute.003"].width  = 140.0
    beamfollow_1.nodes["Store Named Attribute.003"].height = 100.0

    beamfollow_1.nodes["Index.008"].width  = 140.0
    beamfollow_1.nodes["Index.008"].height = 100.0

    beamfollow_1.nodes["Integer Math.017"].width  = 140.0
    beamfollow_1.nodes["Integer Math.017"].height = 100.0

    beamfollow_1.nodes["Index Switch.002"].width  = 140.0
    beamfollow_1.nodes["Index Switch.002"].height = 100.0

    beamfollow_1.nodes["Store Named Attribute.004"].width  = 140.0
    beamfollow_1.nodes["Store Named Attribute.004"].height = 100.0

    beamfollow_1.nodes["Sample Index.009"].width  = 140.0
    beamfollow_1.nodes["Sample Index.009"].height = 100.0

    beamfollow_1.nodes["Named Attribute.003"].width  = 140.0
    beamfollow_1.nodes["Named Attribute.003"].height = 100.0

    beamfollow_1.nodes["Switch.005"].width  = 140.0
    beamfollow_1.nodes["Switch.005"].height = 100.0

    beamfollow_1.nodes["Compare.008"].width  = 140.0
    beamfollow_1.nodes["Compare.008"].height = 100.0

    beamfollow_1.nodes["Value.003"].width  = 140.0
    beamfollow_1.nodes["Value.003"].height = 100.0

    beamfollow_1.nodes["Math.010"].width  = 140.0
    beamfollow_1.nodes["Math.010"].height = 100.0

    beamfollow_1.nodes["Group Input.006"].width  = 140.0
    beamfollow_1.nodes["Group Input.006"].height = 100.0

    beamfollow_1.nodes["Math.011"].width  = 140.0
    beamfollow_1.nodes["Math.011"].height = 100.0

    beamfollow_1.nodes["Compare.010"].width  = 140.0
    beamfollow_1.nodes["Compare.010"].height = 100.0

    beamfollow_1.nodes["Index.011"].width  = 140.0
    beamfollow_1.nodes["Index.011"].height = 100.0

    beamfollow_1.nodes["Integer Math.024"].width  = 140.0
    beamfollow_1.nodes["Integer Math.024"].height = 100.0

    beamfollow_1.nodes["Integer Math.019"].width  = 140.0
    beamfollow_1.nodes["Integer Math.019"].height = 100.0

    beamfollow_1.nodes["Integer Math.025"].width  = 140.0
    beamfollow_1.nodes["Integer Math.025"].height = 100.0

    beamfollow_1.nodes["Boolean Math.007"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.007"].height = 100.0

    beamfollow_1.nodes["Boolean Math.009"].width  = 140.0
    beamfollow_1.nodes["Boolean Math.009"].height = 100.0

    beamfollow_1.nodes["Switch.009"].width  = 140.0
    beamfollow_1.nodes["Switch.009"].height = 100.0

    beamfollow_1.nodes["Vertex of Corner.002"].width  = 140.0
    beamfollow_1.nodes["Vertex of Corner.002"].height = 100.0

    beamfollow_1.nodes["Vertex of Corner.003"].width  = 140.0
    beamfollow_1.nodes["Vertex of Corner.003"].height = 100.0


    # Initialize beamfollow_1 links

    # boolean_math.Boolean -> delete_geometry.Selection
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math"].outputs[0],
        beamfollow_1.nodes["Delete Geometry"].inputs[1]
    )
    # compare_001.Result -> boolean_math.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.001"].outputs[0],
        beamfollow_1.nodes["Boolean Math"].inputs[0]
    )
    # compare.Result -> boolean_math.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare"].outputs[0],
        beamfollow_1.nodes["Boolean Math"].inputs[1]
    )
    # value_001.Time -> compare.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Value.001"].outputs[0],
        beamfollow_1.nodes["Compare"].inputs[0]
    )
    # named_attribute_001.Attribute -> compare.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Named Attribute.001"].outputs[0],
        beamfollow_1.nodes["Compare"].inputs[1]
    )
    # group_input_007.Geometry -> delete_geometry.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.007"].outputs[0],
        beamfollow_1.nodes["Delete Geometry"].inputs[0]
    )
    # value_001.Time -> compare_001.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Value.001"].outputs[0],
        beamfollow_1.nodes["Compare.001"].inputs[0]
    )
    # named_attribute_002.Attribute -> compare_001.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Named Attribute.002"].outputs[0],
        beamfollow_1.nodes["Compare.001"].inputs[1]
    )
    # delete_geometry.Geometry -> sample_index_004.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Delete Geometry"].outputs[0],
        beamfollow_1.nodes["Sample Index.004"].inputs[0]
    )
    # position_002.Position -> sample_index_004.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Position.002"].outputs[0],
        beamfollow_1.nodes["Sample Index.004"].inputs[1]
    )
    # sample_index_004.Value -> compare_005.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Sample Index.004"].outputs[0],
        beamfollow_1.nodes["Compare.005"].inputs[4]
    )
    # group_input_009.source -> compare_005.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.009"].outputs[4],
        beamfollow_1.nodes["Compare.005"].inputs[5]
    )
    # delete_geometry.Geometry -> reroute_008.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Delete Geometry"].outputs[0],
        beamfollow_1.nodes["Reroute.008"].inputs[0]
    )
    # reroute_008.Output -> reroute_009.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.008"].outputs[0],
        beamfollow_1.nodes["Reroute.009"].inputs[0]
    )
    # reroute_009.Output -> join_geometry_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.009"].outputs[0],
        beamfollow_1.nodes["Join Geometry.001"].inputs[0]
    )
    # compare_005.Result -> switch_004.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.005"].outputs[0],
        beamfollow_1.nodes["Switch.004"].inputs[0]
    )
    # switch_004.Output -> mesh_line.Count
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.004"].outputs[0],
        beamfollow_1.nodes["Mesh Line"].inputs[0]
    )
    # group_input_010.source -> mesh_line.Start Location
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.010"].outputs[4],
        beamfollow_1.nodes["Mesh Line"].inputs[2]
    )
    # integer_math_001.Value -> grid_001.Vertices X
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.001"].outputs[0],
        beamfollow_1.nodes["Grid.001"].inputs[2]
    )
    # domain_size_001.Point Count -> integer_math.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Domain Size.001"].outputs[0],
        beamfollow_1.nodes["Integer Math"].inputs[0]
    )
    # integer_math.Value -> integer_math_001.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math"].outputs[0],
        beamfollow_1.nodes["Integer Math.001"].inputs[0]
    )
    # reroute_004.Output -> delete_geometry_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.004"].outputs[0],
        beamfollow_1.nodes["Delete Geometry.001"].inputs[0]
    )
    # index_005.Index -> compare_004.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.005"].outputs[0],
        beamfollow_1.nodes["Compare.004"].inputs[2]
    )
    # integer_math_001.Value -> compare_004.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.001"].outputs[0],
        beamfollow_1.nodes["Compare.004"].inputs[3]
    )
    # index_005.Index -> integer_math_009.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.005"].outputs[0],
        beamfollow_1.nodes["Integer Math.009"].inputs[0]
    )
    # compare_004.Result -> boolean_math_003.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.004"].outputs[0],
        beamfollow_1.nodes["Boolean Math.003"].inputs[1]
    )
    # integer_math_001.Value -> integer_math_011.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.001"].outputs[0],
        beamfollow_1.nodes["Integer Math.011"].inputs[0]
    )
    # index_005.Index -> compare_006.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.005"].outputs[0],
        beamfollow_1.nodes["Compare.006"].inputs[2]
    )
    # integer_math_009.Value -> boolean_math_003.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.009"].outputs[0],
        beamfollow_1.nodes["Boolean Math.003"].inputs[0]
    )
    # integer_math_009.Value -> boolean_math_005.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.009"].outputs[0],
        beamfollow_1.nodes["Boolean Math.005"].inputs[0]
    )
    # boolean_math_005.Boolean -> boolean_math_004.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.005"].outputs[0],
        beamfollow_1.nodes["Boolean Math.004"].inputs[0]
    )
    # compare_006.Result -> boolean_math_004.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.006"].outputs[0],
        beamfollow_1.nodes["Boolean Math.004"].inputs[1]
    )
    # boolean_math_006.Boolean -> boolean_math_008.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.006"].outputs[0],
        beamfollow_1.nodes["Boolean Math.008"].inputs[0]
    )
    # boolean_math_004.Boolean -> boolean_math_008.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.004"].outputs[0],
        beamfollow_1.nodes["Boolean Math.008"].inputs[1]
    )
    # compare_007.Result -> boolean_math_006.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.007"].outputs[0],
        beamfollow_1.nodes["Boolean Math.006"].inputs[1]
    )
    # integer_math_012.Value -> compare_007.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.012"].outputs[0],
        beamfollow_1.nodes["Compare.007"].inputs[3]
    )
    # index_005.Index -> compare_007.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.005"].outputs[0],
        beamfollow_1.nodes["Compare.007"].inputs[2]
    )
    # integer_math_011.Value -> integer_math_012.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.011"].outputs[0],
        beamfollow_1.nodes["Integer Math.012"].inputs[0]
    )
    # boolean_math_008.Boolean -> delete_geometry_001.Selection
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.008"].outputs[0],
        beamfollow_1.nodes["Delete Geometry.001"].inputs[1]
    )
    # boolean_math_003.Boolean -> boolean_math_006.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.003"].outputs[0],
        beamfollow_1.nodes["Boolean Math.006"].inputs[0]
    )
    # integer_math_012.Value -> compare_006.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.012"].outputs[0],
        beamfollow_1.nodes["Compare.006"].inputs[3]
    )
    # grid_001.Mesh -> reroute_002.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Grid.001"].outputs[0],
        beamfollow_1.nodes["Reroute.002"].inputs[0]
    )
    # reroute_002.Output -> reroute_004.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.002"].outputs[0],
        beamfollow_1.nodes["Reroute.004"].inputs[0]
    )
    # delete_geometry_001.Geometry -> set_position.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Delete Geometry.001"].outputs[0],
        beamfollow_1.nodes["Set Position"].inputs[0]
    )
    # index_007.Index -> integer_math_016.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.007"].outputs[0],
        beamfollow_1.nodes["Integer Math.016"].inputs[0]
    )
    # group_input_003.width -> math_008.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.003"].outputs[2],
        beamfollow_1.nodes["Math.008"].inputs[0]
    )
    # math_008.Value -> vector_math_008.Scale
    beamfollow_1.links.new(
        beamfollow_1.nodes["Math.008"].outputs[0],
        beamfollow_1.nodes["Vector Math.008"].inputs[1]
    )
    # vector_math_010.Vector -> vector_math_009.Start
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.010"].outputs[0],
        beamfollow_1.nodes["Vector Math.009"].inputs[0]
    )
    # vector_math_011.Vector -> separate_xyz_003.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.011"].outputs[0],
        beamfollow_1.nodes["Separate XYZ.003"].inputs[0]
    )
    # math_009.Value -> vector_math_009.Scale
    beamfollow_1.links.new(
        beamfollow_1.nodes["Math.009"].outputs[0],
        beamfollow_1.nodes["Vector Math.009"].inputs[1]
    )
    # vector_math_013.Vector -> vector_math_012.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.013"].outputs[0],
        beamfollow_1.nodes["Vector Math.012"].inputs[0]
    )
    # vector_math_014.Vector -> vector_math_012.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.014"].outputs[0],
        beamfollow_1.nodes["Vector Math.012"].inputs[1]
    )
    # separate_xyz_004.X -> combine_xyz_003.X
    beamfollow_1.links.new(
        beamfollow_1.nodes["Separate XYZ.004"].outputs[0],
        beamfollow_1.nodes["Combine XYZ.003"].inputs[0]
    )
    # separate_xyz_004.Y -> combine_xyz_003.Y
    beamfollow_1.links.new(
        beamfollow_1.nodes["Separate XYZ.004"].outputs[1],
        beamfollow_1.nodes["Combine XYZ.003"].inputs[1]
    )
    # vector_math_012.Vector -> separate_xyz_004.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.012"].outputs[0],
        beamfollow_1.nodes["Separate XYZ.004"].inputs[0]
    )
    # combine_xyz_003.Vector -> vector_math_011.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Combine XYZ.003"].outputs[0],
        beamfollow_1.nodes["Vector Math.011"].inputs[0]
    )
    # position_004.Position -> sample_index_006.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Position.004"].outputs[0],
        beamfollow_1.nodes["Sample Index.006"].inputs[1]
    )
    # reroute_010.Output -> vector_math_008.Start
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.010"].outputs[0],
        beamfollow_1.nodes["Vector Math.008"].inputs[0]
    )
    # integer_math_016.Value -> switch_002.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.016"].outputs[0],
        beamfollow_1.nodes["Switch.002"].inputs[0]
    )
    # switch_002.Output -> math_008.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.002"].outputs[0],
        beamfollow_1.nodes["Math.008"].inputs[1]
    )
    # reroute_011.Output -> reroute_010.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Reroute.011"].outputs[0],
        beamfollow_1.nodes["Reroute.010"].inputs[0]
    )
    # position_005.Position -> sample_index_007.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Position.005"].outputs[0],
        beamfollow_1.nodes["Sample Index.007"].inputs[1]
    )
    # sample_index_007.Value -> reroute_011.Input
    beamfollow_1.links.new(
        beamfollow_1.nodes["Sample Index.007"].outputs[0],
        beamfollow_1.nodes["Reroute.011"].inputs[0]
    )
    # index_010.Index -> integer_math_022.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.010"].outputs[0],
        beamfollow_1.nodes["Integer Math.022"].inputs[0]
    )
    # integer_math_022.Value -> integer_math_018.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.022"].outputs[0],
        beamfollow_1.nodes["Integer Math.018"].inputs[0]
    )
    # integer_math_018.Value -> integer_math_023.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.018"].outputs[0],
        beamfollow_1.nodes["Integer Math.023"].inputs[0]
    )
    # switch_007.Output -> sample_index_008.Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.007"].outputs[0],
        beamfollow_1.nodes["Sample Index.008"].inputs[2]
    )
    # position_004.Position -> sample_index_008.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Position.004"].outputs[0],
        beamfollow_1.nodes["Sample Index.008"].inputs[1]
    )
    # sample_index_006.Value -> vector_math_013.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Sample Index.006"].outputs[0],
        beamfollow_1.nodes["Vector Math.013"].inputs[0]
    )
    # sample_index_008.Value -> vector_math_014.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Sample Index.008"].outputs[0],
        beamfollow_1.nodes["Vector Math.014"].inputs[0]
    )
    # integer_math_023.Value -> integer_math_026.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.023"].outputs[0],
        beamfollow_1.nodes["Integer Math.026"].inputs[0]
    )
    # compare_009.Result -> switch_006.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.009"].outputs[0],
        beamfollow_1.nodes["Switch.006"].inputs[0]
    )
    # switch_006.Output -> sample_index_006.Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.006"].outputs[0],
        beamfollow_1.nodes["Sample Index.006"].inputs[2]
    )
    # compare_009.Result -> switch_007.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.009"].outputs[0],
        beamfollow_1.nodes["Switch.007"].inputs[0]
    )
    # integer_math_023.Value -> compare_009.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.023"].outputs[0],
        beamfollow_1.nodes["Compare.009"].inputs[2]
    )
    # vector_math_008.Vector -> set_position.Position
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.008"].outputs[0],
        beamfollow_1.nodes["Set Position"].inputs[2]
    )
    # group_input_005.Material -> set_material_001.Material
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.005"].outputs[1],
        beamfollow_1.nodes["Set Material.001"].inputs[2]
    )
    # integer_math_026.Value -> switch_007.False
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.026"].outputs[0],
        beamfollow_1.nodes["Switch.007"].inputs[1]
    )
    # integer_math_023.Value -> switch_006.False
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.023"].outputs[0],
        beamfollow_1.nodes["Switch.006"].inputs[1]
    )
    # group_001.vup -> vector_math_010.Vector
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group.001"].outputs[1],
        beamfollow_1.nodes["Vector Math.010"].inputs[0]
    )
    # separate_xyz_003.X -> vector_math_010.Scale
    beamfollow_1.links.new(
        beamfollow_1.nodes["Separate XYZ.003"].outputs[0],
        beamfollow_1.nodes["Vector Math.010"].inputs[3]
    )
    # separate_xyz_003.Y -> math_009.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Separate XYZ.003"].outputs[1],
        beamfollow_1.nodes["Math.009"].inputs[0]
    )
    # vector_math_009.Vector -> vector_math_008.Direction
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vector Math.009"].outputs[0],
        beamfollow_1.nodes["Vector Math.008"].inputs[2]
    )
    # store_named_attribute_004.Geometry -> set_material_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Store Named Attribute.004"].outputs[0],
        beamfollow_1.nodes["Set Material.001"].inputs[0]
    )
    # set_material_001.Geometry -> group_output_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Set Material.001"].outputs[0],
        beamfollow_1.nodes["Group Output.001"].inputs[0]
    )
    # join_geometry_001.Geometry -> sample_index_007.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Join Geometry.001"].outputs[0],
        beamfollow_1.nodes["Sample Index.007"].inputs[0]
    )
    # integer_math_023.Value -> sample_index_007.Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.023"].outputs[0],
        beamfollow_1.nodes["Sample Index.007"].inputs[2]
    )
    # join_geometry_001.Geometry -> sample_index_006.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Join Geometry.001"].outputs[0],
        beamfollow_1.nodes["Sample Index.006"].inputs[0]
    )
    # join_geometry_001.Geometry -> sample_index_008.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Join Geometry.001"].outputs[0],
        beamfollow_1.nodes["Sample Index.008"].inputs[0]
    )
    # join_geometry_001.Geometry -> domain_size_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Join Geometry.001"].outputs[0],
        beamfollow_1.nodes["Domain Size.001"].inputs[0]
    )
    # set_position.Geometry -> store_named_attribute_003.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Set Position"].outputs[0],
        beamfollow_1.nodes["Store Named Attribute.003"].inputs[0]
    )
    # vertex_of_corner_003.Vertex Index -> integer_math_017.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vertex of Corner.003"].outputs[0],
        beamfollow_1.nodes["Integer Math.017"].inputs[0]
    )
    # store_named_attribute_003.Geometry -> store_named_attribute_004.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Store Named Attribute.003"].outputs[0],
        beamfollow_1.nodes["Store Named Attribute.004"].inputs[0]
    )
    # named_attribute_003.Attribute -> sample_index_009.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Named Attribute.003"].outputs[0],
        beamfollow_1.nodes["Sample Index.009"].inputs[1]
    )
    # join_geometry_001.Geometry -> sample_index_009.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Join Geometry.001"].outputs[0],
        beamfollow_1.nodes["Sample Index.009"].inputs[0]
    )
    # compare_008.Result -> switch_005.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.008"].outputs[0],
        beamfollow_1.nodes["Switch.005"].inputs[0]
    )
    # value_003.Time -> math_010.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Value.003"].outputs[0],
        beamfollow_1.nodes["Math.010"].inputs[1]
    )
    # math_010.Value -> math_011.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Math.010"].outputs[0],
        beamfollow_1.nodes["Math.011"].inputs[0]
    )
    # group_input_006.amplitude -> math_011.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group Input.006"].outputs[3],
        beamfollow_1.nodes["Math.011"].inputs[1]
    )
    # math_011.Value -> switch_005.False
    beamfollow_1.links.new(
        beamfollow_1.nodes["Math.011"].outputs[0],
        beamfollow_1.nodes["Switch.005"].inputs[1]
    )
    # sample_index_009.Value -> math_010.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Sample Index.009"].outputs[0],
        beamfollow_1.nodes["Math.010"].inputs[0]
    )
    # integer_math.Value -> compare_008.B
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math"].outputs[0],
        beamfollow_1.nodes["Compare.008"].inputs[3]
    )
    # index_switch_002.Output -> store_named_attribute_003.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index Switch.002"].outputs[0],
        beamfollow_1.nodes["Store Named Attribute.003"].inputs[3]
    )
    # integer_math_024.Value -> integer_math_019.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.024"].outputs[0],
        beamfollow_1.nodes["Integer Math.019"].inputs[0]
    )
    # integer_math_019.Value -> integer_math_025.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.019"].outputs[0],
        beamfollow_1.nodes["Integer Math.025"].inputs[0]
    )
    # integer_math_025.Value -> compare_010.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.025"].outputs[0],
        beamfollow_1.nodes["Compare.010"].inputs[2]
    )
    # integer_math_025.Value -> compare_008.A
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.025"].outputs[0],
        beamfollow_1.nodes["Compare.008"].inputs[2]
    )
    # compare_010.Result -> boolean_math_007.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.010"].outputs[0],
        beamfollow_1.nodes["Boolean Math.007"].inputs[0]
    )
    # boolean_math_009.Boolean -> boolean_math_007.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.009"].outputs[0],
        beamfollow_1.nodes["Boolean Math.007"].inputs[1]
    )
    # compare_005.Result -> boolean_math_009.Boolean
    beamfollow_1.links.new(
        beamfollow_1.nodes["Compare.005"].outputs[0],
        beamfollow_1.nodes["Boolean Math.009"].inputs[0]
    )
    # group.vright -> vector_math_009.Direction
    beamfollow_1.links.new(
        beamfollow_1.nodes["Group"].outputs[0],
        beamfollow_1.nodes["Vector Math.009"].inputs[2]
    )
    # switch_005.Output -> store_named_attribute_004.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.005"].outputs[0],
        beamfollow_1.nodes["Store Named Attribute.004"].inputs[3]
    )
    # switch_009.Output -> sample_index_009.Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Switch.009"].outputs[0],
        beamfollow_1.nodes["Sample Index.009"].inputs[2]
    )
    # integer_math_025.Value -> switch_009.False
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.025"].outputs[0],
        beamfollow_1.nodes["Switch.009"].inputs[1]
    )
    # boolean_math_007.Boolean -> switch_009.Switch
    beamfollow_1.links.new(
        beamfollow_1.nodes["Boolean Math.007"].outputs[0],
        beamfollow_1.nodes["Switch.009"].inputs[0]
    )
    # vertex_of_corner_002.Vertex Index -> integer_math_024.Value
    beamfollow_1.links.new(
        beamfollow_1.nodes["Vertex of Corner.002"].outputs[0],
        beamfollow_1.nodes["Integer Math.024"].inputs[0]
    )
    # index_011.Index -> vertex_of_corner_002.Corner Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.011"].outputs[0],
        beamfollow_1.nodes["Vertex of Corner.002"].inputs[0]
    )
    # integer_math_017.Value -> index_switch_002.Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Integer Math.017"].outputs[0],
        beamfollow_1.nodes["Index Switch.002"].inputs[0]
    )
    # index_008.Index -> vertex_of_corner_003.Corner Index
    beamfollow_1.links.new(
        beamfollow_1.nodes["Index.008"].outputs[0],
        beamfollow_1.nodes["Vertex of Corner.003"].inputs[0]
    )
    # mesh_line.Mesh -> join_geometry_001.Geometry
    beamfollow_1.links.new(
        beamfollow_1.nodes["Mesh Line"].outputs[0],
        beamfollow_1.nodes["Join Geometry.001"].inputs[0]
    )

    return beamfollow_1

def cull_backface_1_node_group():
    """Initialize Cull Backface node group"""
    cull_backface_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Cull Backface")

    cull_backface_1.color_tag = 'SHADER'
    cull_backface_1.description = ""
    cull_backface_1.default_group_node_width = 140
    # cull_backface_1 interface

    # Socket Shader
    shader_socket = cull_backface_1.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket Shader
    shader_socket_1 = cull_backface_1.interface.new_socket(name="Shader", in_out='INPUT', socket_type='NodeSocketShader')
    shader_socket_1.attribute_domain = 'POINT'
    shader_socket_1.default_input = 'VALUE'
    shader_socket_1.structure_type = 'AUTO'

    # Initialize cull_backface_1 nodes

    # Node Geometry
    geometry = cull_backface_1.nodes.new("ShaderNodeNewGeometry")
    geometry.name = "Geometry"
    geometry.outputs[0].hide = True
    geometry.outputs[1].hide = True
    geometry.outputs[2].hide = True
    geometry.outputs[3].hide = True
    geometry.outputs[4].hide = True
    geometry.outputs[5].hide = True
    geometry.outputs[7].hide = True
    geometry.outputs[8].hide = True

    # Node Mix Shader
    mix_shader = cull_backface_1.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Transparent BSDF
    transparent_bsdf = cull_backface_1.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Group Output
    group_output = cull_backface_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Node Group Input
    group_input = cull_backface_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True

    # Set locations
    cull_backface_1.nodes["Geometry"].location = (-200.0, 60.0)
    cull_backface_1.nodes["Mix Shader"].location = (-40.0, 0.0)
    cull_backface_1.nodes["Transparent BSDF"].location = (-200.0, -60.0)
    cull_backface_1.nodes["Group Output"].location = (120.0, 0.0)
    cull_backface_1.nodes["Group Input"].location = (-200.0, 0.0)

    # Set dimensions
    cull_backface_1.nodes["Geometry"].width  = 140.0
    cull_backface_1.nodes["Geometry"].height = 100.0

    cull_backface_1.nodes["Mix Shader"].width  = 140.0
    cull_backface_1.nodes["Mix Shader"].height = 100.0

    cull_backface_1.nodes["Transparent BSDF"].width  = 140.0
    cull_backface_1.nodes["Transparent BSDF"].height = 100.0

    cull_backface_1.nodes["Group Output"].width  = 140.0
    cull_backface_1.nodes["Group Output"].height = 100.0

    cull_backface_1.nodes["Group Input"].width  = 140.0
    cull_backface_1.nodes["Group Input"].height = 100.0


    # Initialize cull_backface_1 links

    # geometry.Backfacing -> mix_shader.Factor
    cull_backface_1.links.new(
        cull_backface_1.nodes["Geometry"].outputs[6],
        cull_backface_1.nodes["Mix Shader"].inputs[0]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    cull_backface_1.links.new(
        cull_backface_1.nodes["Transparent BSDF"].outputs[0],
        cull_backface_1.nodes["Mix Shader"].inputs[2]
    )
    # mix_shader.Shader -> group_output.Shader
    cull_backface_1.links.new(
        cull_backface_1.nodes["Mix Shader"].outputs[0],
        cull_backface_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Shader -> mix_shader.Shader
    cull_backface_1.links.new(
        cull_backface_1.nodes["Group Input"].outputs[0],
        cull_backface_1.nodes["Mix Shader"].inputs[1]
    )

    return cull_backface_1

BUILDERS = {
    "Sprite Color": sprite_color_1_node_group,
    "Sprite Frame Offset": sprite_frame_offset_1_node_group,
    "Additive Shader": additive_shader_1_node_group,
    "Trans Alpha Shader": trans_alpha_shader_1_node_group,
    "Transparent Geometry": transparent_geometry_1_node_group,
    "BeamSegs": beamsegs_1_node_group,
    "Animated Texture": animated_texture_1_node_group,
    "Glow Sprite": glow_sprite_1_node_group,
    "FxBlend": fxblend_1_node_group,
    "GlowBlend": glowblend_1_node_group,
    "8-Value Maximum": _8_value_maximum_1_node_group,
    "Viewent Modifier": viewent_modifier_1_node_group,
    "ScreenTransform": screentransform_1_node_group,
    "Camera Basis": camera_basis_1_node_group,
    "Geometry Engine State": engine_state_1_node_group_geometry,
    "Shader Engine State": engine_state_1_node_group_shader,
    "VectorMA": vectorma_1_node_group,
    "BeamFollow": beamfollow_1_node_group,
    "Cull Backface": cull_backface_1_node_group,
}

def ensure_group(name: str):
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]

    builder = BUILDERS.get(name)
    if builder is None:
        raise Exception("Unknown node group!")

    return builder()

def new(nodes, name: str) -> bpy.types.ShaderNodeGroup:
    group = ensure_group(name)

    group_node = nodes.new("ShaderNodeGroup")
    group_node.node_tree = group

    return group_node

def create_compositing_nodes_old(view_layer, no_depth_view_layer):
    bpy.context.scene.compositing_node_group = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Compositing Nodetree")
    compositing_nodetree = bpy.context.scene.compositing_node_group

    # Start with a clean node tree
    for node in compositing_nodetree.nodes:
        compositing_nodetree.nodes.remove(node)
    compositing_nodetree.color_tag = 'NONE'
    compositing_nodetree.description = ""
    compositing_nodetree.default_group_node_width = 140
    # compositing_nodetree interface

    # Socket Image
    image_socket = compositing_nodetree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'

    # Socket Image
    image_socket_1 = compositing_nodetree.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.default_input = 'VALUE'
    image_socket_1.structure_type = 'AUTO'

    # Initialize compositing_nodetree nodes

    # Node Render Layers
    render_layers = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers.name = "Render Layers"
    render_layers.layer = view_layer.name

    # Node Group Output
    group_output = compositing_nodetree.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Viewer
    viewer = compositing_nodetree.nodes.new("CompositorNodeViewer")
    viewer.name = "Viewer"
    viewer.ui_shortcut = 0

    # Node Render Layers.001
    render_layers_001 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_001.name = "Render Layers.001"
    render_layers_001.layer = no_depth_view_layer.name

    # Node Math
    math = compositing_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0

    # Node Cryptomatte
    cryptomatte = compositing_nodetree.nodes.new("CompositorNodeCryptomatteV2")
    cryptomatte.name = "Cryptomatte"
    cryptomatte.add = mathutils.Color((0.0, 0.0, 0.0))
    cryptomatte.frame_duration = 0
    cryptomatte.frame_offset = 0
    cryptomatte.frame_start = 0
    cryptomatte.layer_name = 'ViewLayer.CryptoAsset'
    cryptomatte.matte_id = "viewent"
    cryptomatte.remove = mathutils.Color((0.0, 0.0, 0.0))
    cryptomatte.source = 'RENDER'
    cryptomatte.use_auto_refresh = False
    cryptomatte.use_cyclic = False
    # Image
    cryptomatte.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix
    mix = compositing_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'ADD'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'

    # Set locations
    compositing_nodetree.nodes["Render Layers"].location = (-180.0, 120.0)
    compositing_nodetree.nodes["Group Output"].location = (400.0, 260.0)
    compositing_nodetree.nodes["Viewer"].location = (400.0, 320.0)
    compositing_nodetree.nodes["Render Layers.001"].location = (-180.0, -240.0)
    compositing_nodetree.nodes["Math"].location = (80.0, 260.0)
    compositing_nodetree.nodes["Cryptomatte"].location = (-180.0, 500.0)
    compositing_nodetree.nodes["Mix"].location = (240.0, 260.0)

    # Set dimensions
    compositing_nodetree.nodes["Render Layers"].width  = 240.0
    compositing_nodetree.nodes["Render Layers"].height = 100.0

    compositing_nodetree.nodes["Group Output"].width  = 140.0
    compositing_nodetree.nodes["Group Output"].height = 100.0

    compositing_nodetree.nodes["Viewer"].width  = 140.0
    compositing_nodetree.nodes["Viewer"].height = 100.0

    compositing_nodetree.nodes["Render Layers.001"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.001"].height = 100.0

    compositing_nodetree.nodes["Math"].width  = 140.0
    compositing_nodetree.nodes["Math"].height = 100.0

    compositing_nodetree.nodes["Cryptomatte"].width  = 240.0
    compositing_nodetree.nodes["Cryptomatte"].height = 100.0

    compositing_nodetree.nodes["Mix"].width  = 140.0
    compositing_nodetree.nodes["Mix"].height = 100.0


    # Initialize compositing_nodetree links

    # cryptomatte.Matte -> math.Value
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Cryptomatte"].outputs[1],
        compositing_nodetree.nodes["Math"].inputs[1]
    )
    # render_layers.Image -> mix.A
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[6]
    )
    # render_layers_001.Image -> mix.B
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.001"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[7]
    )
    # mix.Result -> viewer.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Mix"].outputs[2],
        compositing_nodetree.nodes["Viewer"].inputs[0]
    )
    # math.Value -> mix.Factor
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Math"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[0]
    )
    # mix.Result -> group_output.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Mix"].outputs[2],
        compositing_nodetree.nodes["Group Output"].inputs[0]
    )

    return compositing_nodetree

def create_compositing_nodes_new_but_old(view_layer, no_depth_view_layer, viewent_view_layer):
    bpy.context.scene.compositing_node_group = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Compositing Nodetree")
    compositing_nodetree = bpy.context.scene.compositing_node_group

    # Start with a clean node tree
    for node in compositing_nodetree.nodes:
        compositing_nodetree.nodes.remove(node)
    compositing_nodetree.color_tag = 'NONE'
    compositing_nodetree.description = ""
    compositing_nodetree.default_group_node_width = 140
    # compositing_nodetree interface

    # Socket Image
    image_socket = compositing_nodetree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'

    # Socket Image
    image_socket_1 = compositing_nodetree.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.default_input = 'VALUE'
    image_socket_1.structure_type = 'AUTO'

    # Initialize compositing_nodetree nodes

    # Node Render Layers
    render_layers = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers.name = "Render Layers"
    render_layers.layer = view_layer.name

    # Node Group Output
    group_output = compositing_nodetree.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Viewer
    viewer = compositing_nodetree.nodes.new("CompositorNodeViewer")
    viewer.name = "Viewer"
    viewer.ui_shortcut = 0

    # Node Render Layers.001
    render_layers_001 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_001.name = "Render Layers.001"
    render_layers_001.layer = no_depth_view_layer.name

    # Node Math
    math = compositing_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0

    # Node Cryptomatte
    cryptomatte = compositing_nodetree.nodes.new("CompositorNodeCryptomatteV2")
    cryptomatte.name = "Cryptomatte"
    cryptomatte.add = mathutils.Color((0.0, 0.0, 0.0))
    cryptomatte.frame_duration = 0
    cryptomatte.frame_offset = 0
    cryptomatte.frame_start = 0
    cryptomatte.layer_name = 'ViewLayer.CryptoAsset'
    cryptomatte.matte_id = "viewent"
    cryptomatte.remove = mathutils.Color((0.0, 0.0, 0.0))
    cryptomatte.source = 'RENDER'
    cryptomatte.use_auto_refresh = False
    cryptomatte.use_cyclic = False
    # Image
    cryptomatte.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix
    mix = compositing_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'ADD'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'

    # Node Render Layers.002
    render_layers_002 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_002.name = "Render Layers.002"
    render_layers_002.layer = viewent_view_layer.name

    # Node Reroute
    reroute = compositing_nodetree.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketColor"
    # Node Alpha Over
    alpha_over = compositing_nodetree.nodes.new("CompositorNodeAlphaOver")
    alpha_over.name = "Alpha Over"
    # Fac
    alpha_over.inputs[2].default_value = 1.0
    # Type
    alpha_over.inputs[3].default_value = 'Over'
    # Straight Alpha
    alpha_over.inputs[4].default_value = False

    # Node Set Alpha
    set_alpha = compositing_nodetree.nodes.new("CompositorNodeSetAlpha")
    set_alpha.name = "Set Alpha"
    # Type
    set_alpha.inputs[2].default_value = 'Apply Mask'

    # Node Frame
    frame = compositing_nodetree.nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Set parents
    compositing_nodetree.nodes["Group Output"].parent = compositing_nodetree.nodes["Frame"]
    compositing_nodetree.nodes["Viewer"].parent = compositing_nodetree.nodes["Frame"]
    compositing_nodetree.nodes["Reroute"].parent = compositing_nodetree.nodes["Frame"]

    # Set locations
    compositing_nodetree.nodes["Render Layers"].location = (-220.0, 120.0)
    compositing_nodetree.nodes["Group Output"].location = (55.0, -90.0)
    compositing_nodetree.nodes["Viewer"].location = (55.0, -30.0)
    compositing_nodetree.nodes["Render Layers.001"].location = (-220.0, -260.0)
    compositing_nodetree.nodes["Math"].location = (200.0, 260.0)
    compositing_nodetree.nodes["Cryptomatte"].location = (-220.0, 360.0)
    compositing_nodetree.nodes["Mix"].location = (360.0, 120.0)
    compositing_nodetree.nodes["Render Layers.002"].location = (-220.0, -100.0)
    compositing_nodetree.nodes["Reroute"].location = (35.0, -90.0)
    compositing_nodetree.nodes["Alpha Over"].location = (200.0, 100.0)
    compositing_nodetree.nodes["Set Alpha"].location = (40.0, 40.0)
    compositing_nodetree.nodes["Frame"].location = (525.0, 150.0)

    # Set dimensions
    compositing_nodetree.nodes["Render Layers"].width  = 240.0
    compositing_nodetree.nodes["Render Layers"].height = 100.0

    compositing_nodetree.nodes["Group Output"].width  = 140.0
    compositing_nodetree.nodes["Group Output"].height = 100.0

    compositing_nodetree.nodes["Viewer"].width  = 140.0
    compositing_nodetree.nodes["Viewer"].height = 100.0

    compositing_nodetree.nodes["Render Layers.001"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.001"].height = 100.0

    compositing_nodetree.nodes["Math"].width  = 140.0
    compositing_nodetree.nodes["Math"].height = 100.0

    compositing_nodetree.nodes["Cryptomatte"].width  = 240.0
    compositing_nodetree.nodes["Cryptomatte"].height = 100.0

    compositing_nodetree.nodes["Mix"].width  = 140.0
    compositing_nodetree.nodes["Mix"].height = 100.0

    compositing_nodetree.nodes["Render Layers.002"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.002"].height = 100.0

    compositing_nodetree.nodes["Reroute"].width  = 10.0
    compositing_nodetree.nodes["Reroute"].height = 100.0

    compositing_nodetree.nodes["Alpha Over"].width  = 140.0
    compositing_nodetree.nodes["Alpha Over"].height = 100.0

    compositing_nodetree.nodes["Set Alpha"].width  = 140.0
    compositing_nodetree.nodes["Set Alpha"].height = 100.0

    compositing_nodetree.nodes["Frame"].width  = 225.0
    compositing_nodetree.nodes["Frame"].height = 192.0


    # Initialize compositing_nodetree links

    # cryptomatte.Matte -> math.Value
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Cryptomatte"].outputs[1],
        compositing_nodetree.nodes["Math"].inputs[1]
    )
    # alpha_over.Image -> mix.A
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Alpha Over"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[6]
    )
    # render_layers_001.Image -> mix.B
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.001"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[7]
    )
    # math.Value -> mix.Factor
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Math"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[0]
    )
    # reroute.Output -> group_output.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Reroute"].outputs[0],
        compositing_nodetree.nodes["Group Output"].inputs[0]
    )
    # reroute.Output -> viewer.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Reroute"].outputs[0],
        compositing_nodetree.nodes["Viewer"].inputs[0]
    )
    # mix.Result -> reroute.Input
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Mix"].outputs[2],
        compositing_nodetree.nodes["Reroute"].inputs[0]
    )
    # render_layers.Image -> alpha_over.Background
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[0]
    )
    # render_layers_002.Image -> set_alpha.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.002"].outputs[0],
        compositing_nodetree.nodes["Set Alpha"].inputs[0]
    )
    # set_alpha.Image -> alpha_over.Foreground
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Set Alpha"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[1]
    )
    # cryptomatte.Matte -> set_alpha.Alpha
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Cryptomatte"].outputs[1],
        compositing_nodetree.nodes["Set Alpha"].inputs[1]
    )

    return compositing_nodetree

def create_compositing_nodes(default_view_layer, no_depth_view_layer, viewent_view_layer):
    bpy.context.scene.compositing_node_group = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Compositing Nodetree")
    compositing_nodetree = bpy.context.scene.compositing_node_group

    # Start with a clean node tree
    for node in compositing_nodetree.nodes:
        compositing_nodetree.nodes.remove(node)
    compositing_nodetree.color_tag = 'NONE'
    compositing_nodetree.description = ""
    compositing_nodetree.default_group_node_width = 140
    # compositing_nodetree interface

    # Socket Image
    image_socket = compositing_nodetree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'

    # Socket Image
    image_socket_1 = compositing_nodetree.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.default_input = 'VALUE'
    image_socket_1.structure_type = 'AUTO'

    # Initialize compositing_nodetree nodes

    # Node Render Layers
    render_layers = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers.name = "Render Layers"
    render_layers.layer = default_view_layer.name

    # Node Group Output
    group_output = compositing_nodetree.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Viewer
    viewer = compositing_nodetree.nodes.new("CompositorNodeViewer")
    viewer.name = "Viewer"
    viewer.ui_shortcut = 0

    # Node Render Layers.001
    render_layers_001 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_001.name = "Render Layers.001"
    render_layers_001.layer = no_depth_view_layer.name

    # Node Mix
    mix = compositing_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'ADD'
    mix.clamp_factor = False
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Render Layers.002
    render_layers_002 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_002.name = "Render Layers.002"
    render_layers_002.layer = viewent_view_layer.name

    # Node Reroute
    reroute = compositing_nodetree.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketColor"
    # Node Alpha Over
    alpha_over = compositing_nodetree.nodes.new("CompositorNodeAlphaOver")
    alpha_over.name = "Alpha Over"
    # Fac
    alpha_over.inputs[2].default_value = 1.0
    # Type
    alpha_over.inputs[3].default_value = 'Over'
    # Straight Alpha
    alpha_over.inputs[4].default_value = False

    # Node Frame
    frame = compositing_nodetree.nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Set parents
    compositing_nodetree.nodes["Group Output"].parent = compositing_nodetree.nodes["Frame"]
    compositing_nodetree.nodes["Viewer"].parent = compositing_nodetree.nodes["Frame"]
    compositing_nodetree.nodes["Reroute"].parent = compositing_nodetree.nodes["Frame"]

    # Set locations
    compositing_nodetree.nodes["Render Layers"].location = (-220.0, 180.0)
    compositing_nodetree.nodes["Group Output"].location = (55.0, -90.0)
    compositing_nodetree.nodes["Viewer"].location = (55.0, -30.0)
    compositing_nodetree.nodes["Render Layers.001"].location = (-220.0, 20.0)
    compositing_nodetree.nodes["Mix"].location = (40.0, 180.0)
    compositing_nodetree.nodes["Render Layers.002"].location = (-220.0, -140.0)
    compositing_nodetree.nodes["Reroute"].location = (35.0, -90.0)
    compositing_nodetree.nodes["Alpha Over"].location = (200.0, 20.0)
    compositing_nodetree.nodes["Frame"].location = (365.0, 50.0)

    # Set dimensions
    compositing_nodetree.nodes["Render Layers"].width  = 240.0
    compositing_nodetree.nodes["Render Layers"].height = 100.0

    compositing_nodetree.nodes["Group Output"].width  = 140.0
    compositing_nodetree.nodes["Group Output"].height = 100.0

    compositing_nodetree.nodes["Viewer"].width  = 140.0
    compositing_nodetree.nodes["Viewer"].height = 100.0

    compositing_nodetree.nodes["Render Layers.001"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.001"].height = 100.0

    compositing_nodetree.nodes["Mix"].width  = 140.0
    compositing_nodetree.nodes["Mix"].height = 100.0

    compositing_nodetree.nodes["Render Layers.002"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.002"].height = 100.0

    compositing_nodetree.nodes["Reroute"].width  = 10.0
    compositing_nodetree.nodes["Reroute"].height = 100.0

    compositing_nodetree.nodes["Alpha Over"].width  = 140.0
    compositing_nodetree.nodes["Alpha Over"].height = 100.0

    compositing_nodetree.nodes["Frame"].width  = 225.0
    compositing_nodetree.nodes["Frame"].height = 192.0


    # Initialize compositing_nodetree links

    # render_layers_001.Image -> mix.B
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.001"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[7]
    )
    # reroute.Output -> group_output.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Reroute"].outputs[0],
        compositing_nodetree.nodes["Group Output"].inputs[0]
    )
    # reroute.Output -> viewer.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Reroute"].outputs[0],
        compositing_nodetree.nodes["Viewer"].inputs[0]
    )
    # render_layers_002.Image -> alpha_over.Foreground
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.002"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[1]
    )
    # render_layers.Image -> mix.A
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers"].outputs[0],
        compositing_nodetree.nodes["Mix"].inputs[6]
    )
    # mix.Result -> alpha_over.Background
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Mix"].outputs[2],
        compositing_nodetree.nodes["Alpha Over"].inputs[0]
    )
    # alpha_over.Image -> reroute.Input
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Alpha Over"].outputs[0],
        compositing_nodetree.nodes["Reroute"].inputs[0]
    )

    return compositing_nodetree

# R_DrawSpriteModel and some context in R_DrawTEntitiesOnList
def setup_sprite_nodes(shader_nodetree, image, frame_count):
    """Initialize Shader Nodetree node group"""
    # Node Group
    group = shader_nodetree.nodes.new("ShaderNodeGroup")
    group.name = "Group"
    group.node_tree = ensure_group("Sprite Color")

    # Node Group.001
    group_001 = shader_nodetree.nodes.new("ShaderNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = ensure_group("Sprite Frame Offset")
    # Socket_1
    group_001.inputs[0].default_value = frame_count

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'CLIP'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Attribute.002
    attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "rendermode"
    attribute_002.attribute_type = 'OBJECT'

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.label = "GL_MODULATE"
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Material Output.001
    material_output_001 = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output_001.name = "Material Output.001"
    material_output_001.is_active_output = True
    material_output_001.target = 'ALL'
    # Displacement
    material_output_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output_001.inputs[3].default_value = 0.0

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.label = "Is TextureColor"
    math.name = "Math"
    math.operation = 'COMPARE'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 1.0
    # Value_002
    math.inputs[2].default_value = 0.0

    # Node Math.005
    math_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'SUBTRACT'
    math_005.use_clamp = False
    # Value
    math_005.inputs[0].default_value = 1.0

    # Node Math.006
    math_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_006.label = "GL_MOD alpha"
    math_006.name = "Math.006"
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.label = "GL_BLEND"
    mix_shader.name = "Mix Shader"

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.label = "Is Glow"
    math_007.name = "Math.007"
    math_007.operation = 'COMPARE'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = 3.0
    # Value_002
    math_007.inputs[2].default_value = 0.0

    # Node Mix Shader.001
    mix_shader_001 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_001.label = "Nothing?"
    mix_shader_001.name = "Mix Shader.001"

    # Node Transparent BSDF.003
    transparent_bsdf_003 = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf_003.name = "Transparent BSDF.003"
    # Color
    transparent_bsdf_003.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Math.008
    math_008 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_008.label = "Is Additive"
    math_008.name = "Math.008"
    math_008.operation = 'COMPARE'
    math_008.use_clamp = False
    # Value_001
    math_008.inputs[1].default_value = 5.0
    # Value_002
    math_008.inputs[2].default_value = 0.0

    # Node Add Shader
    add_shader = shader_nodetree.nodes.new("ShaderNodeAddShader")
    add_shader.label = "Additive Rendering"
    add_shader.name = "Add Shader"

    # Node Mix Shader.006
    mix_shader_006 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_006.label = "Additive?"
    mix_shader_006.name = "Mix Shader.006"

    # Node Attribute.004
    attribute_004 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_004.name = "Attribute.004"
    attribute_004.attribute_name = "draw_no_depth"
    attribute_004.attribute_type = 'VIEW_LAYER'

    # Node Math.009
    math_009 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_009.label = "Is no_depth"
    math_009.name = "Math.009"
    math_009.operation = 'COMPARE'
    math_009.use_clamp = False
    # Value_001
    math_009.inputs[1].default_value = 1.0
    # Value_002
    math_009.inputs[2].default_value = 0.0

    # Node Mix Shader.007
    mix_shader_007 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_007.label = "no_depth?"
    mix_shader_007.name = "Mix Shader.007"

    # Node Mix Shader.008
    mix_shader_008 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_008.label = "Glow"
    mix_shader_008.name = "Mix Shader.008"

    # Node Diffuse BSDF
    diffuse_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_bsdf.name = "Diffuse BSDF"
    # Roughness
    diffuse_bsdf.inputs[1].default_value = 0.0
    # Normal
    diffuse_bsdf.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Group.002
    group_002 = shader_nodetree.nodes.new("ShaderNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = ensure_group("FxBlend")

    # Node Math.010
    math_010 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_010.label = "Is Glow"
    math_010.name = "Math.010"
    math_010.operation = 'COMPARE'
    math_010.use_clamp = False
    # Value_001
    math_010.inputs[1].default_value = 3.0
    # Value_002
    math_010.inputs[2].default_value = 0.0

    # Node Math.002
    math_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'DIVIDE'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 255.0

    # Node Math.003
    math_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 255.0

    # Node Group.003
    group_003 = shader_nodetree.nodes.new("ShaderNodeGroup")
    group_003.name = "Group.003"
    group_003.node_tree = ensure_group("GlowBlend")

    # Node Mix.001
    mix_001 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = False
    mix_001.clamp_result = False
    mix_001.data_type = 'FLOAT'
    mix_001.factor_mode = 'UNIFORM'

    # Set locations
    shader_nodetree.nodes["Group"].location = (-20.0, -1100.0)
    shader_nodetree.nodes["Group.001"].location = (-340.0, -1340.0)
    shader_nodetree.nodes["Image Texture"].location = (-180.0, -1280.0)
    shader_nodetree.nodes["Attribute.002"].location = (-660.0, -800.0)
    shader_nodetree.nodes["Mix"].location = (140.0, -940.0)
    shader_nodetree.nodes["Emission"].location = (460.0, -940.0)
    shader_nodetree.nodes["Material Output.001"].location = (1740.0, -940.0)
    shader_nodetree.nodes["Math"].location = (-180.0, -940.0)
    shader_nodetree.nodes["Math.005"].location = (-20.0, -940.0)
    shader_nodetree.nodes["Math.006"].location = (300.0, -1180.0)
    shader_nodetree.nodes["Mix Shader"].location = (460.0, -1060.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (300.0, -1080.0)
    shader_nodetree.nodes["Math.007"].location = (620.0, -760.0)
    shader_nodetree.nodes["Mix Shader.001"].location = (780.0, -940.0)
    shader_nodetree.nodes["Transparent BSDF.003"].location = (460.0, -1200.0)
    shader_nodetree.nodes["Math.008"].location = (940.0, -760.0)
    shader_nodetree.nodes["Add Shader"].location = (780.0, -1080.0)
    shader_nodetree.nodes["Mix Shader.006"].location = (1100.0, -940.0)
    shader_nodetree.nodes["Attribute.004"].location = (1260.0, -760.0)
    shader_nodetree.nodes["Math.009"].location = (1420.0, -760.0)
    shader_nodetree.nodes["Mix Shader.007"].location = (1580.0, -940.0)
    shader_nodetree.nodes["Mix Shader.008"].location = (1100.0, -1080.0)
    shader_nodetree.nodes["Diffuse BSDF"].location = (300.0, -940.0)
    shader_nodetree.nodes["Group.002"].location = (-660.0, -1180.0)
    shader_nodetree.nodes["Math.010"].location = (-500.0, -1000.0)
    shader_nodetree.nodes["Math.002"].location = (-500.0, -1180.0)
    shader_nodetree.nodes["Math.003"].location = (-180.0, -1120.0)
    shader_nodetree.nodes["Group.003"].location = (-500.0, -1340.0)
    shader_nodetree.nodes["Mix.001"].location = (-340.0, -1120.0)

    # Set dimensions
    shader_nodetree.nodes["Group"].width  = 140.0
    shader_nodetree.nodes["Group"].height = 100.0

    shader_nodetree.nodes["Group.001"].width  = 140.0
    shader_nodetree.nodes["Group.001"].height = 100.0

    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Attribute.002"].width  = 140.0
    shader_nodetree.nodes["Attribute.002"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Material Output.001"].width  = 140.0
    shader_nodetree.nodes["Material Output.001"].height = 100.0

    shader_nodetree.nodes["Math"].width  = 140.0
    shader_nodetree.nodes["Math"].height = 100.0

    shader_nodetree.nodes["Math.005"].width  = 140.0
    shader_nodetree.nodes["Math.005"].height = 100.0

    shader_nodetree.nodes["Math.006"].width  = 140.0
    shader_nodetree.nodes["Math.006"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Math.007"].width  = 140.0
    shader_nodetree.nodes["Math.007"].height = 100.0

    shader_nodetree.nodes["Mix Shader.001"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.001"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF.003"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF.003"].height = 100.0

    shader_nodetree.nodes["Math.008"].width  = 140.0
    shader_nodetree.nodes["Math.008"].height = 100.0

    shader_nodetree.nodes["Add Shader"].width  = 140.0
    shader_nodetree.nodes["Add Shader"].height = 100.0

    shader_nodetree.nodes["Mix Shader.006"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.006"].height = 100.0

    shader_nodetree.nodes["Attribute.004"].width  = 140.0
    shader_nodetree.nodes["Attribute.004"].height = 100.0

    shader_nodetree.nodes["Math.009"].width  = 140.0
    shader_nodetree.nodes["Math.009"].height = 100.0

    shader_nodetree.nodes["Mix Shader.007"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.007"].height = 100.0

    shader_nodetree.nodes["Mix Shader.008"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.008"].height = 100.0

    shader_nodetree.nodes["Diffuse BSDF"].width  = 140.0
    shader_nodetree.nodes["Diffuse BSDF"].height = 100.0

    shader_nodetree.nodes["Group.002"].width  = 140.0
    shader_nodetree.nodes["Group.002"].height = 100.0

    shader_nodetree.nodes["Math.010"].width  = 140.0
    shader_nodetree.nodes["Math.010"].height = 100.0

    shader_nodetree.nodes["Math.002"].width  = 140.0
    shader_nodetree.nodes["Math.002"].height = 100.0

    shader_nodetree.nodes["Math.003"].width  = 140.0
    shader_nodetree.nodes["Math.003"].height = 100.0

    shader_nodetree.nodes["Group.003"].width  = 140.0
    shader_nodetree.nodes["Group.003"].height = 100.0

    shader_nodetree.nodes["Mix.001"].width  = 140.0
    shader_nodetree.nodes["Mix.001"].height = 100.0


    # Initialize shader_nodetree links

    # group_001.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group.001"].outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # attribute_002.Factor -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math"].inputs[0]
    )
    # image_texture.Color -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # group.Result -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # math.Value -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math"].outputs[0],
        shader_nodetree.nodes["Math.005"].inputs[1]
    )
    # image_texture.Alpha -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[1],
        shader_nodetree.nodes["Math.006"].inputs[0]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # math_006.Value -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # attribute_002.Factor -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.007"].inputs[0]
    )
    # math_007.Value -> mix_shader_001.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[0]
    )
    # attribute_002.Factor -> math_008.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.008"].inputs[0]
    )
    # emission.Emission -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[0]
    )
    # transparent_bsdf_003.BSDF -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF.003"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[1]
    )
    # math_008.Value -> mix_shader_006.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.008"].outputs[0],
        shader_nodetree.nodes["Mix Shader.006"].inputs[0]
    )
    # add_shader.Shader -> mix_shader_006.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Add Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.006"].inputs[2]
    )
    # mix_shader_001.Shader -> mix_shader_006.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.001"].outputs[0],
        shader_nodetree.nodes["Mix Shader.006"].inputs[1]
    )
    # attribute_004.Factor -> math_009.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.004"].outputs[2],
        shader_nodetree.nodes["Math.009"].inputs[0]
    )
    # mix_shader_006.Shader -> mix_shader_007.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.006"].outputs[0],
        shader_nodetree.nodes["Mix Shader.007"].inputs[1]
    )
    # mix_shader_008.Shader -> mix_shader_007.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.008"].outputs[0],
        shader_nodetree.nodes["Mix Shader.007"].inputs[2]
    )
    # math_007.Value -> mix_shader_008.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["Mix Shader.008"].inputs[0]
    )
    # add_shader.Shader -> mix_shader_008.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Add Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.008"].inputs[2]
    )
    # transparent_bsdf_003.BSDF -> mix_shader_008.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF.003"].outputs[0],
        shader_nodetree.nodes["Mix Shader.008"].inputs[1]
    )
    # mix.Result -> diffuse_bsdf.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Diffuse BSDF"].inputs[0]
    )
    # diffuse_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Diffuse BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # mix.Result -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # mix_shader.Shader -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[1]
    )
    # transparent_bsdf_003.BSDF -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF.003"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[2]
    )
    # mix_shader_007.Shader -> material_output_001.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.007"].outputs[0],
        shader_nodetree.nodes["Material Output.001"].inputs[0]
    )
    # math_005.Value -> mix.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.005"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[0]
    )
    # math_003.Value -> group.Blend
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.003"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[0]
    )
    # attribute_002.Factor -> math_010.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.010"].inputs[0]
    )
    # group_002.Value -> math_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group.002"].outputs[0],
        shader_nodetree.nodes["Math.002"].inputs[0]
    )
    # math_010.Value -> mix_001.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.010"].outputs[0],
        shader_nodetree.nodes["Mix.001"].inputs[0]
    )
    # mix_001.Result -> math_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.001"].outputs[0],
        shader_nodetree.nodes["Math.003"].inputs[0]
    )
    # mix_001.Result -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.001"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[1]
    )
    # math_002.Value -> mix_001.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.002"].outputs[0],
        shader_nodetree.nodes["Mix.001"].inputs[2]
    )
    # group_003.Value -> mix_001.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group.003"].outputs[0],
        shader_nodetree.nodes["Mix.001"].inputs[3]
    )
    # math_009.Value -> mix_shader_007.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.009"].outputs[0],
        shader_nodetree.nodes["Mix Shader.007"].inputs[0]
    )

    return shader_nodetree

def setup_beam_nodes(shader_nodetree, image, frame_count):
    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Group
    sprite_frame_offset = new(shader_nodetree.nodes, "Sprite Frame Offset")
    sprite_frame_offset.inputs[0].default_value = frame_count

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 5.0

    # Node Attribute
    attribute = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "color"
    attribute.attribute_type = 'OBJECT'

    # Node Gamma
    gamma = shader_nodetree.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Add Shader
    add_shader = shader_nodetree.nodes.new("ShaderNodeAddShader")
    add_shader.name = "Add Shader"

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Attribute.001
    attribute_001 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_001.name = "Attribute.001"
    attribute_001.attribute_name = "brightness"
    attribute_001.attribute_type = 'OBJECT'

    # Set locations
    shader_nodetree.nodes["Image Texture"].location = (0.0, 0.0)
    sprite_frame_offset.location = (-160.0, -140.0)
    shader_nodetree.nodes["Material Output"].location = (960.0, 180.0)
    shader_nodetree.nodes["Emission"].location = (480.0, 180.0)
    shader_nodetree.nodes["Attribute"].location = (0.0, 180.0)
    shader_nodetree.nodes["Gamma"].location = (160.0, 180.0)
    shader_nodetree.nodes["Mix"].location = (320.0, 180.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (480.0, 60.0)
    shader_nodetree.nodes["Add Shader"].location = (640.0, 180.0)
    shader_nodetree.nodes["Mix Shader"].location = (800.0, 180.0)
    shader_nodetree.nodes["Attribute.001"].location = (640.0, 360.0)

    # Set dimensions
    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    sprite_frame_offset.width  = 140.0
    sprite_frame_offset.height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Attribute"].width  = 140.0
    shader_nodetree.nodes["Attribute"].height = 100.0

    shader_nodetree.nodes["Gamma"].width  = 140.0
    shader_nodetree.nodes["Gamma"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Add Shader"].width  = 140.0
    shader_nodetree.nodes["Add Shader"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Attribute.001"].width  = 140.0
    shader_nodetree.nodes["Attribute.001"].height = 100.0


    # Initialize shader_nodetree links

    # group.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        sprite_frame_offset.outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # attribute.Color -> gamma.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute"].outputs[0],
        shader_nodetree.nodes["Gamma"].inputs[0]
    )
    # gamma.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Gamma"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # image_texture.Color -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # mix.Result -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # emission.Emission -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[0]
    )
    # transparent_bsdf.BSDF -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[1]
    )
    # mix_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # attribute_001.Factor -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.001"].outputs[2],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # add_shader.Shader -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Add Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )

def setup_beamfollow_nodes(shader_nodetree, image, frame_count):
    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Group
    group = shader_nodetree.nodes.new("ShaderNodeGroup")
    group.name = "Group"
    group.node_tree = ensure_group("Sprite Frame Offset")
    # Socket_1
    group.inputs[0].default_value = frame_count

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Attribute
    attribute = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "color"
    attribute.attribute_type = 'OBJECT'

    # Node Gamma
    gamma = shader_nodetree.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Add Shader
    add_shader = shader_nodetree.nodes.new("ShaderNodeAddShader")
    add_shader.name = "Add Shader"

    # Node Mix.001
    mix_001 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'MULTIPLY'
    mix_001.clamp_factor = False
    mix_001.clamp_result = False
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    # B_Color
    mix_001.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Attribute.002
    attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "brightness"
    attribute_002.attribute_type = 'GEOMETRY'

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0

    # Set locations
    shader_nodetree.nodes["Image Texture"].location = (0.0, 0.0)
    shader_nodetree.nodes["Group"].location = (-160.0, -140.0)
    shader_nodetree.nodes["Material Output"].location = (960.0, 180.0)
    shader_nodetree.nodes["Emission"].location = (640.0, 180.0)
    shader_nodetree.nodes["Attribute"].location = (0.0, 180.0)
    shader_nodetree.nodes["Gamma"].location = (160.0, 180.0)
    shader_nodetree.nodes["Mix"].location = (320.0, 180.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (640.0, 60.0)
    shader_nodetree.nodes["Add Shader"].location = (800.0, 180.0)
    shader_nodetree.nodes["Mix.001"].location = (480.0, 180.0)
    shader_nodetree.nodes["Attribute.002"].location = (160.0, 360.0)
    shader_nodetree.nodes["Math"].location = (320.0, 360.0)

    # Set dimensions
    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Group"].width  = 140.0
    shader_nodetree.nodes["Group"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Attribute"].width  = 140.0
    shader_nodetree.nodes["Attribute"].height = 100.0

    shader_nodetree.nodes["Gamma"].width  = 140.0
    shader_nodetree.nodes["Gamma"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Add Shader"].width  = 140.0
    shader_nodetree.nodes["Add Shader"].height = 100.0

    shader_nodetree.nodes["Mix.001"].width  = 140.0
    shader_nodetree.nodes["Mix.001"].height = 100.0

    shader_nodetree.nodes["Attribute.002"].width  = 140.0
    shader_nodetree.nodes["Attribute.002"].height = 100.0

    shader_nodetree.nodes["Math"].width  = 140.0
    shader_nodetree.nodes["Math"].height = 100.0


    # Initialize shader_nodetree links

    # attribute.Color -> gamma.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute"].outputs[0],
        shader_nodetree.nodes["Gamma"].inputs[0]
    )
    # gamma.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Gamma"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # image_texture.Color -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # emission.Emission -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[0]
    )
    # transparent_bsdf.BSDF -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[1]
    )
    # group.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group"].outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # mix.Result -> mix_001.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Mix.001"].inputs[6]
    )
    # mix_001.Result -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.001"].outputs[2],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # math.Value -> mix_001.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math"].outputs[0],
        shader_nodetree.nodes["Mix.001"].inputs[0]
    )
    # attribute_002.Factor -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math"].inputs[1]
    )
    # add_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Add Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

def setup_transparent_bsp_nodes(nodes, links, image):
    # Node Principled BSDF
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.0
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Geometry
    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.name = "Geometry"
    geometry.outputs[0].hide = True
    geometry.outputs[1].hide = True
    geometry.outputs[2].hide = True
    geometry.outputs[3].hide = True
    geometry.outputs[4].hide = True
    geometry.outputs[5].hide = True
    geometry.outputs[7].hide = True
    geometry.outputs[8].hide = True

    # Node Mix Shader
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Transparent BSDF
    transparent_bsdf = nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Set locations
    nodes["Principled BSDF"].location = (-360.0, 140.0)
    nodes["Material Output"].location = (240.0, 140.0)
    nodes["Image Texture"].location = (-620.0, 140.0)
    nodes["Geometry"].location = (-100.0, 180.0)
    nodes["Mix Shader"].location = (80.0, 140.0)
    nodes["Transparent BSDF"].location = (-100.0, 40.0)

    # Set dimensions
    nodes["Principled BSDF"].width  = 240.0
    nodes["Principled BSDF"].height = 100.0

    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    nodes["Geometry"].width  = 140.0
    nodes["Geometry"].height = 100.0

    nodes["Mix Shader"].width  = 140.0
    nodes["Mix Shader"].height = 100.0

    nodes["Transparent BSDF"].width  = 140.0
    nodes["Transparent BSDF"].height = 100.0


    # Initialize shader_nodetree links

    # mix_shader.Shader -> material_output.Surface
    links.new(
        nodes["Mix Shader"].outputs[0],
        nodes["Material Output"].inputs[0]
    )
    # image_texture.Color -> principled_bsdf.Base Color
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Principled BSDF"].inputs[0]
    )
    # geometry.Backfacing -> mix_shader.Factor
    links.new(
        nodes["Geometry"].outputs[6],
        nodes["Mix Shader"].inputs[0]
    )
    # image_texture.Alpha -> principled_bsdf.Alpha
    links.new(
        nodes["Image Texture"].outputs[1],
        nodes["Principled BSDF"].inputs[4]
    )
    # principled_bsdf.BSDF -> mix_shader.Shader
    links.new(
        nodes["Principled BSDF"].outputs[0],
        nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    links.new(
        nodes["Transparent BSDF"].outputs[0],
        nodes["Mix Shader"].inputs[2]
    )


def setup_bsp_nodes(shader_nodetree, image):
    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Group.001
    group_001 = shader_nodetree.nodes.new("ShaderNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = ensure_group("Cull Backface")

    # Node FxBlend
    fxblend = shader_nodetree.nodes.new("ShaderNodeGroup")
    fxblend.name = "FxBlend"
    fxblend.node_tree = ensure_group("FxBlend")

    # Node Math.002
    math_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'DIVIDE'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 255.0

    # Node Attribute.002
    attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "rendermode"
    attribute_002.attribute_type = 'OBJECT'

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'COMPARE'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 0.0
    # Value_002
    math.inputs[2].default_value = 0.0

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Math.001
    math_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False

    # Node Principled BSDF.001
    principled_bsdf_001 = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.name = "Principled BSDF.001"
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf_001.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf_001.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf_001.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf_001.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf_001.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf_001.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf_001.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf_001.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf_001.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf_001.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf_001.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf_001.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf_001.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf_001.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf_001.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf_001.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf_001.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf_001.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf_001.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf_001.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf_001.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf_001.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf_001.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf_001.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf_001.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf_001.inputs[30].default_value = 1.3300000429153442

    # Node Math.003
    math_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'COMPARE'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 1.0
    # Value_002
    math_003.inputs[2].default_value = 0.0

    # Node Math.004
    math_004 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'COMPARE'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 4.0
    # Value_002
    math_004.inputs[2].default_value = 0.0

    # Node Mix Shader.001
    mix_shader_001 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_001.name = "Mix Shader.001"

    # Node Mix Shader.002
    mix_shader_002 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_002.name = "Mix Shader.002"

    # Node Attribute.003
    attribute_003 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_003.name = "Attribute.003"
    attribute_003.attribute_name = "rendercolor"
    attribute_003.attribute_type = 'OBJECT'

    # Node Principled BSDF.002
    principled_bsdf_002 = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.name = "Principled BSDF.002"
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf_002.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf_002.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf_002.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf_002.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf_002.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf_002.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf_002.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf_002.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf_002.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf_002.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf_002.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf_002.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf_002.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf_002.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf_002.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf_002.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf_002.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf_002.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf_002.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf_002.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf_002.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf_002.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf_002.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf_002.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf_002.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf_002.inputs[30].default_value = 1.3300000429153442

    # Node Gamma
    gamma = shader_nodetree.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Node Principled BSDF.003
    principled_bsdf_003 = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_003.name = "Principled BSDF.003"
    principled_bsdf_003.distribution = 'MULTI_GGX'
    principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf_003.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf_003.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf_003.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf_003.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf_003.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf_003.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf_003.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf_003.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf_003.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf_003.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf_003.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf_003.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf_003.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf_003.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf_003.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf_003.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf_003.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf_003.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf_003.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf_003.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf_003.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf_003.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf_003.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf_003.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf_003.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf_003.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf_003.inputs[30].default_value = 1.3300000429153442

    # Node Math.005
    math_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'COMPARE'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = 0.0
    # Value_002
    math_005.inputs[2].default_value = 0.0

    # Node Math.006
    math_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'SUBTRACT'
    math_006.use_clamp = False
    # Value
    math_006.inputs[0].default_value = 1.0

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'COMPARE'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = 5.0
    # Value_002
    math_007.inputs[2].default_value = 0.0

    # Node Mix Shader.003
    mix_shader_003 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_003.name = "Mix Shader.003"

    # Node Add Shader
    add_shader = shader_nodetree.nodes.new("ShaderNodeAddShader")
    add_shader.name = "Add Shader"

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Principled BSDF.004
    principled_bsdf_004 = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_004.name = "Principled BSDF.004"
    principled_bsdf_004.distribution = 'MULTI_GGX'
    principled_bsdf_004.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf_004.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf_004.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf_004.inputs[3].default_value = 1.0
    # Alpha
    principled_bsdf_004.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf_004.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf_004.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf_004.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf_004.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf_004.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf_004.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf_004.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf_004.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf_004.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf_004.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf_004.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf_004.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf_004.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf_004.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf_004.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf_004.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf_004.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf_004.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf_004.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf_004.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf_004.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf_004.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf_004.inputs[30].default_value = 1.3300000429153442

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Frame
    frame = shader_nodetree.nodes.new("NodeFrame")
    frame.label = "kRenderNormal"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Node Frame.001
    frame_001 = shader_nodetree.nodes.new("NodeFrame")
    frame_001.label = "kRenderTransColor"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Frame.002
    frame_002 = shader_nodetree.nodes.new("NodeFrame")
    frame_002.label = "kRenderTransAlpha"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # Node Frame.003
    frame_003 = shader_nodetree.nodes.new("NodeFrame")
    frame_003.label = "kRenderTransAdd"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # Node Frame.004
    frame_004 = shader_nodetree.nodes.new("NodeFrame")
    frame_004.label = "r_blend"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # Node Frame.005
    frame_005 = shader_nodetree.nodes.new("NodeFrame")
    frame_005.label = "default"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    # Node Frame.006
    frame_006 = shader_nodetree.nodes.new("NodeFrame")
    frame_006.label = "R_SetRenderMode"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    # Node Reroute
    reroute = shader_nodetree.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketColor"
    # Node Reroute.001
    reroute_001 = shader_nodetree.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketColor"
    # Node Reroute.003
    reroute_003 = shader_nodetree.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketColor"
    # Node Reroute.004
    reroute_004 = shader_nodetree.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketColor"
    # Node Reroute.005
    reroute_005 = shader_nodetree.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.socket_idname = "NodeSocketColor"
    # Node Reroute.006
    reroute_006 = shader_nodetree.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.socket_idname = "NodeSocketColor"
    # Node Reroute.002
    reroute_002 = shader_nodetree.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketFloat"
    # Node Reroute.008
    reroute_008 = shader_nodetree.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketFloat"
    # Node Reroute.009
    reroute_009 = shader_nodetree.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketFloat"
    # Node Reroute.007
    reroute_007 = shader_nodetree.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.socket_idname = "NodeSocketFloat"
    # Node Reroute.010
    reroute_010 = shader_nodetree.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketFloat"
    # Node Reroute.011
    reroute_011 = shader_nodetree.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketFloat"
    # Node Reroute.012
    reroute_012 = shader_nodetree.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.socket_idname = "NodeSocketFloat"
    # Node Reroute.013
    reroute_013 = shader_nodetree.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.socket_idname = "NodeSocketFloat"
    # Node Reroute.014
    reroute_014 = shader_nodetree.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.socket_idname = "NodeSocketFloat"
    # Node Reroute.015
    reroute_015 = shader_nodetree.nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.socket_idname = "NodeSocketFloat"
    # Node Reroute.019
    reroute_019 = shader_nodetree.nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.socket_idname = "NodeSocketShader"
    # Node Reroute.020
    reroute_020 = shader_nodetree.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.socket_idname = "NodeSocketShader"
    # Node Reroute.021
    reroute_021 = shader_nodetree.nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    reroute_021.socket_idname = "NodeSocketShader"
    # Node Reroute.022
    reroute_022 = shader_nodetree.nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    reroute_022.socket_idname = "NodeSocketShader"
    # Node Reroute.023
    reroute_023 = shader_nodetree.nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    reroute_023.socket_idname = "NodeSocketShader"
    # Node Reroute.024
    reroute_024 = shader_nodetree.nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    reroute_024.socket_idname = "NodeSocketShader"
    # Set parents
    shader_nodetree.nodes["Principled BSDF"].parent = shader_nodetree.nodes["Frame.005"]
    shader_nodetree.nodes["FxBlend"].parent = shader_nodetree.nodes["Frame.004"]
    shader_nodetree.nodes["Math.002"].parent = shader_nodetree.nodes["Frame.004"]
    shader_nodetree.nodes["Attribute.002"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Math"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Mix Shader"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Math.001"].parent = shader_nodetree.nodes["Frame.005"]
    shader_nodetree.nodes["Principled BSDF.001"].parent = shader_nodetree.nodes["Frame"]
    shader_nodetree.nodes["Math.003"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Math.004"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Mix Shader.001"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Mix Shader.002"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Attribute.003"].parent = shader_nodetree.nodes["Frame.001"]
    shader_nodetree.nodes["Principled BSDF.002"].parent = shader_nodetree.nodes["Frame.001"]
    shader_nodetree.nodes["Gamma"].parent = shader_nodetree.nodes["Frame.001"]
    shader_nodetree.nodes["Principled BSDF.003"].parent = shader_nodetree.nodes["Frame.002"]
    shader_nodetree.nodes["Math.005"].parent = shader_nodetree.nodes["Frame.002"]
    shader_nodetree.nodes["Math.006"].parent = shader_nodetree.nodes["Frame.002"]
    shader_nodetree.nodes["Math.007"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Mix Shader.003"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Add Shader"].parent = shader_nodetree.nodes["Frame.003"]
    shader_nodetree.nodes["Transparent BSDF"].parent = shader_nodetree.nodes["Frame.003"]
    shader_nodetree.nodes["Principled BSDF.004"].parent = shader_nodetree.nodes["Frame.003"]
    shader_nodetree.nodes["Mix"].parent = shader_nodetree.nodes["Frame.003"]
    shader_nodetree.nodes["Frame"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Frame.001"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Frame.002"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Frame.003"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Frame.005"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.001"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.003"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.004"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.005"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.006"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.002"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.008"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.009"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.007"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.010"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.011"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.012"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.013"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.014"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.015"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.019"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.020"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.021"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.022"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.023"].parent = shader_nodetree.nodes["Frame.006"]
    shader_nodetree.nodes["Reroute.024"].parent = shader_nodetree.nodes["Frame.006"]

    # Set locations
    shader_nodetree.nodes["Image Texture"].location = (0.0, 0.0)
    shader_nodetree.nodes["Principled BSDF"].location = (190.0, -36.0)
    shader_nodetree.nodes["Material Output"].location = (3380.0, 0.0)
    shader_nodetree.nodes["Group.001"].location = (3220.0, 0.0)
    shader_nodetree.nodes["FxBlend"].location = (30.0, -36.0)
    shader_nodetree.nodes["Math.002"].location = (190.0, -36.0)
    shader_nodetree.nodes["Attribute.002"].location = (75.0, -36.0)
    shader_nodetree.nodes["Math"].location = (675.0, -36.0)
    shader_nodetree.nodes["Mix Shader"].location = (835.0, -36.0)
    shader_nodetree.nodes["Math.001"].location = (30.0, -36.0)
    shader_nodetree.nodes["Principled BSDF.001"].location = (30.0, -36.0)
    shader_nodetree.nodes["Math.003"].location = (1315.0, -36.0)
    shader_nodetree.nodes["Math.004"].location = (1955.0, -36.0)
    shader_nodetree.nodes["Mix Shader.001"].location = (1475.0, -36.0)
    shader_nodetree.nodes["Mix Shader.002"].location = (2115.0, -36.0)
    shader_nodetree.nodes["Attribute.003"].location = (30.0, -36.0)
    shader_nodetree.nodes["Principled BSDF.002"].location = (350.0, -36.0)
    shader_nodetree.nodes["Gamma"].location = (190.0, -36.0)
    shader_nodetree.nodes["Principled BSDF.003"].location = (350.0, -36.0)
    shader_nodetree.nodes["Math.005"].location = (30.0, -36.0)
    shader_nodetree.nodes["Math.006"].location = (190.0, -36.0)
    shader_nodetree.nodes["Math.007"].location = (2595.0, -36.0)
    shader_nodetree.nodes["Mix Shader.003"].location = (2755.0, -36.0)
    shader_nodetree.nodes["Add Shader"].location = (450.0, -36.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (290.0, -36.0)
    shader_nodetree.nodes["Principled BSDF.004"].location = (190.0, -136.0)
    shader_nodetree.nodes["Mix"].location = (30.0, -136.0)
    shader_nodetree.nodes["Frame"].location = (525.0, -280.0)
    shader_nodetree.nodes["Frame.001"].location = (845.0, -280.0)
    shader_nodetree.nodes["Frame.002"].location = (1485.0, -280.0)
    shader_nodetree.nodes["Frame.003"].location = (2125.0, -280.0)
    shader_nodetree.nodes["Frame.004"].location = (-130.0, 316.0)
    shader_nodetree.nodes["Frame.005"].location = (45.0, -280.0)
    shader_nodetree.nodes["Frame.006"].location = (265.0, 316.0)
    shader_nodetree.nodes["Reroute"].location = (35.0, -236.0)
    shader_nodetree.nodes["Reroute.001"].location = (515.0, -236.0)
    shader_nodetree.nodes["Reroute.003"].location = (835.0, -236.0)
    shader_nodetree.nodes["Reroute.004"].location = (1475.0, -236.0)
    shader_nodetree.nodes["Reroute.005"].location = (1475.0, -236.0)
    shader_nodetree.nodes["Reroute.006"].location = (2115.0, -236.0)
    shader_nodetree.nodes["Reroute.002"].location = (35.0, -216.0)
    shader_nodetree.nodes["Reroute.008"].location = (835.0, -216.0)
    shader_nodetree.nodes["Reroute.009"].location = (2115.0, -216.0)
    shader_nodetree.nodes["Reroute.007"].location = (35.0, -256.0)
    shader_nodetree.nodes["Reroute.010"].location = (515.0, -256.0)
    shader_nodetree.nodes["Reroute.011"].location = (835.0, -256.0)
    shader_nodetree.nodes["Reroute.012"].location = (1475.0, -256.0)
    shader_nodetree.nodes["Reroute.013"].location = (2115.0, -256.0)
    shader_nodetree.nodes["Reroute.014"].location = (515.0, -216.0)
    shader_nodetree.nodes["Reroute.015"].location = (1475.0, -216.0)
    shader_nodetree.nodes["Reroute.019"].location = (515.0, -336.0)
    shader_nodetree.nodes["Reroute.020"].location = (835.0, -336.0)
    shader_nodetree.nodes["Reroute.021"].location = (1475.0, -336.0)
    shader_nodetree.nodes["Reroute.022"].location = (2115.0, -336.0)
    shader_nodetree.nodes["Reroute.023"].location = (2755.0, -336.0)
    shader_nodetree.nodes["Reroute.024"].location = (515.0, -76.0)

    # Set dimensions
    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Group.001"].width  = 140.0
    shader_nodetree.nodes["Group.001"].height = 100.0

    shader_nodetree.nodes["FxBlend"].width  = 140.0
    shader_nodetree.nodes["FxBlend"].height = 100.0

    shader_nodetree.nodes["Math.002"].width  = 140.0
    shader_nodetree.nodes["Math.002"].height = 100.0

    shader_nodetree.nodes["Attribute.002"].width  = 140.0
    shader_nodetree.nodes["Attribute.002"].height = 100.0

    shader_nodetree.nodes["Math"].width  = 140.0
    shader_nodetree.nodes["Math"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Math.001"].width  = 140.0
    shader_nodetree.nodes["Math.001"].height = 100.0

    shader_nodetree.nodes["Principled BSDF.001"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF.001"].height = 100.0

    shader_nodetree.nodes["Math.003"].width  = 140.0
    shader_nodetree.nodes["Math.003"].height = 100.0

    shader_nodetree.nodes["Math.004"].width  = 140.0
    shader_nodetree.nodes["Math.004"].height = 100.0

    shader_nodetree.nodes["Mix Shader.001"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.001"].height = 100.0

    shader_nodetree.nodes["Mix Shader.002"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.002"].height = 100.0

    shader_nodetree.nodes["Attribute.003"].width  = 140.0
    shader_nodetree.nodes["Attribute.003"].height = 100.0

    shader_nodetree.nodes["Principled BSDF.002"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF.002"].height = 100.0

    shader_nodetree.nodes["Gamma"].width  = 140.0
    shader_nodetree.nodes["Gamma"].height = 100.0

    shader_nodetree.nodes["Principled BSDF.003"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF.003"].height = 100.0

    shader_nodetree.nodes["Math.005"].width  = 140.0
    shader_nodetree.nodes["Math.005"].height = 100.0

    shader_nodetree.nodes["Math.006"].width  = 140.0
    shader_nodetree.nodes["Math.006"].height = 100.0

    shader_nodetree.nodes["Math.007"].width  = 140.0
    shader_nodetree.nodes["Math.007"].height = 100.0

    shader_nodetree.nodes["Mix Shader.003"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.003"].height = 100.0

    shader_nodetree.nodes["Add Shader"].width  = 140.0
    shader_nodetree.nodes["Add Shader"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Principled BSDF.004"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF.004"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Frame"].width  = 300.0
    shader_nodetree.nodes["Frame"].height = 406.0

    shader_nodetree.nodes["Frame.001"].width  = 620.0
    shader_nodetree.nodes["Frame.001"].height = 406.0

    shader_nodetree.nodes["Frame.002"].width  = 620.0
    shader_nodetree.nodes["Frame.002"].height = 406.0

    shader_nodetree.nodes["Frame.003"].width  = 620.0
    shader_nodetree.nodes["Frame.003"].height = 506.0

    shader_nodetree.nodes["Frame.004"].width  = 360.0
    shader_nodetree.nodes["Frame.004"].height = 214.0

    shader_nodetree.nodes["Frame.005"].width  = 460.0
    shader_nodetree.nodes["Frame.005"].height = 406.0

    shader_nodetree.nodes["Frame.006"].width  = 2925.0
    shader_nodetree.nodes["Frame.006"].height = 816.0

    shader_nodetree.nodes["Reroute"].width  = 10.0
    shader_nodetree.nodes["Reroute"].height = 100.0

    shader_nodetree.nodes["Reroute.001"].width  = 10.0
    shader_nodetree.nodes["Reroute.001"].height = 100.0

    shader_nodetree.nodes["Reroute.003"].width  = 10.0
    shader_nodetree.nodes["Reroute.003"].height = 100.0

    shader_nodetree.nodes["Reroute.004"].width  = 10.0
    shader_nodetree.nodes["Reroute.004"].height = 100.0

    shader_nodetree.nodes["Reroute.005"].width  = 10.0
    shader_nodetree.nodes["Reroute.005"].height = 100.0

    shader_nodetree.nodes["Reroute.006"].width  = 10.0
    shader_nodetree.nodes["Reroute.006"].height = 100.0

    shader_nodetree.nodes["Reroute.002"].width  = 10.0
    shader_nodetree.nodes["Reroute.002"].height = 100.0

    shader_nodetree.nodes["Reroute.008"].width  = 10.0
    shader_nodetree.nodes["Reroute.008"].height = 100.0

    shader_nodetree.nodes["Reroute.009"].width  = 10.0
    shader_nodetree.nodes["Reroute.009"].height = 100.0

    shader_nodetree.nodes["Reroute.007"].width  = 10.0
    shader_nodetree.nodes["Reroute.007"].height = 100.0

    shader_nodetree.nodes["Reroute.010"].width  = 10.0
    shader_nodetree.nodes["Reroute.010"].height = 100.0

    shader_nodetree.nodes["Reroute.011"].width  = 10.0
    shader_nodetree.nodes["Reroute.011"].height = 100.0

    shader_nodetree.nodes["Reroute.012"].width  = 10.0
    shader_nodetree.nodes["Reroute.012"].height = 100.0

    shader_nodetree.nodes["Reroute.013"].width  = 10.0
    shader_nodetree.nodes["Reroute.013"].height = 100.0

    shader_nodetree.nodes["Reroute.014"].width  = 10.0
    shader_nodetree.nodes["Reroute.014"].height = 100.0

    shader_nodetree.nodes["Reroute.015"].width  = 10.0
    shader_nodetree.nodes["Reroute.015"].height = 100.0

    shader_nodetree.nodes["Reroute.019"].width  = 10.0
    shader_nodetree.nodes["Reroute.019"].height = 100.0

    shader_nodetree.nodes["Reroute.020"].width  = 10.0
    shader_nodetree.nodes["Reroute.020"].height = 100.0

    shader_nodetree.nodes["Reroute.021"].width  = 10.0
    shader_nodetree.nodes["Reroute.021"].height = 100.0

    shader_nodetree.nodes["Reroute.022"].width  = 10.0
    shader_nodetree.nodes["Reroute.022"].height = 100.0

    shader_nodetree.nodes["Reroute.023"].width  = 10.0
    shader_nodetree.nodes["Reroute.023"].height = 100.0

    shader_nodetree.nodes["Reroute.024"].width  = 10.0
    shader_nodetree.nodes["Reroute.024"].height = 100.0


    # Initialize shader_nodetree links

    # fxblend.Value -> math_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["FxBlend"].outputs[0],
        shader_nodetree.nodes["Math.002"].inputs[0]
    )
    # attribute_002.Factor -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math"].inputs[0]
    )
    # math.Value -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # math_001.Value -> principled_bsdf.Alpha
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[4]
    )
    # attribute_002.Factor -> math_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.003"].inputs[0]
    )
    # attribute_002.Factor -> math_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.004"].inputs[0]
    )
    # math_004.Value -> mix_shader_002.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.004"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[0]
    )
    # math_003.Value -> mix_shader_001.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.003"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[0]
    )
    # gamma.Color -> principled_bsdf_002.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Gamma"].outputs[0],
        shader_nodetree.nodes["Principled BSDF.002"].inputs[0]
    )
    # attribute_003.Color -> gamma.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.003"].outputs[0],
        shader_nodetree.nodes["Gamma"].inputs[0]
    )
    # mix_shader_003.Shader -> group_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.003"].outputs[0],
        shader_nodetree.nodes["Group.001"].inputs[0]
    )
    # group_001.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group.001"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # mix_shader_001.Shader -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.001"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[1]
    )
    # mix_shader.Shader -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[1]
    )
    # math_006.Value -> principled_bsdf_003.Alpha
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["Principled BSDF.003"].inputs[4]
    )
    # math_005.Value -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.005"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[1]
    )
    # mix_shader_002.Shader -> mix_shader_003.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.002"].outputs[0],
        shader_nodetree.nodes["Mix Shader.003"].inputs[1]
    )
    # math_007.Value -> mix_shader_003.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["Mix Shader.003"].inputs[0]
    )
    # attribute_002.Factor -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[2],
        shader_nodetree.nodes["Math.007"].inputs[0]
    )
    # transparent_bsdf.BSDF -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[0]
    )
    # principled_bsdf_004.BSDF -> add_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF.004"].outputs[0],
        shader_nodetree.nodes["Add Shader"].inputs[1]
    )
    # mix.Result -> principled_bsdf_004.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF.004"].inputs[0]
    )
    # mix.Result -> principled_bsdf_004.Emission Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF.004"].inputs[27]
    )
    # image_texture.Color -> reroute.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Reroute"].inputs[0]
    )
    # reroute.Output -> reroute_001.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute"].outputs[0],
        shader_nodetree.nodes["Reroute.001"].inputs[0]
    )
    # reroute_003.Output -> reroute_005.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.003"].outputs[0],
        shader_nodetree.nodes["Reroute.005"].inputs[0]
    )
    # reroute_005.Output -> reroute_006.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.005"].outputs[0],
        shader_nodetree.nodes["Reroute.006"].inputs[0]
    )
    # reroute_001.Output -> reroute_003.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.001"].outputs[0],
        shader_nodetree.nodes["Reroute.003"].inputs[0]
    )
    # math_002.Value -> reroute_002.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.002"].outputs[0],
        shader_nodetree.nodes["Reroute.002"].inputs[0]
    )
    # reroute_014.Output -> reroute_008.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.014"].outputs[0],
        shader_nodetree.nodes["Reroute.008"].inputs[0]
    )
    # reroute_008.Output -> principled_bsdf_002.Alpha
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.008"].outputs[0],
        shader_nodetree.nodes["Principled BSDF.002"].inputs[4]
    )
    # reroute_015.Output -> reroute_009.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.015"].outputs[0],
        shader_nodetree.nodes["Reroute.009"].inputs[0]
    )
    # reroute_009.Output -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.009"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # reroute_006.Output -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.006"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # image_texture.Alpha -> reroute_007.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[1],
        shader_nodetree.nodes["Reroute.007"].inputs[0]
    )
    # reroute_007.Output -> reroute_010.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.007"].outputs[0],
        shader_nodetree.nodes["Reroute.010"].inputs[0]
    )
    # reroute_010.Output -> reroute_011.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.010"].outputs[0],
        shader_nodetree.nodes["Reroute.011"].inputs[0]
    )
    # reroute_011.Output -> reroute_012.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.011"].outputs[0],
        shader_nodetree.nodes["Reroute.012"].inputs[0]
    )
    # reroute_012.Output -> reroute_013.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.012"].outputs[0],
        shader_nodetree.nodes["Reroute.013"].inputs[0]
    )
    # reroute_002.Output -> reroute_014.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.002"].outputs[0],
        shader_nodetree.nodes["Reroute.014"].inputs[0]
    )
    # reroute_008.Output -> reroute_015.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.008"].outputs[0],
        shader_nodetree.nodes["Reroute.015"].inputs[0]
    )
    # reroute_002.Output -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.002"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[1]
    )
    # reroute_007.Output -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.007"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[0]
    )
    # reroute_001.Output -> principled_bsdf_001.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.001"].outputs[0],
        shader_nodetree.nodes["Principled BSDF.001"].inputs[0]
    )
    # reroute_005.Output -> principled_bsdf_003.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.005"].outputs[0],
        shader_nodetree.nodes["Principled BSDF.003"].inputs[0]
    )
    # reroute_012.Output -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.012"].outputs[0],
        shader_nodetree.nodes["Math.005"].inputs[0]
    )
    # reroute.Output -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # principled_bsdf.BSDF -> reroute_019.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Reroute.019"].inputs[0]
    )
    # reroute_024.Output -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.024"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # principled_bsdf_001.BSDF -> reroute_020.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF.001"].outputs[0],
        shader_nodetree.nodes["Reroute.020"].inputs[0]
    )
    # reroute_020.Output -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.020"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # principled_bsdf_002.BSDF -> reroute_021.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF.002"].outputs[0],
        shader_nodetree.nodes["Reroute.021"].inputs[0]
    )
    # reroute_021.Output -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.021"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[2]
    )
    # principled_bsdf_003.BSDF -> reroute_022.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF.003"].outputs[0],
        shader_nodetree.nodes["Reroute.022"].inputs[0]
    )
    # reroute_022.Output -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.022"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[2]
    )
    # add_shader.Shader -> reroute_023.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Add Shader"].outputs[0],
        shader_nodetree.nodes["Reroute.023"].inputs[0]
    )
    # reroute_023.Output -> mix_shader_003.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.023"].outputs[0],
        shader_nodetree.nodes["Mix Shader.003"].inputs[2]
    )
    # reroute_019.Output -> reroute_024.Input
    shader_nodetree.links.new(
        shader_nodetree.nodes["Reroute.019"].outputs[0],
        shader_nodetree.nodes["Reroute.024"].inputs[0]
    )

def setup_bsp_nodes_old(nodes, links, image):
    # Node Principled BSDF
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.0
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Set locations
    nodes["Principled BSDF"].location = (-200.0, 100.0)
    nodes["Material Output"].location = (60.0, 100.0)
    nodes["Image Texture"].location = (-460.0, 100.0)

    # Set dimensions
    nodes["Principled BSDF"].width  = 240.0
    nodes["Principled BSDF"].height = 100.0

    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    links.new(
        nodes["Principled BSDF"].outputs[0],
        nodes["Material Output"].inputs[0]
    )
    # image_texture.Color -> principled_bsdf.Base Color
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Principled BSDF"].inputs[0]
    )

def setup_decal_nodes(nodes, links, image):
    # Node Principled BSDF
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.0
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Float Curve
    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    # Mapping settings
    float_curve.mapping.extend = 'EXTRAPOLATED'
    float_curve.mapping.tone = 'STANDARD'
    float_curve.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve.mapping.clip_min_x = 0.0
    float_curve.mapping.clip_min_y = 0.0
    float_curve.mapping.clip_max_x = 1.0
    float_curve.mapping.clip_max_y = 1.0
    float_curve.mapping.use_clip = True
    # Curve 0
    float_curve_curve_0 = float_curve.mapping.curves[0]
    float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
    float_curve_curve_0_point_0.location = (0.0, 0.0)
    float_curve_curve_0_point_0.handle_type = 'AUTO'
    float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
    float_curve_curve_0_point_1.location = (0.5, 0.75)
    float_curve_curve_0_point_1.handle_type = 'AUTO'
    float_curve_curve_0_point_2 = float_curve_curve_0.points.new(1.0, 1.0)
    float_curve_curve_0_point_2.handle_type = 'AUTO'
    # Update curve after changes
    float_curve.mapping.update()
    # Factor
    float_curve.inputs[0].default_value = 1.0

    # Set locations
    nodes["Principled BSDF"].location = (-160.0, 100.0)
    nodes["Material Output"].location = (100.0, 100.0)
    nodes["Image Texture"].location = (-680.0, 100.0)
    nodes["Float Curve"].location = (-420.0, 20.0)

    # Set dimensions
    nodes["Principled BSDF"].width  = 240.0
    nodes["Principled BSDF"].height = 100.0

    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    nodes["Float Curve"].width  = 240.0
    nodes["Float Curve"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    links.new(
        nodes["Principled BSDF"].outputs[0],
        nodes["Material Output"].inputs[0]
    )
    # image_texture.Color -> principled_bsdf.Base Color
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Principled BSDF"].inputs[0]
    )
    # float_curve.Value -> principled_bsdf.Alpha
    links.new(
        nodes["Float Curve"].outputs[0],
        nodes["Principled BSDF"].inputs[4]
    )
    # image_texture.Alpha -> float_curve.Value
    links.new(
        nodes["Image Texture"].outputs[1],
        nodes["Float Curve"].inputs[1]
    )

def setup_anim_bsp_nodes(nodes, links, image, main_frame_count, alt_frame_count):
    # Node Principled BSDF
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.0
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Animated Texture
    animated_texture = new(nodes, "Animated Texture")
    # Socket_1
    animated_texture.inputs[0].default_value = main_frame_count
    # Socket_2
    animated_texture.inputs[1].default_value = alt_frame_count

    # Set locations
    nodes["Principled BSDF"].location = (-200.0, 100.0)
    nodes["Material Output"].location = (60.0, 100.0)
    nodes["Image Texture"].location = (-460.0, 100.0)
    animated_texture.location = (-620.0, -40.0)

    # Set dimensions
    nodes["Principled BSDF"].width  = 240.0
    nodes["Principled BSDF"].height = 100.0

    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    animated_texture.width  = 140.0
    animated_texture.height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    links.new(
        nodes["Principled BSDF"].outputs[0],
        nodes["Material Output"].inputs[0]
    )
    # image_texture.Color -> principled_bsdf.Base Color
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Principled BSDF"].inputs[0]
    )
    # animated_texture.Vector -> image_texture.Vector
    links.new(
        animated_texture.outputs[0],
        nodes["Image Texture"].inputs[0]
    )

# R_DrawSkybox, MakeSkyVec
# params matching skyname suffixes
def setup_sky_nodes(shader_nodetree, rt, bk, lf, ft, up, dn):
    # Node Texture Coordinate.001
    texture_coordinate_001 = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.name = "Texture Coordinate.001"
    texture_coordinate_001.from_instancer = False

    # Node Vector Transform.001
    vector_transform_001 = shader_nodetree.nodes.new("ShaderNodeVectorTransform")
    vector_transform_001.name = "Vector Transform.001"
    vector_transform_001.convert_from = 'CAMERA'
    vector_transform_001.convert_to = 'WORLD'
    vector_transform_001.vector_type = 'VECTOR'

    # Node Combine XYZ.004
    combine_xyz_004 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"
    # Z
    combine_xyz_004.inputs[2].default_value = 0.0

    # Node Vector Math.017
    vector_math_017 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_017.name = "Vector Math.017"
    vector_math_017.operation = 'MULTIPLY'

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'DIVIDE'
    math_007.use_clamp = False
    # Value
    math_007.inputs[0].default_value = 1.0

    # Node Math.035
    math_035 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_035.name = "Math.035"
    math_035.operation = 'MULTIPLY'
    math_035.use_clamp = False
    # Value_001
    math_035.inputs[1].default_value = -1.0

    # Node Math.036
    math_036 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_036.name = "Math.036"
    math_036.operation = 'MULTIPLY'
    math_036.use_clamp = False
    # Value_001
    math_036.inputs[1].default_value = 1.0

    # Node Image Texture.015
    image_texture_015 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_015.name = "Image Texture.015"
    image_texture_015.extension = 'CLIP'
    image_texture_015.image = up
    image_texture_015.image_user.frame_current = 0
    image_texture_015.image_user.frame_duration = 1
    image_texture_015.image_user.frame_offset = -1
    image_texture_015.image_user.frame_start = 1
    image_texture_015.image_user.tile = 0
    image_texture_015.image_user.use_auto_refresh = False
    image_texture_015.image_user.use_cyclic = False
    image_texture_015.interpolation = 'Linear'
    image_texture_015.projection = 'FLAT'
    image_texture_015.projection_blend = 1.0

    # Node Material Output.002
    material_output_002 = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output_002.name = "Material Output.002"
    material_output_002.is_active_output = True
    material_output_002.target = 'ALL'
    # Displacement
    material_output_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output_002.inputs[3].default_value = 0.0

    # Node Emission.002
    emission_002 = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission_002.name = "Emission.002"
    # Strength
    emission_002.inputs[1].default_value = 1.0

    # Node Vector Math.014
    vector_math_014 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_014.name = "Vector Math.014"
    vector_math_014.operation = 'ADD'
    # Vector_001
    vector_math_014.inputs[1].default_value = (-1.0, 1.0, 0.0)

    # Node Vector Math.015
    vector_math_015 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_015.name = "Vector Math.015"
    vector_math_015.operation = 'DIVIDE'
    # Vector_001
    vector_math_015.inputs[1].default_value = (-2.0, 2.0, 1.0)

    # Node Math.042
    math_042 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_042.name = "Math.042"
    math_042.operation = 'LESS_THAN'
    math_042.use_clamp = False
    # Value_001
    math_042.inputs[1].default_value = 0.0

    # Node Image Texture.016
    image_texture_016 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_016.name = "Image Texture.016"
    image_texture_016.extension = 'CLIP'
    image_texture_016.image = dn
    image_texture_016.image_user.frame_current = 0
    image_texture_016.image_user.frame_duration = 1
    image_texture_016.image_user.frame_offset = -1
    image_texture_016.image_user.frame_start = 1
    image_texture_016.image_user.tile = 0
    image_texture_016.image_user.use_auto_refresh = False
    image_texture_016.image_user.use_cyclic = False
    image_texture_016.interpolation = 'Linear'
    image_texture_016.projection = 'FLAT'
    image_texture_016.projection_blend = 1.0

    # Node Mix.001
    mix_001 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'LIGHTEN'
    mix_001.clamp_factor = False
    mix_001.clamp_result = False
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_001.inputs[0].default_value = 1.0

    # Node Vector Math.019
    vector_math_019 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_019.name = "Vector Math.019"
    vector_math_019.operation = 'ADD'
    # Vector_001
    vector_math_019.inputs[1].default_value = (1.0, 1.0, 0.0)

    # Node Vector Math.023
    vector_math_023 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_023.name = "Vector Math.023"
    vector_math_023.operation = 'DIVIDE'
    # Vector_001
    vector_math_023.inputs[1].default_value = (2.0, 2.0, 1.0)

    # Node Math.043
    math_043 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_043.name = "Math.043"
    math_043.operation = 'GREATER_THAN'
    math_043.use_clamp = False
    # Value_001
    math_043.inputs[1].default_value = 0.0

    # Node Separate XYZ.001
    separate_xyz_001 = shader_nodetree.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    # Node Combine XYZ.006
    combine_xyz_006 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_006.name = "Combine XYZ.006"
    # Z
    combine_xyz_006.inputs[2].default_value = 0.0

    # Node Vector Math.025
    vector_math_025 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_025.name = "Vector Math.025"
    vector_math_025.operation = 'MULTIPLY'

    # Node Math.044
    math_044 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_044.name = "Math.044"
    math_044.operation = 'DIVIDE'
    math_044.use_clamp = False
    # Value
    math_044.inputs[0].default_value = 1.0

    # Node Math.045
    math_045 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_045.name = "Math.045"
    math_045.operation = 'MULTIPLY'
    math_045.use_clamp = False
    # Value_001
    math_045.inputs[1].default_value = 1.0

    # Node Math.046
    math_046 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_046.name = "Math.046"
    math_046.operation = 'MULTIPLY'
    math_046.use_clamp = False
    # Value_001
    math_046.inputs[1].default_value = 1.0

    # Node Image Texture.017
    image_texture_017 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_017.name = "Image Texture.017"
    image_texture_017.extension = 'CLIP'
    image_texture_017.image = bk
    image_texture_017.image_user.frame_current = 0
    image_texture_017.image_user.frame_duration = 1
    image_texture_017.image_user.frame_offset = -1
    image_texture_017.image_user.frame_start = 1
    image_texture_017.image_user.tile = 0
    image_texture_017.image_user.use_auto_refresh = False
    image_texture_017.image_user.use_cyclic = False
    image_texture_017.interpolation = 'Linear'
    image_texture_017.projection = 'FLAT'
    image_texture_017.projection_blend = 1.0

    # Node Vector Math.026
    vector_math_026 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_026.name = "Vector Math.026"
    vector_math_026.operation = 'ADD'
    # Vector_001
    vector_math_026.inputs[1].default_value = (1.0, 1.0, 0.0)

    # Node Vector Math.027
    vector_math_027 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_027.name = "Vector Math.027"
    vector_math_027.operation = 'DIVIDE'
    # Vector_001
    vector_math_027.inputs[1].default_value = (2.0, 2.0, 1.0)

    # Node Math.047
    math_047 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_047.name = "Math.047"
    math_047.operation = 'LESS_THAN'
    math_047.use_clamp = False
    # Value_001
    math_047.inputs[1].default_value = 0.0

    # Node Image Texture.018
    image_texture_018 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_018.name = "Image Texture.018"
    image_texture_018.extension = 'CLIP'
    image_texture_018.image = ft
    image_texture_018.image_user.frame_current = 0
    image_texture_018.image_user.frame_duration = 1
    image_texture_018.image_user.frame_offset = -1
    image_texture_018.image_user.frame_start = 1
    image_texture_018.image_user.tile = 0
    image_texture_018.image_user.use_auto_refresh = False
    image_texture_018.image_user.use_cyclic = False
    image_texture_018.interpolation = 'Linear'
    image_texture_018.projection = 'FLAT'
    image_texture_018.projection_blend = 1.0

    # Node Mix.002
    mix_002 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.blend_type = 'LIGHTEN'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_002.inputs[0].default_value = 1.0

    # Node Vector Math.028
    vector_math_028 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_028.name = "Vector Math.028"
    vector_math_028.operation = 'ADD'
    # Vector_001
    vector_math_028.inputs[1].default_value = (1.0, -1.0, 0.0)

    # Node Vector Math.029
    vector_math_029 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_029.name = "Vector Math.029"
    vector_math_029.operation = 'DIVIDE'
    # Vector_001
    vector_math_029.inputs[1].default_value = (2.0, -2.0, 1.0)

    # Node Math.048
    math_048 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_048.name = "Math.048"
    math_048.operation = 'GREATER_THAN'
    math_048.use_clamp = False
    # Value_001
    math_048.inputs[1].default_value = 0.0

    # Node Combine XYZ.010
    combine_xyz_010 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_010.name = "Combine XYZ.010"
    # Z
    combine_xyz_010.inputs[2].default_value = 0.0

    # Node Vector Math.032
    vector_math_032 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_032.name = "Vector Math.032"
    vector_math_032.operation = 'MULTIPLY'

    # Node Math.049
    math_049 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_049.name = "Math.049"
    math_049.operation = 'DIVIDE'
    math_049.use_clamp = False
    # Value
    math_049.inputs[0].default_value = 1.0

    # Node Math.050
    math_050 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_050.name = "Math.050"
    math_050.operation = 'MULTIPLY'
    math_050.use_clamp = False
    # Value_001
    math_050.inputs[1].default_value = 1.0

    # Node Math.051
    math_051 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_051.name = "Math.051"
    math_051.operation = 'MULTIPLY'
    math_051.use_clamp = False
    # Value_001
    math_051.inputs[1].default_value = 1.0

    # Node Image Texture.019
    image_texture_019 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_019.name = "Image Texture.019"
    image_texture_019.extension = 'CLIP'
    image_texture_019.image = rt
    image_texture_019.image_user.frame_current = 0
    image_texture_019.image_user.frame_duration = 1
    image_texture_019.image_user.frame_offset = -1
    image_texture_019.image_user.frame_start = 1
    image_texture_019.image_user.tile = 0
    image_texture_019.image_user.use_auto_refresh = False
    image_texture_019.image_user.use_cyclic = False
    image_texture_019.interpolation = 'Linear'
    image_texture_019.projection = 'FLAT'
    image_texture_019.projection_blend = 1.0

    # Node Vector Math.033
    vector_math_033 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_033.name = "Vector Math.033"
    vector_math_033.operation = 'ADD'
    # Vector_001
    vector_math_033.inputs[1].default_value = (-1.0, 1.0, 0.0)

    # Node Vector Math.034
    vector_math_034 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_034.name = "Vector Math.034"
    vector_math_034.operation = 'DIVIDE'
    # Vector_001
    vector_math_034.inputs[1].default_value = (-2.0, 2.0, 1.0)

    # Node Math.052
    math_052 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_052.name = "Math.052"
    math_052.operation = 'LESS_THAN'
    math_052.use_clamp = False
    # Value_001
    math_052.inputs[1].default_value = 0.0

    # Node Image Texture.020
    image_texture_020 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_020.name = "Image Texture.020"
    image_texture_020.extension = 'CLIP'
    image_texture_020.image = lf
    image_texture_020.image_user.frame_current = 0
    image_texture_020.image_user.frame_duration = 1
    image_texture_020.image_user.frame_offset = -1
    image_texture_020.image_user.frame_start = 1
    image_texture_020.image_user.tile = 0
    image_texture_020.image_user.use_auto_refresh = False
    image_texture_020.image_user.use_cyclic = False
    image_texture_020.interpolation = 'Linear'
    image_texture_020.projection = 'FLAT'
    image_texture_020.projection_blend = 1.0

    # Node Mix.004
    mix_004 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.blend_type = 'LIGHTEN'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_004.inputs[0].default_value = 1.0

    # Node Vector Math.035
    vector_math_035 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_035.name = "Vector Math.035"
    vector_math_035.operation = 'ADD'
    # Vector_001
    vector_math_035.inputs[1].default_value = (-1.0, -1.0, 0.0)

    # Node Vector Math.036
    vector_math_036 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_036.name = "Vector Math.036"
    vector_math_036.operation = 'DIVIDE'
    # Vector_001
    vector_math_036.inputs[1].default_value = (-2.0, -2.0, 1.0)

    # Node Math.053
    math_053 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_053.name = "Math.053"
    math_053.operation = 'GREATER_THAN'
    math_053.use_clamp = False
    # Value_001
    math_053.inputs[1].default_value = 0.0

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'LIGHTEN'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Mix.003
    mix_003 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.blend_type = 'LIGHTEN'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_003.inputs[0].default_value = 1.0

    # Node Mix.005
    mix_005 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_005.name = "Mix.005"
    mix_005.blend_type = 'MULTIPLY'
    mix_005.clamp_factor = False
    mix_005.clamp_result = False
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_005.inputs[0].default_value = 1.0

    # Node Mix.006
    mix_006 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_006.name = "Mix.006"
    mix_006.blend_type = 'MULTIPLY'
    mix_006.clamp_factor = False
    mix_006.clamp_result = False
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_006.inputs[0].default_value = 1.0

    # Node Mix.007
    mix_007 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_007.name = "Mix.007"
    mix_007.blend_type = 'MULTIPLY'
    mix_007.clamp_factor = False
    mix_007.clamp_result = False
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_007.inputs[0].default_value = 1.0

    # Node Mix.008
    mix_008 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_008.name = "Mix.008"
    mix_008.blend_type = 'MULTIPLY'
    mix_008.clamp_factor = False
    mix_008.clamp_result = False
    mix_008.data_type = 'RGBA'
    mix_008.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_008.inputs[0].default_value = 1.0

    # Node Mix.009
    mix_009 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_009.name = "Mix.009"
    mix_009.blend_type = 'MULTIPLY'
    mix_009.clamp_factor = False
    mix_009.clamp_result = False
    mix_009.data_type = 'RGBA'
    mix_009.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_009.inputs[0].default_value = 1.0

    # Node Mix.010
    mix_010 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_010.name = "Mix.010"
    mix_010.blend_type = 'MULTIPLY'
    mix_010.clamp_factor = False
    mix_010.clamp_result = False
    mix_010.data_type = 'RGBA'
    mix_010.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_010.inputs[0].default_value = 1.0

    # Node Vector Math
    vector_math = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'
    # Vector_001
    vector_math.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.001
    vector_math_001 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'
    # Vector_001
    vector_math_001.inputs[1].default_value = (0.001953125, 0.001953125, 0.0)

    # Node Vector Math.002
    vector_math_002 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'MULTIPLY'
    # Vector_001
    vector_math_002.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.003
    vector_math_003 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'ADD'
    # Vector_001
    vector_math_003.inputs[1].default_value = (0.0019529999699443579, 0.001953125, 0.0)

    # Node Vector Math.004
    vector_math_004 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'MULTIPLY'
    # Vector_001
    vector_math_004.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.005
    vector_math_005 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'ADD'
    # Vector_001
    vector_math_005.inputs[1].default_value = (0.001953125, 0.001953125, 0.0)

    # Node Vector Math.006
    vector_math_006 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'MULTIPLY'
    # Vector_001
    vector_math_006.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.007
    vector_math_007 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'ADD'
    # Vector_001
    vector_math_007.inputs[1].default_value = (0.001953125, 0.001953125, 0.0)

    # Node Vector Math.008
    vector_math_008 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'MULTIPLY'
    # Vector_001
    vector_math_008.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.009
    vector_math_009 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'ADD'
    # Vector_001
    vector_math_009.inputs[1].default_value = (0.001953125, 0.001953125, 0.0)

    # Node Vector Math.010
    vector_math_010 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'MULTIPLY'
    # Vector_001
    vector_math_010.inputs[1].default_value = (0.99609375, 0.99609375, 0.0)

    # Node Vector Math.011
    vector_math_011 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.operation = 'ADD'
    # Vector_001
    vector_math_011.inputs[1].default_value = (0.001953125, 0.001953125, 0.0)

    # Set locations
    shader_nodetree.nodes["Texture Coordinate.001"].location = (-2500.0, 0.0)
    shader_nodetree.nodes["Vector Transform.001"].location = (-2340.0, 0.0)
    shader_nodetree.nodes["Combine XYZ.004"].location = (-1640.0, 560.0)
    shader_nodetree.nodes["Vector Math.017"].location = (-1480.0, 560.0)
    shader_nodetree.nodes["Math.007"].location = (-1640.0, 420.0)
    shader_nodetree.nodes["Math.035"].location = (-1800.0, 560.0)
    shader_nodetree.nodes["Math.036"].location = (-1960.0, 560.0)
    shader_nodetree.nodes["Image Texture.015"].location = (-680.0, 840.0)
    shader_nodetree.nodes["Material Output.002"].location = (540.0, 20.0)
    shader_nodetree.nodes["Emission.002"].location = (380.0, 20.0)
    shader_nodetree.nodes["Vector Math.014"].location = (-1320.0, 760.0)
    shader_nodetree.nodes["Vector Math.015"].location = (-1160.0, 760.0)
    shader_nodetree.nodes["Math.042"].location = (-420.0, 440.0)
    shader_nodetree.nodes["Image Texture.016"].location = (-680.0, 560.0)
    shader_nodetree.nodes["Mix.001"].location = (-100.0, 560.0)
    shader_nodetree.nodes["Vector Math.019"].location = (-1320.0, 560.0)
    shader_nodetree.nodes["Vector Math.023"].location = (-1160.0, 560.0)
    shader_nodetree.nodes["Math.043"].location = (-420.0, 720.0)
    shader_nodetree.nodes["Separate XYZ.001"].location = (-2180.0, 0.0)
    shader_nodetree.nodes["Combine XYZ.006"].location = (-1640.0, 0.0)
    shader_nodetree.nodes["Vector Math.025"].location = (-1480.0, 0.0)
    shader_nodetree.nodes["Math.044"].location = (-1640.0, -140.0)
    shader_nodetree.nodes["Math.045"].location = (-1800.0, 0.0)
    shader_nodetree.nodes["Math.046"].location = (-1960.0, 0.0)
    shader_nodetree.nodes["Image Texture.017"].location = (-680.0, 280.0)
    shader_nodetree.nodes["Vector Math.026"].location = (-1320.0, 200.0)
    shader_nodetree.nodes["Vector Math.027"].location = (-1160.0, 200.0)
    shader_nodetree.nodes["Math.047"].location = (-420.0, -120.0)
    shader_nodetree.nodes["Image Texture.018"].location = (-680.0, 0.0)
    shader_nodetree.nodes["Mix.002"].location = (-100.0, 140.0)
    shader_nodetree.nodes["Vector Math.028"].location = (-1320.0, 0.0)
    shader_nodetree.nodes["Vector Math.029"].location = (-1160.0, 0.0)
    shader_nodetree.nodes["Math.048"].location = (-420.0, 160.0)
    shader_nodetree.nodes["Combine XYZ.010"].location = (-1640.0, -560.0)
    shader_nodetree.nodes["Vector Math.032"].location = (-1480.0, -560.0)
    shader_nodetree.nodes["Math.049"].location = (-1640.0, -700.0)
    shader_nodetree.nodes["Math.050"].location = (-1800.0, -560.0)
    shader_nodetree.nodes["Math.051"].location = (-1960.0, -560.0)
    shader_nodetree.nodes["Image Texture.019"].location = (-680.0, -280.0)
    shader_nodetree.nodes["Vector Math.033"].location = (-1320.0, -360.0)
    shader_nodetree.nodes["Vector Math.034"].location = (-1160.0, -360.0)
    shader_nodetree.nodes["Math.052"].location = (-420.0, -680.0)
    shader_nodetree.nodes["Image Texture.020"].location = (-680.0, -560.0)
    shader_nodetree.nodes["Mix.004"].location = (-100.0, -280.0)
    shader_nodetree.nodes["Vector Math.035"].location = (-1320.0, -560.0)
    shader_nodetree.nodes["Vector Math.036"].location = (-1160.0, -560.0)
    shader_nodetree.nodes["Math.053"].location = (-420.0, -400.0)
    shader_nodetree.nodes["Mix"].location = (220.0, 20.0)
    shader_nodetree.nodes["Mix.003"].location = (60.0, -160.0)
    shader_nodetree.nodes["Mix.005"].location = (-260.0, 840.0)
    shader_nodetree.nodes["Mix.006"].location = (-260.0, 560.0)
    shader_nodetree.nodes["Mix.007"].location = (-260.0, 280.0)
    shader_nodetree.nodes["Mix.008"].location = (-260.0, 0.0)
    shader_nodetree.nodes["Mix.009"].location = (-260.0, -280.0)
    shader_nodetree.nodes["Mix.010"].location = (-260.0, -560.0)
    shader_nodetree.nodes["Vector Math"].location = (-1000.0, 760.0)
    shader_nodetree.nodes["Vector Math.001"].location = (-840.0, 760.0)
    shader_nodetree.nodes["Vector Math.002"].location = (-1000.0, 560.0)
    shader_nodetree.nodes["Vector Math.003"].location = (-840.0, 560.0)
    shader_nodetree.nodes["Vector Math.004"].location = (-1000.0, 200.0)
    shader_nodetree.nodes["Vector Math.005"].location = (-840.0, 200.0)
    shader_nodetree.nodes["Vector Math.006"].location = (-1000.0, 0.0)
    shader_nodetree.nodes["Vector Math.007"].location = (-840.0, 0.0)
    shader_nodetree.nodes["Vector Math.008"].location = (-1000.0, -360.0)
    shader_nodetree.nodes["Vector Math.009"].location = (-840.0, -360.0)
    shader_nodetree.nodes["Vector Math.010"].location = (-1000.0, -560.0)
    shader_nodetree.nodes["Vector Math.011"].location = (-840.0, -560.0)

    # Set dimensions
    shader_nodetree.nodes["Texture Coordinate.001"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate.001"].height = 100.0

    shader_nodetree.nodes["Vector Transform.001"].width  = 140.0
    shader_nodetree.nodes["Vector Transform.001"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.004"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.004"].height = 100.0

    shader_nodetree.nodes["Vector Math.017"].width  = 140.0
    shader_nodetree.nodes["Vector Math.017"].height = 100.0

    shader_nodetree.nodes["Math.007"].width  = 140.0
    shader_nodetree.nodes["Math.007"].height = 100.0

    shader_nodetree.nodes["Math.035"].width  = 140.0
    shader_nodetree.nodes["Math.035"].height = 100.0

    shader_nodetree.nodes["Math.036"].width  = 140.0
    shader_nodetree.nodes["Math.036"].height = 100.0

    shader_nodetree.nodes["Image Texture.015"].width  = 240.0
    shader_nodetree.nodes["Image Texture.015"].height = 100.0

    shader_nodetree.nodes["Material Output.002"].width  = 140.0
    shader_nodetree.nodes["Material Output.002"].height = 100.0

    shader_nodetree.nodes["Emission.002"].width  = 140.0
    shader_nodetree.nodes["Emission.002"].height = 100.0

    shader_nodetree.nodes["Vector Math.014"].width  = 140.0
    shader_nodetree.nodes["Vector Math.014"].height = 100.0

    shader_nodetree.nodes["Vector Math.015"].width  = 140.0
    shader_nodetree.nodes["Vector Math.015"].height = 100.0

    shader_nodetree.nodes["Math.042"].width  = 140.0
    shader_nodetree.nodes["Math.042"].height = 100.0

    shader_nodetree.nodes["Image Texture.016"].width  = 240.0
    shader_nodetree.nodes["Image Texture.016"].height = 100.0

    shader_nodetree.nodes["Mix.001"].width  = 140.0
    shader_nodetree.nodes["Mix.001"].height = 100.0

    shader_nodetree.nodes["Vector Math.019"].width  = 140.0
    shader_nodetree.nodes["Vector Math.019"].height = 100.0

    shader_nodetree.nodes["Vector Math.023"].width  = 140.0
    shader_nodetree.nodes["Vector Math.023"].height = 100.0

    shader_nodetree.nodes["Math.043"].width  = 140.0
    shader_nodetree.nodes["Math.043"].height = 100.0

    shader_nodetree.nodes["Separate XYZ.001"].width  = 140.0
    shader_nodetree.nodes["Separate XYZ.001"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.006"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.006"].height = 100.0

    shader_nodetree.nodes["Vector Math.025"].width  = 140.0
    shader_nodetree.nodes["Vector Math.025"].height = 100.0

    shader_nodetree.nodes["Math.044"].width  = 140.0
    shader_nodetree.nodes["Math.044"].height = 100.0

    shader_nodetree.nodes["Math.045"].width  = 140.0
    shader_nodetree.nodes["Math.045"].height = 100.0

    shader_nodetree.nodes["Math.046"].width  = 140.0
    shader_nodetree.nodes["Math.046"].height = 100.0

    shader_nodetree.nodes["Image Texture.017"].width  = 240.0
    shader_nodetree.nodes["Image Texture.017"].height = 100.0

    shader_nodetree.nodes["Vector Math.026"].width  = 140.0
    shader_nodetree.nodes["Vector Math.026"].height = 100.0

    shader_nodetree.nodes["Vector Math.027"].width  = 140.0
    shader_nodetree.nodes["Vector Math.027"].height = 100.0

    shader_nodetree.nodes["Math.047"].width  = 140.0
    shader_nodetree.nodes["Math.047"].height = 100.0

    shader_nodetree.nodes["Image Texture.018"].width  = 240.0
    shader_nodetree.nodes["Image Texture.018"].height = 100.0

    shader_nodetree.nodes["Mix.002"].width  = 140.0
    shader_nodetree.nodes["Mix.002"].height = 100.0

    shader_nodetree.nodes["Vector Math.028"].width  = 140.0
    shader_nodetree.nodes["Vector Math.028"].height = 100.0

    shader_nodetree.nodes["Vector Math.029"].width  = 140.0
    shader_nodetree.nodes["Vector Math.029"].height = 100.0

    shader_nodetree.nodes["Math.048"].width  = 140.0
    shader_nodetree.nodes["Math.048"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.010"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.010"].height = 100.0

    shader_nodetree.nodes["Vector Math.032"].width  = 140.0
    shader_nodetree.nodes["Vector Math.032"].height = 100.0

    shader_nodetree.nodes["Math.049"].width  = 140.0
    shader_nodetree.nodes["Math.049"].height = 100.0

    shader_nodetree.nodes["Math.050"].width  = 140.0
    shader_nodetree.nodes["Math.050"].height = 100.0

    shader_nodetree.nodes["Math.051"].width  = 140.0
    shader_nodetree.nodes["Math.051"].height = 100.0

    shader_nodetree.nodes["Image Texture.019"].width  = 240.0
    shader_nodetree.nodes["Image Texture.019"].height = 100.0

    shader_nodetree.nodes["Vector Math.033"].width  = 140.0
    shader_nodetree.nodes["Vector Math.033"].height = 100.0

    shader_nodetree.nodes["Vector Math.034"].width  = 140.0
    shader_nodetree.nodes["Vector Math.034"].height = 100.0

    shader_nodetree.nodes["Math.052"].width  = 140.0
    shader_nodetree.nodes["Math.052"].height = 100.0

    shader_nodetree.nodes["Image Texture.020"].width  = 240.0
    shader_nodetree.nodes["Image Texture.020"].height = 100.0

    shader_nodetree.nodes["Mix.004"].width  = 140.0
    shader_nodetree.nodes["Mix.004"].height = 100.0

    shader_nodetree.nodes["Vector Math.035"].width  = 140.0
    shader_nodetree.nodes["Vector Math.035"].height = 100.0

    shader_nodetree.nodes["Vector Math.036"].width  = 140.0
    shader_nodetree.nodes["Vector Math.036"].height = 100.0

    shader_nodetree.nodes["Math.053"].width  = 140.0
    shader_nodetree.nodes["Math.053"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Mix.003"].width  = 140.0
    shader_nodetree.nodes["Mix.003"].height = 100.0

    shader_nodetree.nodes["Mix.005"].width  = 140.0
    shader_nodetree.nodes["Mix.005"].height = 100.0

    shader_nodetree.nodes["Mix.006"].width  = 140.0
    shader_nodetree.nodes["Mix.006"].height = 100.0

    shader_nodetree.nodes["Mix.007"].width  = 140.0
    shader_nodetree.nodes["Mix.007"].height = 100.0

    shader_nodetree.nodes["Mix.008"].width  = 140.0
    shader_nodetree.nodes["Mix.008"].height = 100.0

    shader_nodetree.nodes["Mix.009"].width  = 140.0
    shader_nodetree.nodes["Mix.009"].height = 100.0

    shader_nodetree.nodes["Mix.010"].width  = 140.0
    shader_nodetree.nodes["Mix.010"].height = 100.0

    shader_nodetree.nodes["Vector Math"].width  = 140.0
    shader_nodetree.nodes["Vector Math"].height = 100.0

    shader_nodetree.nodes["Vector Math.001"].width  = 140.0
    shader_nodetree.nodes["Vector Math.001"].height = 100.0

    shader_nodetree.nodes["Vector Math.002"].width  = 140.0
    shader_nodetree.nodes["Vector Math.002"].height = 100.0

    shader_nodetree.nodes["Vector Math.003"].width  = 140.0
    shader_nodetree.nodes["Vector Math.003"].height = 100.0

    shader_nodetree.nodes["Vector Math.004"].width  = 140.0
    shader_nodetree.nodes["Vector Math.004"].height = 100.0

    shader_nodetree.nodes["Vector Math.005"].width  = 140.0
    shader_nodetree.nodes["Vector Math.005"].height = 100.0

    shader_nodetree.nodes["Vector Math.006"].width  = 140.0
    shader_nodetree.nodes["Vector Math.006"].height = 100.0

    shader_nodetree.nodes["Vector Math.007"].width  = 140.0
    shader_nodetree.nodes["Vector Math.007"].height = 100.0

    shader_nodetree.nodes["Vector Math.008"].width  = 140.0
    shader_nodetree.nodes["Vector Math.008"].height = 100.0

    shader_nodetree.nodes["Vector Math.009"].width  = 140.0
    shader_nodetree.nodes["Vector Math.009"].height = 100.0

    shader_nodetree.nodes["Vector Math.010"].width  = 140.0
    shader_nodetree.nodes["Vector Math.010"].height = 100.0

    shader_nodetree.nodes["Vector Math.011"].width  = 140.0
    shader_nodetree.nodes["Vector Math.011"].height = 100.0


    # Initialize shader_nodetree links

    # texture_coordinate_001.Camera -> vector_transform_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate.001"].outputs[4],
        shader_nodetree.nodes["Vector Transform.001"].inputs[0]
    )
    # combine_xyz_004.Vector -> vector_math_017.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.004"].outputs[0],
        shader_nodetree.nodes["Vector Math.017"].inputs[0]
    )
    # math_007.Value -> vector_math_017.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["Vector Math.017"].inputs[1]
    )
    # math_035.Value -> combine_xyz_004.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.035"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.004"].inputs[1]
    )
    # math_036.Value -> combine_xyz_004.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.036"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.004"].inputs[0]
    )
    # emission_002.Emission -> material_output_002.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission.002"].outputs[0],
        shader_nodetree.nodes["Material Output.002"].inputs[0]
    )
    # vector_math_014.Vector -> vector_math_015.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.014"].outputs[0],
        shader_nodetree.nodes["Vector Math.015"].inputs[0]
    )
    # vector_math_017.Vector -> vector_math_014.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.017"].outputs[0],
        shader_nodetree.nodes["Vector Math.014"].inputs[0]
    )
    # mix_006.Result -> mix_001.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.006"].outputs[2],
        shader_nodetree.nodes["Mix.001"].inputs[7]
    )
    # vector_math_019.Vector -> vector_math_023.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.019"].outputs[0],
        shader_nodetree.nodes["Vector Math.023"].inputs[0]
    )
    # vector_math_017.Vector -> vector_math_019.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.017"].outputs[0],
        shader_nodetree.nodes["Vector Math.019"].inputs[0]
    )
    # vector_transform_001.Vector -> separate_xyz_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Transform.001"].outputs[0],
        shader_nodetree.nodes["Separate XYZ.001"].inputs[0]
    )
    # separate_xyz_001.Z -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[2],
        shader_nodetree.nodes["Math.007"].inputs[1]
    )
    # separate_xyz_001.Z -> math_042.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[2],
        shader_nodetree.nodes["Math.042"].inputs[0]
    )
    # separate_xyz_001.Z -> math_043.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[2],
        shader_nodetree.nodes["Math.043"].inputs[0]
    )
    # combine_xyz_006.Vector -> vector_math_025.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.006"].outputs[0],
        shader_nodetree.nodes["Vector Math.025"].inputs[0]
    )
    # math_044.Value -> vector_math_025.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.044"].outputs[0],
        shader_nodetree.nodes["Vector Math.025"].inputs[1]
    )
    # math_045.Value -> combine_xyz_006.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.045"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.006"].inputs[1]
    )
    # math_046.Value -> combine_xyz_006.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.046"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.006"].inputs[0]
    )
    # vector_math_026.Vector -> vector_math_027.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.026"].outputs[0],
        shader_nodetree.nodes["Vector Math.027"].inputs[0]
    )
    # vector_math_025.Vector -> vector_math_026.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.025"].outputs[0],
        shader_nodetree.nodes["Vector Math.026"].inputs[0]
    )
    # vector_math_028.Vector -> vector_math_029.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.028"].outputs[0],
        shader_nodetree.nodes["Vector Math.029"].inputs[0]
    )
    # vector_math_025.Vector -> vector_math_028.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.025"].outputs[0],
        shader_nodetree.nodes["Vector Math.028"].inputs[0]
    )
    # separate_xyz_001.X -> math_046.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[0],
        shader_nodetree.nodes["Math.046"].inputs[0]
    )
    # separate_xyz_001.Y -> math_044.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[1],
        shader_nodetree.nodes["Math.044"].inputs[1]
    )
    # separate_xyz_001.Y -> math_048.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[1],
        shader_nodetree.nodes["Math.048"].inputs[0]
    )
    # separate_xyz_001.Y -> math_047.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[1],
        shader_nodetree.nodes["Math.047"].inputs[0]
    )
    # separate_xyz_001.Z -> math_045.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[2],
        shader_nodetree.nodes["Math.045"].inputs[0]
    )
    # combine_xyz_010.Vector -> vector_math_032.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.010"].outputs[0],
        shader_nodetree.nodes["Vector Math.032"].inputs[0]
    )
    # math_049.Value -> vector_math_032.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.049"].outputs[0],
        shader_nodetree.nodes["Vector Math.032"].inputs[1]
    )
    # math_050.Value -> combine_xyz_010.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.050"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.010"].inputs[1]
    )
    # math_051.Value -> combine_xyz_010.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.051"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.010"].inputs[0]
    )
    # vector_math_033.Vector -> vector_math_034.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.033"].outputs[0],
        shader_nodetree.nodes["Vector Math.034"].inputs[0]
    )
    # vector_math_032.Vector -> vector_math_033.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.032"].outputs[0],
        shader_nodetree.nodes["Vector Math.033"].inputs[0]
    )
    # vector_math_035.Vector -> vector_math_036.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.035"].outputs[0],
        shader_nodetree.nodes["Vector Math.036"].inputs[0]
    )
    # vector_math_032.Vector -> vector_math_035.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.032"].outputs[0],
        shader_nodetree.nodes["Vector Math.035"].inputs[0]
    )
    # separate_xyz_001.Y -> math_051.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[1],
        shader_nodetree.nodes["Math.051"].inputs[0]
    )
    # separate_xyz_001.Z -> math_050.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[2],
        shader_nodetree.nodes["Math.050"].inputs[0]
    )
    # separate_xyz_001.X -> math_049.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[0],
        shader_nodetree.nodes["Math.049"].inputs[1]
    )
    # separate_xyz_001.X -> math_053.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[0],
        shader_nodetree.nodes["Math.053"].inputs[0]
    )
    # separate_xyz_001.X -> math_052.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[0],
        shader_nodetree.nodes["Math.052"].inputs[0]
    )
    # mix_001.Result -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.001"].outputs[2],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # mix_004.Result -> mix_003.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.004"].outputs[2],
        shader_nodetree.nodes["Mix.003"].inputs[7]
    )
    # mix_003.Result -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.003"].outputs[2],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # mix_002.Result -> mix_003.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.002"].outputs[2],
        shader_nodetree.nodes["Mix.003"].inputs[6]
    )
    # vector_math_001.Vector -> image_texture_015.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.001"].outputs[0],
        shader_nodetree.nodes["Image Texture.015"].inputs[0]
    )
    # image_texture_015.Color -> mix_005.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.015"].outputs[0],
        shader_nodetree.nodes["Mix.005"].inputs[6]
    )
    # mix_005.Result -> mix_001.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.005"].outputs[2],
        shader_nodetree.nodes["Mix.001"].inputs[6]
    )
    # math_043.Value -> mix_005.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.043"].outputs[0],
        shader_nodetree.nodes["Mix.005"].inputs[7]
    )
    # image_texture_016.Color -> mix_006.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.016"].outputs[0],
        shader_nodetree.nodes["Mix.006"].inputs[6]
    )
    # math_042.Value -> mix_006.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.042"].outputs[0],
        shader_nodetree.nodes["Mix.006"].inputs[7]
    )
    # image_texture_017.Color -> mix_007.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.017"].outputs[0],
        shader_nodetree.nodes["Mix.007"].inputs[6]
    )
    # mix_007.Result -> mix_002.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.007"].outputs[2],
        shader_nodetree.nodes["Mix.002"].inputs[6]
    )
    # image_texture_018.Color -> mix_008.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.018"].outputs[0],
        shader_nodetree.nodes["Mix.008"].inputs[6]
    )
    # mix_008.Result -> mix_002.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.008"].outputs[2],
        shader_nodetree.nodes["Mix.002"].inputs[7]
    )
    # math_047.Value -> mix_008.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.047"].outputs[0],
        shader_nodetree.nodes["Mix.008"].inputs[7]
    )
    # math_048.Value -> mix_007.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.048"].outputs[0],
        shader_nodetree.nodes["Mix.007"].inputs[7]
    )
    # image_texture_019.Color -> mix_009.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.019"].outputs[0],
        shader_nodetree.nodes["Mix.009"].inputs[6]
    )
    # mix_009.Result -> mix_004.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.009"].outputs[2],
        shader_nodetree.nodes["Mix.004"].inputs[6]
    )
    # image_texture_020.Color -> mix_010.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.020"].outputs[0],
        shader_nodetree.nodes["Mix.010"].inputs[6]
    )
    # mix_010.Result -> mix_004.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.010"].outputs[2],
        shader_nodetree.nodes["Mix.004"].inputs[7]
    )
    # math_053.Value -> mix_009.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.053"].outputs[0],
        shader_nodetree.nodes["Mix.009"].inputs[7]
    )
    # math_052.Value -> mix_010.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.052"].outputs[0],
        shader_nodetree.nodes["Mix.010"].inputs[7]
    )
    # mix.Result -> emission_002.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Emission.002"].inputs[0]
    )
    # separate_xyz_001.Y -> math_036.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[1],
        shader_nodetree.nodes["Math.036"].inputs[0]
    )
    # separate_xyz_001.X -> math_035.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.001"].outputs[0],
        shader_nodetree.nodes["Math.035"].inputs[0]
    )
    # vector_math_015.Vector -> vector_math.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.015"].outputs[0],
        shader_nodetree.nodes["Vector Math"].inputs[0]
    )
    # vector_math.Vector -> vector_math_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math"].outputs[0],
        shader_nodetree.nodes["Vector Math.001"].inputs[0]
    )
    # vector_math_002.Vector -> vector_math_003.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.002"].outputs[0],
        shader_nodetree.nodes["Vector Math.003"].inputs[0]
    )
    # vector_math_023.Vector -> vector_math_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.023"].outputs[0],
        shader_nodetree.nodes["Vector Math.002"].inputs[0]
    )
    # vector_math_003.Vector -> image_texture_016.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.003"].outputs[0],
        shader_nodetree.nodes["Image Texture.016"].inputs[0]
    )
    # vector_math_004.Vector -> vector_math_005.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.004"].outputs[0],
        shader_nodetree.nodes["Vector Math.005"].inputs[0]
    )
    # vector_math_006.Vector -> vector_math_007.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.006"].outputs[0],
        shader_nodetree.nodes["Vector Math.007"].inputs[0]
    )
    # vector_math_027.Vector -> vector_math_004.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.027"].outputs[0],
        shader_nodetree.nodes["Vector Math.004"].inputs[0]
    )
    # vector_math_005.Vector -> image_texture_017.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.005"].outputs[0],
        shader_nodetree.nodes["Image Texture.017"].inputs[0]
    )
    # vector_math_029.Vector -> vector_math_006.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.029"].outputs[0],
        shader_nodetree.nodes["Vector Math.006"].inputs[0]
    )
    # vector_math_007.Vector -> image_texture_018.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.007"].outputs[0],
        shader_nodetree.nodes["Image Texture.018"].inputs[0]
    )
    # vector_math_008.Vector -> vector_math_009.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.008"].outputs[0],
        shader_nodetree.nodes["Vector Math.009"].inputs[0]
    )
    # vector_math_010.Vector -> vector_math_011.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.010"].outputs[0],
        shader_nodetree.nodes["Vector Math.011"].inputs[0]
    )
    # vector_math_034.Vector -> vector_math_008.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.034"].outputs[0],
        shader_nodetree.nodes["Vector Math.008"].inputs[0]
    )
    # vector_math_009.Vector -> image_texture_019.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.009"].outputs[0],
        shader_nodetree.nodes["Image Texture.019"].inputs[0]
    )
    # vector_math_036.Vector -> vector_math_010.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.036"].outputs[0],
        shader_nodetree.nodes["Vector Math.010"].inputs[0]
    )
    # vector_math_011.Vector -> image_texture_020.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.011"].outputs[0],
        shader_nodetree.nodes["Image Texture.020"].inputs[0]
    )

def setup_sprite_light_nodes(shader_nodetree):
    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"

    # Node Light Output
    light_output = shader_nodetree.nodes.new("ShaderNodeOutputLight")
    light_output.name = "Light Output"
    light_output.is_active_output = True
    light_output.target = 'ALL'

    # Node Attribute
    attribute = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "light_color"
    attribute.attribute_type = 'INSTANCER'
    attribute.outputs[1].hide = True
    attribute.outputs[2].hide = True
    attribute.outputs[3].hide = True

    # Node Attribute.001
    attribute_001 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_001.name = "Attribute.001"
    attribute_001.attribute_name = "size"
    attribute_001.attribute_type = 'INSTANCER'
    attribute_001.outputs[0].hide = True
    attribute_001.outputs[1].hide = True
    attribute_001.outputs[3].hide = True

    # Node Attribute.002
    attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "scale"
    attribute_002.attribute_type = 'INSTANCER'
    attribute_002.outputs[0].hide = True
    attribute_002.outputs[2].hide = True
    attribute_002.outputs[3].hide = True

    # Node Separate XYZ
    separate_xyz = shader_nodetree.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"
    separate_xyz.outputs[1].hide = True
    separate_xyz.outputs[2].hide = True

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False

    # Node Math.001
    math_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'POWER'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 3.0

    # Node Math.002
    math_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 700.0

    # Node Group.002
    group_002 = shader_nodetree.nodes.new("ShaderNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = ensure_group("FxBlend")

    # Node Math.003
    math_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'DIVIDE'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 255.0

    # Node Attribute.006
    attribute_006 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_006.label = "renderamt"
    attribute_006.name = "Attribute.006"
    attribute_006.attribute_name = "renderamt"
    attribute_006.attribute_type = 'INSTANCER'

    # Node Math.004
    math_004 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 255.0

    # Node Math.005
    math_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False

    # Node Math.006
    math_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'COMPARE'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = 3.0
    # Value_002
    math_007.inputs[2].default_value = 0.0

    # Node Attribute.007
    attribute_007 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_007.label = "rendermode"
    attribute_007.name = "Attribute.007"
    attribute_007.attribute_name = "rendermode"
    attribute_007.attribute_type = 'INSTANCER'

    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = False
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # B_Color
    mix.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Math.008
    math_008 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'SUBTRACT'
    math_008.use_clamp = False
    # Value
    math_008.inputs[0].default_value = 1.0

    # Node Attribute.008
    attribute_008 = shader_nodetree.nodes.new("ShaderNodeAttribute")
    attribute_008.name = "Attribute.008"
    attribute_008.attribute_name = "glow_light"
    attribute_008.attribute_type = 'INSTANCER'

    # Node Math.009
    math_009 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False

    # Set locations
    shader_nodetree.nodes["Emission"].location = (40.0, 160.0)
    shader_nodetree.nodes["Light Output"].location = (200.0, 160.0)
    shader_nodetree.nodes["Attribute"].location = (-280.0, 160.0)
    shader_nodetree.nodes["Attribute.001"].location = (-760.0, 40.0)
    shader_nodetree.nodes["Attribute.002"].location = (-920.0, -80.0)
    shader_nodetree.nodes["Separate XYZ"].location = (-760.0, -80.0)
    shader_nodetree.nodes["Math"].location = (-600.0, 40.0)
    shader_nodetree.nodes["Math.001"].location = (-440.0, 40.0)
    shader_nodetree.nodes["Math.002"].location = (-280.0, 40.0)
    shader_nodetree.nodes["Group.002"].location = (-600.0, -120.0)
    shader_nodetree.nodes["Math.003"].location = (-440.0, -120.0)
    shader_nodetree.nodes["Attribute.006"].location = (-600.0, -280.0)
    shader_nodetree.nodes["Math.004"].location = (-440.0, -280.0)
    shader_nodetree.nodes["Math.005"].location = (-280.0, -120.0)
    shader_nodetree.nodes["Math.006"].location = (-120.0, 40.0)
    shader_nodetree.nodes["Math.007"].location = (-600.0, 320.0)
    shader_nodetree.nodes["Attribute.007"].location = (-760.0, 320.0)
    shader_nodetree.nodes["Mix"].location = (-120.0, 280.0)
    shader_nodetree.nodes["Math.008"].location = (-280.0, 320.0)
    shader_nodetree.nodes["Attribute.008"].location = (-600.0, 500.0)
    shader_nodetree.nodes["Math.009"].location = (-440.0, 320.0)

    # Set dimensions
    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Light Output"].width  = 140.0
    shader_nodetree.nodes["Light Output"].height = 100.0

    shader_nodetree.nodes["Attribute"].width  = 140.0
    shader_nodetree.nodes["Attribute"].height = 100.0

    shader_nodetree.nodes["Attribute.001"].width  = 140.0
    shader_nodetree.nodes["Attribute.001"].height = 100.0

    shader_nodetree.nodes["Attribute.002"].width  = 140.0
    shader_nodetree.nodes["Attribute.002"].height = 100.0

    shader_nodetree.nodes["Separate XYZ"].width  = 140.0
    shader_nodetree.nodes["Separate XYZ"].height = 100.0

    shader_nodetree.nodes["Math"].width  = 140.0
    shader_nodetree.nodes["Math"].height = 100.0

    shader_nodetree.nodes["Math.001"].width  = 140.0
    shader_nodetree.nodes["Math.001"].height = 100.0

    shader_nodetree.nodes["Math.002"].width  = 140.0
    shader_nodetree.nodes["Math.002"].height = 100.0

    shader_nodetree.nodes["Group.002"].width  = 140.0
    shader_nodetree.nodes["Group.002"].height = 100.0

    shader_nodetree.nodes["Math.003"].width  = 140.0
    shader_nodetree.nodes["Math.003"].height = 100.0

    shader_nodetree.nodes["Attribute.006"].width  = 140.0
    shader_nodetree.nodes["Attribute.006"].height = 100.0

    shader_nodetree.nodes["Math.004"].width  = 140.0
    shader_nodetree.nodes["Math.004"].height = 100.0

    shader_nodetree.nodes["Math.005"].width  = 140.0
    shader_nodetree.nodes["Math.005"].height = 100.0

    shader_nodetree.nodes["Math.006"].width  = 140.0
    shader_nodetree.nodes["Math.006"].height = 100.0

    shader_nodetree.nodes["Math.007"].width  = 140.0
    shader_nodetree.nodes["Math.007"].height = 100.0

    shader_nodetree.nodes["Attribute.007"].width  = 140.0
    shader_nodetree.nodes["Attribute.007"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Math.008"].width  = 140.0
    shader_nodetree.nodes["Math.008"].height = 100.0

    shader_nodetree.nodes["Attribute.008"].width  = 140.0
    shader_nodetree.nodes["Attribute.008"].height = 100.0

    shader_nodetree.nodes["Math.009"].width  = 140.0
    shader_nodetree.nodes["Math.009"].height = 100.0


    # Initialize shader_nodetree links

    # emission.Emission -> light_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Light Output"].inputs[0]
    )
    # mix.Result -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # attribute_002.Vector -> separate_xyz.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.002"].outputs[1],
        shader_nodetree.nodes["Separate XYZ"].inputs[0]
    )
    # attribute_001.Factor -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.001"].outputs[2],
        shader_nodetree.nodes["Math"].inputs[0]
    )
    # separate_xyz.X -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ"].outputs[0],
        shader_nodetree.nodes["Math"].inputs[1]
    )
    # math.Value -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[0]
    )
    # math_001.Value -> math_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Math.002"].inputs[0]
    )
    # group_002.Value -> math_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group.002"].outputs[0],
        shader_nodetree.nodes["Math.003"].inputs[0]
    )
    # attribute_006.Factor -> math_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.006"].outputs[2],
        shader_nodetree.nodes["Math.004"].inputs[0]
    )
    # math_003.Value -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.003"].outputs[0],
        shader_nodetree.nodes["Math.005"].inputs[0]
    )
    # math_004.Value -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.004"].outputs[0],
        shader_nodetree.nodes["Math.005"].inputs[1]
    )
    # math_002.Value -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.002"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[0]
    )
    # math_005.Value -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.005"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[1]
    )
    # math_006.Value -> emission.Strength
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["Emission"].inputs[1]
    )
    # attribute_007.Factor -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.007"].outputs[2],
        shader_nodetree.nodes["Math.007"].inputs[0]
    )
    # attribute.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # attribute_008.Factor -> math_009.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Attribute.008"].outputs[2],
        shader_nodetree.nodes["Math.009"].inputs[0]
    )
    # math_009.Value -> math_008.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.009"].outputs[0],
        shader_nodetree.nodes["Math.008"].inputs[1]
    )
    # math_008.Value -> mix.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.008"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[0]
    )
    # math_007.Value -> math_009.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["Math.009"].inputs[1]
    )

    return shader_nodetree

def setup_emissive_nodes(shader_nodetree, image, emission_color, strength):
    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Closest'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Color
    color = shader_nodetree.nodes.new("ShaderNodeRGB")
    color.name = "Color"

    color.outputs[0].default_value = emission_color
    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = False
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Light Path
    light_path = shader_nodetree.nodes.new("ShaderNodeLightPath")
    light_path.name = "Light Path"
    light_path.outputs[1].hide = True
    light_path.outputs[2].hide = True
    light_path.outputs[3].hide = True
    light_path.outputs[4].hide = True
    light_path.outputs[5].hide = True
    light_path.outputs[6].hide = True
    light_path.outputs[7].hide = True
    light_path.outputs[8].hide = True
    light_path.outputs[9].hide = True
    light_path.outputs[10].hide = True
    light_path.outputs[11].hide = True
    light_path.outputs[12].hide = True
    light_path.outputs[13].hide = True
    light_path.outputs[14].hide = True

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = strength

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Set locations
    shader_nodetree.nodes["Image Texture"].location = (0.0, 0.0)
    shader_nodetree.nodes["Principled BSDF"].location = (420.0, 0.0)
    shader_nodetree.nodes["Material Output"].location = (840.0, 0.0)
    shader_nodetree.nodes["Color"].location = (100.0, 160.0)
    shader_nodetree.nodes["Mix"].location = (260.0, 0.0)
    shader_nodetree.nodes["Light Path"].location = (520.0, 180.0)
    shader_nodetree.nodes["Emission"].location = (520.0, 120.0)
    shader_nodetree.nodes["Mix Shader"].location = (680.0, 120.0)

    # Set dimensions
    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Color"].width  = 140.0
    shader_nodetree.nodes["Color"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Light Path"].width  = 140.0
    shader_nodetree.nodes["Light Path"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0


    # Initialize shader_nodetree links

    # image_texture.Alpha -> principled_bsdf.Alpha
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[1],
        shader_nodetree.nodes["Principled BSDF"].inputs[4]
    )
    # color.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # image_texture.Color -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # mix.Result -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # mix.Result -> principled_bsdf.Emission Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF"].inputs[27]
    )
    # color.Color -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color"].outputs[0],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # principled_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # mix_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # emission.Emission -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # light_path.Is Camera Ray -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Light Path"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )

    return shader_nodetree
