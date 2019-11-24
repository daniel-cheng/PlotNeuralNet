
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

    #block-001
    to_XceptionElu( name='entry_b1', s_filer=224, n_filer=(128,128,128), offset="(0,0,0)", to="(0,0,0)", width=(2.75,2.75,2.75), height=40, depth=40 ),
    to_Pool(name="pool_entry_b1", offset="(0,0,0)", to="(entry_b1-east)", width=1, height=32, depth=32, opacity=0.5),
    
    *block_XceptionPool( name='entry_b2', botton='pool_entry_b1', top='pool_entry_b2', s_filer=112, n_filer=(256,256,256), offset="(1.5,0,0)", width=(3.0,3.0,3.0), height=32, depth=32, opacity=0.5 ),
    *block_XceptionPool( name='entry_b3', botton='pool_entry_b2', top='pool_entry_b3', s_filer=56, n_filer=(728,728,728), offset="(1.5,0,0)", width=(3.5,3.5,3.5), height=25, depth=25, opacity=0.5 ),

    #Bottleneck
    #block-005
    to_XceptionElu( name='middle_b1', s_filer=28, n_filer=(728,728,728), offset="(1.5,0,0)", to="(pool_entry_b3-east)", width=(3.5,3.5,3.5), height=15, depth=15, caption="" ),
    to_connection( "pool_entry_b3", "middle_b1"),

    *block_XceptionPoolDashed( name='exit_b1', botton='middle_b1', top='end_exit_b1', s_filer=28, n_filer=(728,1024,1024), offset="(5,0,0)", width=(3.5,4,4), height=12, depth=12, opacity=0.5, caption=""),
    *block_XceptionPool( name='exit_b2', botton='end_exit_b1', top='end_exit_b2', s_filer=14, n_filer=(1536,1536,2048), offset="(1,0,0)", width=(4.5,5,5), height=5, depth=5, opacity=0.5 ),

    #Decoder
    to_Conv( name='aspp_b0', offset="(0,6.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=1' ),
    to_Conv( name='aspp_b1', offset="(0,4.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=1' ),
    to_Conv( name='aspp_b2', offset="(0,2.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=2' ),
    #to_UnPool( name='aspp_b4', offset="(0,-2,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=10, depth=10, caption='maxpool' ),
    #to_Conv( name='aspp_b4', offset="(0,-2,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3.25, height=10, depth=10, caption='maxpool' ),
    to_Conv( name='aspp_b3', offset="(0,-2.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=3' ),
    to_Conv( name='aspp_b5', offset="(0,-4.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=4' ),
    to_Conv( name='aspp_b6', offset="(0,-6.0,0)", to="(end_exit_b2-east)", s_filer=14, n_filer=256, width=3, height=5, depth=5, caption='rate=5' ),

    to_Add(name="add_b0", offset="(1.5,0,0)", to="(end_exit_b2-east)", radius=0.33, scale=1, opacity=0.5),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b0-east"),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b1-east"),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b2-east"),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b3-east"),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b5-east"),
    to_connection_straight( "end_exit_b2-northeast", "aspp_b6-east"),
    to_connection_straight( "aspp_b0-east", "add_b0-north"),
    to_connection_straight( "aspp_b1-east", "add_b0-north"),
    to_connection_straight( "aspp_b2-east", "add_b0-north"),
    to_connection_straight( "aspp_b3-east", "add_b0-south"),
    to_connection_straight( "aspp_b5-east", "add_b0-south"),
    to_connection_straight( "aspp_b6-east", "add_b0-south"),
    to_connection( "end_exit_b2", "add_b0"),
    to_skip( of='middle_b1', to='add_b0', pos=1.25),    

    *block_UnconvDeeplab( name="b7", botton="add_b0", top='end_b7', s_filer=14, n_filer=256, offset="(1.5,0,0)", size=(25,25,4.5), opacity=0.5 ),
    to_skip( of='ccr_entry_b3', to='ccr_res_b7', pos=1.25),    
    
    to_ConvSoftMax( name="sigmoid1", s_filer=224, n_filer=2, offset="(2.0,0,0)", to="(end_b7-east)", width=1, height=40, depth=40, caption="Sigmoid" ),
    to_connection( "end_b7", "sigmoid1"),
     
    to_end_image('Upernavik-NE_LT05_L1TP_1995-09-09_017-008_T1_B4_mask.png', name="output", to="(sigmoid1-east)") 
    #to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
