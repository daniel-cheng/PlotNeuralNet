
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
    to_ConvSoftMax( name="input1", s_filer="Resolution", n_filer=("filters",0,0), offset="(0,0,0)", width=4, height=10, depth=10, fontsize='\small', caption="I/O Block" ),

    to_SepConv( name='conv', offset="(2.5,0,0)", to="(input1-east)", width=4, height=10, depth=10, caption="Convolution" ),

    to_Pool(name="pool_entry_b1", offset="(2.5,0,0)", to="(conv-east)", width=4, height=10, depth=10, opacity=0.5, caption="Max-Pool" ),
    to_connection_straight( "conv-east", "pool_entry_b1-west", style="--", connection="dashed-connection", arrow='\midarrow', caption="Repeat" ),

    to_UnPool( name='aspp_b4_unpool', offset="(2.5,0,0)", to="(pool_entry_b1-east)", width=4, height=10, depth=10, caption="Upsample" ),
    to_connection_straight( "pool_entry_b1-east", "aspp_b4_unpool-west", style="--", arrow='\midarrow', caption="Flow" ),

    to_ConvRes(name='concat0', offset="(2.5,0,0)", to="(aspp_b4_unpool-east)", width=4, height=10, depth=10, caption="Concatenate" ),       
    to_skip( of="aspp_b4_unpool", to="concat0", pos=1.25, caption="Skip"),

     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
