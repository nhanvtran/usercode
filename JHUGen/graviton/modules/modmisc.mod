	  +  %   k820309              11.0        �~O                                                                                                           
       mod_Misc.F90 MODMISC                                                           o #MINKOWSKYPRODUCT    #MINKOWSKYPRODUCTC                                                              o #VECTORCROSS    %         @    X                                             
       #P1    #P2              
      �                                              
    p          & p        p            p                                    
      �                                              
    p          & p        p            p                          %         @    X                                                     #P1    #P2              
      �                                                  p          & p        p            p                                    
      �                                                  p          & p        p            p                          (         `    X �                                                            
    #P1    #P2 	   p          & p        p            p                                    
      �                                              
    p          & p        p            p                                    
      �                           	                   
    p          & p        p            p                          %         @                               
                  
       #GET_PT%DSQRT    #MOM                                                    DSQRT                �                                              
     p          & p        p            p                          %         @                                                  
       #MOM                   �                                              
 	    p          & p        p            p                          %         @                                                 
       #GET_MINV%DSQRT    #MOM                                                    DSQRT                �                                              
 
    p          & p        p            p                          %         @                                                
       #GET_ETA%DLOG    #MOM                                                    DLOG                �                                              
     p          & p        p            p                          %         @                                                
       #GET_PHI%DATAN2    #MOM                                                    DATAN2                �                                              
     p          & p        p            p                          %         @                                                 
       #GET_R%DABS    #GET_R%DSQRT    #MOM1    #MOM2                                                    DABS                                                 DSQRT           D @   �                                              
     p          & p        p            p                                    D @   �                                              
     p          & p        p            p                          #         @                                                    #ERROR%PRESENT    #MESSAGE    #ERRNUM                                                     PRESENT                                                                1            @                                            %         @                                !                          #X "                                             "     
          �         fn#fn    �   m      u@DOT    *  Q      u@CROSS !   {  `       MINKOWSKYPRODUCT $   �  �   a   MINKOWSKYPRODUCT%P1 $     �   a   MINKOWSKYPRODUCT%P2 "   #  `       MINKOWSKYPRODUCTC %   �  �   a   MINKOWSKYPRODUCTC%P1 %   '  �   a   MINKOWSKYPRODUCTC%P2    �  �       VECTORCROSS    �  �   a   VECTORCROSS%P1    3  �   a   VECTORCROSS%P2    �  k       GET_PT    B  >      GET_PT%DSQRT    �  �   a   GET_PT%MOM    $  Y       GET_PT2    }  �   a   GET_PT2%MOM    !	  m       GET_MINV    �	  >      GET_MINV%DSQRT    �	  �   a   GET_MINV%MOM    p
  k       GET_ETA    �
  =      GET_ETA%DLOG      �   a   GET_ETA%MOM    �  m       GET_PHI    )  ?      GET_PHI%DATAN2    h  �   a   GET_PHI%MOM      �       GET_R    �  =      GET_R%DABS    �  >      GET_R%DSQRT      �   a   GET_R%MOM1    �  �   a   GET_R%MOM2    T  t       ERROR    �  @      ERROR%PRESENT      L   a   ERROR%MESSAGE    T  @   a   ERROR%ERRNUM    �  W       ISNAN    �  @   a   ISNAN%X 