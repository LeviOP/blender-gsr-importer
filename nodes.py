import bpy

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

    # Initialize sprite_color_1 nodes

    # Node Group Output
    group_output = sprite_color_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Attribute
    attribute = sprite_color_1.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "r_blend"
    attribute.attribute_type = 'OBJECT'

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

    # Set locations
    sprite_color_1.nodes["Group Output"].location = (480.0, 120.0)
    sprite_color_1.nodes["Attribute"].location = (160.0, -120.0)
    sprite_color_1.nodes["Attribute.003"].location = (0.0, -60.0)
    sprite_color_1.nodes["Gamma"].location = (160.0, -40.0)
    sprite_color_1.nodes["Mix"].location = (320.0, 120.0)
    sprite_color_1.nodes["Attribute.004"].location = (-320.0, 120.0)
    sprite_color_1.nodes["Math.005"].location = (-160.0, 120.0)
    sprite_color_1.nodes["Math.006"].location = (0.0, 120.0)
    sprite_color_1.nodes["Math.007"].location = (160.0, 120.0)

    # Set dimensions
    sprite_color_1.nodes["Group Output"].width  = 140.0
    sprite_color_1.nodes["Group Output"].height = 100.0

    sprite_color_1.nodes["Attribute"].width  = 140.0
    sprite_color_1.nodes["Attribute"].height = 100.0

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


    # Initialize sprite_color_1 links

    # math_006.Value -> math_007.Value
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.006"].outputs[0],
        sprite_color_1.nodes["Math.007"].inputs[0]
    )
    # attribute.Color -> mix.B
    sprite_color_1.links.new(
        sprite_color_1.nodes["Attribute"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[7]
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
    # math_007.Value -> mix.Factor
    sprite_color_1.links.new(
        sprite_color_1.nodes["Math.007"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[0]
    )
    # gamma.Color -> mix.A
    sprite_color_1.links.new(
        sprite_color_1.nodes["Gamma"].outputs[0],
        sprite_color_1.nodes["Mix"].inputs[6]
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

    # Node Texture Coordinate
    texture_coordinate = sprite_frame_offset_1.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

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

    # Set locations
    sprite_frame_offset_1.nodes["Group Output"].location = (80.0, 40.0)
    sprite_frame_offset_1.nodes["Group Input"].location = (-440.0, 0.0)
    sprite_frame_offset_1.nodes["Texture Coordinate"].location = (-800.0, 40.0)
    sprite_frame_offset_1.nodes["Separate XYZ"].location = (-620.0, -80.0)
    sprite_frame_offset_1.nodes["Attribute"].location = (-620.0, 120.0)
    sprite_frame_offset_1.nodes["Math"].location = (-440.0, 160.0)
    sprite_frame_offset_1.nodes["Math.001"].location = (-260.0, 160.0)
    sprite_frame_offset_1.nodes["Combine XYZ"].location = (-80.0, 40.0)

    # Set dimensions
    sprite_frame_offset_1.nodes["Group Output"].width  = 140.0
    sprite_frame_offset_1.nodes["Group Output"].height = 100.0

    sprite_frame_offset_1.nodes["Group Input"].width  = 140.0
    sprite_frame_offset_1.nodes["Group Input"].height = 100.0

    sprite_frame_offset_1.nodes["Texture Coordinate"].width  = 140.0
    sprite_frame_offset_1.nodes["Texture Coordinate"].height = 100.0

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


    # Initialize sprite_frame_offset_1 links

    # texture_coordinate.UV -> separate_xyz.Vector
    sprite_frame_offset_1.links.new(
        sprite_frame_offset_1.nodes["Texture Coordinate"].outputs[2],
        sprite_frame_offset_1.nodes["Separate XYZ"].inputs[0]
    )
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
    object_info.transform_space = 'ORIGINAL'
    if "model_0" in bpy.data.objects:
        object_info.inputs[0].default_value = bpy.data.objects["model_0"]
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Evaluate on Domain
    evaluate_on_domain = transparent_geometry_1.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.data_type = 'INT'
    evaluate_on_domain.domain = 'FACE'

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

    # Node Math.001
    math_001 = transparent_geometry_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'LESS_THAN'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 0.009999999776482582

    # Set locations
    transparent_geometry_1.nodes["Group Input"].location = (120.0, 0.0)
    transparent_geometry_1.nodes["Group Output"].location = (440.0, 0.0)
    transparent_geometry_1.nodes["Object Info"].location = (-360.0, -100.0)
    transparent_geometry_1.nodes["Evaluate on Domain"].location = (120.0, -100.0)
    transparent_geometry_1.nodes["Delete Geometry"].location = (280.0, 0.0)
    transparent_geometry_1.nodes["Geometry Proximity"].location = (-200.0, -100.0)
    transparent_geometry_1.nodes["Math.001"].location = (-40.0, -100.0)

    # Set dimensions
    transparent_geometry_1.nodes["Group Input"].width  = 140.0
    transparent_geometry_1.nodes["Group Input"].height = 100.0

    transparent_geometry_1.nodes["Group Output"].width  = 140.0
    transparent_geometry_1.nodes["Group Output"].height = 100.0

    transparent_geometry_1.nodes["Object Info"].width  = 140.0
    transparent_geometry_1.nodes["Object Info"].height = 100.0

    transparent_geometry_1.nodes["Evaluate on Domain"].width  = 140.0
    transparent_geometry_1.nodes["Evaluate on Domain"].height = 100.0

    transparent_geometry_1.nodes["Delete Geometry"].width  = 140.0
    transparent_geometry_1.nodes["Delete Geometry"].height = 100.0

    transparent_geometry_1.nodes["Geometry Proximity"].width  = 140.0
    transparent_geometry_1.nodes["Geometry Proximity"].height = 100.0

    transparent_geometry_1.nodes["Math.001"].width  = 140.0
    transparent_geometry_1.nodes["Math.001"].height = 100.0


    # Initialize transparent_geometry_1 links

    # geometry_proximity.Distance -> math_001.Value
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Geometry Proximity"].outputs[1],
        transparent_geometry_1.nodes["Math.001"].inputs[0]
    )
    # math_001.Value -> evaluate_on_domain.Value
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Math.001"].outputs[0],
        transparent_geometry_1.nodes["Evaluate on Domain"].inputs[0]
    )
    # delete_geometry.Geometry -> group_output.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Delete Geometry"].outputs[0],
        transparent_geometry_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Geometry -> delete_geometry.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Group Input"].outputs[0],
        transparent_geometry_1.nodes["Delete Geometry"].inputs[0]
    )
    # evaluate_on_domain.Value -> delete_geometry.Selection
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Evaluate on Domain"].outputs[0],
        transparent_geometry_1.nodes["Delete Geometry"].inputs[1]
    )
    # object_info.Geometry -> geometry_proximity.Geometry
    transparent_geometry_1.links.new(
        transparent_geometry_1.nodes["Object Info"].outputs[4],
        transparent_geometry_1.nodes["Geometry Proximity"].inputs[0]
    )

    return transparent_geometry_1

def goldsrc_emissive_1_node_group():
    """Initialize GoldSrc Emissive node group"""
    goldsrc_emissive_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "GoldSrc Emissive")

    goldsrc_emissive_1.color_tag = 'NONE'
    goldsrc_emissive_1.description = ""
    goldsrc_emissive_1.default_group_node_width = 160
    # goldsrc_emissive_1 interface

    # Socket Shader
    shader_socket = goldsrc_emissive_1.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket Texture
    texture_socket = goldsrc_emissive_1.interface.new_socket(name="Texture", in_out='INPUT', socket_type='NodeSocketColor')
    texture_socket.default_value = (0.5, 0.5, 0.5, 1.0)
    texture_socket.attribute_domain = 'POINT'
    texture_socket.default_input = 'VALUE'
    texture_socket.structure_type = 'AUTO'

    # Socket Color
    color_socket = goldsrc_emissive_1.interface.new_socket(name="Color", in_out='INPUT', socket_type='NodeSocketColor')
    color_socket.default_value = (0.42326438426971436, 0.5583407878875732, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.default_input = 'VALUE'
    color_socket.structure_type = 'AUTO'

    # Socket Strength
    strength_socket = goldsrc_emissive_1.interface.new_socket(name="Strength", in_out='INPUT', socket_type='NodeSocketFloat')
    strength_socket.default_value = 50.0
    strength_socket.min_value = 0.0
    strength_socket.max_value = 1000000.0
    strength_socket.subtype = 'NONE'
    strength_socket.attribute_domain = 'POINT'
    strength_socket.default_input = 'VALUE'
    strength_socket.structure_type = 'AUTO'

    # Initialize goldsrc_emissive_1 nodes

    # Node Group Output
    group_output = goldsrc_emissive_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = goldsrc_emissive_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Emission
    emission = goldsrc_emissive_1.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"

    # Node Mix Shader
    mix_shader = goldsrc_emissive_1.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Light Path
    light_path = goldsrc_emissive_1.nodes.new("ShaderNodeLightPath")
    light_path.name = "Light Path"

    # Node Mix
    mix = goldsrc_emissive_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = False
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Set locations
    goldsrc_emissive_1.nodes["Group Output"].location = (400.0, 220.0)
    goldsrc_emissive_1.nodes["Group Input"].location = (-140.0, -60.0)
    goldsrc_emissive_1.nodes["Emission"].location = (40.0, -100.0)
    goldsrc_emissive_1.nodes["Mix Shader"].location = (220.0, 220.0)
    goldsrc_emissive_1.nodes["Light Path"].location = (-140.0, 320.0)
    goldsrc_emissive_1.nodes["Mix"].location = (40.0, 140.0)

    # Set dimensions
    goldsrc_emissive_1.nodes["Group Output"].width  = 140.0
    goldsrc_emissive_1.nodes["Group Output"].height = 100.0

    goldsrc_emissive_1.nodes["Group Input"].width  = 140.0
    goldsrc_emissive_1.nodes["Group Input"].height = 100.0

    goldsrc_emissive_1.nodes["Emission"].width  = 140.0
    goldsrc_emissive_1.nodes["Emission"].height = 100.0

    goldsrc_emissive_1.nodes["Mix Shader"].width  = 140.0
    goldsrc_emissive_1.nodes["Mix Shader"].height = 100.0

    goldsrc_emissive_1.nodes["Light Path"].width  = 140.0
    goldsrc_emissive_1.nodes["Light Path"].height = 100.0

    goldsrc_emissive_1.nodes["Mix"].width  = 140.0
    goldsrc_emissive_1.nodes["Mix"].height = 100.0


    # Initialize goldsrc_emissive_1 links

    # light_path.Is Camera Ray -> mix_shader.Factor
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Light Path"].outputs[0],
        goldsrc_emissive_1.nodes["Mix Shader"].inputs[0]
    )
    # mix.Result -> mix_shader.Shader
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Mix"].outputs[2],
        goldsrc_emissive_1.nodes["Mix Shader"].inputs[2]
    )
    # emission.Emission -> mix_shader.Shader
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Emission"].outputs[0],
        goldsrc_emissive_1.nodes["Mix Shader"].inputs[1]
    )
    # group_input.Color -> emission.Color
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Group Input"].outputs[1],
        goldsrc_emissive_1.nodes["Emission"].inputs[0]
    )
    # group_input.Strength -> emission.Strength
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Group Input"].outputs[2],
        goldsrc_emissive_1.nodes["Emission"].inputs[1]
    )
    # group_input.Color -> mix.B
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Group Input"].outputs[1],
        goldsrc_emissive_1.nodes["Mix"].inputs[7]
    )
    # group_input.Texture -> mix.A
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Group Input"].outputs[0],
        goldsrc_emissive_1.nodes["Mix"].inputs[6]
    )
    # mix_shader.Shader -> group_output.Shader
    goldsrc_emissive_1.links.new(
        goldsrc_emissive_1.nodes["Mix Shader"].outputs[0],
        goldsrc_emissive_1.nodes["Group Output"].inputs[0]
    )

    return goldsrc_emissive_1

def beam_1_node_group():
    """Initialize Beam node group"""
    beam_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Beam Segment")

    beam_1.color_tag = 'NONE'
    beam_1.description = ""
    beam_1.default_group_node_width = 140
    beam_1.show_modifier_manage_panel = True

    # beam_1 interface

    # Socket Geometry
    geometry_socket = beam_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Material
    material_socket = beam_1.interface.new_socket(name="Material", in_out='INPUT', socket_type='NodeSocketMaterial')
    material_socket.attribute_domain = 'POINT'
    material_socket.default_input = 'VALUE'
    material_socket.structure_type = 'AUTO'

    # Socket Source
    source_socket = beam_1.interface.new_socket(name="Source", in_out='INPUT', socket_type='NodeSocketVector')
    source_socket.default_value = (0.0, 0.0, 0.0)
    source_socket.min_value = -3.4028234663852886e+38
    source_socket.max_value = 3.4028234663852886e+38
    source_socket.subtype = 'XYZ'
    source_socket.attribute_domain = 'POINT'
    source_socket.default_input = 'VALUE'
    source_socket.structure_type = 'AUTO'

    # Socket Delta
    delta_socket = beam_1.interface.new_socket(name="Delta", in_out='INPUT', socket_type='NodeSocketVector')
    delta_socket.default_value = (0.0, 0.0, 0.0)
    delta_socket.min_value = -3.4028234663852886e+38
    delta_socket.max_value = 3.4028234663852886e+38
    delta_socket.subtype = 'XYZ'
    delta_socket.attribute_domain = 'POINT'
    delta_socket.default_input = 'VALUE'
    delta_socket.structure_type = 'AUTO'

    # Socket Width
    width_socket = beam_1.interface.new_socket(name="Width", in_out='INPUT', socket_type='NodeSocketFloat')
    width_socket.default_value = 0.0
    width_socket.min_value = -3.4028234663852886e+38
    width_socket.max_value = 3.4028234663852886e+38
    width_socket.subtype = 'NONE'
    width_socket.attribute_domain = 'POINT'
    width_socket.default_input = 'VALUE'
    width_socket.structure_type = 'AUTO'

    # Socket Segments
    segments_socket = beam_1.interface.new_socket(name="Segments", in_out='INPUT', socket_type='NodeSocketInt')
    segments_socket.default_value = 0
    segments_socket.min_value = -2147483648
    segments_socket.max_value = 2147483647
    segments_socket.subtype = 'NONE'
    segments_socket.attribute_domain = 'POINT'
    segments_socket.default_input = 'VALUE'
    segments_socket.structure_type = 'AUTO'

    # Initialize beam_1 nodes

    # Node Group Output
    group_output = beam_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = beam_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Object Info
    object_info = beam_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Active Camera
    active_camera = beam_1.nodes.new("GeometryNodeInputActiveCamera")
    active_camera.name = "Active Camera"

    # Node Grid
    grid = beam_1.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0
    # Vertices Y
    grid.inputs[3].default_value = 2

    # Node Vector Math.001
    vector_math_001 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'LENGTH'

    # Node Vector Math.002
    vector_math_002 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.label = "beam_dir"
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'NORMALIZE'

    # Node Position
    position = beam_1.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    # Node Separate XYZ
    separate_xyz = beam_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Map Range
    map_range = beam_1.nodes.new("ShaderNodeMapRange")
    map_range.label = "t"
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    # From Min
    map_range.inputs[1].default_value = -0.5
    # From Max
    map_range.inputs[2].default_value = 0.5
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0

    # Node Set Position
    set_position = beam_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.005
    vector_math_005 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'SCALE'

    # Node Math
    math = beam_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False

    # Node Vector Math.003
    vector_math_003 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.label = "beam_point"
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'ADD'

    # Node Math.001
    math_001 = beam_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'SIGN'
    math_001.use_clamp = False

    # Node Math.002
    math_002 = beam_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False

    # Node Vector Math.006
    vector_math_006 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'SCALE'

    # Node Vector Math.008
    vector_math_008 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'ADD'

    # Node Math.003
    math_003 = beam_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = -1.0

    # Node Set Material
    set_material = beam_1.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    # Selection
    set_material.inputs[1].default_value = True

    # Node Store Named Attribute
    store_named_attribute = beam_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT2'
    store_named_attribute.domain = 'CORNER'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"

    # Node Combine XYZ.001
    combine_xyz_001 = beam_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    # Z
    combine_xyz_001.inputs[2].default_value = 0.0

    # Node Map Range.002
    map_range_002 = beam_1.nodes.new("ShaderNodeMapRange")
    map_range_002.label = "t"
    map_range_002.name = "Map Range.002"
    map_range_002.clamp = True
    map_range_002.data_type = 'FLOAT'
    map_range_002.interpolation_type = 'LINEAR'
    # From Min
    map_range_002.inputs[1].default_value = -0.5
    # From Max
    map_range_002.inputs[2].default_value = 0.5
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 1.0

    # Node Math.005
    math_005 = beam_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    # Value
    math_005.inputs[0].default_value = 0.0
    # Value_001
    math_005.inputs[1].default_value = 0.0

    # Node Integer Math
    integer_math = beam_1.nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.operation = 'MODULO'
    # Value_001
    integer_math.inputs[1].default_value = 1

    # Node Math.006
    math_006 = beam_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'ADD'
    math_006.use_clamp = False

    # Node Transform Point
    transform_point = beam_1.nodes.new("FunctionNodeTransformPoint")
    transform_point.name = "Transform Point"

    # Node Invert Matrix
    invert_matrix = beam_1.nodes.new("FunctionNodeInvertMatrix")
    invert_matrix.name = "Invert Matrix"

    # Node Separate XYZ.001
    separate_xyz_001 = beam_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    # Node Math.004
    math_004 = beam_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False

    # Node Math.007
    math_007 = beam_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = -1.0

    # Node Math.008
    math_008 = beam_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'DIVIDE'
    math_008.use_clamp = False

    # Node Combine XYZ
    combine_xyz = beam_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Transform Point.001
    transform_point_001 = beam_1.nodes.new("FunctionNodeTransformPoint")
    transform_point_001.name = "Transform Point.001"

    # Node Separate XYZ.002
    separate_xyz_002 = beam_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_002.name = "Separate XYZ.002"

    # Node Math.009
    math_009 = beam_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'DIVIDE'
    math_009.use_clamp = False

    # Node Math.010
    math_010 = beam_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False
    # Value_001
    math_010.inputs[1].default_value = -1.0

    # Node Math.011
    math_011 = beam_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'DIVIDE'
    math_011.use_clamp = False

    # Node Combine XYZ.002
    combine_xyz_002 = beam_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_002.name = "Combine XYZ.002"
    # Z
    combine_xyz_002.inputs[2].default_value = 0.0

    # Node Vector Math
    vector_math = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'ADD'

    # Node Vector Math.009
    vector_math_009 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'SUBTRACT'

    # Node Vector Math.010
    vector_math_010 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'NORMALIZE'

    # Node Transform Direction
    transform_direction = beam_1.nodes.new("FunctionNodeTransformDirection")
    transform_direction.name = "Transform Direction"
    # Direction
    transform_direction.inputs[0].default_value = (1.0, 0.0, 0.0)

    # Node Transform Direction.001
    transform_direction_001 = beam_1.nodes.new("FunctionNodeTransformDirection")
    transform_direction_001.name = "Transform Direction.001"
    # Direction
    transform_direction_001.inputs[0].default_value = (0.0, 1.0, 0.0)

    # Node Vector Math.011
    vector_math_011 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.operation = 'MULTIPLY'

    # Node Separate XYZ.003
    separate_xyz_003 = beam_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"

    # Node Vector Math.012
    vector_math_012 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.operation = 'MULTIPLY'

    # Node Vector Math.013
    vector_math_013 = beam_1.nodes.new("ShaderNodeVectorMath")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.operation = 'SUBTRACT'

    # Set locations
    beam_1.nodes["Group Output"].location = (1260.0, -60.0)
    beam_1.nodes["Group Input"].location = (-2220.0, -80.0)
    beam_1.nodes["Object Info"].location = (-1960.0, -300.0)
    beam_1.nodes["Active Camera"].location = (-2120.0, -420.0)
    beam_1.nodes["Grid"].location = (620.0, -60.0)
    beam_1.nodes["Vector Math.001"].location = (-20.0, -200.0)
    beam_1.nodes["Vector Math.002"].location = (-20.0, -80.0)
    beam_1.nodes["Position"].location = (-340.0, -580.0)
    beam_1.nodes["Separate XYZ"].location = (-180.0, -580.0)
    beam_1.nodes["Map Range"].location = (-20.0, -320.0)
    beam_1.nodes["Set Position"].location = (940.0, -60.0)
    beam_1.nodes["Vector Math.005"].location = (300.0, -180.0)
    beam_1.nodes["Math"].location = (140.0, -180.0)
    beam_1.nodes["Vector Math.003"].location = (460.0, -180.0)
    beam_1.nodes["Math.001"].location = (-20.0, -580.0)
    beam_1.nodes["Math.002"].location = (140.0, -580.0)
    beam_1.nodes["Vector Math.006"].location = (460.0, -340.0)
    beam_1.nodes["Vector Math.008"].location = (620.0, -240.0)
    beam_1.nodes["Math.003"].location = (300.0, -580.0)
    beam_1.nodes["Set Material"].location = (1100.0, -60.0)
    beam_1.nodes["Store Named Attribute"].location = (780.0, -60.0)
    beam_1.nodes["Combine XYZ.001"].location = (620.0, -740.0)
    beam_1.nodes["Map Range.002"].location = (-20.0, -740.0)
    beam_1.nodes["Math.005"].location = (140.0, -820.0)
    beam_1.nodes["Integer Math"].location = (300.0, -820.0)
    beam_1.nodes["Math.006"].location = (460.0, -820.0)
    beam_1.nodes["Transform Point"].location = (-1620.0, -440.0)
    beam_1.nodes["Invert Matrix"].location = (-1780.0, -440.0)
    beam_1.nodes["Separate XYZ.001"].location = (-1460.0, -440.0)
    beam_1.nodes["Math.004"].location = (-1300.0, -440.0)
    beam_1.nodes["Math.007"].location = (-1460.0, -580.0)
    beam_1.nodes["Math.008"].location = (-1300.0, -600.0)
    beam_1.nodes["Combine XYZ"].location = (-1140.0, -440.0)
    beam_1.nodes["Transform Point.001"].location = (-1620.0, -760.0)
    beam_1.nodes["Separate XYZ.002"].location = (-1460.0, -760.0)
    beam_1.nodes["Math.009"].location = (-1300.0, -760.0)
    beam_1.nodes["Math.010"].location = (-1460.0, -900.0)
    beam_1.nodes["Math.011"].location = (-1300.0, -920.0)
    beam_1.nodes["Combine XYZ.002"].location = (-1140.0, -760.0)
    beam_1.nodes["Vector Math"].location = (-1780.0, -760.0)
    beam_1.nodes["Vector Math.009"].location = (-980.0, -440.0)
    beam_1.nodes["Vector Math.010"].location = (-820.0, -440.0)
    beam_1.nodes["Transform Direction"].location = (-660.0, -580.0)
    beam_1.nodes["Transform Direction.001"].location = (-660.0, -300.0)
    beam_1.nodes["Vector Math.011"].location = (-500.0, -340.0)
    beam_1.nodes["Separate XYZ.003"].location = (-660.0, -440.0)
    beam_1.nodes["Vector Math.012"].location = (-500.0, -480.0)
    beam_1.nodes["Vector Math.013"].location = (-340.0, -400.0)

    # Set dimensions
    beam_1.nodes["Group Output"].width  = 140.0
    beam_1.nodes["Group Output"].height = 100.0

    beam_1.nodes["Group Input"].width  = 140.0
    beam_1.nodes["Group Input"].height = 100.0

    beam_1.nodes["Object Info"].width  = 140.0
    beam_1.nodes["Object Info"].height = 100.0

    beam_1.nodes["Active Camera"].width  = 140.0
    beam_1.nodes["Active Camera"].height = 100.0

    beam_1.nodes["Grid"].width  = 140.0
    beam_1.nodes["Grid"].height = 100.0

    beam_1.nodes["Vector Math.001"].width  = 140.0
    beam_1.nodes["Vector Math.001"].height = 100.0

    beam_1.nodes["Vector Math.002"].width  = 140.0
    beam_1.nodes["Vector Math.002"].height = 100.0

    beam_1.nodes["Position"].width  = 140.0
    beam_1.nodes["Position"].height = 100.0

    beam_1.nodes["Separate XYZ"].width  = 140.0
    beam_1.nodes["Separate XYZ"].height = 100.0

    beam_1.nodes["Map Range"].width  = 140.0
    beam_1.nodes["Map Range"].height = 100.0

    beam_1.nodes["Set Position"].width  = 140.0
    beam_1.nodes["Set Position"].height = 100.0

    beam_1.nodes["Vector Math.005"].width  = 140.0
    beam_1.nodes["Vector Math.005"].height = 100.0

    beam_1.nodes["Math"].width  = 140.0
    beam_1.nodes["Math"].height = 100.0

    beam_1.nodes["Vector Math.003"].width  = 140.0
    beam_1.nodes["Vector Math.003"].height = 100.0

    beam_1.nodes["Math.001"].width  = 140.0
    beam_1.nodes["Math.001"].height = 100.0

    beam_1.nodes["Math.002"].width  = 140.0
    beam_1.nodes["Math.002"].height = 100.0

    beam_1.nodes["Vector Math.006"].width  = 140.0
    beam_1.nodes["Vector Math.006"].height = 100.0

    beam_1.nodes["Vector Math.008"].width  = 140.0
    beam_1.nodes["Vector Math.008"].height = 100.0

    beam_1.nodes["Math.003"].width  = 140.0
    beam_1.nodes["Math.003"].height = 100.0

    beam_1.nodes["Set Material"].width  = 140.0
    beam_1.nodes["Set Material"].height = 100.0

    beam_1.nodes["Store Named Attribute"].width  = 140.0
    beam_1.nodes["Store Named Attribute"].height = 100.0

    beam_1.nodes["Combine XYZ.001"].width  = 140.0
    beam_1.nodes["Combine XYZ.001"].height = 100.0

    beam_1.nodes["Map Range.002"].width  = 140.0
    beam_1.nodes["Map Range.002"].height = 100.0

    beam_1.nodes["Math.005"].width  = 140.0
    beam_1.nodes["Math.005"].height = 100.0

    beam_1.nodes["Integer Math"].width  = 140.0
    beam_1.nodes["Integer Math"].height = 100.0

    beam_1.nodes["Math.006"].width  = 140.0
    beam_1.nodes["Math.006"].height = 100.0

    beam_1.nodes["Transform Point"].width  = 140.0
    beam_1.nodes["Transform Point"].height = 100.0

    beam_1.nodes["Invert Matrix"].width  = 140.0
    beam_1.nodes["Invert Matrix"].height = 100.0

    beam_1.nodes["Separate XYZ.001"].width  = 140.0
    beam_1.nodes["Separate XYZ.001"].height = 100.0

    beam_1.nodes["Math.004"].width  = 140.0
    beam_1.nodes["Math.004"].height = 100.0

    beam_1.nodes["Math.007"].width  = 140.0
    beam_1.nodes["Math.007"].height = 100.0

    beam_1.nodes["Math.008"].width  = 140.0
    beam_1.nodes["Math.008"].height = 100.0

    beam_1.nodes["Combine XYZ"].width  = 140.0
    beam_1.nodes["Combine XYZ"].height = 100.0

    beam_1.nodes["Transform Point.001"].width  = 140.0
    beam_1.nodes["Transform Point.001"].height = 100.0

    beam_1.nodes["Separate XYZ.002"].width  = 140.0
    beam_1.nodes["Separate XYZ.002"].height = 100.0

    beam_1.nodes["Math.009"].width  = 140.0
    beam_1.nodes["Math.009"].height = 100.0

    beam_1.nodes["Math.010"].width  = 140.0
    beam_1.nodes["Math.010"].height = 100.0

    beam_1.nodes["Math.011"].width  = 140.0
    beam_1.nodes["Math.011"].height = 100.0

    beam_1.nodes["Combine XYZ.002"].width  = 140.0
    beam_1.nodes["Combine XYZ.002"].height = 100.0

    beam_1.nodes["Vector Math"].width  = 140.0
    beam_1.nodes["Vector Math"].height = 100.0

    beam_1.nodes["Vector Math.009"].width  = 140.0
    beam_1.nodes["Vector Math.009"].height = 100.0

    beam_1.nodes["Vector Math.010"].width  = 140.0
    beam_1.nodes["Vector Math.010"].height = 100.0

    beam_1.nodes["Transform Direction"].width  = 140.0
    beam_1.nodes["Transform Direction"].height = 100.0

    beam_1.nodes["Transform Direction.001"].width  = 140.0
    beam_1.nodes["Transform Direction.001"].height = 100.0

    beam_1.nodes["Vector Math.011"].width  = 140.0
    beam_1.nodes["Vector Math.011"].height = 100.0

    beam_1.nodes["Separate XYZ.003"].width  = 140.0
    beam_1.nodes["Separate XYZ.003"].height = 100.0

    beam_1.nodes["Vector Math.012"].width  = 140.0
    beam_1.nodes["Vector Math.012"].height = 100.0

    beam_1.nodes["Vector Math.013"].width  = 140.0
    beam_1.nodes["Vector Math.013"].height = 100.0


    # Initialize beam_1 links

    # active_camera.Active Camera -> object_info.Object
    beam_1.links.new(
        beam_1.nodes["Active Camera"].outputs[0],
        beam_1.nodes["Object Info"].inputs[0]
    )
    # separate_xyz.X -> map_range.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ"].outputs[0],
        beam_1.nodes["Map Range"].inputs[0]
    )
    # math.Value -> vector_math_005.Scale
    beam_1.links.new(
        beam_1.nodes["Math"].outputs[0],
        beam_1.nodes["Vector Math.005"].inputs[3]
    )
    # map_range.Result -> math.Value
    beam_1.links.new(
        beam_1.nodes["Map Range"].outputs[0],
        beam_1.nodes["Math"].inputs[1]
    )
    # vector_math_001.Value -> math.Value
    beam_1.links.new(
        beam_1.nodes["Vector Math.001"].outputs[1],
        beam_1.nodes["Math"].inputs[0]
    )
    # vector_math_002.Vector -> vector_math_005.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.002"].outputs[0],
        beam_1.nodes["Vector Math.005"].inputs[0]
    )
    # group_input.Source -> vector_math_003.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[1],
        beam_1.nodes["Vector Math.003"].inputs[0]
    )
    # vector_math_005.Vector -> vector_math_003.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.005"].outputs[0],
        beam_1.nodes["Vector Math.003"].inputs[1]
    )
    # separate_xyz.Y -> math_001.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ"].outputs[1],
        beam_1.nodes["Math.001"].inputs[0]
    )
    # math_001.Value -> math_002.Value
    beam_1.links.new(
        beam_1.nodes["Math.001"].outputs[0],
        beam_1.nodes["Math.002"].inputs[0]
    )
    # vector_math_003.Vector -> vector_math_008.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.003"].outputs[0],
        beam_1.nodes["Vector Math.008"].inputs[0]
    )
    # vector_math_006.Vector -> vector_math_008.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.006"].outputs[0],
        beam_1.nodes["Vector Math.008"].inputs[1]
    )
    # vector_math_008.Vector -> set_position.Position
    beam_1.links.new(
        beam_1.nodes["Vector Math.008"].outputs[0],
        beam_1.nodes["Set Position"].inputs[2]
    )
    # group_input.Width -> math_002.Value
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[3],
        beam_1.nodes["Math.002"].inputs[1]
    )
    # math_002.Value -> math_003.Value
    beam_1.links.new(
        beam_1.nodes["Math.002"].outputs[0],
        beam_1.nodes["Math.003"].inputs[0]
    )
    # group_input.Segments -> grid.Vertices X
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[4],
        beam_1.nodes["Grid"].inputs[2]
    )
    # group_input.Delta -> vector_math_001.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[2],
        beam_1.nodes["Vector Math.001"].inputs[0]
    )
    # group_input.Delta -> vector_math_002.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[2],
        beam_1.nodes["Vector Math.002"].inputs[0]
    )
    # group_input.Material -> set_material.Material
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[0],
        beam_1.nodes["Set Material"].inputs[2]
    )
    # set_position.Geometry -> set_material.Geometry
    beam_1.links.new(
        beam_1.nodes["Set Position"].outputs[0],
        beam_1.nodes["Set Material"].inputs[0]
    )
    # separate_xyz.Y -> map_range_002.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ"].outputs[1],
        beam_1.nodes["Map Range.002"].inputs[0]
    )
    # math_005.Value -> integer_math.Value
    beam_1.links.new(
        beam_1.nodes["Math.005"].outputs[0],
        beam_1.nodes["Integer Math"].inputs[0]
    )
    # integer_math.Value -> math_006.Value
    beam_1.links.new(
        beam_1.nodes["Integer Math"].outputs[0],
        beam_1.nodes["Math.006"].inputs[1]
    )
    # math.Value -> math_006.Value
    beam_1.links.new(
        beam_1.nodes["Math"].outputs[0],
        beam_1.nodes["Math.006"].inputs[0]
    )
    # math_006.Value -> combine_xyz_001.Y
    beam_1.links.new(
        beam_1.nodes["Math.006"].outputs[0],
        beam_1.nodes["Combine XYZ.001"].inputs[1]
    )
    # map_range_002.Result -> combine_xyz_001.X
    beam_1.links.new(
        beam_1.nodes["Map Range.002"].outputs[0],
        beam_1.nodes["Combine XYZ.001"].inputs[0]
    )
    # combine_xyz_001.Vector -> store_named_attribute.Value
    beam_1.links.new(
        beam_1.nodes["Combine XYZ.001"].outputs[0],
        beam_1.nodes["Store Named Attribute"].inputs[3]
    )
    # set_material.Geometry -> group_output.Geometry
    beam_1.links.new(
        beam_1.nodes["Set Material"].outputs[0],
        beam_1.nodes["Group Output"].inputs[0]
    )
    # grid.Mesh -> store_named_attribute.Geometry
    beam_1.links.new(
        beam_1.nodes["Grid"].outputs[0],
        beam_1.nodes["Store Named Attribute"].inputs[0]
    )
    # store_named_attribute.Geometry -> set_position.Geometry
    beam_1.links.new(
        beam_1.nodes["Store Named Attribute"].outputs[0],
        beam_1.nodes["Set Position"].inputs[0]
    )
    # invert_matrix.Matrix -> transform_point.Transform
    beam_1.links.new(
        beam_1.nodes["Invert Matrix"].outputs[0],
        beam_1.nodes["Transform Point"].inputs[1]
    )
    # position.Position -> separate_xyz.Vector
    beam_1.links.new(
        beam_1.nodes["Position"].outputs[0],
        beam_1.nodes["Separate XYZ"].inputs[0]
    )
    # object_info.Transform -> invert_matrix.Matrix
    beam_1.links.new(
        beam_1.nodes["Object Info"].outputs[0],
        beam_1.nodes["Invert Matrix"].inputs[0]
    )
    # transform_point.Vector -> separate_xyz_001.Vector
    beam_1.links.new(
        beam_1.nodes["Transform Point"].outputs[0],
        beam_1.nodes["Separate XYZ.001"].inputs[0]
    )
    # separate_xyz_001.Z -> math_007.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.001"].outputs[2],
        beam_1.nodes["Math.007"].inputs[0]
    )
    # separate_xyz_001.X -> math_004.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.001"].outputs[0],
        beam_1.nodes["Math.004"].inputs[0]
    )
    # math_007.Value -> math_004.Value
    beam_1.links.new(
        beam_1.nodes["Math.007"].outputs[0],
        beam_1.nodes["Math.004"].inputs[1]
    )
    # separate_xyz_001.Y -> math_008.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.001"].outputs[1],
        beam_1.nodes["Math.008"].inputs[0]
    )
    # math_007.Value -> math_008.Value
    beam_1.links.new(
        beam_1.nodes["Math.007"].outputs[0],
        beam_1.nodes["Math.008"].inputs[1]
    )
    # math_004.Value -> combine_xyz.X
    beam_1.links.new(
        beam_1.nodes["Math.004"].outputs[0],
        beam_1.nodes["Combine XYZ"].inputs[0]
    )
    # math_008.Value -> combine_xyz.Y
    beam_1.links.new(
        beam_1.nodes["Math.008"].outputs[0],
        beam_1.nodes["Combine XYZ"].inputs[1]
    )
    # group_input.Source -> transform_point.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[1],
        beam_1.nodes["Transform Point"].inputs[0]
    )
    # transform_point_001.Vector -> separate_xyz_002.Vector
    beam_1.links.new(
        beam_1.nodes["Transform Point.001"].outputs[0],
        beam_1.nodes["Separate XYZ.002"].inputs[0]
    )
    # separate_xyz_002.Z -> math_010.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.002"].outputs[2],
        beam_1.nodes["Math.010"].inputs[0]
    )
    # separate_xyz_002.X -> math_009.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.002"].outputs[0],
        beam_1.nodes["Math.009"].inputs[0]
    )
    # math_010.Value -> math_009.Value
    beam_1.links.new(
        beam_1.nodes["Math.010"].outputs[0],
        beam_1.nodes["Math.009"].inputs[1]
    )
    # separate_xyz_002.Y -> math_011.Value
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.002"].outputs[1],
        beam_1.nodes["Math.011"].inputs[0]
    )
    # math_010.Value -> math_011.Value
    beam_1.links.new(
        beam_1.nodes["Math.010"].outputs[0],
        beam_1.nodes["Math.011"].inputs[1]
    )
    # math_009.Value -> combine_xyz_002.X
    beam_1.links.new(
        beam_1.nodes["Math.009"].outputs[0],
        beam_1.nodes["Combine XYZ.002"].inputs[0]
    )
    # math_011.Value -> combine_xyz_002.Y
    beam_1.links.new(
        beam_1.nodes["Math.011"].outputs[0],
        beam_1.nodes["Combine XYZ.002"].inputs[1]
    )
    # invert_matrix.Matrix -> transform_point_001.Transform
    beam_1.links.new(
        beam_1.nodes["Invert Matrix"].outputs[0],
        beam_1.nodes["Transform Point.001"].inputs[1]
    )
    # group_input.Source -> vector_math.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[1],
        beam_1.nodes["Vector Math"].inputs[0]
    )
    # group_input.Delta -> vector_math.Vector
    beam_1.links.new(
        beam_1.nodes["Group Input"].outputs[2],
        beam_1.nodes["Vector Math"].inputs[1]
    )
    # vector_math.Vector -> transform_point_001.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math"].outputs[0],
        beam_1.nodes["Transform Point.001"].inputs[0]
    )
    # combine_xyz.Vector -> vector_math_009.Vector
    beam_1.links.new(
        beam_1.nodes["Combine XYZ"].outputs[0],
        beam_1.nodes["Vector Math.009"].inputs[0]
    )
    # combine_xyz_002.Vector -> vector_math_009.Vector
    beam_1.links.new(
        beam_1.nodes["Combine XYZ.002"].outputs[0],
        beam_1.nodes["Vector Math.009"].inputs[1]
    )
    # vector_math_009.Vector -> vector_math_010.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.009"].outputs[0],
        beam_1.nodes["Vector Math.010"].inputs[0]
    )
    # object_info.Transform -> transform_direction.Transform
    beam_1.links.new(
        beam_1.nodes["Object Info"].outputs[0],
        beam_1.nodes["Transform Direction"].inputs[1]
    )
    # object_info.Transform -> transform_direction_001.Transform
    beam_1.links.new(
        beam_1.nodes["Object Info"].outputs[0],
        beam_1.nodes["Transform Direction.001"].inputs[1]
    )
    # vector_math_010.Vector -> separate_xyz_003.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.010"].outputs[0],
        beam_1.nodes["Separate XYZ.003"].inputs[0]
    )
    # transform_direction_001.Direction -> vector_math_011.Vector
    beam_1.links.new(
        beam_1.nodes["Transform Direction.001"].outputs[0],
        beam_1.nodes["Vector Math.011"].inputs[0]
    )
    # separate_xyz_003.X -> vector_math_011.Vector
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.003"].outputs[0],
        beam_1.nodes["Vector Math.011"].inputs[1]
    )
    # transform_direction.Direction -> vector_math_012.Vector
    beam_1.links.new(
        beam_1.nodes["Transform Direction"].outputs[0],
        beam_1.nodes["Vector Math.012"].inputs[1]
    )
    # separate_xyz_003.Y -> vector_math_012.Vector
    beam_1.links.new(
        beam_1.nodes["Separate XYZ.003"].outputs[1],
        beam_1.nodes["Vector Math.012"].inputs[0]
    )
    # vector_math_012.Vector -> vector_math_013.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.012"].outputs[0],
        beam_1.nodes["Vector Math.013"].inputs[1]
    )
    # vector_math_011.Vector -> vector_math_013.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.011"].outputs[0],
        beam_1.nodes["Vector Math.013"].inputs[0]
    )
    # vector_math_013.Vector -> vector_math_006.Vector
    beam_1.links.new(
        beam_1.nodes["Vector Math.013"].outputs[0],
        beam_1.nodes["Vector Math.006"].inputs[0]
    )
    # math_003.Value -> vector_math_006.Scale
    beam_1.links.new(
        beam_1.nodes["Math.003"].outputs[0],
        beam_1.nodes["Vector Math.006"].inputs[3]
    )

    return beam_1

BUILDERS = {
    "Sprite Color": sprite_color_1_node_group,
    "Sprite Frame Offset": sprite_frame_offset_1_node_group,
    "Additive Shader": additive_shader_1_node_group,
    "Trans Alpha Shader": trans_alpha_shader_1_node_group,
    "Transparent Geometry": transparent_geometry_1_node_group,
    "GoldSrc Emissive": goldsrc_emissive_1_node_group,
    "Beam Segment": beam_1_node_group,
}

def ensure_group(name: str):
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]

    builder = BUILDERS.get(name)
    if builder is None:
        raise Exception("Unknown node group!")

    return builder()

def new(nodes, name: str):
    group = ensure_group(name)

    group_node = nodes.new("ShaderNodeGroup")
    group_node.node_tree = group

    return group_node

def create_compositing_nodes(view_layer, no_depth_view_layer, viewmodel_view_layer):
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

    # Node Render Layers.002
    render_layers_002 = compositing_nodetree.nodes.new("CompositorNodeRLayers")
    render_layers_002.name = "Render Layers.002"
    render_layers_002.layer = viewmodel_view_layer.name

    # Node Alpha Over
    alpha_over = compositing_nodetree.nodes.new("CompositorNodeAlphaOver")
    alpha_over.name = "Alpha Over"
    # Type
    alpha_over.inputs[3].default_value = 'Over'
    # Straight Alpha
    alpha_over.inputs[4].default_value = False

    # Node Math
    math = compositing_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0

    # Set locations
    compositing_nodetree.nodes["Render Layers"].location = (-340.0, 260.0)
    compositing_nodetree.nodes["Group Output"].location = (400.0, 0.0)
    compositing_nodetree.nodes["Viewer"].location = (400.0, 60.0)
    compositing_nodetree.nodes["Render Layers.001"].location = (-340.0, -40.0)
    compositing_nodetree.nodes["Render Layers.002"].location = (-340.0, -360.0)
    compositing_nodetree.nodes["Alpha Over"].location = (200.0, 0.0)
    compositing_nodetree.nodes["Math"].location = (0.0, -220.0)

    # Set dimensions
    compositing_nodetree.nodes["Render Layers"].width  = 240.0
    compositing_nodetree.nodes["Render Layers"].height = 100.0

    compositing_nodetree.nodes["Group Output"].width  = 140.0
    compositing_nodetree.nodes["Group Output"].height = 100.0

    compositing_nodetree.nodes["Viewer"].width  = 140.0
    compositing_nodetree.nodes["Viewer"].height = 100.0

    compositing_nodetree.nodes["Render Layers.001"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.001"].height = 100.0

    compositing_nodetree.nodes["Render Layers.002"].width  = 240.0
    compositing_nodetree.nodes["Render Layers.002"].height = 100.0

    compositing_nodetree.nodes["Alpha Over"].width  = 140.0
    compositing_nodetree.nodes["Alpha Over"].height = 100.0

    compositing_nodetree.nodes["Math"].width  = 140.0
    compositing_nodetree.nodes["Math"].height = 100.0


    # Initialize compositing_nodetree links

    # alpha_over.Image -> viewer.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Alpha Over"].outputs[0],
        compositing_nodetree.nodes["Viewer"].inputs[0]
    )
    # render_layers_001.Image -> alpha_over.Foreground
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.001"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[1]
    )
    # render_layers_002.Alpha -> math.Value
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers.002"].outputs[1],
        compositing_nodetree.nodes["Math"].inputs[1]
    )
    # math.Value -> alpha_over.Factor
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Math"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[2]
    )
    # alpha_over.Image -> group_output.Image
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Alpha Over"].outputs[0],
        compositing_nodetree.nodes["Group Output"].inputs[0]
    )
    # render_layers.Image -> alpha_over.Background
    compositing_nodetree.links.new(
        compositing_nodetree.nodes["Render Layers"].outputs[0],
        compositing_nodetree.nodes["Alpha Over"].inputs[0]
    )

def setup_sprite_nodes(nodes, links, image, frame_count):
    # Node Group
    sprite_color = new(nodes, "Sprite Color")

    # Node Group.001
    sprite_frame_offset = new(nodes, "Sprite Frame Offset")
    sprite_frame_offset.inputs[0].default_value = frame_count

    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.image = image
    image_texture.interpolation = "Closest"
    image_texture.extension = "CLIP"

    # Node Attribute.002
    attribute_002 = nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "rendermode"
    attribute_002.attribute_type = 'OBJECT'

    # Node Mix
    mix = nodes.new("ShaderNodeMix")
    mix.label = "GL_MODULATE"
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'

    # Node Emission
    emission = nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Material Output.001
    material_output_001 = nodes.new("ShaderNodeOutputMaterial")
    material_output_001.name = "Material Output.001"
    material_output_001.is_active_output = True
    material_output_001.target = 'ALL'
    # Displacement
    material_output_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output_001.inputs[3].default_value = 0.0

    # Node Math
    math = nodes.new("ShaderNodeMath")
    math.label = "Is TextureColor"
    math.name = "Math"
    math.operation = 'COMPARE'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 1.0
    # Value_002
    math.inputs[2].default_value = 0.0

    # Node Math.005
    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'SUBTRACT'
    math_005.use_clamp = False
    # Value
    math_005.inputs[0].default_value = 1.0

    # Node Attribute.003
    attribute_003 = nodes.new("ShaderNodeAttribute")
    attribute_003.name = "Attribute.003"
    attribute_003.attribute_name = "r_blend"
    attribute_003.attribute_type = 'OBJECT'

    # Node Math.006
    math_006 = nodes.new("ShaderNodeMath")
    math_006.label = "GL_MOD alpha"
    math_006.name = "Math.006"
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False

    # Node Mix Shader
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.label = "GL_BLEND"
    mix_shader.name = "Mix Shader"

    # Node Transparent BSDF
    transparent_bsdf = nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Math.007
    math_007 = nodes.new("ShaderNodeMath")
    math_007.label = "Is Glow"
    math_007.name = "Math.007"
    math_007.operation = 'COMPARE'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = 3.0
    # Value_002
    math_007.inputs[2].default_value = 0.0

    # Node Mix Shader.001
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.label = "Nothing?"
    mix_shader_001.name = "Mix Shader.001"

    # Node Transparent BSDF.003
    transparent_bsdf_003 = nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf_003.name = "Transparent BSDF.003"
    # Color
    transparent_bsdf_003.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Math.008
    math_008 = nodes.new("ShaderNodeMath")
    math_008.label = "Is Additive"
    math_008.name = "Math.008"
    math_008.operation = 'COMPARE'
    math_008.use_clamp = False
    # Value_001
    math_008.inputs[1].default_value = 5.0
    # Value_002
    math_008.inputs[2].default_value = 0.0

    # Node Add Shader
    add_shader = nodes.new("ShaderNodeAddShader")
    add_shader.label = "Additive Rendering"
    add_shader.name = "Add Shader"

    # Node Mix Shader.006
    mix_shader_006 = nodes.new("ShaderNodeMixShader")
    mix_shader_006.label = "Additive?"
    mix_shader_006.name = "Mix Shader.006"

    # Node Attribute.004
    attribute_004 = nodes.new("ShaderNodeAttribute")
    attribute_004.name = "Attribute.004"
    attribute_004.attribute_name = "draw_no_depth"
    attribute_004.attribute_type = 'VIEW_LAYER'

    # Node Math.009
    math_009 = nodes.new("ShaderNodeMath")
    math_009.label = "Is no_depth"
    math_009.name = "Math.009"
    math_009.operation = 'COMPARE'
    math_009.use_clamp = False
    # Value_001
    math_009.inputs[1].default_value = 1.0
    # Value_002
    math_009.inputs[2].default_value = 0.0

    # Node Mix Shader.007
    mix_shader_007 = nodes.new("ShaderNodeMixShader")
    mix_shader_007.label = "no_depth?"
    mix_shader_007.name = "Mix Shader.007"

    # Node Mix Shader.008
    mix_shader_008 = nodes.new("ShaderNodeMixShader")
    mix_shader_008.label = "Glow"
    mix_shader_008.name = "Mix Shader.008"

    # Node Mix Shader.002
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.name = "Mix Shader.002"

    # Node Light Path
    light_path = nodes.new("ShaderNodeLightPath")
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

    # Node Diffuse BSDF
    diffuse_bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_bsdf.name = "Diffuse BSDF"
    # Roughness
    diffuse_bsdf.inputs[1].default_value = 0.0
    # Normal
    diffuse_bsdf.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Set locations
    nodes["Group"].location = (-180.0, -1120.0)
    sprite_frame_offset.location = (-340.0, -1360.0)
    nodes["Image Texture"].location = (-180.0, -1220.0)
    nodes["Attribute.002"].location = (-340.0, -800.0)
    nodes["Mix"].location = (140.0, -940.0)
    nodes["Emission"].location = (780.0, -1060.0)
    nodes["Material Output.001"].location = (1920.0, -940.0)
    nodes["Math"].location = (-180.0, -940.0)
    nodes["Math.005"].location = (-20.0, -940.0)
    nodes["Attribute.003"].location = (140.0, -1180.0)
    nodes["Math.006"].location = (300.0, -1180.0)
    nodes["Mix Shader"].location = (460.0, -1060.0)
    nodes["Transparent BSDF"].location = (300.0, -1080.0)
    nodes["Math.007"].location = (780.0, -760.0)
    nodes["Mix Shader.001"].location = (940.0, -940.0)
    nodes["Transparent BSDF.003"].location = (460.0, -1220.0)
    nodes["Math.008"].location = (1100.0, -760.0)
    nodes["Add Shader"].location = (940.0, -1080.0)
    nodes["Mix Shader.006"].location = (1260.0, -940.0)
    nodes["Attribute.004"].location = (1420.0, -760.0)
    nodes["Math.009"].location = (1580.0, -760.0)
    nodes["Mix Shader.007"].location = (1760.0, -940.0)
    nodes["Mix Shader.008"].location = (1260.0, -1080.0)
    nodes["Mix Shader.002"].location = (620.0, -940.0)
    nodes["Light Path"].location = (460.0, -940.0)
    nodes["Diffuse BSDF"].location = (300.0, -940.0)

    # Set dimensions
    sprite_color.width  = 140.0
    sprite_color.height = 100.0

    sprite_frame_offset.width  = 140.0
    sprite_frame_offset.height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    nodes["Attribute.002"].width  = 140.0
    nodes["Attribute.002"].height = 100.0

    nodes["Mix"].width  = 140.0
    nodes["Mix"].height = 100.0

    nodes["Emission"].width  = 140.0
    nodes["Emission"].height = 100.0

    nodes["Material Output.001"].width  = 140.0
    nodes["Material Output.001"].height = 100.0

    nodes["Math"].width  = 140.0
    nodes["Math"].height = 100.0

    nodes["Math.005"].width  = 140.0
    nodes["Math.005"].height = 100.0

    nodes["Attribute.003"].width  = 140.0
    nodes["Attribute.003"].height = 100.0

    nodes["Math.006"].width  = 140.0
    nodes["Math.006"].height = 100.0

    nodes["Mix Shader"].width  = 140.0
    nodes["Mix Shader"].height = 100.0

    nodes["Transparent BSDF"].width  = 140.0
    nodes["Transparent BSDF"].height = 100.0

    nodes["Math.007"].width  = 140.0
    nodes["Math.007"].height = 100.0

    nodes["Mix Shader.001"].width  = 140.0
    nodes["Mix Shader.001"].height = 100.0

    nodes["Transparent BSDF.003"].width  = 140.0
    nodes["Transparent BSDF.003"].height = 100.0

    nodes["Math.008"].width  = 140.0
    nodes["Math.008"].height = 100.0

    nodes["Add Shader"].width  = 140.0
    nodes["Add Shader"].height = 100.0

    nodes["Mix Shader.006"].width  = 140.0
    nodes["Mix Shader.006"].height = 100.0

    nodes["Attribute.004"].width  = 140.0
    nodes["Attribute.004"].height = 100.0

    nodes["Math.009"].width  = 140.0
    nodes["Math.009"].height = 100.0

    nodes["Mix Shader.007"].width  = 140.0
    nodes["Mix Shader.007"].height = 100.0

    nodes["Mix Shader.008"].width  = 140.0
    nodes["Mix Shader.008"].height = 100.0

    nodes["Mix Shader.002"].width  = 140.0
    nodes["Mix Shader.002"].height = 100.0

    nodes["Light Path"].width  = 140.0
    nodes["Light Path"].height = 100.0

    nodes["Diffuse BSDF"].width  = 140.0
    nodes["Diffuse BSDF"].height = 100.0


    # Initialize shader_nodetree links

    # group_001.Vector -> image_texture.Vector
    links.new(
        sprite_frame_offset.outputs[0],
        nodes["Image Texture"].inputs[0]
    )
    # attribute_002.Factor -> math.Value
    links.new(
        nodes["Attribute.002"].outputs[2],
        nodes["Math"].inputs[0]
    )
    # image_texture.Color -> mix.B
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Mix"].inputs[7]
    )
    # group.Result -> mix.A
    links.new(
        sprite_color.outputs[0],
        nodes["Mix"].inputs[6]
    )
    # math.Value -> math_005.Value
    links.new(
        nodes["Math"].outputs[0],
        nodes["Math.005"].inputs[1]
    )
    # math_005.Value -> mix.Factor
    links.new(
        nodes["Math.005"].outputs[0],
        nodes["Mix"].inputs[0]
    )
    # attribute_003.Factor -> math_006.Value
    links.new(
        nodes["Attribute.003"].outputs[2],
        nodes["Math.006"].inputs[1]
    )
    # image_texture.Alpha -> math_006.Value
    links.new(
        nodes["Image Texture"].outputs[1],
        nodes["Math.006"].inputs[0]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    links.new(
        nodes["Transparent BSDF"].outputs[0],
        nodes["Mix Shader"].inputs[1]
    )
    # math_006.Value -> mix_shader.Factor
    links.new(
        nodes["Math.006"].outputs[0],
        nodes["Mix Shader"].inputs[0]
    )
    # attribute_002.Factor -> math_007.Value
    links.new(
        nodes["Attribute.002"].outputs[2],
        nodes["Math.007"].inputs[0]
    )
    # mix_shader.Shader -> mix_shader_001.Shader
    links.new(
        nodes["Mix Shader"].outputs[0],
        nodes["Mix Shader.001"].inputs[1]
    )
    # math_007.Value -> mix_shader_001.Factor
    links.new(
        nodes["Math.007"].outputs[0],
        nodes["Mix Shader.001"].inputs[0]
    )
    # attribute_002.Factor -> math_008.Value
    links.new(
        nodes["Attribute.002"].outputs[2],
        nodes["Math.008"].inputs[0]
    )
    # emission.Emission -> add_shader.Shader
    links.new(
        nodes["Emission"].outputs[0],
        nodes["Add Shader"].inputs[0]
    )
    # transparent_bsdf_003.BSDF -> add_shader.Shader
    links.new(
        nodes["Transparent BSDF.003"].outputs[0],
        nodes["Add Shader"].inputs[1]
    )
    # math_008.Value -> mix_shader_006.Factor
    links.new(
        nodes["Math.008"].outputs[0],
        nodes["Mix Shader.006"].inputs[0]
    )
    # add_shader.Shader -> mix_shader_006.Shader
    links.new(
        nodes["Add Shader"].outputs[0],
        nodes["Mix Shader.006"].inputs[2]
    )
    # mix_shader_001.Shader -> mix_shader_006.Shader
    links.new(
        nodes["Mix Shader.001"].outputs[0],
        nodes["Mix Shader.006"].inputs[1]
    )
    # mix_shader_007.Shader -> material_output_001.Surface
    links.new(
        nodes["Mix Shader.007"].outputs[0],
        nodes["Material Output.001"].inputs[0]
    )
    # attribute_004.Factor -> math_009.Value
    links.new(
        nodes["Attribute.004"].outputs[2],
        nodes["Math.009"].inputs[0]
    )
    # mix_shader_006.Shader -> mix_shader_007.Shader
    links.new(
        nodes["Mix Shader.006"].outputs[0],
        nodes["Mix Shader.007"].inputs[1]
    )
    # math_009.Value -> mix_shader_007.Factor
    links.new(
        nodes["Math.009"].outputs[0],
        nodes["Mix Shader.007"].inputs[0]
    )
    # mix_shader_008.Shader -> mix_shader_007.Shader
    links.new(
        nodes["Mix Shader.008"].outputs[0],
        nodes["Mix Shader.007"].inputs[2]
    )
    # math_007.Value -> mix_shader_008.Factor
    links.new(
        nodes["Math.007"].outputs[0],
        nodes["Mix Shader.008"].inputs[0]
    )
    # add_shader.Shader -> mix_shader_008.Shader
    links.new(
        nodes["Add Shader"].outputs[0],
        nodes["Mix Shader.008"].inputs[2]
    )
    # transparent_bsdf_003.BSDF -> mix_shader_008.Shader
    links.new(
        nodes["Transparent BSDF.003"].outputs[0],
        nodes["Mix Shader.008"].inputs[1]
    )
    # light_path.Is Camera Ray -> mix_shader_002.Factor
    links.new(
        nodes["Light Path"].outputs[0],
        nodes["Mix Shader.002"].inputs[0]
    )
    # mix_shader.Shader -> mix_shader_002.Shader
    links.new(
        nodes["Mix Shader"].outputs[0],
        nodes["Mix Shader.002"].inputs[1]
    )
    # transparent_bsdf_003.BSDF -> mix_shader_002.Shader
    links.new(
        nodes["Transparent BSDF.003"].outputs[0],
        nodes["Mix Shader.002"].inputs[2]
    )
    # mix_shader_002.Shader -> mix_shader_001.Shader
    links.new(
        nodes["Mix Shader.002"].outputs[0],
        nodes["Mix Shader.001"].inputs[2]
    )
    # mix.Result -> diffuse_bsdf.Color
    links.new(
        nodes["Mix"].outputs[2],
        nodes["Diffuse BSDF"].inputs[0]
    )
    # diffuse_bsdf.BSDF -> mix_shader.Shader
    links.new(
        nodes["Diffuse BSDF"].outputs[0],
        nodes["Mix Shader"].inputs[2]
    )
    # mix.Result -> emission.Color
    links.new(
        nodes["Mix"].outputs[2],
        nodes["Emission"].inputs[0]
    )

def setup_beam_nodes(nodes, links, image, frame_count):
    # Node Image Texture
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.image = image
    image_texture.interpolation = "Closest"
    image_texture.extension = "REPEAT"

    # Node Group.001
    sprite_frame_offset = new(nodes, "Sprite Frame Offset")
    sprite_frame_offset.inputs[0].default_value = frame_count

    # Node Material Output
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Emission
    emission = nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 5.0

    # Node Attribute
    attribute = nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "color"
    attribute.attribute_type = 'OBJECT'

    # Node Gamma
    gamma = nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # Node Mix
    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 1.0

    # Node Transparent BSDF
    transparent_bsdf = nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Add Shader
    add_shader = nodes.new("ShaderNodeAddShader")
    add_shader.name = "Add Shader"

    # Set locations
    nodes["Image Texture"].location = (0.0, 0.0)
    sprite_frame_offset.location = (-160.0, -140.0)
    nodes["Material Output"].location = (800.0, 180.0)
    nodes["Emission"].location = (480.0, 180.0)
    nodes["Attribute"].location = (0.0, 180.0)
    nodes["Gamma"].location = (160.0, 180.0)
    nodes["Mix"].location = (320.0, 180.0)
    nodes["Transparent BSDF"].location = (480.0, 60.0)
    nodes["Add Shader"].location = (640.0, 180.0)

    # Set dimensions
    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    sprite_frame_offset.width  = 140.0
    sprite_frame_offset.height = 100.0

    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Emission"].width  = 140.0
    nodes["Emission"].height = 100.0

    nodes["Attribute"].width  = 140.0
    nodes["Attribute"].height = 100.0

    nodes["Gamma"].width  = 140.0
    nodes["Gamma"].height = 100.0

    nodes["Mix"].width  = 140.0
    nodes["Mix"].height = 100.0

    nodes["Transparent BSDF"].width  = 140.0
    nodes["Transparent BSDF"].height = 100.0

    nodes["Add Shader"].width  = 140.0
    nodes["Add Shader"].height = 100.0


    # Initialize shader_nodetree links

    # group_001.Vector -> image_texture.Vector
    links.new(
        sprite_frame_offset.outputs[0],
        nodes["Image Texture"].inputs[0]
    )
    # attribute.Color -> gamma.Color
    links.new(
        nodes["Attribute"].outputs[0],
        nodes["Gamma"].inputs[0]
    )
    # gamma.Color -> mix.A
    links.new(
        nodes["Gamma"].outputs[0],
        nodes["Mix"].inputs[6]
    )
    # image_texture.Color -> mix.B
    links.new(
        nodes["Image Texture"].outputs[0],
        nodes["Mix"].inputs[7]
    )
    # mix.Result -> emission.Color
    links.new(
        nodes["Mix"].outputs[2],
        nodes["Emission"].inputs[0]
    )
    # emission.Emission -> add_shader.Shader
    links.new(
        nodes["Emission"].outputs[0],
        nodes["Add Shader"].inputs[0]
    )
    # transparent_bsdf.BSDF -> add_shader.Shader
    links.new(
        nodes["Transparent BSDF"].outputs[0],
        nodes["Add Shader"].inputs[1]
    )
    # add_shader.Shader -> material_output.Surface
    links.new(
        nodes["Add Shader"].outputs[0],
        nodes["Material Output"].inputs[0]
    )

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

def setup_bsp_nodes(nodes, links, image):
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

def setup_emissive_bsp_nodes(nodes, links, image, color, strength):
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

    # Node Group
    goldsrc_emissive = new(nodes, "GoldSrc Emissive")
    goldsrc_emissive.inputs[1].default_value = color
    goldsrc_emissive.inputs[2].default_value = strength

    # Set locations
    nodes["Material Output"].location = (160.0, 180.0)
    nodes["Image Texture"].location = (-281.83062744140625, 176.3377685546875)
    nodes["Group"].location = (-20.0, 180.0)

    # Set dimensions
    nodes["Material Output"].width  = 140.0
    nodes["Material Output"].height = 100.0

    nodes["Image Texture"].width  = 240.0
    nodes["Image Texture"].height = 100.0

    nodes["Group"].width  = 160.0
    nodes["Group"].height = 100.0


    # Initialize shader_nodetree links

    # image_texture.Color -> group.Texture
    links.new(
        nodes["Image Texture"].outputs[0],
        goldsrc_emissive.inputs[0]
    )
    # group.Shader -> material_output.Surface
    links.new(
        goldsrc_emissive.outputs[0],
        nodes["Material Output"].inputs[0]
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
