# MIT License

# Copyright (c) 2024 Guzman Tierno

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from manim import *
import random 
from math import *

# colors
EMPY_SET_COLOR = RED
BORDER_COLOR = WHITE
HIGHLIGHT_BORDER_COLOR = YELLOW

# braces
open_braces = { "(", "[", "{", "<" }
close_braces = { ")", "]", "}", ">" }

# spacing and heights
STD_SPACING = 0.06                      
SPACING = STD_SPACING
SPACING2 = 0.25
FLOOR_RATIO = 0.9
CORNER_RADIUS = 0.3                 
CORNER_RATIO = 0.9
BORDER_WIDTH = 4

# zones
RIGHT_MARGIN = 6
LEFT_MARGIN = -6
DISPLAY_WIDTH = 1
TOP_MARGIN = 4
BOTTOM_MARGIN = -4
DISPLAY_HEIGHT = 1
DISPLAY_SPACING = 0.25

# TODO: space of blocks according to the number of sons - respace after changes
# TODO: display for music notes
# TODO: notes-as-stairs display

# 🎆🎇✨🎻🪕  

# Tower Structure. This class is NOT IN USE.
# This represents the structure of a tower. 
# The class has not been actually used in the final project.
# the empty tower may have subtowers set to None
# or it may have an empty list of subtowers.


# Class for towers. 
class Tower(VGroup):

    instrument_icon = None

    # constructor
    def __init__(
            self, 
            block_width = 2, 
            block_height = 1, 
            corner_radius = CORNER_RADIUS,
            border_width = BORDER_WIDTH,
        ):

        super().__init__()

        self.block_width = block_width
        self.block_height = block_height

        self.parts = VGroup()
        self.subtowers = VGroup()

        self.submobjects.append(self.parts)
        self.submobjects.append(self.subtowers)

        self.rect = RoundedRectangle(
            width=block_width, height=block_height, corner_radius=corner_radius, fill_opacity=1, color=BLUE_D
        )
        self.border = RoundedRectangle(
            width=block_width, height=block_height, corner_radius=corner_radius, color=BORDER_COLOR,
            stroke_width=border_width
        )

        self.parts.add(self.rect)
        self.parts.add(self.border)

    # count descendants
    def count_descendants(self):

        total = 0
        if self.subtowers is not None:
            for st in self.subtowers:
                total += st.count_descendants()            

        return total+1
    
    # children count
    def count_children(self):

        if self.subtowers is None:
            return 0
        
        return len(self.subtowers)
    
    

    # count floors    
    def count_floors(self):

        max = 0

        if not self.subtowers is None:
            for t in self.subtowers:
                n = t.count_floors() + 1
                if n>max:
                    max = n
        
        return max 


    # set block border color
    def set_block_border_color(self, scene, color, transition_run_time=0.5):

        scene.play( 
            self.border.animate.set_color(color), run_time=transition_run_time 
        )

    # set block border color
    def set_block_color(self, scene, color, transition_run_time=0.5):

        scene.play( 
            self.parts.animate.set_color(color), run_time=transition_run_time 
        )

    # set tower border color
    def set_tower_border_color(self, scene, color, transition_run_time=0.05):
        scene.play( 
            self.border.animate.set_color(color), run_time=transition_run_time 
        )

        for st in self.subtowers:
            st.set_tower_border_color(scene, color, transition_run_time)


    
    # highlight block 
    def highlight_block(self, scene, transition_run_time=0.5):

        self.set_block_color(scene, HIGHLIGHT_BORDER_COLOR, transition_run_time=transition_run_time)



    # recursively copy heights and widths
    def copy_measures_to_block(self):
        self.block_height = self.parts.height
        self.block_width = self.parts.width

        if self.subtowers is None:
            return
        
        for s in self.subtowers:
            s.copy_measures_to_block()


    # set base block width
    def set_block_width(self, block_width, level):

        # new_height = self.block_height * (0.9**level)

        self.scale_to_fit_width( block_width )

        self.copy_measures_to_block()


    # color by level 
    @staticmethod
    def select_color_by_level(level, type=0):
        if type == 0:
            colors = [ 
                BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A, 
                PURPLE_A, PURPLE_B, PURPLE_C, PURPLE_D, PURPLE_E, 
            ] 
        elif type == 1:
            colors = [ 
                YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A, 
                BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E, 
            ] 
        elif type == 2:
            colors = [ 
                YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A, 
                GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E, 
            ] 

        if level>len(colors)-1:
            level = len(colors)-1
        return colors[level]

    # sets subtowers for a new tower 
    def set_subtowers(self, subtowers, level=0, color_type=1):

        self.subtowers = VGroup()
        self.submobjects[1] = self.subtowers    

        if len(subtowers) == 0:
            self.rect.set_color( EMPY_SET_COLOR )
            
        for st in subtowers:
            self.subtowers.add(st)      

        return self

    # sets subtowers for a new tower and resizes them
    def set_and_resize_subtowers(self, subtowers, level=0, color_type=1):

        self.subtowers = VGroup()
        self.submobjects[1] = self.subtowers    

        self.rect.set_color( Tower.select_color_by_level(level, color_type) )

        n = len(subtowers)

        if n==0:
            self.rect.set_color( EMPY_SET_COLOR )
            
        if n>0:            
            subtowers_width = ( self.block_width - (n+1) * SPACING ) / n

            i=0
            x_spacing = SPACING
            top = self.get_top()
            left = self.get_left()
            for st in subtowers:
                self.subtowers.add(st)      
                st.set_block_width(subtowers_width, level)
                st.align_to([left[0]+x_spacing, 0, 0], LEFT)
                st.align_to([0, top[1], 0], DOWN)
                x_spacing += subtowers_width + SPACING
                i += 1

        return self


    # tower from string bottom up
    # returns (the tower, the index where it stopped)
    @staticmethod
    def from_string_bottom_up(
        string, 
        start = 0, block_width = 2, block_height = 1, corner_radius = CORNER_RADIUS,
        border_width = BORDER_WIDTH, level = 0, color_type = 0
    ):

        l = len(string)    
        i = start

        # remove spaces
        string = string.replace(' ', '')        

        if string[i] in open_braces:  
            st = []
            i += 1
            
            while i<l:                                                                      
                if string[i] in close_braces:
                    t = Tower(                      
                        block_width, block_height, corner_radius*(CORNER_RATIO**level), border_width
                    )
                    t.set_and_resize_subtowers(st, level, color_type)
                    return t, i

                # TODO: width factor 0.5
                sub_tower, end = Tower.from_string_bottom_up( 
                    string, i, 
                    block_width*0.5, block_height*FLOOR_RATIO, corner_radius, border_width,
                    level=level+1, color_type = color_type
                )

                if not sub_tower is None:
                    st.append(sub_tower)
                
                i = end + 1

    # select instrument 
    @staticmethod
    def select_instrument(probabilities):
        r = random.random()
        for i in range(len(probabilities)):
            if probabilities[i]>r:
                return i
            
        return 0

    # place_on_earth
    def place_on_earth(self, earth):

        return self.align_to( [0, earth.get_level(), 0], DOWN  )
    
    # place_on_base
    def place_on_base(self, base):

        return self.align_to( [0, base.get_top()[1], 0], DOWN  )


    # get_left of towers
    @staticmethod
    def get_left_of_towers( towers ):

        left = 7
        for t in towers:
            l = t.get_left()[0] 
            if l<left:
                left = l
        
        return left


    # get_right of towers
    @staticmethod
    def get_right_of_towers( towers ):

        right = -7
        for t in towers:
            r = t.get_right()[0] 
            if r>right:
                right = r
        
        return right

    # get_bottom of towers
    @staticmethod
    def get_bottom_of_towers( towers ):

        bottom = 7
        for t in towers:
            b = t.get_bottom()[1] 
            if b<bottom:
                bottom = b
        
        return bottom

    # get_top of towers
    @staticmethod
    def get_top_of_towers( towers ):

        top = -7
        for t in towers:
            t = t.get_top()[1] 
            if t>top:
                top = t
        
        return top


    # get_max_floors of towers
    @staticmethod
    def get_max_floors( towers ):

        max = 0
        for t in towers:
            f = t.count_floors()
            if f>max:
                max = f
        
        return max


    # towers container 
    @staticmethod       
    def towers_container(
        towers, corner_radius = CORNER_RADIUS, border_width = BORDER_WIDTH, 
        color_type = 0, height = 0
    ):

        left = Tower.get_left_of_towers( towers )
        right = Tower.get_right_of_towers( towers )
        bottom = Tower.get_bottom_of_towers( towers )
        top = Tower.get_top_of_towers( towers )
        
        
        width = right-left + SPACING*2

        level = Tower.get_max_floors( towers )
        if height==0:
            height = (FLOOR_RATIO ** level )

        pos = [ (left+right)/2, bottom, 0 ]

        container = Tower( 
            width, height, corner_radius*(CORNER_RATIO ** level ), border_width 
        ).move_to(
            [pos[0], pos[1]+height/2, pos[2]]
        )

        color = Tower.select_color_by_level(level, color_type)
        container.rect.set_color( color )
        container.border.set_color( BORDER_COLOR ) 

        return container



    # raise towers creating new base
    @staticmethod
    def raise_towers(
        scene, towers, corner_radius = CORNER_RADIUS, border_width = BORDER_WIDTH, 
        instrument = None, color_type = 1, height = 0,
        transitions_run_time = 0.05
    ):
        container = Tower.towers_container(
            towers, corner_radius = corner_radius, border_width=border_width, 
            color_type = color_type, height=height
        )

        left = Tower.get_left_of_towers( towers )
        right = Tower.get_right_of_towers( towers )
        bottom = Tower.get_bottom_of_towers( towers )

        width = right-left + SPACING*2
        level = Tower.get_max_floors( towers )

        container.move_to( [7, bottom+container.block_height/2, 0] )
        scene.play( 
            container.animate.shift( [right-7-container.block_width/2+width, 0, 0] )  
        )


        i = len(towers)-1
        for i in range(len(towers)-1, -1, -1):
            t = towers[i]
            
            count_children = t.count_children()
            instruments = scene.instrument_player.play_sound( level, count_children )

            scene.play( 
                t.animate.shift([0, container.block_height, 0 ]),
                run_time = transitions_run_time
            )
            t.save_state()
            scene.play(
                Rotate(t,PI/6), 
                *scene.instrument_display.vibrate(instruments, level ),
                run_time = transitions_run_time
            )
            scene.wait( 0.05 )
            scene.play(Rotate(t,-PI/6), run_time = transitions_run_time)
            t.restore()

            scene.play( 
                container.animate.shift( [-t.block_width-SPACING, 0, 0] ),
                run_time = transitions_run_time  
            )

        scene.play( 
            container.animate.move_to(  
                [(left+right)/2, bottom+container.block_height/2, 0]
            ),
            run_time = transitions_run_time  
        )

        container.set_subtowers(towers)
        scene.wait(1)

        return container



    # raise towers with existing base
    @staticmethod
    def raise_towers_with_base( 
        scene, towers, base, transitions_run_time = 0.05
    ):

        far_right = 7    

        left = Tower.get_left_of_towers( towers )
        right = Tower.get_right_of_towers( towers )
        bottom = Tower.get_bottom_of_towers( towers )

        width = right-left + SPACING*2

        base.parts.move_to(  [far_right,bottom,0]   )    
        base.parts.align_to(  [0,bottom,0], DOWN   )    

        scene.wait(transitions_run_time)

        scene.play( 
            base.parts.animate.shift( [right-far_right-base.block_width/2+width, 0, 0] ),
            run_time = transitions_run_time
        )


        scene.wait(transitions_run_time)

        i = len(towers)-1
        for i in range(len(towers)-1, -1, -1):
            t = towers[i]

            level = t.count_floors()
            count_children = t.count_children()
            
            instruments = scene.instrument_player.play_sound( level, count_children )

            scene.play( 
                t.animate.align_to( base.border.get_top(), DOWN ),
                run_time = transitions_run_time
            )
            t.save_state()
            scene.play(
                Rotate(t,PI/6), 
                *scene.instrument_display.vibrate(instruments, level ),
                *scene.level_display.update(level=level ),
                *scene.subtowers_display.update(subtowers=count_children ),
                run_time = transitions_run_time
            )
            scene.wait( 0.05 )  

            scene.play(
                Rotate(t,-PI/6),
                base.parts.animate.align_to( t, LEFT ),
                *scene.earth.vibrate(1.01, 0.01),
                run_time = transitions_run_time  
            )
            t.restore()


        scene.play(
            base.parts.animate.shift(  
                [ (left+right)/2 - base.parts.get_center()[0], 0, 0] 
            ), 
            run_time = transitions_run_time  
        )

        scene.wait(transitions_run_time)


    # raise towers with existing base, from left to right
    @staticmethod
    def raise_towers_with_base2( 
        scene, towers, base, transitions_run_time = 0.05
    ):

        far_left = -7    

        left = Tower.get_left_of_towers( towers )
        right = Tower.get_right_of_towers( towers )
        bottom = Tower.get_bottom_of_towers( towers )

        width = right-left + SPACING*2

        base.parts.move_to(  [far_left,bottom,0]   )    
        base.parts.align_to(  [0,bottom,0], DOWN   )    

        scene.wait(transitions_run_time)

        scene.play( 
            base.parts.animate.shift( [-left+far_left+base.block_width/2+width, 0, 0] ),
            run_time = transitions_run_time
        )


        scene.wait(transitions_run_time)

        i = 0
        for i in range(0,len(towers)):
            t = towers[i]

            level = t.count_floors()
            count_children = t.count_children()
            
            instruments = scene.instrument_player.play_sound( level, count_children )

            scene.play( 
                t.animate.align_to( base.border.get_top(), DOWN ),
                run_time = transitions_run_time
            )
            t.save_state()
            scene.play(
                Rotate(t,-PI/6), 
                *scene.instrument_display.vibrate(instruments, level ),
                *scene.level_display.update(level=level ),
                *scene.subtowers_display.update(subtowers=count_children ),
                run_time = transitions_run_time
            )
            scene.wait( 0.05 )  

            scene.play(
                Rotate(t,PI/6),
                base.parts.animate.align_to( t, RIGHT ),
                run_time = transitions_run_time  
            )
            t.restore()


        scene.play(
            base.parts.animate.shift(  
                [ -(left+right)/2 + base.parts.get_center()[0], 0, 0] 
            ), 
            run_time = transitions_run_time  
        )

        scene.wait(transitions_run_time)



    # raise tower: builds a towers showing animation and music
    # moves the existing layers to reach each one its position
    def raise_tower( 
        self, scene, corner_radius = CORNER_RADIUS, border_width = BORDER_WIDTH, 
        color_type = 1, height = 0, transitions_run_time = 0.05, up = True,
        to_flush = None
    ):
        
        floor = scene.earth.get_level()
        
        if self.subtowers is None or len(self.subtowers) == 0:
            self.shift( [ 0, floor - self.get_bottom()[1] , 0 ] )
            scene.add( self.parts )

            expr_mobj = None
            if scene.expr_display is not None:
                expr_mobj = scene.expr_display.update(token = " () ", dir = RIGHT, color = RED)
            
            # also play when creating blocks (doesn't sound good)
            # instruments = scene.instrument_player.play_sound( 0, 0 )
            # scene.play( 
            #     Create(self.parts),
            #     *scene.instrument_display.vibrate(instruments, 0 ),
            #     *scene.level_display.update(level=0 ),
            #     run_time = transitions_run_time  
            # )
            # scene.wait(0.08)

            return expr_mobj
        
        if scene.expr_display is not None:
            saved_expr_mobj = scene.expr_display.copy_state()

        new_expressions = []
        for t in self.subtowers:            
            new_expr = t.raise_tower(
                scene, corner_radius, border_width, 
                color_type, height, transitions_run_time, up,
                to_flush = to_flush
            )
            new_expressions.append(new_expr)
            if to_flush is not None:
                to_flush.flush(scene, 0.02)
                to_flush = None

        self.raise_towers_with_base( scene, self.subtowers, self, transitions_run_time )
        color = Tower.select_color_by_level(floor)
        updated_new_expr_mobj = None
        if scene.expr_display is not None:
            updated_new_expr_mobj = scene.expr_display.reset_state(
                saved_expr_mobj, "( ", new_expressions, ") ", color
            )

        return updated_new_expr_mobj


    def raise_subtowers_with_new_base( 
        self, scene, transitions_run_time = 0.05
    ):
        new_bases = []
        for t in self.subtowers:            
            new_base = t.copy().set_color(YELLOW)
            new_bases.append(new_base)
            self.raise_towers_with_base(
                scene, [t], new_base, transitions_run_time = transitions_run_time
            )
            scene.play( new_base.rect.animate.set_color(BLUE_A) )

        return new_bases

    def add_base( self, scene, color, height = 1, transitions_run_time= 0.05 ):
        base , _ = Tower.from_string_bottom_up( " ( ) ", 0,  self.parts.width, height, 0.1 )
        base.rect.set_color(color)
        base.move_to( self )
        base.align_to( self.get_bottom(), DOWN)

        self.raise_towers_with_base(scene, [self], base, transitions_run_time )

        return base

    def successive( self, scene, color=YELLOW, height = 1, transitions_run_time = 0.05 ):

        base = self.add_base(scene, color, height, transitions_run_time )
        
        scene.play( 
            self.animate.scale(0.45), 
            run_time=transitions_run_time 
        )
        scene.play( 
            self.animate.align_to( base.parts.get_top(), DOWN), 
            run_time=transitions_run_time 
        )
        scene.play( 
            self.animate.align_to( [base.get_right()[0]-SPACING,0,0], RIGHT),
            run_time=transitions_run_time
        )
        cp = self.copy()

        scene.play( 
            cp.animate.align_to( [base.get_left()[0]+SPACING,0,0], LEFT),
            run_time = transitions_run_time            
        ) 

        base2 = self.add_base(scene, color, height*0.7, transitions_run_time )
        base2.set_subtowers([self])
        base.set_subtowers([cp, base2])

        base2.align_to( base.get_right(), RIGHT )

        return base

        












    # drop subtowers
    def drop_subtowers(self, scene, drop_run_time = 0.4, height = None ):

        if self.subtowers is None:
            return

        for t in self.subtowers:
            level = t.count_floors()
            center = t.get_center()
            if height is None:
                scene.play( 
                    t.animate.place_on_earth(scene.earth), 
                    run_time = drop_run_time 
                )
            else:
                scene.play( 
                    t.animate.align_to( [center[0], height, 0], DOWN  ), 
                    run_time = drop_run_time 
                )
            instruments = scene.instrument_player.play_sound( level, 0 )
            scene.play( 
                *scene.instrument_display.vibrate(instruments, level ),
                *scene.level_display.update(level=level ),
                *scene.earth.vibrate(),
                run_time = drop_run_time 
            )
            
            
    # drop tower
    def drop_tower(self, scene, drop_run_time = 0.4 ):

        t = self
        level = t.count_floors()
        children = t.count_children()
        scene.play( 
            t.animate.place_on_earth(scene.earth), 
            run_time = drop_run_time 
        )
        instruments = scene.instrument_player.play_sound( level, children )
        scene.play( 
            *scene.instrument_display.vibrate(instruments, level ),
            *scene.level_display.update(level=level ),
            *scene.earth.vibrate(),
            run_time = drop_run_time 
        )
        
    # drop tower
    def drop_tower_to_base(self, scene, base, drop_run_time = 0.4 ):

        t = self
        level = t.count_floors()
        children = t.count_children()
        scene.play( 
            t.animate.place_on_base(base), 
            run_time = drop_run_time 
        )
        instruments = scene.instrument_player.play_sound( level, children )
        scene.play( 
            *scene.instrument_display.vibrate(instruments, level ),
            *scene.level_display.update(level=level ),
            *scene.earth.vibrate(),
            run_time = drop_run_time 
        )
        
            
        
    # center subtowers
    def center_subtowers( self, scene, transition_run_time = 0.1 ):

        center = self.get_center()
        center2 = self.subtowers.get_center()

        scene.add_sound( "./sounds/whoosh.wav")
        scene.play(
            self.subtowers.animate.shift( [center[0] - center2[0], 0, 0] ),
            run_time = transition_run_time
        )
            
        
    # union
    def union( self, scene, transition_run_time = 0.1 ):

        if self.subtowers is None:
            return

        for t in self.subtowers:
            scene.play( Indicate(t.parts) )
            scene.add_sound("./sounds/zoop.wav")
            t.highlight_block(scene, transition_run_time=transition_run_time)

        scene.wait(3)

        subsubtowers = []
        for t in self.subtowers:
            scene.play( Uncreate(t.parts) )
            t.drop_subtowers(
                scene, drop_run_time = transition_run_time, 
                height = self.parts.get_top()[1]
            )
            if t.subtowers is not None and len(t.subtowers)>0:
                for sst in t.subtowers:
                    subsubtowers.append(sst)
        
        self.set_subtowers(subsubtowers)
        self.center_subtowers(scene, transition_run_time=transition_run_time)


    # equals
    def equals(self, other):

        if self.subtowers is None:
            return other.subtowers is None
        
        if other.subtowers is None:
            return False
            
        if len(self.subtowers) != len(other.subtowers):
            return False
        
        for i in range(len(self.subtowers)):
            if not self.subtowers[i].equals( other.subtowers[i] ):
                return False

        return True
    
    # non equality != for towers structures
    def not_equals(self, other):

        return not self.equals(other)

    # remove duplicate subtowers
    def remove_duplicate_subtowers(self, scene, step_run_time):
        if self.subtowers is None:
            return self
        
        st = self.subtowers

        i = 0
        to_remove = []
        while i < len(st)-1:
            j = i+1
            while j < len(st):
                if st[i].equals( st[j] ):
                    to_remove.append(st[j])
                    
                    scene.play( Indicate(st[i]), run_time = step_run_time ) 
                    scene.play( Indicate(st[j]), run_time = step_run_time )
                    scene.add_sound( "./sounds/laser1.wav", gain = -4)        
                    scene.play( Uncreate(st[j]), run_time = step_run_time )                                        
                j += 1
            i += 1

        for k in to_remove:
            st.remove(k)
        if len(to_remove)>0:
            self.set_subtowers(st)   
            self.center_subtowers(scene)
            

        return self

    # remove duplicate subtowers recursively
    def remove_duplicate_subtowers_recursively(self, scene, step_run_time = 0.5):
        if self.subtowers is None:
            return self
        
        for t in self.subtowers:
            t.remove_duplicate_subtowers_recursively(scene, step_run_time = step_run_time)

        self.remove_duplicate_subtowers(scene, step_run_time = step_run_time)

        return self


    # swap subtowers
    def swap_subtowers(self, scene, i, j, run_time = 0.5):

        if self.subtowers is None:
            return
        
        if i>=len(self.subtowers) or j>=len(self.subtowers):
            return

        scene.add_sound( "./sounds/whoosh.wav" )
        scene.play( Swap(self.subtowers[i], self.subtowers[j]), run_time = run_time )
        scene.play(
            self.subtowers[i].animate.align_to( [0, self.parts.get_top()[1], 0], DOWN  ),
            self.subtowers[j].animate.align_to( [0, self.parts.get_top()[1], 0], DOWN  ),
            run_time = run_time
        )



        temp = self.subtowers[i]
        self.subtowers[i] = self.subtowers[j]
        self.subtowers[j] = temp

        return self

    # resize 
    def resize(self, scene, step_run_time = 0.1):

        scene.play( 
            self.parts.animate.stretch_to_fit_width( 
                self.parts.width*( 0.8 + random.random()*0.5 )
            ),
            run_time = step_run_time
        )

        for t in self.subtowers:
            if random.random()>0.8:
                scene.play( 
                    t.animate.stretch_to_fit_width( t.width*0.6  ),
                    run_time = step_run_time
                )
            else:
                scene.play( 
                    t.animate.stretch_to_fit_height( 
                        t.height * ( 0.8 + random.random()*0.7 )
                    ),
                    run_time = step_run_time
                )
                scene.play( 
                    t.animate.align_to( [0, self.parts.get_top()[1], 0], DOWN  ),
                    run_time = step_run_time
                )
            t.resize(scene)
        


    # select subtowers
    def select_subtowers(self, scene, check_function, step_run_time = 0.5):

        st = self.subtowers
        to_remove = []
        for t in self.subtowers:
            scene.play( Indicate(t), run_time = step_run_time )
            scene.add_sound( "./sounds/laser1.wav", gain=-4 )
            if not check_function(self, t):
                to_remove.append(t)                
                scene.play( Uncreate(t), run_time = step_run_time )                    

        for k in to_remove:
            st.remove(k)

        if len(to_remove)>0:
            self.set_subtowers(st)            
            self.center_subtowers(scene)


    def flush(self, scene, run_time=0.05):

        scene.play( self.animate.align_to([-9, 0, 0], RIGHT), run_time=run_time)




# ---------------------------------

# base class for instrument displays (they implement vibrate)
class InstrumentDisplay():

    def __init__(self, instruments, colors) -> None:
        self.icons = []

        for i in range(len(instruments)):
            self.icons.append( self.get_icon(instruments[i], colors[i]) )

    def get_icon(self, instrument, color = None):

        if color is not None:
            instrument.icon.set_color(color)

        return instrument.icon

    
    def vibrate( self, instruments, level, subtowers = None ):
        pass

# display with separate instruments
class InstrumentSeparateDisplay(InstrumentDisplay):

    def __init__(
            self, scene, instruments, colors, on_opacities, off_opacities
    ) -> None:
        super().__init__(instruments, colors)

        self.scene = scene
        self.instruments = instruments
        self.colors = colors
        self.on_opacities = on_opacities
        self.off_opacities = off_opacities
        self.instrument_count = len(instruments)

        self.rect = RoundedRectangle(
            width=self.instrument_count, height=1, corner_radius=0.3, 
            color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0,TOP_MARGIN-DISPLAY_HEIGHT,0])
        self.rect.align_to([RIGHT_MARGIN,0,0], RIGHT)

        for i in range(len(self.icons)):
            self.icons[i].move_to([RIGHT_MARGIN-DISPLAY_WIDTH/2-i, self.rect.get_center()[1], 0])
            scene.add( self.rect ) 
            scene.add( self.icons[i] ) 
            self.icons[i].set_opacity(0)

    
    def vibrate( self, indices, level, subtowers = None ):
        for i in range(len(self.instruments)):
            if i in indices:
                self.icons[i].set_opacity(self.on_opacities[i])
            else:
                self.icons[i].set_opacity(self.off_opacities[i])

        return [
            Wiggle(self.icons[index], 1.2, 0.2, 4) for index in indices
        ]

# display that alternates instruments
class InstrumentAlternateDisplay(InstrumentDisplay):

    def __init__(self, scene, instruments, colors, off_opacity=0.1 ) -> None:
        super().__init__(instruments, colors)

        self.scene = scene
        self.instruments = instruments
        self.colors = colors
        self.current_icon = None
        self.off_opacity = off_opacity

        self.rect = RoundedRectangle(
            width=1, height=1, corner_radius=0.3, color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0,TOP_MARGIN-DISPLAY_HEIGHT,0])
        self.rect.align_to([RIGHT_MARGIN,0,0], RIGHT)

        for icon in self.icons:
            icon.move_to(self.rect)

        self.current_icon = self.icons[0]
        scene.play( Create(self.rect), Create(self.current_icon) )


    def vibrate( self, instruments, level, subtowers = None ):
        if self.current_icon is not None:
            self.current_icon.set_opacity(self.off_opacity)
        self.current_icon = self.icons[ instruments[0] ]
        self.current_icon.set_opacity(1)
        return [Wiggle(self.icons[instruments[0]], 1.2, 0.2, 4)]

# base class for instrument players
class InstrumentPlayer():

    def __init__(self) -> None:
        pass


    def play_sound( self, level, subtowers_count ):
        pass

# Player that plays more instruments separately (ie: at the same time)
class InstrumentSeparatePlayer( InstrumentPlayer ):

    def __init__( 
        self, scene, instruments, probabilities, gains, instrument_display,
        use = "nesting", up = True                 
    ):
        self.scene = scene
        self.instruments = instruments
        self.probabilities = probabilities
        self.instrument_display = instrument_display
        self.up = up
        self.use = use
        self.gains = gains
    
    def play_sound( self, level, subtowers_count ):

        selected = []

        for i in range(len(self.instruments)):
            if random.random()<self.probabilities[i]:
                selected.append(i)

        if self.use == "nesting":         
            note = level
        else: 
            note = subtowers_count

        for i in range(len(selected)):
            sounds = self.instruments[selected[i]].sounds(note)
            
            for s in sounds:
                self.scene.add_sound( s, gain = self.gains[selected[i]] )  

        return selected


# Player that plays instruments alternatively    
class InstrumentAlternatePlayer( InstrumentPlayer ):

    def __init__( 
        self, scene, instruments, probabilities, gains, instrument_display, 
        use = "nesting", up=True 
    ):

        self.scene = scene
        self.instruments = instruments
        self.probabilities = probabilities
        self.instrument_display = instrument_display
        self.up = up
        self.use = use
        self.gains = gains

    
    # select instrument 
    def select_instrument(self):
        r = random.random()
        total = 0
        for i in range(len(self.probabilities)):
            total += self.probabilities[i]
            if total>r:
                return i
        
        return None
    

    def play_sound( self, level, subtowers_count ):

        i = self.select_instrument()

        if self.use == "nesting":
            note = level
        else: 
            note = subtowers_count

        sounds = self.instruments[i].sounds(note)
        
        for s in sounds:
            self.scene.add_sound( s, self.gains[i] )  

        return [i]
    
    
    
# base class for displays (they implement update)
class TowerAppDisplay():

    def __init__(self) -> None:
        pass

    def update(self, level = None, subtowers = None, rule = None):
        pass

# null display
class NullDisplay():

    def __init__(self, scene) -> None:
        self.scene = scene
        return

    def update(self, level = None, subtowers = None, rule = None):
        return []

# display for level
class LevelDisplay(TowerAppDisplay):

    def __init__(self, scene) -> None:
        
        self.scene = scene
        self.rect = RoundedRectangle(
            width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, 
            corner_radius=0.3, color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0,TOP_MARGIN - DISPLAY_HEIGHT*2 - DISPLAY_SPACING,0])
        self.rect.align_to([RIGHT_MARGIN,0,0], RIGHT)
        scene.add( self.rect )
        lvl = Text("lvl", font_size = 14, color = BLUE).move_to(self.rect)
        lvl.align_to([0,self.rect.get_top()[1]-0.05,0], UP)
        scene.add(lvl)

        self.value = "."
        self.num = Text(self.value).move_to(self.rect)

    def update(self, level = None, subtowers = None, rule = None):            

        self.value = level
        self.tmp = self.num
        self.num = Text(str(level), color=Tower.select_color_by_level(level))
        if level == -1:
            self.num = Text(str("∞"), color=Tower.select_color_by_level(1))
        self.num.move_to(self.rect) 
        
        return [ReplacementTransform(self.tmp, self.num)]
    
# display for number of subtowers
class SubtowersDisplay(TowerAppDisplay):

    def __init__(self, scene) -> None:
        
        self.scene = scene
        self.rect = RoundedRectangle(
            width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, 
            corner_radius=0.3, color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0,TOP_MARGIN - DISPLAY_HEIGHT*3 - DISPLAY_SPACING*2,0])
        self.rect.align_to([RIGHT_MARGIN,0,0], RIGHT)
        scene.add( self.rect )
        chd = Text("children", font_size = 14, color = BLUE).move_to(self.rect)
        chd.align_to([0,self.rect.get_top()[1]-0.05,0], UP)
        scene.add(chd)

        self.value = "."
        self.num = Text(self.value).move_to(self.rect)

    def update(self, level = None, subtowers = None, rule = None):            

        self.value = level
        self.tmp = self.num
        self.num = Text(str(subtowers), color=Tower.select_color_by_level(subtowers))
        self.num.move_to(self.rect) 
        
        return [ReplacementTransform(self.tmp, self.num)]

# display for rule being used
class RuleDisplay(TowerAppDisplay):

    def __init__(self, scene, title = None, subtitle = None, blocks = 5) -> None:

        if title is None and subtitle is None:
            return
        
        self.scene = scene
        self.rect = RoundedRectangle(
            width=DISPLAY_WIDTH*blocks, height=DISPLAY_HEIGHT, 
            corner_radius=0.3, color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0,TOP_MARGIN - DISPLAY_HEIGHT,0])
        self.rect.align_to([LEFT_MARGIN,0,0], LEFT)
        scene.add( self.rect )

        if title is not None:
            txt = Text(title, color = YELLOW, font_size = 18).move_to(self.rect)
            # txt.stretch_to_fit_width(DISPLAY_WIDTH*3)
            txt.align_to([self.rect.get_left()[0]+0.3,0], LEFT)
            txt.align_to([0,self.rect.get_top()[1]-0.05,0], UP)
            scene.add(txt)

        self.rule = subtitle
        txt2 = Text(subtitle, color = YELLOW)
        # txt2.stretch_to_fit_width(DISPLAY_WIDTH*2)
        txt2.align_to([self.rect.get_left()[0]+0.4,0], LEFT)
        txt2.align_to([0,self.rect.get_bottom()[1]+0.1,0], DOWN)
        self.txt2 = txt2
        scene.add(txt2)

    def update(self, level = None, subtowers = None, rule = None):            
        return []


# display for the expression of the set (or tower)
class ExpressionDisplay():

    def __init__(self, scene, blocks = 10) -> None:

        self.scene = scene
        self.rect = RoundedRectangle(
            width=DISPLAY_WIDTH*blocks, height=DISPLAY_HEIGHT, 
            corner_radius=0.3, color=BORDER_COLOR, stroke_width=2
        )
        self.rect.move_to([0, BOTTOM_MARGIN + DISPLAY_HEIGHT,0])
        self.expr_mobj = VGroup().move_to(self.rect)
        self.saved_expr_mobj = None
        self.new_expr_mobj = VGroup().move_to(self.rect)
        scene.add( self.rect )

    def update(self, token = None, dir = RIGHT, color = BLUE):            
        if token is not None:
            self.scene.remove(self.expr_mobj)

            expr = Text(token, color = color).next_to(self.expr_mobj, dir)        
            self.expr_mobj.add( expr ).move_to(self.rect)
    
            self.display_expression()

            return expr
    
    def display_expression(self):

        if self.expr_mobj.width>self.rect.width:
            self.expr_mobj.stretch_to_fit_width(self.rect.width)

        self.scene.add( self.expr_mobj )



    def copy_state(self):
        return self.expr_mobj.copy()

    def reset_state( self, old_state, token1, new_expressions, token2, color ):

        self.scene.remove( self.expr_mobj )
        self.expr_mobj = old_state

        open = Text(token1, color = color).next_to(self.expr_mobj, RIGHT) 

        current = open
        for n in new_expressions:
            n.next_to(current, RIGHT)
            current = n

        close = Text(token2, color = color).next_to(current, RIGHT) 

        updated_new_expr_mobj = VGroup()
        updated_new_expr_mobj.add( open )
        updated_new_expr_mobj.add( *new_expressions )
        updated_new_expr_mobj.add( close )

        self.expr_mobj.add(updated_new_expr_mobj)

        self.expr_mobj.move_to( self.rect )

        self.display_expression()

        return updated_new_expr_mobj
        




        
        



# Earth object where towers lie
class Earth(VGroup):

    def __init__(self, level, minx, maxx) -> None:
        super().__init__()
        self.level = level
        self.minx = minx
        self.maxx = maxx
        self.line = Line([minx, level, 0], [maxx, level, 0])        
        self.add(self.line)

    def get_level(self):
        return self.level

    def get_minx(self):
        return self.minx

    def get_maxx(self):
        return self.maxx

    def vibrate(self, scale = 1.15, angle = 0.02, level = None, subtowers = None, rule = None):
        return [Wiggle(self.line, scale_value=scale ,rotation_angle=angle)]

# Scales and Progressions
C_Major_Scale = ["C", "D", "E", "F", "G", "A", "B", "C2"]
E_Major_Scale = ["E", "Fs", "G#", "A", "B", "C2s", "D2s", "E2"]
Pentatonic_Scale = ["Cs", "Ds", "Fs", "Gs", "As" ]
Choords_1451 = [ ["C", "E", "G"], ["F", "A", "C"], ["G", "B", "D"], ["C", "E", "G"] ]
Diatonic_Scale = [ "F", "C", "G", "D", "F", "A", "E", "B"]

# Std scale used as default
Std_Scale = C_Major_Scale




class Instrument():

    def __init__(
        self, name, 
        icon_txt = None, 
        icon_color = YELLOW,
        icon_svg_file = None, 
        icon_svg_color = None,
        icon_svg_dir = "./instruments/svg/", 
        max = 8, 
        scale = Std_Scale

    ) -> None:
        self.name = name
        self.icon_txt = icon_txt
        if icon_txt is not None:
            self.icon_type = "txt"
        
        self.icon_svg_file = icon_svg_file
        if icon_svg_file is not None:
            self.icon_type = "svg"

        self.icon_svg_dir = icon_svg_dir

        self.max = max
        self.scale = scale

        if self.icon_type == "txt":
            self.icon = Text(self.icon_txt, color=icon_color)
            if self.icon.width>DISPLAY_WIDTH*0.9:
                self.icon.scale_to_fit_width(DISPLAY_WIDTH*0.9)
            if self.icon.height>DISPLAY_HEIGHT*0.9:
                self.icon.scale_to_fit_height(DISPLAY_HEIGHT*0.9)
        else:
            self.icon = SVGMobject( 
                icon_svg_dir + self.icon_svg_file + ".svg", height = 0.7*DISPLAY_HEIGHT, 
            )
            if icon_svg_color is not None:
                self.icon.set_color(icon_svg_color)

    def set_scale( self, scale ):

        self.scale = scale

    def sounds(self, number):
        if self.max<1:
            return []        # no sound for this instrument

        # number %= self.max
        number %= len(self.scale) # TODO: use max or len(scale)

        if isinstance(self.scale[number],list):
            return [
                "./instruments/" + self.name + "/" + sound  for sound in self.scale[number]
            ]
        
        return [
            "./instruments/" + self.name + "/" + self.scale[number]
        ]





class StringPlayer():

    @staticmethod
    def is_open_parenthesis( c ):
        return c=="(" or c=="[" or c=="{" or c=="<"

    @staticmethod
    def is_closed_parenthesis( c ):
        return c==")" or c=="]" or c=="}" or c==">"


    @staticmethod
    def play_string( string, scene, instrument, sound_time=0.2 ):

        level = 0
        for c in string:
            if StringPlayer.is_open_parenthesis(c):
                level += 1
            elif StringPlayer.is_closed_parenthesis(c):
                level -= 1

            level %= len(instrument.scale)

            [ scene.add_sound( s )  for s in instrument.sounds(level) ]
            scene.wait( sound_time )



# Instruments
# TODO: avoid max
# TOOD: piano

# Percussions
Drums_Scale = ["0", "2", "3", "5", "7", "8", "10", "11" ]
Drums_Scale = ["2", "3", "5", "7", "8", "10", "11" ]        # some sounds do not work
Drums = Instrument("drums", icon_svg_file = "drums", max = 11, scale = Drums_Scale)
Cymbals = Instrument("cymbals", icon_svg_file="cymbals", max=3, scale = ["0", "1", "2"])          
Tom = Instrument("tom", "🥁", icon_color = GRAY )

# Wind
Trombone = Instrument("trombone", icon_color=ORANGE, icon_svg_file = "trombone")   
Trumpet = Instrument("trumpet", "🎺", icon_color = YELLOW)
Sax = Instrument("sax", "🎷", icon_color = YELLOW)       

Sax_S_Scale = ["B", "C", "D", "E", "F", "G", "C2", "A"]
Sax_s = Instrument("sax_s", "🎷", icon_color = YELLOW, scale = Sax_S_Scale )       

# Voice
Voice = Instrument("voice", "👧" )
VoiceChoords = Instrument("voice", "👧", scale = Choords_1451, max = 3 )

Squeak = Instrument("squeak", "🚪" )
Dancers = Instrument("dancers", "💃🏼🕺", icon_color = RED, max = -1)


# Strings
Guitar = Instrument("guitar", "🎸", icon_color = RED)
ClassicGuitar = Instrument("classicguitar", icon_svg_file="classicguitar", scale = Pentatonic_Scale, max = 5)
GuitarChoords = Instrument("guitar", "🎸", icon_color = YELLOW_A, scale = Choords_1451, max = 3)

ElecBass = Instrument("elecbass", icon_svg_file="elecbass")
Bass = Instrument("bass", "🎸", icon_color = RED_A)               
# Bass = Instrument("bass", icon_svg_color = RED_A, icon_svg_file = "bass")               
BassChoords = Instrument("bass", "🎸", icon_color = RED_A, scale = Choords_1451, max = 3)

DoubleBass2 = Instrument("doublebass2", icon_svg_file="doublebass")

Banjo = Instrument("banjo", icon_svg_file = "banjo")
Banjo2 = Instrument("banjo2", icon_svg_file = "banjo")

PianoChoords_Scale = ["A", "C", "F", "G", "C"]
PianoChoords = Instrument("pianochoords", icon_svg_file = "piano", max = 5, scale = PianoChoords_Scale)



# the app 
class TowerApp(Scene):

    def create_displays(
        self, instruments, colors, probabilities, gains = None,
        on_opacities = None, off_opacities = None, 
        rule_display_size = 0, rule_title = None, rule_subtitle = None,
        separted = True, levels_on = True, subtowers_on = True,
        expr_display_on = False
    ):
        if colors == None:
            colors = [None for i in range(len(instruments))]
        if on_opacities == None:
            on_opacities = [1 for i in range(len(instruments))]
        if off_opacities == None:
            off_opacities = [1 for i in range(len(instruments))]
        if gains == None:
            gains = [0 for i in range(len(instruments))]

        self.expr_display_on = expr_display_on

        if separted:
            self.instrument_display = InstrumentSeparateDisplay(
                self, instruments, colors, on_opacities, off_opacities
            )
            self.instrument_player = InstrumentSeparatePlayer(
                self, instruments, probabilities, gains, self.instrument_display, use = "nesting"
            ) 
        else:
            self.instrument_display = InstrumentAlternateDisplay(
                self, instruments, colors, off_opacities[0]  
            )
            self.instrument_player = InstrumentAlternatePlayer(
                self, instruments, probabilities, gains, self.instrument_display, use = "nesting"
            )
        
        if  levels_on:
            self.level_display = LevelDisplay(self)
        else:
            self.level_display = NullDisplay(self)
        
        if subtowers_on:     
            self.subtowers_display = SubtowersDisplay(self)
        else:
            self.subtowers_display = NullDisplay(self)

        if rule_display_size > 0:
            self.rule_display = RuleDisplay(
                self, rule_title, rule_subtitle, rule_display_size
            )      

        self.earth = Earth(-2, -5.5, 5.5)

        self.play( Create(self.earth) )

        self.expr_display = None
        if expr_display_on:
            self.expr_display = ExpressionDisplay(self, 10)

    def update_displays( self, tower ):

        anis1 = self.level_display.update(level = tower.count_floors())
        anis2 = self.subtowers_display.update(subtowers = tower.count_children())

        if len(anis1)+len(anis2)>0:
            self.play( *anis1, *anis2, run_time = 0.04 )



    def construct(self):

        # self.animateRain()
        # self.animateSwap()
        # self.animateResize()
        # self.animateDuplicates2()
        # self.animateTwoTowers()
        # self.animateExample1()
        # self.animateSingleton()
        # self.animateFirstFloor()
        # self.animateSelect()
        # self.animateInfinite()
        # self.animateSubstitute()
        # self.animateSubstitute2()
        # self.animateSubstitute3()
        # self.animateReveal()
        # self.animateCombo()
        # self.animateNumbers()

        # self.try_string()
        # self.try_string_player()
        self.snippet1()


    # -------------- Scenes -----------------------
        
    def try_string_player(self):
        
        s = " (( ( ((())) ()  () (()) )  ((()()()) () ()) ))"
        s = " (((((()((())) ())))((())))) "

        sounds = Guitar.sounds(2)

        StringPlayer.play_string(s, self, Guitar )

        self.wait(3)
        

    # Try string:
    def try_string(self):
        
        prova1 = "( ( ( (()()) ((())())()) (()()) ) )"

        sequence = [prova1]
        
        # instrument
        instruments = [Sax, Tom, GuitarChoords, Guitar ]
        probabilities = [ 1, 0.6, 0.5, 0.5  ] 
        gains = [0,0,-5, 0]
        off_opacities = [ 1,  1,  1,  1, 1 ]

        self.create_displays(
            instruments, None, probabilities, gains,
            off_opacities, separted = True,        
            # rule_title=None, rule_subtitle=instruments[0].name, rule_display_size=4
            rule_title=None, rule_subtitle="Math+Music", rule_display_size=6
        )


        s_old = None
        for p in sequence:
            s , _ = Tower.from_string_bottom_up( p, 0,  6, 0.5, 0.1 )
            s.animate.place_on_earth(self.earth)
            if s_old is not None:
                s_old.flush(self, 0.02)

            s.raise_tower(self, transitions_run_time=0.04,)
            self.update_displays(s)
            s_old = s

        self.wait(3)



    def play_set(  
        self, instruments, probabilities, sequence,
        rule_display_size = 2, rule_display_txt = "♫♫"
    ):
        self.create_displays(
            instruments, None, probabilities,  
            rule_subtitle=rule_display_txt, rule_display_size=rule_display_size
        )

        s , _ = Tower.from_string_bottom_up( sequence, 0,  7, 0.6, 0.2 )
        s.animate.place_on_earth(self.earth)

        s.raise_tower(self, transitions_run_time=0.04,)

        self.wait(3)




    def snippet1(self):
        
        sequence  = " < ( (  ([[][]])  [][<>][]   ([[][]])  [] [] []      ) ) [][]  > "
        instruments = [Tom, GuitarChoords, Trumpet, Cymbals ]
        probabilities = [ 1, 0.75, 0.5, 0.3  ]         

        self.play_set( instruments, probabilities, sequence )


    
    # animate Two Towers (pair)
    def animateTwoTowers(self):

        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            4, "Regla 1", "Fusión", 
            # 4, "Regola 1", "Fusione",        
            # 4, "Rule 1", "Merge", 
        )

        prova1 = "  < ( [()] [] ) [ (( ()() )[]) ] >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  6, 0.6, 0.3 )
        s.animate.place_on_earth(self.earth)


        s.drop_subtowers(self)

        self.wait(3)

        s.raise_towers_with_base( self, s.subtowers, s, transitions_run_time= 0.04 )
        self.update_displays(s)

        self.wait(3)
        s.resize(self)


        self.wait(0.3)

        
    # animate Reveal 
    def animateReveal(self):

        instruments = [Tom, Bass]
        probabilities = [1, 0.7]
        colors = [GRAY, RED ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 4, None, "Sorpresa", 
            4, "Sveliamo il", "Mistero",        
            # 3, None, "Reveal", 
        )

        prova1 = "  ([] ( ()([]) )) "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  6, 1.2, 0.1 )
        s.animate.place_on_earth(self.earth)


        s.drop_tower(self)

        self.update_displays(s)

        self.wait(3)



        self.wait(0.3)

        
    # animate Singleton 
    def animateSingleton(self):

        instruments = [Tom, PianoChoords]
        probabilities = [1, 0.5]
        colors = [GRAY, None ]
        on_opacities = [1, 1]
        off_opacities = [1, 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 4, None, "Otra base", 
            # 6, None, "Aggiungi base",        
            4, None, "Add base", 
        )

        prova1 = " ( [()] [[[]][]] ) "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  4, 0.6, 0.3 )
        s.shift([-2.5,0,0])
        t = s.copy()
        s.drop_tower(self)
        self.update_displays(s)

        self.wait(3)

        new_base = s.copy()
        new_base.rect.set_color(YELLOW)
        Tower.raise_towers_with_base(self, [s], new_base  )
        self.update_displays(s)
        new_base.set_subtowers([s])

        self.wait(3)

        self.play( Uncreate(new_base), run_time=0.1 )
        u = t.copy()
        t.drop_tower(self)
        self.update_displays(t)

        self.wait(2)

        u.shift([5,0,0])
        u.drop_tower(self)

        self.wait(2)

        prova1 = " (  ) "

        v , _ = Tower.from_string_bottom_up( prova1, 0,  10, 0.6, 0.3 )
        v.rect.set_color(BLUE)

        # merge = Text("regla: fusión", font_size=18).move_to([0,2,0])
        # merge = Text("regola: fusione", font_size=18).move_to([0,2,0])
        merge = Text("rule: merge", font_size=18).move_to([0,2,0])
        self.play( Write(merge) )

        Tower.raise_towers_with_base(self, [t, u], v )
        v.set_subtowers([t,u])
        self.wait(3)


        # dup = Text("regla: borrar", font_size=18).move_to([0,2,0])
        # dup = Text("regola: doppioni", font_size=18).move_to([0,2,0])
        dup = Text("rule: erase", font_size=18).move_to([0,2,0])
        self.play( ReplacementTransform(merge, dup) )

        v.remove_duplicate_subtowers( self, 0.5  )

        self.play(
            Uncreate(dup),
            v.parts.animate.stretch_to_fit_width(5)
        )

        self.wait(3)

    # animate Example1
    def animateExample1(self):

        instruments = [Tom, PianoChoords]
        probabilities = [1, 0.5]
        colors = [GRAY, None ]
        on_opacities = [1, 1]
        off_opacities = [1, 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 4, None, "Ejemplo", 
            4, None, "Esempio",        
            # 4, None, "Example", 
        )

        prova1 = " ( () ) "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  4, 0.6, 0.3 )
        s.drop_tower(self)
        self.update_displays(s)

        self.wait(2)

        self.play( s.animate.scale(0.4), run_time=0.3)
        self.play( s.animate.move_to([-3,2,0]), run_time=0.3)

        prova1 = " (  ) "
        v , _ = Tower.from_string_bottom_up( prova1, 0,  2, 0.6, 0.3 )
        v.move_to([-1, 0, 0])
        w , _ = Tower.from_string_bottom_up( prova1, 0,  2, 0.6, 0.3 )
        w.move_to([1, 0, 0])


        v.drop_tower(self)
        w.drop_tower(self)

        self.update_displays(v)

        self.wait(2)

        # merge = Text("regla: fusión", font_size=18).move_to([0,2,0])
        merge = Text("regola: fusione", font_size=18).move_to([0,2,0])
        # merge = Text("rule: merge", font_size=18).move_to([0,2,0])
        self.play( Write(merge) )

        base = Tower.raise_towers(self, [v,w])
        self.play( base.rect.animate.set_color(BLUE_E) )

        self.update_displays(base)

        self.wait(2)

        # dup = Text("regla: borrar", font_size=18).move_to([0,2,0])
        dup = Text("regola: doppioni", font_size=18).move_to([0,2,0])
        # dup = Text("rule: erase", font_size=18).move_to([0,2,0])
        self.play( ReplacementTransform(merge, dup) )
        base.remove_duplicate_subtowers_recursively(self)

        self.update_displays(base)

        base.parts.stretch_to_fit_width(3.5)

        self.play( Uncreate(dup) )


        self.wait(3)

        
    # animate First Floor (union)
    def animateFirstFloor(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 5, "Rule 4", "First Floor"
            # 5, "Regla 4", "Primer Piso"
            5, "Regola 4", "Primo Piano"
        )

        prova1 = "  < [ (( ()() )[]) ] ( [()] [] ) [[]] []>  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        s.union(self)

        self.update_displays(s)

        self.wait(0.3)

    # animate Duplicates (extensionality)
    def animateDuplicates(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            4, "Regola 3", "Doppioni"
            # 4, "Regla 3", "Borrar"
            # 4, "Rule 3", "Erase"
        )

        prova1 = "  < [( () )[]] ( [()] [] ) ( [()] ()()() )    >  "
        prova1 = "  <  ((())()) ((())) ((())()) >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        self.wait(2)

        s.remove_duplicate_subtowers_recursively(self, 1)

        self.update_displays(s)

        self.wait(0.3)


    # animate Duplicates (extensionality)
    def animateDuplicates2(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            4, "Regola 3", "Doppioni"
            # 4, "Regla 3", "Borrar"
            # 4, "Rule 3", "Erase"
        )

        prova1 = "  < [( () )[]] ( [()] [] ) ( [()] ()()() )    >  "
        prova1 = "  <  ((())(())) ((()())(())) ((())(())) >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        self.wait(2)

        s.remove_duplicate_subtowers_recursively(self, 1)

        self.update_displays(s)

        self.wait(1)


    # animate Rain
    def animateRain(self):
        instruments = [Tom, GuitarChoords]
        probabilities = [0.7, 1]
        gains = [0, -4]
        colors = [RED, YELLOW_B ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, gains, on_opacities, off_opacities,
            # 3, "Rule 0", "Start", True, False, False
            # 3, "Regla 0", "Inicio", True, False, False        
            3, "Regola 0", "Inizio", True, False, False
        )

        prova1 = "  <  >  "

        columns = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(4):
            f = 0.2
            h = f + (1-f)*random.random()
            w = f + (1-f)*random.random()
            s , _ = Tower.from_string_bottom_up( prova1, 0,  w, h, 0.1 )

            col = random.randint(1,6) + random.randint(1,6)
            s.move_to([col-6.8, 7, 0])

            self.play( s.animate.move_to( [
                col-6.8+random.random()/3-0.16, 
                columns[col]+self.earth.get_level()+s.parts.height/2, 
                0
            ]), run_time = random.random() )

            self.instrument_player.play_sound(random.randint(0,4), 0)
            self.play( 
                *self.instrument_display.vibrate([random.randint(0,1)], random.randint(1,3) ),
                *self.earth.vibrate(),
                run_time = 0.03 
            )

            columns[col] += h

        self.wait(1)


    # animate Swap (extensionality)
    def animateSwap(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]        
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            4, "Rule 2", "Swap"
            # 4, "Regla 2", "Cambio"
            # 4, "Regola 2", "Scambio"         
        )

        prova1 = "  < [( () )[]] ( [()] [] ) ( [()] ()()() )    >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        s.swap_subtowers(self, 0, 1)
        s.swap_subtowers(self, 1, 2)
        s.subtowers[1].swap_subtowers(self, 0, 2)

        self.update_displays(s)

        self.wait(1)


    # animate Resize (extensionality)
    def animateResize(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [RED, ORANGE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities
        )

        prova1 = "  < [( () )[]] ( [()] [] ) ( [()] ()()() )    >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        s.resize(self)
        s.remove_duplicate_subtowers_recursively(self)

        self.wait(1)


    # animate Select (specification)
    def animateSelect(self):
        instruments = [Tom, PianoChoords]
        probabilities = [0.9, 0.7]
        colors = [RED, None ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 3, "Rule 5", "Sieve"
            # 3, "Regla 5", "Tamiz"
            4, "Regola 5", "Setaccio"
        )


        prova1 = "  < []  [[][]] [[[]]] []  [[]] [[[]][[[]]]]  >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )

        s.drop_tower(self)
        self.update_displays(s)

        self.wait(2)

        self.play( Create( Text("#piani>3").move_to([0,3,0])  ) )

        self.wait(2)


        def check_function(base, subtower):
            return subtower.count_floors()>2

        s.select_subtowers(self, check_function)
        s.center_subtowers(self)
        self.update_displays(s)

        self.wait(1)

    # animate Infinite
    def animateInfinite(self):
        instruments = [Tom, Bass]
        probabilities = [1, 1]
        colors = [GRAY, RED ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            3, "Regola 7", "Città", True, True, False 
            # 3, "Regla 7", "Ciudad", True, True, False
            # 3, "Rule 7", "City", True, True, False
        )

        prova1 = "  < [] [[]] [[[]]] [[[[]]]] [[[[[]]]]] [[[[[[]]]]]] [[[[[[[]]]]]]] [[[[[[[[]]]]]]]] >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  13, 0.44, 0.1 )
        s.move_to([2.2,10,0])
        s.parts.shift( [0, self.earth.get_level()-s.parts.get_bottom()[1],0 ] )
        self.play( Create(s.parts) )
        s.drop_subtowers(self,  drop_run_time=0.3, height=s.parts.get_top()[1] )

        for i in range(8, 30):
            instruments = self.instrument_player.play_sound( i, 0 )
            self.play( 
                *self.instrument_display.vibrate(instruments, i ),
                *self.level_display.update(level=i ),
                *self.earth.vibrate(),
                run_time = 0.03 
            )

        self.play( 
            *self.level_display.update(level=-1 ),
            run_time = 0.3 
        )



        self.wait(2)


    # animate Substitute
    def animateSubstitute(self):
        instruments = [Tom, GuitarChoords]
        probabilities = [0.9, 0.9]
        colors = [RED, YELLOW_B ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 4, "Rule 6", "Transform"
            # 6, "Regla 6", "Transformación"
            6, "Regola 6", "Trasformazione"
        )

        font_size = 90
        rock = Text("♜", font_size = font_size, color = RED).move_to([-2,1,0])  #♖♜
        self.play( Create(rock) )
        arrow = Text("→", font_size = font_size, color = RED).next_to(rock)
        self.play( Create(arrow) )
        base = Text("▭", font_size = font_size, color = RED)  # ▬
        base.next_to(arrow).align_to(rock, DOWN)
        self.play( Create(base) )
        rock2 = Text("♜", font_size = font_size, color = RED)
        rock2.next_to(base, UP).align_to([0,base.get_top()[1],0], DOWN)
        self.play( Create(rock2) )

        self.wait(2)

        rule = VGroup()
        rule.add(rock, arrow, base, rock2)

        self.add_sound( "./sounds/whoosh.wav" )
        self.play( rule.animate.scale(0.6) )
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( rule.animate.move_to([-5,1.8,0]))


        self.wait(2)


        prova1 = "  < [( () )[]] ( [()] [] ) ( [()] ()()() )    >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )
        s.raise_tower(self)

        self.wait(2)

        new_bases = s.raise_subtowers_with_new_base(self)

        for t in new_bases:
            self.play( t.border.animate.set_color(WHITE), run_time = 0.2 )


        self.wait(1)


    # animate Substitute2
    def animateSubstitute2(self):
        instruments = [Tom, GuitarChoords]
        probabilities = [1, 0.9]
        colors = [RED, YELLOW_B ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 4, "Rule 6", "Transform"
            # 6, "Regla 6", "Transformación"
            6, "Regola 6", "Trasformazione"
        )

        font_size = 90
        rock = Text("♜", font_size = font_size, color = RED).move_to([-2,1,0])  #♖♜
        self.play( Create(rock) )
        arrow = Text("→", font_size = font_size, color = RED).next_to(rock)
        self.play( Create(arrow) )
        base1 = Text("▭", font_size = font_size+font_size, color = RED)  # ▬
        base1.next_to(arrow).align_to(rock, DOWN)
        self.play( Create(base1) )
        base2 = Text("▭", font_size = font_size, color = RED)  
        base2.align_to([0,base1.get_top()[1],0], DOWN)
        base2.align_to([base1.get_right()[0],0,0], RIGHT)
        self.play( Create(base2) )
        rock2 = Text("♜", font_size = font_size, color = RED)
        rock2.next_to(base2, UP).align_to([0,base2.get_top()[1],0], DOWN)
        self.play( Create(rock2) )
        rock3 = Text("♜", font_size = font_size, color = RED)
        rock3.next_to(base1, UP).align_to([0,base1.get_top()[1],0], DOWN)
        rock3.align_to([base1.get_left()[0],0,0], LEFT)
        self.play( Create(rock3) )

        rule = VGroup()
        rule.add(rock, arrow, base1, base2, rock2, rock3)

        self.add_sound( "./sounds/whoosh.wav" )
        self.play( rule.animate.scale(0.6) )
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( rule.animate.move_to([-5,1.6,0]))

        prova1 = "  < [( () )[]] ( [()] [()] ) ( [()] ()()() )    >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )
        s.raise_tower(self)

        bases = []
        for t in s.subtowers:
            base = t.successive(self, height = 0.8 )
            bases.append( base )
            bases.append( base.subtowers[1] )

        for b in bases:
            self.play( b.rect.animate.set_color( BLUE_A ), run_time = 0.2 )

        self.wait(1)


    # animate Substitute3
    def animateSubstitute3(self):
        instruments = [Tom, Bass]
        probabilities = [1, 0.5]
        colors = [GRAY, RED ]
        on_opacities = [1, 1]
        off_opacities = [1, 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            5, "La Regla de Fusión es", "Redundante"  
            # 5, "La Regola di Fusione è", "Ridondante"
            # 5, "Merge Rule is", "Redundant"
        )

        prova1 = "  < >  "
        font_size = 60

        rock1 = Text("♜", font_size = font_size, color = BLUE).move_to([-0.5,1,0])  #♖♜
        rock2 = Text("♜", font_size = font_size, color = RED).move_to([0.5,1,0])  #♖♜

        group = VGroup( rock1, rock2 )
        self.play( Create(group) )
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( group.animate.move_to([-4,2,0]) )

        prova1 = "()"

        s , _ = Tower.from_string_bottom_up( prova1, 0,  1, 1, 0.3 )

        s.move_to([0,1,0])
        self.play( Create(s) )

        combo = Text("regla: combo", font_size=18).move_to([0,2,0])
        # combo = Text("regola: combo", font_size=18).move_to([0,2,0])
        # combo = Text("rule: combo", font_size=18).move_to([0,2,0])
        self.play( Write(combo) )

        self.wait(2)

        prova2 = "<>"

        t , _ = Tower.from_string_bottom_up( prova2, 0,  3, 0.7, 0.3 )
        t.rect.set_color(BLUE)
        t.drop_tower(self)

        self.update_displays(t)

        self.wait(2)

        s.drop_tower_to_base(self, t)
        t.set_subtowers([s])

        self.update_displays(t)

        self.wait(1)

        combo2 = combo.copy()
        self.play( 
            t.animate.shift([0,2,0]),
            Uncreate(combo)
        )

        self.wait(1)
  
        self.play( Write(combo2) )
        u = t.copy()
        u.shift([-1.5, 0, 0])
        u.set_subtowers([])
        
        prova3 = "<>"

        z , _ = Tower.from_string_bottom_up( prova3, 0,  7, 0.7, 0.3 )
        z.rect.set_color(BLUE)
        z.drop_tower(self)

        u.drop_tower_to_base( self, z )
        t.shift([1.5, 0, 0])
        t.drop_tower_to_base( self, z )

        z.set_subtowers([u,t])
        self.update_displays(z)

        self.wait(2)

        self.play( Uncreate(combo2) )

        self.play( rock1.animate.next_to(rock2, DOWN*1.6) )
        arrow2 = Text("→", font_size = font_size, color = YELLOW).next_to(rock2,LEFT )
        self.play( Create(arrow2) )
        base2 = Text("▭", font_size = font_size+font_size, color = RED)  
        base2.next_to(arrow2, LEFT).align_to(rock2, DOWN)
        self.play( Create(base2) )
        
        arrow3 = Text("→", font_size = font_size, color = YELLOW).next_to(rock1, LEFT )
        self.play( Create(arrow3))
        base1 = Text("▭", font_size = font_size+font_size, color = BLUE)  
        base1.next_to(arrow3, LEFT).align_to(rock1, DOWN)
        self.play( Create(base1) )
        base3 = Text("▭", font_size = font_size, color = RED)  
        base3.align_to([0,base1.get_top()[1],0], DOWN)
        base3.align_to([base1.get_right()[0],0,0], RIGHT)
        self.play( Create(base3) )

        combo = Text("regla: Transformación", font_size=18).move_to([0,2,0]) 
        # combo = Text("regola: Trasformazione", font_size=18).move_to([0,2,0])
        # combo = Text("rule: Transform", font_size=18).move_to([0,2,0])
        self.play( Write(combo) )

        rock1b = rock1.copy()
        rock1b.scale(2)
        rock1b.move_to(t)
        rock2b = rock2.copy()
        rock2b.scale(2)
        rock2b.move_to(u)
        rock1b.align_to(z.parts.get_top(), DOWN),
        rock2b.align_to(z.parts.get_top(), DOWN),

        self.add_sound( "./sounds/whoosh.wav" )
        self.play( ReplacementTransform( u, rock2b ) )
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( ReplacementTransform( t, rock1b ) )
        
        self.wait(2)


    # animate Combo
    def animateCombo(self):
        instruments = [Tom, GuitarChoords]
        probabilities = [0.7, 1]
        colors = [RED, BLUE ]
        on_opacities = [1, 1]
        off_opacities = [1 , 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,
            # 3, "Rule 8", "Combo"
            # 3, "Regla 8", "Combo"
            3, "Regola 8", "Combo"
        )

        prova1 = "  < [[]] (() (()))  [[[]] [[]]]  >  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  7, 1, 0.3 )
        s.raise_tower(self)

        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s.animate.scale(0.5) )
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s.animate.move_to([0.5,2.5,0]))

        prova2 = "  <   >  "

        self.wait(3)

        t , _ = Tower.from_string_bottom_up( prova2, 0,  13.8, 0.7, 0.3 )
        t.rect.set_color(BLUE)
        t.drop_tower(self)

        self.wait(2)

        st = []

        #0
        s1 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s1.animate.shift([-5.8,-1,0]))
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s1.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s1.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s1.drop_tower_to_base(self, t.parts)
        st.append(s1)
        t.set_subtowers(st)
        self.update_displays(t)

        #1
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([-4.2,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain=-4 )
        self.play( s2.subtowers[0].animate.set_color(YELLOW) )
        self.play( Uncreate( s2.subtowers[0] ) )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #2
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([-2.6,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain= -4 )
        self.play( s2.subtowers[1].animate.set_color(YELLOW) )
        self.play( Uncreate( s2.subtowers[1] ) )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #3
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([-1,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain = -4 )
        self.play( s2.subtowers[2].animate.set_color(YELLOW) )
        self.play( Uncreate( s2.subtowers[2] ) )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #4
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([0.6,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain = -4 )
        self.play( 
            s2.subtowers[0].animate.set_color(YELLOW), 
            s2.subtowers[1].animate.set_color(YELLOW),
        )
        self.play( 
            Uncreate( s2.subtowers[0] ),
            Uncreate( s2.subtowers[1] ),
        )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #5
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([2.2,-1,0]))
        self.add_sound( "./sounds/laser1.wav" , gain = -4 )
        self.play( 
            s2.subtowers[1].animate.set_color(YELLOW), 
            s2.subtowers[2].animate.set_color(YELLOW),
        )
        self.play( 
            Uncreate( s2.subtowers[1] ),
            Uncreate( s2.subtowers[2] ),
        )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #6
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([3.8,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain = -4 )
        self.play( 
            s2.subtowers[0].animate.set_color(YELLOW), 
            s2.subtowers[2].animate.set_color(YELLOW),
        )
        self.play( 
            Uncreate( s2.subtowers[0] ),
            Uncreate( s2.subtowers[2] ),
        )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        #5
        s2 = s.copy()
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.shift([5.4,-1,0]))
        self.add_sound( "./sounds/laser1.wav", gain = -4 )
        self.play( 
            s2.subtowers[1].animate.set_color(YELLOW), 
            s2.subtowers[2].animate.set_color(YELLOW),
            s2.subtowers[0].animate.set_color(YELLOW),
        )
        self.play( 
            Uncreate( s2.subtowers[1] ),
            Uncreate( s2.subtowers[2] ),
            Uncreate( s2.subtowers[0] ),
        )
        self.wait(1)
        self.add_sound( "./sounds/whoosh.wav" )
        self.play( s2.animate.scale(0.36))
        self.add_sound( "./sounds/whoosh.wav" )
        # self.play( s2.animate.align_to(
        #     [0,self.earth.get_level()+t.get_block_height(),0], DOWN
        # ))
        s2.drop_tower_to_base(self, t.parts)
        st.append(s2)
        t.set_subtowers(st)
        self.update_displays(t)

        self.wait(3)


    # animate Numbers
    def animateNumbers(self):
        instruments = [Bass, Tom, GuitarChoords]
        probabilities = [1, 0.5, 0.6]
        colors = [RED, ORANGE, YELLOW ]
        on_opacities = [1, 1, 1]
        off_opacities = [1 , 1, 1]
        self.create_displays(
            instruments, colors, probabilities, None, on_opacities, off_opacities,            
            4, None, "Números"
            # 4, None, "Numeri"
            # 4, None, "Numbers"
        )

        prova1 = "  ( )  "

        s , _ = Tower.from_string_bottom_up( prova1, 0,  8, 2, 0.3 )
        s.raise_tower(self)

        height = 1
        for i in range(5):
            s = s.successive(self, height=height, color=BLUE, transitions_run_time=0.05)
            height *= 0.8
            

        self.wait(1)


