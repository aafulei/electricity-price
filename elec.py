import itertools as it
g_no_plot = False
try:
    import pandas as pd
except ImportError:
    g_no_plot = True

g_fuel_clause_charge = 0.329
g_special_rebate = 0.01
g_govt_subsidy = 80
g_govt_relief = 50


def net_rate(units):
    a = [0.674, 0.813, 0.952, 1.188, 1.327, 1.466, 1.605]
    b = [150, 150, 200, 200, 300, 500]
    c = [x[0] * x[1] for x in zip(a, b)]
    B = list(it.accumulate(b))
    C = list(it.accumulate(c))
    for i in reversed(range(len(B))):
        if units > B[i]:
            return (units - B[i]) * a[i+1] + C[i]
    return units * a[0]


def rate(units):
    return net_rate(units) + (g_fuel_clause_charge - g_special_rebate) * units


def charge(units):
    r = rate(units)
    if units <= 100:
        r *= 0.95
    return r - g_govt_subsidy - g_govt_relief


def bar():
    print("-" * 60)


def tu(max_units, headline=True):
    """Total units in a month"""
    if headline:
        bar()
        au = max_units / 30
        aw = au * 1000 / 24
        print(f"Using {max_units} units a month " +
              f"({au:.1f} units @ {aw:.0f}W a day)")
        bar()
    samples = list(range(0, int(max_units) + 1, 1))
    charges = [charge(x) for x in samples]
    print(" Unit(kWh)       Charge        Per Unit")
    for i, v in enumerate(charges):
        if i and i % 100 == 0:
            a = v / i
            print(f"{i:>4}\t\t{v:>7.2f}\t\t{a:>5.2f}")
    units = samples[-1]
    paid = charges[-1]
    average = paid / units
    marginal = charge(units + 1) - paid
    bar()
    print(f"Fuel clause charge for 1 unit @ HK${g_fuel_clause_charge:.3f}")
    print(f"Special rebate for 1 unit @ HK${g_special_rebate:.2f}")
    print(f"Govt subsidy @ HK${g_govt_subsidy}")
    print(f"Govt relief @ HK${g_govt_relief}")
    bar()
    print(f"For each 1 unit you pay HK${average:.2f}")
    print(f"For the next 1 more unit you need to pay HK${marginal:.2f}")
    print(f"For {units:,} units you pay HK${paid:,.2f}")
    bar()

    if not g_no_plot:
        s = pd.Series(charges, index=samples)
        s.plot.line(style=".-", markevery=100)


def wa(watts):
    """Daily watts on average"""
    bar()
    u = watts * 24 / 1000
    print(f"Running {watts}W ({u:.0f} units per day) for 1 month")
    bar()
    tu(watts * 24 * 30 / 1000, headline=False)


def du(daily_units):
    """Daily units on average"""
    bar()
    w = daily_units / 24 * 1000
    print(f"Using {daily_units} units per day (avg {w:.0f}W) for 1 month")
    bar()
    tu(daily_units * 30, headline=False)
