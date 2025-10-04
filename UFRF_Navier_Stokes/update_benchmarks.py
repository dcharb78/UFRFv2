import os
import json


def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return None


def main():
    root = os.path.abspath('.')
    entries = {}
    # 3D TG
    tg = read_json(os.path.join(root, 'results3d', 'tg_summary.json'))
    if tg:
        entries['3D_TG'] = tg
    # Forced comparisons (2D)
    kol = read_json(os.path.join(root, 'results_forced', 'ForcedTurbulence.json'))
    ufrf = read_json(os.path.join(root, 'results_forced', 'ForcedTurbulenceUFRF.json'))
    if kol and ufrf:
        entries['2D_forced'] = {'kolmogorov': kol, 'ufrf_wedge': ufrf}
    # Boundary
    cav = read_json(os.path.join(root, 'results_boundary', 'cavity_summary.json'))
    chn = read_json(os.path.join(root, 'results_boundary', 'channel_summary.json'))
    if cav:
        entries['2D_cavity'] = cav
    if chn:
        entries['2D_channel'] = chn

    # Write block to append into BenchmarkComparison.md
    block = [
        '## Current Metrics (auto)\n\n\n',
        '```json\n',
        json.dumps(entries, indent=2),
        '\n```\n'
    ]
    bm_path = os.path.join(root, 'BenchmarkComparison.md')
    with open(bm_path, 'a') as f:
        f.writelines(block)
    print('BenchmarkComparison.md updated with current metrics.')


if __name__ == '__main__':
    main()


