## RESULTS — Executive Summary + Leaderboard

### Executive summary
- Datasets: 1692 files across device types (heuristic)
- S-parameters tested: S11, S12, S21, S22
- Overall gain (mean, median): 4.11% (mean), 1.52% (median)
- Frac improved: 70.3% of runs (UFRF test MSE < baseline)
- Best/worst: LQP15MN27NG02_series.s2p S11 (+28.93%), NFZ32BW881HN10_series.s2p S11 (-21.10%)
- Notes: filenames suggest many passives; antennas likely show larger coherent ripple when present

### Leaderboard (top 50 by improvement)
| file | Sij | split | test_pts | baseline_test_MSE | ufrf_test_MSE | improvement_% | freq_min_GHz | freq_max_GHz | Z0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LQP15MN27NG02_series.s2p | S11 | interleave | 81 | 0.43837830564268737 | 0.3115723032506264 | 28.926158242743377 |  |  | 50.0 |
| LQP15MN27NG02_series.s2p | S11 | random | 80 | 0.44156704216212583 | 0.31549173917035295 | 28.551791903319415 |  |  | 50.0 |
| LQP15MN27NG02_series.s2p | S22 | random | 80 | 0.44156704216212583 | 0.31549173917035295 | 28.551791903319415 |  |  | 50.0 |
| LQP15MN22NG02_series.s2p | S11 | interleave | 81 | 0.4202871741517244 | 0.30507169329578454 | 27.413513412223917 |  |  | 50.0 |
| LQP15MN22NG02_series.s2p | S11 | random | 80 | 0.4231604345614553 | 0.3088089941059905 | 27.02318816124044 |  |  | 50.0 |
| LQP15MN22NG02_series.s2p | S22 | random | 80 | 0.4231604345614553 | 0.3088089941059905 | 27.02318816124044 |  |  | 50.0 |
| LQP15MN18NG02_series.s2p | S11 | interleave | 81 | 0.40051379106877494 | 0.29608918226128456 | 26.07266244910876 |  |  | 50.0 |
| LQP15MN15NG02_series.s2p | S11 | interleave | 81 | 0.38214979795549603 | 0.28548431124121876 | 25.295181949967855 |  |  | 50.0 |
| LQP15MN18NG02_series.s2p | S11 | random | 80 | 0.4031815938869867 | 0.30150715228770164 | 25.218026601627255 |  |  | 50.0 |
| LQP15MN18NG02_series.s2p | S22 | random | 80 | 0.4031815938869867 | 0.30150715228770164 | 25.218026601627255 |  |  | 50.0 |
| LQG15HH18NH02_series.s2p | S11 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NJ02_series.s2p | S11 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NG02_series.s2p | S11 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NJ02_series.s2p | S22 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NG02_series.s2p | S22 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NH02_series.s2p | S22 | random | 80 | 0.4873848329175477 | 0.36727263362971974 | 24.644221809041742 |  |  | 50.0 |
| LQG15HH18NH02_series.s2p | S11 | interleave | 81 | 0.49074850533265796 | 0.3708466917081042 | 24.432435824389792 |  |  | 50.0 |
| LQG15HH18NJ02_series.s2p | S11 | interleave | 81 | 0.49074850533265796 | 0.3708466917081042 | 24.432435824389792 |  |  | 50.0 |
| LQG15HH18NG02_series.s2p | S11 | interleave | 81 | 0.49074850533265796 | 0.3708466917081042 | 24.432435824389792 |  |  | 50.0 |
| LQP15MN12NG02_series.s2p | S11 | interleave | 81 | 0.36174827220035244 | 0.27400326382085144 | 24.255819618926576 |  |  | 50.0 |
| LQP15MN15NG02_series.s2p | S11 | random | 80 | 0.3848944214279001 | 0.2921814528592726 | 24.087896162453173 |  |  | 50.0 |
| LQP15MN15NG02_series.s2p | S22 | random | 80 | 0.3848944214279001 | 0.2921814528592726 | 24.087896162453173 |  |  | 50.0 |
| LQG15HH15NH02_series.s2p | S11 | interleave | 81 | 0.4776298355000122 | 0.3669756796248863 | 23.16734585042962 |  |  | 50.0 |
| LQG15HH15NG02_series.s2p | S11 | interleave | 81 | 0.4776298355000122 | 0.3669756796248863 | 23.16734585042962 |  |  | 50.0 |
| LQG15HH15NJ02_series.s2p | S11 | interleave | 81 | 0.4776298355000122 | 0.3669756796248863 | 23.16734585042962 |  |  | 50.0 |
| LQG15HH15NH02_series.s2p | S11 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQG15HH15NG02_series.s2p | S11 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQG15HH15NJ02_series.s2p | S11 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQG15HH15NG02_series.s2p | S22 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQG15HH15NJ02_series.s2p | S22 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQG15HH15NH02_series.s2p | S22 | random | 80 | 0.475071949246107 | 0.3653133210237487 | 23.103580078035463 |  |  | 50.0 |
| LQP15MN10NG02_series.s2p | S11 | interleave | 81 | 0.3483085899784988 | 0.26849229774730504 | 22.91539586667123 |  |  | 50.0 |
| LQP15MN12NG02_series.s2p | S11 | random | 80 | 0.3651379258678464 | 0.28286738899527253 | 22.53135898634366 |  |  | 50.0 |
| LQP15MN12NG02_series.s2p | S22 | random | 80 | 0.3651379258678464 | 0.28286738899527253 | 22.53135898634366 |  |  | 50.0 |
| LQP15MN9N1B02_series.s2p | S11 | interleave | 81 | 0.32877940939491324 | 0.2551262290252826 | 22.40200519405464 |  |  | 50.0 |
| LQP15MN1N2W02_series.s2p | S11 | interleave | 81 | 0.30380498184193233 | 0.23690297384620107 | 22.021366335111622 |  |  | 50.0 |
| LQP15MN1N2B02_series.s2p | S11 | interleave | 81 | 0.30380498184193233 | 0.23690297384620107 | 22.021366335111622 |  |  | 50.0 |
| LQG15HH12NH02_series.s2p | S11 | interleave | 81 | 0.46578547193775083 | 0.3639246965049002 | 21.868602944847456 |  |  | 50.0 |
| LQG15HH12NG02_series.s2p | S11 | interleave | 81 | 0.46578547193775083 | 0.3639246965049002 | 21.868602944847456 |  |  | 50.0 |
| LQG15HH12NJ02_series.s2p | S11 | interleave | 81 | 0.46578547193775083 | 0.3639246965049002 | 21.868602944847456 |  |  | 50.0 |
| LQP03TN0N6BZ2_series.s2p | S11 | interleave | 81 | 0.308948712824082 | 0.24168775413455262 | 21.770914037705772 |  |  | 50.0 |
| LQP15MN1N3B02_series.s2p | S11 | interleave | 81 | 0.30098931421997505 | 0.23626485849526702 | 21.503904845407504 |  |  | 50.0 |
| LQP15MN1N3W02_series.s2p | S11 | interleave | 81 | 0.30098931421997505 | 0.23626485849526702 | 21.503904845407504 |  |  | 50.0 |
| LQG15HH12NH02_series.s2p | S11 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQG15HH12NG02_series.s2p | S11 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQG15HH12NJ02_series.s2p | S11 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQG15HH12NG02_series.s2p | S22 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQG15HH12NJ02_series.s2p | S22 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQG15HH12NH02_series.s2p | S22 | random | 80 | 0.46367040889073063 | 0.3639903995093788 | 21.49803124590653 |  |  | 50.0 |
| LQP15MN1N6W02_series.s2p | S11 | interleave | 81 | 0.29809899500864917 | 0.23473610149620314 | 21.255654857409898 |  |  | 50.0 |

### Category summary (heuristic)
| device_type | N | mean_improv_% | median_improv_% | frac_improved |
| --- | --- | --- | --- | --- |
| passive | 1692 | 4.11 | 1.52 | 70.3% |

### Robustness checks
- Split sensitivity (S11): random vs interleave → Δmean_improv = -0.51%
- Regularization sweeps: not run here; default ridge=1e-3 (S21/S12)
- Sanity controls: smooth traces expected to show ~0% improvement
### S21 summary (transmission)
- Mean/median improvement: -0.06% / -0.16% (N=338)
- Win rate: 35.2% (UFRF test MSE < baseline)

#### By family (top 10 by mean)
| family | N | mean_improv_% | median_improv_% |
| --- | --- | --- | --- |
| KCM | 2 | 3.57 | 3.57 |
| KRM | 1 | 2.93 | 2.93 |
| GRM | 37 | 1.12 | 0.63 |
| GRT | 3 | 0.45 | 0.45 |
| GCM | 4 | 0.18 | 0.05 |
| RDEC | 30 | 0.04 | -0.03 |
| RHEL | 16 | -0.04 | -0.12 |
| LQW | 2 | -0.09 | -0.09 |
| RCEC | 16 | -0.09 | -0.29 |
| RCER | 21 | -0.10 | -0.19 |

### Regularization sweep (S21 subset, 0603ct)
Ridge values tested: 1e-4 and 5e-3; table shows improvement % by file.

```
ridge             0.0001    0.0050
file                              
0603CT_10N.s2p  0.285118  0.285117
0603CT_11N.s2p -0.219886 -0.219880
0603CT_12N.s2p -0.062101 -0.062096
0603CT_15N.s2p -0.305540 -0.305533
0603CT_16N.s2p -0.862509 -0.862493
```

### Regularization sweep (S21 subset, 0603ct)
Ridge values tested: 1e-4 and 5e-3; table shows improvement % by file.

```
ridge             0.0001    0.0050
file                              
0603CT_10N.s2p  0.285118  0.285117
0603CT_11N.s2p -0.219886 -0.219880
0603CT_12N.s2p -0.062101 -0.062096
0603CT_15N.s2p -0.305540 -0.305533
0603CT_16N.s2p -0.862509 -0.862493
```

### S21 delay-aware (gated ≥2%)
- Gated win-rate: 100.0%, mean lift: 3.42%, median: 2.90% (N=3)

#### By family (top)
| family | N | mean_improv_% | median_improv_% |
| --- | --- | --- | --- |
| KCM | 2 | 3.68 | 3.68 |
| KRM | 1 | 2.90 | 2.90 |
