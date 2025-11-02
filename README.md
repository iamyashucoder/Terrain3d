# 3D Terrain Generator

A Python project that generates realistic procedural terrain landscapes using Perlin noise with textures, water planes, and realistic lighting effects.

## Features

- **Perlin Noise Generation**: Multi-octave Perlin noise for realistic terrain
- **Realistic Textures**: Elevation-based coloring (water, sand, grass, forest, rock, snow)
- **Water Simulation**: Transparent water plane with proper depth shading
- **Advanced Lighting**: Directional light source for realistic shadows and highlights
- **Multiple Views**: Generate terrain from different angles
- **Customizable**: Adjust size, scale, detail level, and random seed
![Demo Animation](./assets/demo.gif)

## Setup Instructions

### 1. Create Conda Environment

```bash
conda create -n terrain3d python=3.9 -y
conda activate terrain3d
```

### 2. Install Required Packages

```bash
pip install numpy matplotlib
```

Only two packages needed - same as the maze project!

### 3. Run the Demo

```bash
python main.py
```

## How It Works

### Perlin Noise Algorithm
- **Multi-octave noise**: Combines multiple frequencies for realistic detail
- **Persistence**: Controls how quickly amplitude decreases (default: 0.5)
- **Lacunarity**: Controls frequency increase between octaves (default: 2.0)
- **Octaves**: Number of noise layers combined (default: 6)

### Texture System
Elevation-based coloring creates realistic biomes:

| Elevation | Color | Terrain Type |
|-----------|-------|--------------|
| 0.00 - 0.25 | Deep Blue | Deep Water |
| 0.25 - 0.30 | Cyan | Shallow Water |
| 0.30 - 0.35 | Beige | Beach/Sand |
| 0.35 - 0.50 | Light Green | Grasslands |
| 0.50 - 0.65 | Green | Grass/Forest |
| 0.65 - 0.75 | Dark Green | Dense Forest |
| 0.75 - 0.85 | Brown | Rocky Terrain |
| 0.85 - 1.00 | Gray to White | Mountains/Snow |

### Lighting
- **Light Source**: Positioned at azimuth 315° and altitude 45°
- **Soft Blending**: Creates smooth, realistic shadows
- **Vertex Exaggeration**: Enhances terrain features without distortion

### Water Rendering
- Semi-transparent blue plane at elevation 0.30
- Only visible where terrain is below water level
- Proper depth-based shading

## Controls

When the visualization windows open:
- **Click and drag**: Rotate the 3D view
- **Scroll wheel**: Zoom in/out
- **Close window**: Continue to next visualization

## Customization

Edit these parameters in `main.py` to customize terrain:

```python
terrain_gen = TerrainGenerator(
    size=100,          # Grid resolution (50-200 recommended)
    scale=25.0,        # Feature size (10-50)
    octaves=6,         # Detail level (3-8)
    persistence=0.5,   # Amplitude decay (0.3-0.7)
    lacunarity=2.0,    # Frequency growth (1.5-3.0)
    seed=12345         # For reproducible terrain
)
```

### Parameter Guide

**size**: Grid resolution
- 50 = Fast, less detail
- 100 = Balanced (default)
- 200 = High detail, slower

**scale**: Feature size
- 10 = Many small features
- 25 = Balanced (default)
- 50 = Large, smooth features

**octaves**: Detail layers
- 3 = Smooth terrain
- 6 = Realistic (default)
- 8 = Very detailed, rocky

**persistence**: Height variation
- 0.3 = Gentle hills
- 0.5 = Balanced (default)
- 0.7 = Dramatic peaks

**water_level**: Adjust water coverage
```python
terrain_gen.water_level = 0.25  # More water
terrain_gen.water_level = 0.35  # Less water
```

## Project Structure

```
├── main.py          # Complete implementation
└── README.md        # This file
```

## Example Output

```
============================================================
3D TERRAIN GENERATOR
============================================================

[1/5] Initializing terrain generator...
✓ Using seed: 7342 (for reproducibility)
[2/5] Generating terrain using Perlin noise...
✓ Terrain generated successfully!
✓ Water coverage: 32.4%
[3/5] Applying realistic textures based on elevation...
  ✓ Deep water (blue)
  ✓ Shallow water (cyan)
  ✓ Beach/sand (beige)
  ✓ Grasslands (green)
  ✓ Forests (dark green)
  ✓ Rocky terrain (brown)
  ✓ Mountains (gray)
  ✓ Snow peaks (white)
[4/5] Adding water plane and lighting effects...
✓ Water plane added at elevation 0.30
✓ Directional lighting applied (azimuth: 315°, altitude: 45°)
[5/5] Generating 3D visualization...

Controls:
  - Click and drag to rotate the view
  - Scroll to zoom in/out
  - Blue areas = Water
  - Green areas = Land
  - White peaks = Mountains

Close the window to continue...
```

## Advanced Features

### Wireframe Mode
Enable wireframe overlay to see mesh structure:
```python
terrain_gen.visualize(show_water=True, show_wireframe=True)
```

### Disable Water
View terrain without water plane:
```python
terrain_gen.visualize(show_water=False, show_wireframe=False)
```

### Multiple Views
The demo automatically shows 4 different viewing angles:
1. Perspective View (30°, 45°)
2. Aerial View (60°, 135°)
3. Side View (15°, 90°)
4. Front View (45°, 0°)

## Tips for Best Results

1. **Island Generation**: Use lower water_level (0.25) for more water
2. **Mountain Ranges**: Use higher persistence (0.6-0.7) and more octaves (7-8)
3. **Rolling Hills**: Use fewer octaves (3-4) and lower persistence (0.4)
4. **Performance**: Reduce size to 50 for faster generation
5. **Detail**: Increase size to 150-200 for publication-quality renders

## Requirements

- Python 3.9+
- numpy
- matplotlib

## Troubleshooting

**Issue**: Visualization is slow
- **Solution**: Reduce `size` parameter (try 50 or 75)

**Issue**: Terrain looks too smooth
- **Solution**: Increase `octaves` to 7-8 or reduce `scale` to 15-20

**Issue**: Terrain looks too chaotic
- **Solution**: Reduce `octaves` to 4-5 or increase `scale` to 30-40

**Issue**: Not enough water/land
- **Solution**: Adjust `terrain_gen.water_level` (0.20-0.40 range)

**Issue**: Colors look unrealistic
- **Solution**: Modify color thresholds in `get_color_map()` method

## Technical Details

### Perlin Noise Implementation
- Uses gradient-based interpolation for smooth terrain
- Implements fade function for organic transitions
- Combines multiple octaves using fractal Brownian motion (fBm)

### Color Interpolation
- Linear interpolation between elevation thresholds
- Hex to RGB conversion for precise color control
- Smooth transitions between biomes

### Lighting Model
- Uses matplotlib's LightSource for realistic shading
- Soft blend mode for natural appearance
- Configurable light direction and intensity

## License

Free to use and modify for educational and personal projects.

## Author

Created as a demonstration of procedural terrain generation using Perlin noise.