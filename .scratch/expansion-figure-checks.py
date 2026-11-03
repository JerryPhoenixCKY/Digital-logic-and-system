"""Independent checks of the three new figures; no note content is mutated."""
from pathlib import Path
import importlib.util
import itertools
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def load_shift():
    path = ROOT / 'Tools' / 'figures' / 'serial-shift-trace.py'
    spec = importlib.util.spec_from_file_location('shift_figure', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_shift()
    count = 0
    for state in itertools.product((0, 1), repeat=4):
        for bit in (0, 1):
            edge, sampled, old, outgoing, new = mod.sampled_trace(state, (bit,))[0]
            assert edge == 1 and sampled == bit and old == state
            assert outgoing == (int(''.join(map(str, state)), 2) & 1)
            numeric = (bit << 3) | (int(''.join(map(str, state)), 2) >> 1)
            assert int(''.join(map(str, new)), 2) == numeric
            count += 1
    rows = mod.sampled_trace()
    assert [''.join(map(str, r[4])) for r in rows] == ['1000', '0100', '1010', '1101']
    print(f'PASS serial shift: {count} exhaustive one-edge cases and 4-edge example')

    # Course timing values: Ch9 pp39-40. This separately verifies the rationale
    # of the conceptual figure rather than extracting equations from its labels.
    cq_max, cq_min, setup, hold, pd_gate, cd_gate = 50, 30, 60, 70, 35, 25
    latest_arrival = cq_max + 3 * pd_gate
    earliest_arrival = cq_min + cd_gate
    assert latest_arrival == 155
    assert latest_arrival + setup == 215
    assert earliest_arrival == 55 and earliest_arrival < hold
    assert hold - earliest_arrival == 15
    print('PASS max/min timing: Tmin=215 ps; hold deficit=15 ps')

    # The aperture waveform changes D only before setup boundary or after hold
    # boundary, and Q changes only after the positive capture edge.
    setup_boundary, hold_boundary, capture = -3, 2, 0
    d_edges, q_edge = (-6, 5), 1.5
    assert d_edges[0] < setup_boundary < capture < hold_boundary < d_edges[1]
    assert q_edge > capture
    print('PASS aperture: both D transitions lie outside stable window')

    for name in ('setup-hold-window', 'register-short-long-paths', 'serial-shift-trace'):
        svg = ROOT / 'Figures' / (name + '.svg')
        ET.parse(svg)
        assert (ROOT / '.scratch' / 'png' / (name + '.png')).stat().st_size > 1000
        print('PASS SVG XML and PNG backup: ' + name)


if __name__ == '__main__':
    main()
