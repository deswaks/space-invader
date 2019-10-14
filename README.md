# Space Invader
<img align="center" src="https://raw.githubusercontent.com/deswaks/space-invader/master/data/space-invader.png" width="280"/>

Tools for locating and reconstructing analytical building spaces with <a href="https://www.rhino3d.com/">Rhinoceros</a> and <a href="https://www.grasshopper3d.com/">Grasshopper</a>.

The tools has been created as a project at the Technical University of Denmark, August 2019. They are a work in progress and some still contain errors.

# Installation
<b>NB:</b> This software requires <a href="https://www.rhino3d.com/">Rhinoceros</a> and <a href="https://www.grasshopper3d.com/">Grasshopper</a>
1. Clone or download the repository.
2. Copy all the files from the <a href="https://github.com/deswaks/space-invader/tree/master/components">components folder</a>.
3. Paste the files into the Grasshopper User Objects Folder (optionally create a subfolder for the files).

# How to use
The tools of this package are not finished programs in themselves. They provide functions that are useful for location and reconstruction of analytical building spaces.

For instructions on how to use each component, refer to the documentation supplied in the file <i>documentation.pdf</i>

# Example
The file <i>example.gh</i> is a complete program that makes use of the majority of the functions and can locate and recreate rooms in 2D building models. For further examples on how to use all the functions, see the program files in the <i>program</i> folder in which we have made use of the rest of the tools.

# Contents of folders
<b>/components/</b> Contains all the Grasshopper components readu to be used on a Grasshopper canvas.

<b>/data/</b> Contains a collection of test models used in the development and misc. data.

<b>/ghpython component source code/</b> Contains the source code used in all the components written in GHPython and a test file for each.

<b>/programs/</b> Contains a collection of programs for locating and reconstructing building spaces. most are not finished though they still serve as examples and building blocks for further development. See the example for a finished program.

# Acknowledgements
This project was realized by Anders Bomann Christensen, Niklas Rosenkilde and Sebastian Dahl Meier with the support of The Technical University of Denmark under supervision of Assistant Professor Kristoffer Negendal and the foundation Martha og Paul Kerrn-Jespersens Fond.
