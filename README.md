# GridLang1
Early prototype of glyph based circuitry I dug up from years ago, I made it for writing programs shorthand on pen and paper.
User creates a grid of interconnected nodes, which change state based on the input from their neighbours most applications were intended to be audio processing and synthesis.

While they can be part of each glyph, the main flow doesn't support loops or conditional branches, because of this all structures that this system can represent could also be represented by a feed forward network with custom nodes. This realisation is why I abandoned the project to work on a feedforward version which would be easier to transpile into C or Pascal to increase performance.

My project particle brain is a spiritual successor in that in revolves around optimising feed-forward networks of custom nodes, although it focuses more on tweaking connection weights.
