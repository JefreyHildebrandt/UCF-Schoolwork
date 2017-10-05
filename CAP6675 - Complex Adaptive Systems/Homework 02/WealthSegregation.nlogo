globals [
  percent-similar  ;; on the average, what percent of a turtle's neighbors
                   ;; are the same color as that turtle?
  percent-unhappy  ;; what percent of the turtles are unhappy?

  quadrants
  quad-color
  number
  price
  reds
  blues
  empty-patches

  quad-one-price
  quad-two-price
  quad-three-price
  quad-four-price

  quad-one-red-count
  quad-one-blue-count
  quad-two-red-count
  quad-two-blue-count
  quad-three-red-count
  quad-three-blue-count
  quad-four-red-count
  quad-four-blue-count

  ;; the following 4 variables are lists of lists with 0 = pxcor and y = pycor
  quad-one-empty-patches
  quad-two-empty-patches
  quad-three-empty-patches
  quad-four-empty-patches

  total-money
  ;;salary-increase-percent-range-min
  ;;salary-increase-percent-range-max
  ;;starting-cash-range-min
  ;;starting-cash-range-max
]

turtles-own [
  happy?           ;; for each turtle, indicates whether at least %-similar-wanted percent of
                   ;;   that turtle's neighbors are the same color as the turtle
  similar-nearby   ;; how many neighboring patches have a turtle with my color?
  other-nearby     ;; how many have a turtle of another color?
  total-nearby     ;; sum of previous two variables
  cash
  wealth-type
]

patches-own [
  quadrant
]

to update-quadrants
  set quad-one-price mean [cash] of turtles with [quadrant = 1]
  set quad-two-price mean [cash] of turtles with [quadrant = 2]
  set quad-three-price mean [cash] of turtles with [quadrant = 3]
  set quad-four-price mean [cash] of turtles with [quadrant = 4]

  set quad-one-red-count count turtles with [color = red and quadrant = 1]
  set quad-one-blue-count count turtles with [color = sky and quadrant = 1]
  set quad-two-red-count count turtles with [color = red and quadrant = 2]
  set quad-two-blue-count count turtles with [color = sky and quadrant = 2]
  set quad-three-red-count count turtles with [color = red and quadrant = 3]
  set quad-three-blue-count count turtles with [color = sky and quadrant = 3]
  set quad-four-red-count count turtles with [color = red and quadrant = 4]
  set quad-four-blue-count count turtles with [color = sky and quadrant = 4]

  set quad-one-empty-patches get-free-patches 1
  set quad-two-empty-patches get-free-patches 2
  set quad-three-empty-patches get-free-patches 3
  set quad-four-empty-patches get-free-patches 4

  ;;print length quad-one-empty-patches
end

to create-quadrants
  print min-pxcor
  print min-pycor
  print max-pxcor
  print max-pycor

  set quadrants (list)
  let i 0
  while [i < number-of-quadrants ]
  [ set quadrants lput (list random 140 i) quadrants
    set i i + 1 ]
end

to set-quadrant-colors
  ifelse pxcor = 0
  [ set quadrant 0
    set pcolor black ]
  [ ifelse pycor = 0
    [ set quadrant 0
      set pcolor black ]
    [ ifelse pxcor < 0
      [ ifelse pycor > 0
        [ set quadrant 1
          set pcolor 2 ] ;; gray
        [ set quadrant 3
          set pcolor 22 ]] ;; orange
      [ ifelse pycor > 0
        [ set quadrant 2
          set pcolor 112 ] ;; purple
        [ set quadrant 4
          set pcolor 62 ]]]] ;; green

end

to setup
  clear-all
  set total-money  1000000
  create-quadrants
  ;; create turtles on random patches.
  ask patches [
    set-quadrant-colors
    if random 100 < density [   ;; set the occupancy density
      if quadrant != 0
      [ sprout 1 [
        set color one-of [red sky] ;; red blue
        let wealth-level random 100
        ifelse wealth-level = 0
        [ set wealth-type "Top 1%"]
        [ ifelse wealth-level >= 1 and wealth-level < 5
          [ set wealth-type "Next 4%"]
          [ ifelse wealth-level >= 5 and wealth-level < 10
            [ set wealth-type "Next 5%"]
            [ ifelse wealth-level >= 10 and wealth-level < 20
              [ set wealth-type "Next 10%"]
              [ ifelse wealth-level >= 20 and wealth-level < 40
                [ set wealth-type "Upper Middle 20%"]
                [ ifelse wealth-level >= 40 and wealth-level < 60
                  [ set wealth-type "Middle 20%"]
                  [ set wealth-type "Bottom 40%"]]]]]]
      ]]
    ]
  ]
  set-cash
  update-quadrants
  ;;update-turtles
  ;;update-globals
  reset-ticks
end

to set-cash
  let total-turtles count turtles
  let top-1%-cash total-money * .35
  let next-4%-cash total-money * .27
  let next-5%-cash total-money * .11
  let next-10%-cash total-money * .12
  let upper-middle-20%-cash total-money * .11
  let middle-20%-cash total-money * .04
  let bottom-40%-cash total-money * .01

  let total-1% count turtles with [wealth-type = "Top 1%"]
  ask turtles with [wealth-type = "Top 1%"]
  [ set cash top-1%-cash / total-1%
    set shape "box"]

  let total-4% count turtles with [wealth-type = "Next 4%"]
  ask turtles with [wealth-type = "Next 4%"]
  [ set cash next-4%-cash / total-1%
    set shape "airplane"]

  let total-5% count turtles with [wealth-type = "Next 5%"]
  ask turtles with [wealth-type = "Next 5%"]
  [ set cash next-5%-cash / total-5%
    set shape "house"]

  let total-10% count turtles with [wealth-type = "Next 10%"]
  ask turtles with [wealth-type = "Next 10%"]
  [ set cash next-10%-cash / total-10%
    set shape "truck"]

  let total-u-m-20% count turtles with [wealth-type = "Upper Middle 20%"]
  ask turtles with [wealth-type = "Upper Middle 20%"]
  [ set cash upper-middle-20%-cash / total-u-m-20%
    set shape "square"]

  let total-m-20% count turtles with [wealth-type = "Middle 20%"]
  ask turtles with [wealth-type = "Middle 20%"]
  [ set cash middle-20%-cash / total-m-20%
    set shape "square-x"]

  let total-b-40% count turtles with [wealth-type = "Bottom 40%"]
  ask turtles with [wealth-type = "Bottom 40%"]
  [ set cash bottom-40%-cash / total-b-40%
    set shape "square 2"]
end

;; run the model for one tick
to go
  ;;if all? turtles [ happy? ] [ stop ]
  ;;move-unhappy-turtles
  update-turtles
  ;;update-globals
  update-quadrants
  tick
end

to move-to-different-neighborhood
  let quad-num 0
  let quad-price 1
  let quad-meets-ratio 2
  let quad-has-free-space 3

  let quad-info
   (list
     (list 1 quad-one-price meets-ratio color quad-one-red-count quad-one-blue-count has-free-space 1)
      (list 2 quad-two-price meets-ratio color quad-two-red-count quad-two-blue-count has-free-space 2)
       (list 3 quad-three-price meets-ratio color quad-three-red-count quad-three-blue-count has-free-space 3)
        (list 4 quad-four-price meets-ratio color quad-four-red-count quad-four-blue-count has-free-space 4))
  let my-quad item (quadrant - 1) quad-info

  ;; quadrant info sorted by highest price to lowest
  set quad-info sort-by [[list-one list-two] -> item quad-price list-one > item quad-price list-two] quad-info
  ifelse (item quad-meets-ratio my-quad)
  [ let passed-my-quad? false
    foreach quad-info
    [ cur-quad ->
       if not passed-my-quad?
        [ ifelse item quad-num cur-quad = item quad-num my-quad
          [ set passed-my-quad? true ]
          [ if item quad-has-free-space cur-quad
            [ if cash >= item quad-price cur-quad
              [ move-turtle-to-free-space item quad-num cur-quad ]]]]]]
  [ foreach quad-info
    [ cur-quad ->
      if item quad-has-free-space cur-quad
      [ if cash >= item quad-price cur-quad
        [ if item quad-meets-ratio cur-quad
          [ move-turtle-to-free-space item quad-num cur-quad ]]]]]
end

to-report meets-ratio [my-color red-count blue-count]
  let my-color-count 0
  ifelse my-color = red
  [set my-color-count red-count]
  [set my-color-count blue-count]
  report my-color-count >= (%-similar-wanted * (red-count + blue-count) / 100)
end

to move-turtle-to-free-space [quadrant-number]
  ifelse quadrant-number = 1
    [ let move-to-this-patch item 0 quad-one-empty-patches
      set quad-one-empty-patches remove-item 0 quad-one-empty-patches
      setxy item 0 move-to-this-patch item 1 move-to-this-patch ]
    [ ifelse quadrant-number = 2
      [ let move-to-this-patch item 0 quad-two-empty-patches
        set quad-two-empty-patches remove-item 0 quad-two-empty-patches
        setxy item 0 move-to-this-patch item 1 move-to-this-patch]
      [ ifelse quadrant-number = 3
        [ let move-to-this-patch item 0 quad-three-empty-patches
          set quad-three-empty-patches remove-item 0 quad-three-empty-patches
          setxy item 0 move-to-this-patch item 1 move-to-this-patch]
        [ if quadrant-number = 4
          [ let move-to-this-patch item 0 quad-four-empty-patches
            set quad-four-empty-patches remove-item 0 quad-four-empty-patches
            setxy item 0 move-to-this-patch item 1 move-to-this-patch]]]]
end

to-report has-free-space [quadrant-number]
  ifelse quadrant-number = 1
    [ report length quad-one-empty-patches > 0]
    [ ifelse quadrant-number = 2
      [ report length quad-two-empty-patches > 0]
      [ ifelse quadrant-number = 3
        [ report length quad-three-empty-patches > 0]
        [ if quadrant-number = 4
          [ report length quad-four-empty-patches > 0]]]]
end

to-report get-free-patches [quadrant-number]
  let open-list (list)
  ask patches with [quadrant = quadrant-number and count turtles-here < 1]
  [set open-list lput (list pxcor pycor) open-list]
  report open-list
end

to update-turtles
  ask turtles [
    ;;let salary cash * salary-percent
    ;;set cash cash + salary

    move-to-different-neighborhood

    ;; in next two lines, we use "neighbors" to test the eight patches
    ;; surrounding the current patch
    ;;set similar-nearby count (turtles-on neighbors)  with [ color = [ color ] of myself ]
    ;;set other-nearby count (turtles-on neighbors) with [ color != [ color ] of myself ]
    ;;set total-nearby similar-nearby + other-nearby
    ;;set happy? similar-nearby >= (%-similar-wanted * total-nearby / 100)
    ;;ifelse happy? [ set shape "square" ] [ set shape "square-x" ]
    ;;ifelse cash > quad-one-price and cash > quad-two-price and cash > quad-three-price and cash > quad-four-price
    ;;[ set shape "box" ]
    ;;[ ifelse cash < quad-one-price and cash < quad-two-price and cash < quad-three-price and cash < quad-four-price
    ;;  [ set shape "square 2" ]
    ;;  [ set shape "square" ]]
  ]
end


; Copyright 1997 Uri Wilensky.
; See Info tab for full copyright and license.
@#$#@#$#@
GRAPHICS-WINDOW
353
10
769
427
-1
-1
8.0
1
10
1
1
1
0
1
1
1
-25
25
-25
25
1
1
1
ticks
30.0

MONITOR
262
373
347
418
% unhappy
percent-unhappy
1
1
11

MONITOR
264
233
339
278
% similar
percent-similar
1
1
11

PLOT
13
141
262
284
Percent Similar
time
%
0.0
5.0
0.0
100.0
true
false
"" ""
PENS
"percent" 1.0 0 -2674135 true "" "plot percent-similar"

SLIDER
19
95
279
128
%-similar-wanted
%-similar-wanted
0
100
29.0
1
1
%
HORIZONTAL

BUTTON
20
60
100
93
setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
199
60
279
93
go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

BUTTON
104
60
194
93
go once
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

SLIDER
26
10
281
43
density
density
1
99
59.0
1
1
%
HORIZONTAL

PLOT
14
293
257
443
Number-unhappy
NIL
NIL
0.0
10.0
0.0
100.0
true
false
"" ""
PENS
"default" 1.0 0 -14439633 true "" "plot count turtles with [not happy?]"

MONITOR
261
325
349
370
num-unhappy
count turtles with [not happy?]
1
1
11

MONITOR
266
139
332
184
# agents
count turtles
1
1
11

MONITOR
789
300
887
345
NIL
quad-one-price
17
1
11

MONITOR
906
298
1004
343
NIL
quad-two-price
17
1
11

MONITOR
788
347
895
392
NIL
quad-three-price
17
1
11

MONITOR
903
348
1004
393
NIL
quad-four-price
17
1
11

INPUTBOX
785
68
940
128
number-of-quadrants
15.0
1
0
Number

@#$#@#$#@
## WHAT IS IT?

This project models the behavior of two types of agents in a neighborhood. The red agents and green agents get along with one another. But each agent wants to make sure that it lives near some of "its own." That is, each red agent wants to live near at least some red agents, and each green agent wants to live near at least some green agents. The simulation shows how these individual preferences ripple through the neighborhood, leading to large-scale patterns.

This project was inspired by Thomas Schelling's writings about social systems (such as housing patterns in cities).

## HOW TO USE IT

Click the SETUP button to set up the agents. There are approximately equal numbers of red and green agents. The agents are set up so no patch has more than one agent.  Click GO to start the simulation. If agents don't have enough same-color neighbors, they move to a nearby patch. (The topology is wrapping, so that patches on the bottom edge are neighbors with patches on the top and similar for left and right).

The DENSITY slider controls the occupancy density of the neighborhood (and thus the total number of agents). (It takes effect the next time you click SETUP.)  The %-SIMILAR-WANTED slider controls the percentage of same-color agents that each agent wants among its neighbors. For example, if the slider is set at 30, each green agent wants at least 30% of its neighbors to be green agents.

The % SIMILAR monitor shows the average percentage of same-color neighbors for each agent. It starts at about 50%, since each agent starts (on average) with an equal number of red and green agents as neighbors. The NUM-UNHAPPY monitor shows the number of unhappy agents, and the % UNHAPPY monitor shows the percent of agents that have fewer same-color neighbors than they want (and thus want to move). The % SIMILAR and the NUM-UNHAPPY monitors are also plotted.

The VISUALIZATION chooser gives two options for visualizing the agents. The OLD option uses the visualization that was used by the segregation model in the past. The SQUARE-X option visualizes the agents as squares. The agents have X's in them if they are unhappy.

## THINGS TO NOTICE

When you execute SETUP, the red and green agents are randomly distributed throughout the neighborhood. But many agents are "unhappy" since they don't have enough same-color neighbors. The unhappy agents move to new locations in the vicinity. But in the new locations, they might tip the balance of the local population, prompting other agents to leave. If a few red agents move into an area, the local green agents might leave. But when the green agents move to a new area, they might prompt red agents to leave that area.

Over time, the number of unhappy agents decreases. But the neighborhood becomes more segregated, with clusters of red agents and clusters of green agents.

In the case where each agent wants at least 30% same-color neighbors, the agents end up with (on average) 70% same-color neighbors. So relatively small individual preferences can lead to significant overall segregation.

## THINGS TO TRY

Try different values for %-SIMILAR-WANTED. How does the overall degree of segregation change?

If each agent wants at least 40% same-color neighbors, what percentage (on average) do they end up with?

Try different values of DENSITY. How does the initial occupancy density affect the percentage of unhappy agents? How does it affect the time it takes for the model to finish?

Can you set sliders so that the model never finishes running, and agents keep looking for new locations?

## EXTENDING THE MODEL

The `find-new-spot` procedure has the agents move locally till they find a spot. Can you rewrite this procedure so the agents move directly to an appropriate new spot?

Incorporate social networks into this model.  For instance, have unhappy agents decide on a new location based on information about what a neighborhood is like from other agents in their network.

Change the rules for agent happiness.  One idea: suppose that the agents need some minimum threshold of "good neighbors" to be happy with their location.  Suppose further that they don't always know if someone makes a good neighbor. When they do, they use that information.  When they don't, they use color as a proxy -- i.e., they assume that agents of the same color make good neighbors.

The two different visualizations emphasize different aspects of the model. The SQUARE-X visualization shows whether an agent is happy or not. Can you design a different visualization that emphasizes different aspects?

## NETLOGO FEATURES

`sprout` is used to create agents while ensuring no patch has more than one agent on it.

When an agent moves, `move-to` is used to move the agent to the center of the patch it eventually finds.

Note two different methods that can be used for find-new-spot, one of them (the one we use) is recursive.

## CREDITS AND REFERENCES

Schelling, T. (1978). Micromotives and Macrobehavior. New York: Norton.

See also: Rauch, J. (2002). Seeing Around Corners; The Atlantic Monthly; April 2002;Volume 289, No. 4; 35-48. http://www.theatlantic.com/magazine/archive/2002/04/seeing-around-corners/302471/

## HOW TO CITE

If you mention this model or the NetLogo software in a publication, we ask that you include the citations below.

For the model itself:

* Wilensky, U. (1997).  NetLogo Segregation model.  http://ccl.northwestern.edu/netlogo/models/Segregation.  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

Please cite the NetLogo software as:

* Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

## COPYRIGHT AND LICENSE

Copyright 1997 Uri Wilensky.

![CC BY-NC-SA 3.0](http://ccl.northwestern.edu/images/creativecommons/byncsa.png)

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.  To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.

Commercial licenses are also available. To inquire about commercial licenses, please contact Uri Wilensky at uri@northwestern.edu.

This model was created as part of the project: CONNECTED MATHEMATICS: MAKING SENSE OF COMPLEX PHENOMENA THROUGH BUILDING OBJECT-BASED PARALLEL MODELS (OBPML).  The project gratefully acknowledges the support of the National Science Foundation (Applications of Advanced Technologies Program) -- grant numbers RED #9552950 and REC #9632612.

This model was converted to NetLogo as part of the projects: PARTICIPATORY SIMULATIONS: NETWORK-BASED DESIGN FOR SYSTEMS LEARNING IN CLASSROOMS and/or INTEGRATED SIMULATION AND MODELING ENVIRONMENT. The project gratefully acknowledges the support of the National Science Foundation (REPP & ROLE programs) -- grant numbers REC #9814682 and REC-0126227. Converted from StarLogoT to NetLogo, 2001.

<!-- 1997 2001 -->
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

face-happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face-sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

person2
false
0
Circle -7500403 true true 105 0 90
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 285 180 255 210 165 105
Polygon -7500403 true true 105 90 15 180 60 195 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square - happy
false
0
Rectangle -7500403 true true 30 30 270 270
Polygon -16777216 false false 75 195 105 240 180 240 210 195 75 195

square - unhappy
false
0
Rectangle -7500403 true true 30 30 270 270
Polygon -16777216 false false 60 225 105 180 195 180 240 225 75 225

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

square-small
false
0
Rectangle -7500403 true true 45 45 255 255

square-x
false
0
Rectangle -7500403 true true 30 30 270 270
Line -16777216 false 75 90 210 210
Line -16777216 false 210 90 75 210

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

triangle2
false
0
Polygon -7500403 true true 150 0 0 300 300 300

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.0.2
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
