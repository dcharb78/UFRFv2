#!/usr/bin/env python3
"""
Generate real knot data using spherogram for PD-first workflow.
This script creates a comprehensive dataset of real knots with proper PD codes.
"""

import json
import pandas as pd
import os

def make_real_knots_pd():
    """
    Generate real knot data using spherogram library.
    Creates knots from Rolfsen table up to 8 crossings.
    """
    try:
        from spherogram import Link
        print("✓ spherogram available - using real knot library")
    except ImportError:
        print("✗ spherogram not available - using DT codes as fallback")
        return make_real_knots_dt_fallback()
    
    # Rolfsen table up to 8 crossings - clean subset
    names = [
        "3_1", "4_1", "5_1", "5_2", "6_1", "6_2", "6_3", 
        "7_1", "7_2", "7_3", "7_4", "7_5", "7_6", "7_7",
        "8_1", "8_2", "8_3", "8_4", "8_5", "8_6", "8_7", "8_8", 
        "8_9", "8_10", "8_11", "8_12", "8_13", "8_14", "8_15", 
        "8_16", "8_17", "8_18", "8_19", "8_20", "8_21"
    ]
    
    rows = []
    successful = 0
    failed = []
    
    for name in names:
        try:
            # Create real knot from library
            L = Link(name)
            pc = L.PD_code()  # Get PD code
            
            # Convert to list of tuples for JSON serialization
            pd_list = [tuple(cr) for cr in pc]
            
            # Add original knot
            rows.append({
                "knot_id": f"K_{name}",
                "pd_code": json.dumps(pd_list),
                "dt_code": "",  # Will be filled by pipeline if needed
                "phase_vector": "[0,0,0,0,0,0,0,0,0,0,0,0,0]"  # Default phase vector
            })
            
            # Add mirror (simple reversal for now)
            rows.append({
                "knot_id": f"K_{name}_mirror", 
                "pd_code": json.dumps(pd_list[::-1]),  # Simple mirror placeholder
                "dt_code": "",
                "phase_vector": "[0,0,0,0,0,0,0,0,0,0,0,0,0]"  # Default phase vector
            })
            
            successful += 1
            print(f"✓ Generated {name} (PD with {len(pd_list)} crossings)")
            
        except Exception as e:
            failed.append((name, str(e)))
            print(f"✗ Failed {name}: {e}")
    
    print(f"\nSummary: {successful} knots generated, {len(failed)} failed")
    if failed:
        print("Failed knots:", [name for name, _ in failed])
    
    # Create DataFrame and save
    df = pd.DataFrame(rows)
    output_path = "data/real_knots_pd.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved {len(df)} knots to {output_path}")
    
    return output_path

def make_real_knots_dt_fallback():
    """
    Fallback: Create knot data using DT codes from known sources.
    """
    print("Creating fallback DT-based dataset...")
    
    # DT codes for Rolfsen table (from Knot Atlas/Dartmouth)
    dt_data = {
        "K_3_1": "[4, 6, 2]",
        "K_4_1": "[4, 6, 8, 2]", 
        "K_5_1": "[6, 8, 10, 2, 4]",
        "K_5_2": "[4, 8, 10, 2, 6]",
        "K_6_1": "[4, 6, 10, 12, 2, 8]",
        "K_6_2": "[4, 8, 12, 2, 10, 6]",
        "K_6_3": "[6, 10, 12, 2, 4, 8]",
        "K_7_1": "[8, 10, 12, 14, 2, 4, 6]",
        "K_7_2": "[4, 8, 12, 14, 2, 6, 10]",
        "K_7_3": "[4, 10, 12, 14, 2, 6, 8]",
        "K_7_4": "[6, 8, 12, 14, 2, 4, 10]",
        "K_7_5": "[6, 10, 14, 2, 4, 8, 12]",
        "K_7_6": "[4, 8, 10, 14, 2, 6, 12]",
        "K_7_7": "[4, 6, 12, 14, 2, 8, 10]"
    }
    
    rows = []
    for knot_id, dt_code in dt_data.items():
        # Add original
        rows.append({
            "knot_id": knot_id,
            "dt_code": dt_code,
            "pd_code": "",
            "phase_vector": ""
        })
        
        # Add mirror (reverse DT)
        mirror_dt = dt_code[::-1] if dt_code else ""
        rows.append({
            "knot_id": knot_id + "_mirror",
            "dt_code": mirror_dt,
            "pd_code": "",
            "phase_vector": ""
        })
    
    df = pd.DataFrame(rows)
    output_path = "data/real_knots_dt.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Saved {len(df)} knots to {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Try PD-first approach
    output_file = make_real_knots_pd()
    
    print(f"\n🎯 Ready to run pipeline with: {output_file}")
    print("\nNext steps:")
    print("1. python scripts/make_composites.py --knots", output_file, "--out data/real_composites_pd.csv --pairs all")
    print("2. python scripts/run_joint_pipeline.py --mode phase --feature_mode multiscale --geometry_mode pd \\")
    print("     --knots", output_file, "--composites data/real_composites_pd.csv --out results/real_pd_comprehensive")
    print("3. python scripts/analyze_subadditivity.py --results results/real_pd_comprehensive/phase_results.json --out results/real_pd_comprehensive_plots")
