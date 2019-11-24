
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
    to_ConvConvRelu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=(n_filer,n_filer), 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=size[0] - int(size[0]/4), 
        depth=size[1] - int(size[1]/4), 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]

#define new block
def block_XceptionDashed( name, botton, top, s_filer=256, n_filer=(64,64,64), offset="(1,0,0)", height=32, depth=32, width=(3.5,3.5,3.5), opacity=0.5, caption=""):
    return [
    to_XceptionElu( 
        name="{}".format( top ),
        s_filer=str(s_filer), 
        n_filer=n_filer, 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=width, 
        height=height, 
        depth=depth,   
        caption=caption
        ),    
    to_connection_dashed( 
        "{}".format( botton ), 
        "{}".format( top )
        )
    ]

#define new block
def block_XceptionPoolDashed( name, botton, top, s_filer=256, n_filer=(64,64,64), offset="(1,0,0)", height=32, depth=32, width=(3.5,3.5,3.5), pool_height=24, pool_depth=24, opacity=0.5, caption="" ):
    return [
    to_XceptionElu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=n_filer, 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=width, 
        height=height, 
        depth=depth,   
        caption=caption,
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=pool_height, 
        depth=pool_depth, 
        opacity=opacity, ),
    to_connection_dashed( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]

#define new block
def block_XceptionPool( name, botton, top, s_filer=256, n_filer=(64,64,64), offset="(1,0,0)", height=32, depth=32, width=(3.5,3.5,3.5), pool_height=24, pool_depth=24, opacity=0.5 ):
    return [
    to_XceptionElu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=n_filer, 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=width, 
        height=height, 
        depth=depth,   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=pool_height, 
        depth=pool_depth, 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]

def block_UnconvDeeplab( name, botton, top, s_filer=256, n_filer=(64,64,64), offset="(1,0,0)", width=(3.5,3.5,3.5), height=32, depth=32, opacity=0.5 ):
    return [
        to_UnPool(
            name='unpool_{}'.format(name),
            offset=offset,
            to="({}-east)".format(botton),
            width=1,
            height=height,
            depth=depth,
            opacity=opacity
            ),
        to_ConvRes(
            name='ccr_res_{}'.format(name),
            offset="(0,0,0)",
            to="(unpool_{}-east)".format(name),
            s_filer=str(s_filer),
            n_filer=str(n_filer[0]),
            width=width[0],
            height=height,
            depth=depth,
            opacity=opacity
            ),       
        to_SepConv(
            name='ccr_{}'.format(name),
            offset="(0,0,0)",
            to="(ccr_res_{}-east)".format(name),
            s_filer=str(s_filer),
            n_filer=str(n_filer[1]),
            width=width[1],
            height=height,
            depth=depth
            ),
        to_SepConv(
            name='{}'.format(top),
            offset="(0,0,0)",
            to="(ccr_{}-east)".format(name),
            s_filer=str(s_filer),
            n_filer=str(n_filer[2]),
            width=width[2],
            height=height,
            depth=depth
            ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]

def block_Unconv( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]




def block_Res( num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            s_filer=str(s_filer), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


