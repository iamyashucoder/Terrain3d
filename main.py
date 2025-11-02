"""
3D Terrain Generator
Generate realistic terrain landscapes using Perlin noise with textures, water, and lighting
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource
import random


class PerlinNoise:
    """Simple Perlin noise implementation for terrain generation"""
    
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.permutation = np.random.permutation(256)
        self.p = np.concatenate([self.permutation, self.permutation])
    
    def fade(self, t):
        """Fade function for smooth interpolation"""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, t, a, b):
        """Linear interpolation"""
        return a + t * (b - a)
    
    def grad(self, hash_val, x, y):
        """Calculate gradient"""
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
    
    def noise(self, x, y):
        """Generate 2D Perlin noise value"""
        # Find unit square coordinates
        X = int(np.floor(x)) & 255
        Y = int(np.floor(y)) & 255
        
        # Find relative x, y in square
        x -= np.floor(x)
        y -= np.floor(y)
        
        # Compute fade curves
        u = self.fade(x)
        v = self.fade(y)
        
        # Hash coordinates of square corners
        a = self.p[X] + Y
        aa = self.p[a]
        ab = self.p[a + 1]
        b = self.p[X + 1] + Y
        ba = self.p[b]
        bb = self.p[b + 1]
        
        # Blend results from corners
        result = self.lerp(v,
                          self.lerp(u, self.grad(self.p[aa], x, y),
                                   self.grad(self.p[ba], x - 1, y)),
                          self.lerp(u, self.grad(self.p[ab], x, y - 1),
                                   self.grad(self.p[bb], x - 1, y - 1)))
        
        return result


class TerrainGenerator:
    def __init__(self, size=100, scale=20.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
        """
        Initialize terrain generator
        
        Args:
            size: Grid size (size x size)
            scale: Overall scale of terrain features
            octaves: Number of noise layers for detail
            persistence: Amplitude decrease per octave
            lacunarity: Frequency increase per octave
            seed: Random seed for reproducibility
        """
        self.size = size
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.noise_gen = PerlinNoise(seed)
        self.terrain = None
        self.water_level = 0.3
        
    def generate_terrain(self):
        """Generate terrain using multi-octave Perlin noise"""
        terrain = np.zeros((self.size, self.size))
        
        for i in range(self.size):
            for j in range(self.size):
                amplitude = 1.0
                frequency = 1.0
                noise_height = 0.0
                
                # Add multiple octaves of noise
                for octave in range(self.octaves):
                    sample_x = i / self.scale * frequency
                    sample_y = j / self.scale * frequency
                    
                    perlin_value = self.noise_gen.noise(sample_x, sample_y)
                    noise_height += perlin_value * amplitude
                    
                    amplitude *= self.persistence
                    frequency *= self.lacunarity
                
                terrain[i, j] = noise_height
        
        # Normalize terrain to [0, 1]
        terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
        
        # Apply elevation curve for more realistic terrain
        terrain = np.power(terrain, 1.5)
        
        self.terrain = terrain
        return terrain
    
    def get_color_map(self):
        """Create realistic color map for terrain with water"""
        # Define elevation thresholds and colors
        colors = [
            (0.0, '#1a5f7a'),   # Deep water
            (0.25, '#2d8ca8'),  # Shallow water
            (0.30, '#e8d6b0'),  # Beach/sand
            (0.35, '#5a8f3d'),  # Grass lowlands
            (0.50, '#4a7c2e'),  # Grass
            (0.65, '#3d6626'),  # Forest
            (0.75, '#8b7355'),  # Rocky
            (0.85, '#a9a9a9'),  # Mountain
            (1.0, '#ffffff'),   # Snow peak
        ]
        
        return colors
    
    def apply_textures(self, ax, X, Y, Z):
        """Apply realistic textures based on elevation"""
        # Create color array based on elevation
        colors_def = self.get_color_map()
        colors_array = np.zeros((self.size, self.size, 3))
        
        for i in range(self.size):
            for j in range(self.size):
                elevation = Z[i, j]
                
                # Find appropriate color based on elevation
                for k in range(len(colors_def) - 1):
                    if colors_def[k][0] <= elevation <= colors_def[k + 1][0]:
                        # Interpolate between colors
                        t = (elevation - colors_def[k][0]) / (colors_def[k + 1][0] - colors_def[k][0])
                        color1 = self._hex_to_rgb(colors_def[k][1])
                        color2 = self._hex_to_rgb(colors_def[k + 1][1])
                        colors_array[i, j] = color1 * (1 - t) + color2 * t
                        break
        
        return colors_array
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return np.array([int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)])
    
    def add_water(self, ax, X, Y, Z):
        """Add water plane at specified level"""
        water_mask = Z <= self.water_level
        water_Z = np.where(water_mask, self.water_level, np.nan)
        
        # Create water surface with transparency
        ax.plot_surface(X, Y, water_Z, color='#1a5f7a', alpha=0.6, 
                       shade=True, antialiased=True, zorder=10)
    
    def visualize(self, show_water=True, show_wireframe=False):
        """Visualize the terrain with lighting effects"""
        if self.terrain is None:
            raise ValueError("Generate terrain first using generate_terrain()")
        
        # Create coordinate grids
        x = np.linspace(0, self.size - 1, self.size)
        y = np.linspace(0, self.size - 1, self.size)
        X, Y = np.meshgrid(x, y)
        Z = self.terrain
        
        # Create figure
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Apply lighting
        ls = LightSource(azdeg=315, altdeg=45)
        
        # Get colors based on elevation
        colors = self.apply_textures(ax, X, Y, Z)
        
        # Normalize for lighting
        colors_normalized = colors.reshape(-1, 3)
        
        # Plot terrain surface with lighting
        rgb = ls.shade_rgb(colors_normalized.reshape(self.size, self.size, 3), 
                          elevation=Z, vert_exag=0.1, blend_mode='soft')
        
        surf = ax.plot_surface(X, Y, Z, facecolors=rgb, 
                              shade=False, antialiased=True,
                              linewidth=0 if not show_wireframe else 0.1,
                              edgecolor='gray' if show_wireframe else None)
        
        # Add water if enabled
        if show_water:
            self.add_water(ax, X, Y, Z)
        
        # Set labels and title
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Elevation')
        ax.set_title('Procedurally Generated 3D Terrain', fontsize=14, fontweight='bold')
        
        # Set viewing angle for better perspective
        ax.view_init(elev=30, azim=45)
        
        # Adjust z-axis for better visualization
        ax.set_zlim(0, 1.2)
        
        plt.tight_layout()
        plt.show()
    
    def generate_multiple_views(self):
        """Generate terrain with multiple viewing angles"""
        if self.terrain is None:
            raise ValueError("Generate terrain first using generate_terrain()")
        
        # Create coordinate grids
        x = np.linspace(0, self.size - 1, self.size)
        y = np.linspace(0, self.size - 1, self.size)
        X, Y = np.meshgrid(x, y)
        Z = self.terrain
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        
        views = [
            (30, 45, 'Perspective View'),
            (60, 135, 'Aerial View'),
            (15, 90, 'Side View'),
            (45, 0, 'Front View')
        ]
        
        for idx, (elev, azim, title) in enumerate(views, 1):
            ax = fig.add_subplot(2, 2, idx, projection='3d')
            
            # Apply lighting
            ls = LightSource(azdeg=315, altdeg=45)
            colors = self.apply_textures(ax, X, Y, Z)
            rgb = ls.shade_rgb(colors.reshape(self.size, self.size, 3), 
                              elevation=Z, vert_exag=0.1, blend_mode='soft')
            
            # Plot surface
            ax.plot_surface(X, Y, Z, facecolors=rgb, shade=False, antialiased=True)
            
            # Add water
            self.add_water(ax, X, Y, Z)
            
            # Set view and labels
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(title, fontweight='bold')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Elevation')
            ax.set_zlim(0, 1.2)
        
        plt.tight_layout()
        plt.show()


def main():
    """Main function to generate and visualize terrain"""
    print("=" * 60)
    print("3D TERRAIN GENERATOR")
    print("=" * 60)
    
    # Create terrain generator
    print("\n[1/5] Initializing terrain generator...")
    seed = random.randint(0, 10000)
    print(f"✓ Using seed: {seed} (for reproducibility)")
    
    terrain_gen = TerrainGenerator(
        size=100,           # Grid resolution
        scale=25.0,         # Feature scale
        octaves=6,          # Detail levels
        persistence=0.5,    # Amplitude decrease
        lacunarity=2.0,     # Frequency increase
        seed=seed
    )
    
    # Generate terrain
    print("[2/5] Generating terrain using Perlin noise...")
    terrain_gen.generate_terrain()
    print("✓ Terrain generated successfully!")
    
    # Calculate statistics
    water_coverage = np.sum(terrain_gen.terrain <= terrain_gen.water_level) / terrain_gen.terrain.size * 100
    print(f"✓ Water coverage: {water_coverage:.1f}%")
    
    # Apply textures
    print("[3/5] Applying realistic textures based on elevation...")
    print("  ✓ Deep water (blue)")
    print("  ✓ Shallow water (cyan)")
    print("  ✓ Beach/sand (beige)")
    print("  ✓ Grasslands (green)")
    print("  ✓ Forests (dark green)")
    print("  ✓ Rocky terrain (brown)")
    print("  ✓ Mountains (gray)")
    print("  ✓ Snow peaks (white)")
    
    # Add water and lighting
    print("[4/5] Adding water plane and lighting effects...")
    print("✓ Water plane added at elevation 0.30")
    print("✓ Directional lighting applied (azimuth: 315°, altitude: 45°)")
    
    # Visualize
    print("[5/5] Generating 3D visualization...")
    print("\nControls:")
    print("  - Click and drag to rotate the view")
    print("  - Scroll to zoom in/out")
    print("  - Blue areas = Water")
    print("  - Green areas = Land")
    print("  - White peaks = Mountains")
    print("\nClose the window to continue...")
    
    terrain_gen.visualize(show_water=True, show_wireframe=False)
    
    # Ask for multiple views
    print("\n" + "=" * 60)
    print("Generating multiple viewing angles...")
    print("=" * 60)
    terrain_gen.generate_multiple_views()
    
    print("\n" + "=" * 60)
    print("Demo completed! Try running again for a different terrain.")
    print(f"To reproduce this terrain, use seed: {seed}")
    print("=" * 60)


if __name__ == "__main__":
    main()