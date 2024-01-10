# Moirepattern

Moirepattern is a Python library that enables the creation of moire patterns. At the moment, it can only generate simple moire patterns by controlling the angle and distance between interferences. It's planned to have construction operations that would allow the user to make any shape, in 2 or 3 dimensions, and several predefined geometries as well."

## Installation

You can install Moirepattern via pip using the following command:

```bash
pip install git+https://github.com/funkaro1/moire-constructor.git
```
## Creating Moire Patterns

**Create a Moire Object:** 

Initialize a moire object with the following parameters:

- interference_distance: Distance between two interference lines (in 3D cases, this represents the distance on the surface without distortion).

- base_grid_gap: Gap between the lines forming the base grid (the equidistant grid overlaid to create the desired moire pattern).

- angle: Angle of the interference lines.

```bash
moire = Moirepattern.Moire(interference_distance, base_grid_gap, angle)
```

**Set Size:** 

Define the size of the moire pattern using set_size(x_size, y_size)

```bash
moire.set_size(x_size, y_size)
```
**Create Moire Pattern:** 

Generate the moire pattern by specifying the interference type. Currently, only "simple" interference is supported.

```bash
moire.make("simple")
```

## Exporting Results

You can export the generated moire pattern and the base grid:

- export(filename): Export the moire pattern to a file.

- export_base(filename): Export the base grid to a file.

## Accessing Lines

Access the lines generated in the moire pattern using the .poly attribute, which returns an array containing arrays of points defining each line.

```bash
lines = moire.poly
```

## Example Usage

```bash
import Moirepattern as mp

moire = mp.Moire(10, 5, 30)
moire.set_size(800, 600)
moire.make("simple")
moire.export("moire_pattern.svg")
moire.export_base("base_grid.svg")

lines = moire.poly
print(lines)
```
