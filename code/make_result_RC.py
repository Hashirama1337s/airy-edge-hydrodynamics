"""Collect rc_<d>.json into RESULT.json (exact BAR keys, numbers as strings) and RESULT_diag.json (extra diagnostics)."""
import json, os
import numpy as np

H = "out"
res, diag = {}, {}
for d in ("512", "1024", "8192"):
    f = os.path.join(H, "rc_%s.json" % d)
    if not os.path.exists(f):
        continue
    r = json.load(open(f))
    o, i, ry = r['out'], r['in'], r['rays']
    lit = sorted(set(o['lit_1e6_n']) | set(o['lit_1e6_2n']))
    mj = max(max(ry['maxjump_A']), max(ry['maxjump_B']))
    res[d] = {"R_in": repr(r['Rin']), "R_out": repr(r['Rout']),
              "in_max_mismatch_n": "%.3e" % i['max_mismatch_n'], "in_max_mismatch_2n": "%.3e" % i['max_mismatch_2n'],
              "out_lit_sectors": [str(k) for k in lit], "sector_of_c0": str(r['sector_of_c0']),
              "out_mismatch_c0_n": "%.6e" % o['mismatch_c0_n'], "out_mismatch_c0_2n": "%.6e" % o['mismatch_c0_2n'],
              "max_ray_jump": "%.3e" % mj}
    kc = r['sector_of_c0']
    diag[d] = {"units": "mismatch in qnmx w units (wfr = 2 w); lit = mismatch > 1e-6",
               "K": r['K'], "n": r['n'], "tolA": r['tolA'], "dr": r['dr'], "absc0": r['absc0'], "argc0": r['argc0'],
               "in_above_1e9_n": i['above_1e9_n'], "in_above_1e9_2n": i['above_1e9_2n'],
               "in_max_arc_n_vs_2n": float(np.nanmax(i['arc_end_n_vs_2n'])),
               "out_max_mismatch_other_n": o['max_mismatch_other_n'], "out_max_mismatch_other_2n": o['max_mismatch_other_2n'],
               "out_above_1e9_n": o['above_1e9_n'], "out_above_1e9_2n": o['above_1e9_2n'],
               "out_c0_n_vs_2n_rel": abs(o['mismatch_c0_n'] - o['mismatch_c0_2n']) / o['mismatch_c0_2n'],
               "out_c0_arc_end_n_vs_2n": o['arc_end_n_vs_2n'][kc],
               "out_max_arc_n_vs_2n_other": float(np.nanmax(np.delete(np.array(o['arc_end_n_vs_2n']), kc))),
               "ray_maxjump_A": max(ry['maxjump_A']), "ray_maxjump_B": max(ry['maxjump_B']),
               "ray_A_vs_B_max_Rin": max(ry['AB_diff_Rin']), "ray_A_vs_B_max_Rout": max(ry['AB_diff_Rout']),
               "ray_min_spacing": min(ry['minsp_A']), "ray_steps_A_max": max(ry['nstep_A']), "ray_steps_B_max": max(ry['nstep_B']),
               "ray_rejections_A": sum(ry['nrej_A']), "ray_rejections_B": sum(ry['nrej_B']),
               "arc_maxjump": max(max(i['arc_maxjump_n']), max(i['arc_maxjump_2n']), max(o['arc_maxjump_n']), max(o['arc_maxjump_2n'])),
               "arc_stuck_in": i['arc_stuck'], "arc_stuck_out": o['arc_stuck'],
               "arc_rejections": sum(i['arc_rej_n']) + sum(i['arc_rej_2n']) + sum(o['arc_rej_n']) + sum(o['arc_rej_2n']),
               "wall_sec": r['sec'], "rays_sec": ry['sec'], "arcs_sec": r['arcs_sec']}
json.dump(res, open(os.path.join(H, "RESULT.json"), "w"), indent=1)
json.dump(diag, open(os.path.join(H, "RESULT_diag.json"), "w"), indent=1)
print(json.dumps(res, indent=1)); print(json.dumps(diag, indent=1))
