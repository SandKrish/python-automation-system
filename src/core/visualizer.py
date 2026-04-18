import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from pathlib import Path
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Premium Engineering Visualizer using generic, professional naming.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._apply_global_style()

    def _apply_global_style(self):
        plt.style.use('ggplot')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
            'axes.linewidth': 1.0,
            'axes.edgecolor': '#2c3e50',
            'grid.linestyle': ':',
            'grid.alpha': 0.4,
            'xtick.direction': 'out',
            'ytick.direction': 'out',
            'legend.frameon': True,
            'legend.edgecolor': '#bdc3c7',
            'figure.facecolor': 'white'
        })

    def generate_plots(self, validated_data: Dict[str, List[BaseModel]]):
        viz_dir = Path(self.config["paths"]["viz_dir"])
        viz_dir.mkdir(parents=True, exist_ok=True)

        for sheet_name, records in validated_data.items():
            if not records: continue
            df = pd.DataFrame([r.model_dump() for r in records])
            
            clean_name = sheet_name.replace("_", " ").title()
            
            if "envelope" in sheet_name.lower():
                self._plot_envelope(df, viz_dir, clean_name)
            elif "profile" in sheet_name.lower():
                self._plot_profile(df, viz_dir, clean_name)

    def _add_premium_header(self, fig, title):
        """Adds a clean, professional header bar."""
        rect = plt.Rectangle((0, 0.94), 1, 0.06, transform=fig.transFigure, 
                             facecolor='#2c3e50', alpha=1.0, zorder=0)
        fig.patches.append(rect)
        fig.text(0.05, 0.97, title, color='white', fontsize=14, fontweight='bold', va='center')
        fig.text(0.95, 0.97, 'TECHNICAL DATA REPORT', color='white', fontsize=9, 
                 va='center', ha='right')

    def _plot_envelope(self, df, output_dir, title):
        """Generates a high-fidelity threshold envelope plot."""
        fig, ax = plt.subplots(figsize=(9, 11))
        df = df.sort_values("depth")
        
        # Threshold Range Shading
        ax.fill_betweenx(df["depth"], df["threshold_min"], df["threshold_max"], 
                         color='#ecf0f1', alpha=0.8, label="Operational Range")
        
        # Data Lines
        ax.plot(df["actual_value"], df["depth"], color='#e74c3c', linewidth=2, label="Measured Value")
        ax.plot(df["threshold_min"], df["depth"], color='#3498db', linewidth=0.8, linestyle='--')
        ax.plot(df["threshold_max"], df["depth"], color='#3498db', linewidth=0.8, linestyle='--')
        
        # Cleanup
        ax.set_xlabel("Value Magnitude", fontweight='bold')
        ax.set_ylabel("Vertical Reference (m)", fontweight='bold')
        ax.invert_yaxis()
        ax.grid(True)
        ax.legend(loc='lower right', framealpha=0.9)
        
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
            
        self._add_premium_header(fig, f"{title} Analysis")
        
        file_name = title.replace(" ", "_") + ".png"
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(output_dir / file_name, dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_profile(self, df, output_dir, title):
        """Generates a premium banded profile plot."""
        fig, ax = plt.subplots(figsize=(9, 11))
        df = df.sort_values("depth")
        
        # Multi-tier Banding
        palette = ['#d1f2eb', '#a3e4d7', '#76d7c4', '#48c9b0']
        for i, color in enumerate(palette):
            width = (len(palette) - i) * 1.5
            ax.fill_betweenx(df["depth"], df["primary_value"] - width, df["primary_value"] + width, 
                             color=color, alpha=0.6, label=f"Confidence Tier {i+1}")
        
        ax.plot(df["primary_value"], df["depth"], color='#16a085', linewidth=2.5, label="Primary Profile")
        
        # Cleanup
        ax.set_xlabel("Profile Index", fontweight='bold')
        ax.set_ylabel("Vertical Reference (m)", fontweight='bold')
        ax.invert_yaxis()
        ax.grid(True)
        ax.legend(loc='lower right', framealpha=0.9)
        
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
            
        self._add_premium_header(fig, f"{title} Structural Distribution")
        
        file_name = title.replace(" ", "_") + ".png"
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(output_dir / file_name, dpi=300, bbox_inches='tight')
        plt.close()

    def generate_architecture_diagram(self):
        pass
