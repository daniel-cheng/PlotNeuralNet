
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

#* will "extend" the list container, so that the elements that are returned are added to arch, instead of a list of elements.

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'Upernavik-NE_LT05_L1TP_1995-09-09_017-008_T1_B4.png' ),

    #entry flow
    to_XceptionElu( name='entry_b1', s_filer=224, n_filer=(128,128,128), offset="(0,0,0)", to="(0,0,0)", width=(2.75,2.75,2.75), height=40, depth=40 ),
    to_Pool(name="pool_entry_b1", offset="(0,0,0)", to="(entry_b1-east)", width=1, height=23.78, depth=23.78, opacity=0.5),
    
    *block_XceptionPool( name='entry_b2', botton='pool_entry_b1', top='pool_entry_b2', s_filer=112, n_filer=(256,256,256), offset="(1.75,0,0)", width=(3.25,3.25,3.25), height=23.78, depth=23.78, pool_height=14.14, pool_depth=14.14, opacity=0.5 ),
    *block_XceptionPool( name='entry_b3', botton='pool_entry_b2', top='pool_entry_b3', s_filer=56, n_filer=(728,728,728), offset="(1.25,0,0)", width=(3.85,3.85,3.85), height=14.14, depth=14.14, pool_height=8.4, pool_depth=8.4, opacity=0.5 ),

    #middle flow
    to_XceptionElu( name='middle_b1', s_filer=28, n_filer=(728,728,728), offset="(0.75,0,0)", to="(pool_entry_b3-east)", width=(3.85,3.85,3.85), height=8.4, depth=8.4, caption="" ),
    to_connection( "pool_entry_b3", "middle_b1"),

    #exit flow
    *block_XceptionPoolDashed( name='exit_b1', botton='middle_b1', top='end_exit_b1', s_filer=28, n_filer=(728,1024,1024), offset="(2.0,0,0)", width=(3.85,4.4,4.4), height=8.4, depth=8.4, pool_height=5, pool_depth=5, opacity=0.5, caption=""),
    *block_XceptionPool( name='exit_b2', botton='end_exit_b1', top='end_exit_b2', s_filer=14, n_filer=(1536,1536,2048), offset="(0.7,0,0)", width=(5.3,5.3,5.9), height=5, depth=5, pool_height=2.97, pool_depth=2.97, opacity=0.5 ),
    to_SepConv( name='image_pooling', offset="(0.75,0,0)", to="(end_exit_b2-east)", s_filer=7, n_filer=256, width=3.25, height=2.97, depth=2.97 ),

    #ASPP
    to_SepConv( name='aspp_b0', offset="(1.75,6.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_SepConv( name='aspp_b1', offset="(1.75,4.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_SepConv( name='aspp_b2', offset="(1.75,2.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_UnPool( name='aspp_b4_unpool', offset="(0.75,0,0)", to="(image_pooling-east)", width=1, height=5, depth=5 ),
    to_SepConv( name='aspp_b4', offset="(0,0,0)", to="(aspp_b4_unpool-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_SepConv( name='aspp_b3', offset="(1.75,-2.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_SepConv( name='aspp_b5', offset="(1.75,-4.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_SepConv( name='aspp_b6', offset="(1.75,-6.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),

    to_ConvRes( name='concat0', offset="(3.8,0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=1792, width=5.5, height=5, depth=5, opacity=0.5),
    #to_Add(name="concat0", offset="(4.0,0,0)", to="(end_exit_b2-east)", radius=0.33, scale=1, opacity=0.5),
    to_connection_straight( "ccr_exit_b2-northeast", "aspp_b0-west", style="|-"),
    to_connection_straight( "ccr_exit_b2-northeast", "aspp_b1-west", style="|-"),
    to_connection_straight( "ccr_exit_b2-northeast", "aspp_b2-west", style="|-"),
    to_connection_straight( "image_pooling-east", "aspp_b4_unpool-west", style="--", arrow='\midarrow'),
    to_connection_straight( "end_exit_b2-east", "image_pooling-west", style="--", arrow='\midarrow'),
    to_connection_straight( "ccr_exit_b2-southeast", "aspp_b3-west", style="|-"),
    to_connection_straight( "ccr_exit_b2-southeast", "aspp_b5-west", style="|-"),
    to_connection_straight( "ccr_exit_b2-southeast", "aspp_b6-west", style="|-"),
    to_connection_straight( "aspp_b0-east", "concat0-north", style="-|"),
    to_connection_straight( "aspp_b1-east", "concat0-north", style="-|"),
    to_connection_straight( "aspp_b2-east", "concat0-north", style="-|"),
    to_connection_straight( "aspp_b3-east", "concat0-south", style="-|"),
    to_connection_straight( "aspp_b4-east", "concat0-west", style="--", arrow='\midarrow'),
    to_connection_straight( "aspp_b5-east", "concat0-south", style="-|"),
    to_connection_straight( "aspp_b6-east", "concat0-south", style="-|"),


    #Decoder
    to_SepConv( name='feature_projection0', offset="(0.85,0,0)", to="(concat0-east)", s_filer=14, n_filer=256, width=3.25, height=5, depth=5 ),
    to_connection( "concat0", "feature_projection0"),

    *block_UnconvDeeplab( name="feature_projection1", botton="feature_projection0", top='end_feature_projection1', s_filer=56, n_filer=(308,256,256), offset="(1.1,0,0)", width=(3.5,3.25,3.25), height=14.4, depth=14.4, opacity=0.5 ),
    to_skip( of='ccr_entry_b3', to='ccr_res_feature_projection1', pos=3.0),    
    
    to_UnPool( name='last_unpool', offset="(2.15,0,0)", to="(end_feature_projection1-east)", width=1, height=40, depth=40 ),
    to_ConvSoftMax( name="sigmoid1", s_filer=224, n_filer=2, offset="(0,0,0)", to="(last_unpool-east)", width=1, height=40, depth=40, caption="Sigmoid" ),
    to_connection( "end_feature_projection1", "last_unpool"),
     
    to_end_image('Upernavik-NE_LT05_L1TP_1995-09-09_017-008_T1_B4_mask.png', name="output", to="(sigmoid1-east)") 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
