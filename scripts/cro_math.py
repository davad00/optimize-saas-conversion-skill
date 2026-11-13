#!/usr/bin/env python3
"""Read-only CRO arithmetic. Python 3 standard library; JSON results on stdout.

Rates use fractions (0.05 means 5%); money uses Decimal strings.
Statistical outputs assume independent Bernoulli observations and fixed horizons.
They cannot validate an experiment or determine whether a variant should ship.
"""

import argparse
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
import json
import math
import re
from statistics import NormalDist
import sys


NORMAL = NormalDist()


def finite_number(value):
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise argparse.ArgumentTypeError("must be a finite number") from exc
    if not math.isfinite(result):
        raise argparse.ArgumentTypeError("must be a finite number")
    return result


def probability(value):
    result = finite_number(value)
    if not 0 < result < 1:
        raise argparse.ArgumentTypeError("must be strictly between 0 and 1")
    return result


def positive_number(value):
    result = finite_number(value)
    if result <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return result


def count(value):
    if not re.fullmatch(r"[0-9]+", value):
        raise argparse.ArgumentTypeError("must be a nonnegative integer")
    result = int(value)
    if result > 2**53 - 1:
        raise argparse.ArgumentTypeError("count exceeds supported exact-integer range")
    return result


def positive_count(value):
    result = count(value)
    if result < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def money(value):
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("must be a positive finite decimal amount") from exc
    if not result.is_finite() or result <= 0:
        raise argparse.ArgumentTypeError("must be a positive finite decimal amount")
    if len(result.as_tuple().digits) > 28 or not -12 <= result.adjusted() <= 18:
        raise argparse.ArgumentTypeError("use at most 28 significant digits and magnitude 1e-12 to below 1e19")
    return result


def decimal_text(value):
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def z_critical(alpha):
    quantile = 1 - alpha / 2
    if quantile == 1:
        raise ValueError("alpha is too small for floating-point normal quantiles")
    return NORMAL.inv_cdf(quantile)


def plan_ab(args):
    if args.power <= 0.5:
        raise ValueError("power must be greater than 0.5 and below 1")
    delta = args.absolute_mde if args.absolute_mde is not None else args.baseline * args.relative_mde
    target = args.baseline + delta
    if not args.baseline < target < 1:
        raise ValueError("MDE must produce a representable target rate strictly above baseline and below 1")
    z_alpha = z_critical(args.alpha)
    z_power = NORMAL.inv_cdf(args.power)
    pooled = (args.baseline + target) / 2
    numerator = z_alpha * math.sqrt(2 * pooled * (1 - pooled))
    numerator += z_power * math.sqrt(args.baseline * (1 - args.baseline) + target * (1 - target))
    raw_n = (numerator / delta) ** 2
    if not math.isfinite(raw_n):
        raise ValueError("requested MDE requires an unsupported sample size")
    n = math.ceil(raw_n)
    warnings = [
        "Approximate planning calculation, not guaranteed achieved power or a stopping rule.",
        "Assumes equal 50/50 allocation, independent unique units, one binary outcome, two arms, a two-sided test, and a fixed horizon.",
        "Does not account for clusters, repeated looks, multiple comparisons, attrition, seasonality, revenue variance, or conversion lag.",
        "Use an established experimentation engine or statistician for sequential, clustered, or unequal-allocation designs.",
    ]
    if min(n * args.baseline, n * (1 - args.baseline), n * target, n * (1 - target)) < 10:
        warnings.append("Expected success/failure counts are small; normal sample-size approximation may be unreliable.")
    result = {
        "command": "plan-ab",
        "method": "two-sided two-proportion normal approximation, equal allocation, no continuity correction",
        "baseline_rate": args.baseline,
        "target_rate": target,
        "absolute_mde": delta,
        "mde_percentage_points": delta * 100,
        "relative_mde": delta / args.baseline,
        "alpha": args.alpha,
        "power": args.power,
        "users_per_arm": n,
        "users_total": 2 * n,
        "warnings": warnings,
    }
    if args.eligible_users_per_day is not None:
        result["eligible_users_per_day_total"] = args.eligible_users_per_day
        result["minimum_accrual_days"] = math.ceil(2 * n / args.eligible_users_per_day)
        warnings.append("Accrual days exclude conversion-maturation time, ramp-up, and complete business cycles; use eligible new independent units across both arms.")
    return result


def wilson(events, total, z):
    p = events / total
    denom = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return [max(0.0, center - half), min(1.0, center + half)]


def compare_ab(args):
    if args.control_conversions > args.control_users or args.variant_conversions > args.variant_users:
        raise ValueError("conversions cannot exceed the corresponding unique users")
    nc, nv = args.control_users, args.variant_users
    xc, xv = args.control_conversions, args.variant_conversions
    pc, pv = xc / nc, xv / nv
    z = z_critical(args.alpha)
    ci_c, ci_v = wilson(xc, nc, z), wilson(xv, nv, z)
    difference = pv - pc
    difference_ci = [
        max(-1.0, difference - math.hypot(pv - ci_v[0], ci_c[1] - pc)),
        min(1.0, difference + math.hypot(ci_v[1] - pv, pc - ci_c[0])),
    ]
    pooled = (xc + xv) / (nc + nv)
    min_observed_cell = min(xc, nc - xc, xv, nv - xv)
    min_expected_cell = min(nc * pooled, nc * (1 - pooled), nv * pooled, nv * (1 - pooled))
    valid_normal = min_observed_cell >= 10 and min_expected_cell >= 10
    p_value = None
    if valid_normal:
        se = math.sqrt(pooled * (1 - pooled) * (1 / nc + 1 / nv))
        p_value = math.erfc(abs(difference / se) / math.sqrt(2))
    warnings = [
        "Descriptive calculation only: randomization, identity stitching, exposure, maturation, missing data, and stopping rules have not been verified.",
        "Intervals and p-values assume independent units and a fixed horizon; no adjustment for peeking, multiple tests, clustering, or post-hoc segments.",
        "No ship decision follows automatically from these numbers; assess practical effect, data quality, and retention/revenue guardrails.",
        "Difference CI uses Newcombe-Wilson; the pooled z-test uses a different approximation and boundary decisions can differ.",
    ]
    if not valid_normal:
        warnings.append("Normal p-value omitted because an observed or pooled-expected success/failure cell has fewer than 10 observations; use an appropriate exact or specialist method.")
    if pc == 0:
        warnings.append("Relative lift is undefined because the control rate is zero; report absolute percentage-point difference.")
    total = nc + nv
    expected_v = total * args.expected_variant_share
    expected_c = total * (1 - args.expected_variant_share)
    srm_p = None
    if min(expected_v, expected_c) >= 5:
        chi_square = (nv - expected_v) ** 2 / expected_v + (nc - expected_c) ** 2 / expected_c
        srm_p = math.erfc(math.sqrt(chi_square / 2))
    else:
        warnings.append("Sample-ratio-mismatch approximation omitted because an expected allocation count is below 5.")
    srm_flag = None if srm_p is None else srm_p < args.srm_alpha
    if srm_flag:
        warnings.append("Sample-ratio mismatch flag: investigate eligibility, assignment, loss, and instrumentation before interpreting conversion differences.")
    return {
        "command": "compare-ab",
        "confidence_level": 1 - args.alpha,
        "control": {"users": nc, "conversions": xc, "rate": pc, "wilson_ci": ci_c},
        "variant": {"users": nv, "conversions": xv, "rate": pv, "wilson_ci": ci_v},
        "variant_minus_control": {
            "rate_difference": difference,
            "percentage_point_difference": difference * 100,
            "relative_lift": None if pc == 0 else difference / pc,
            "newcombe_wilson_ci": difference_ci,
            "newcombe_wilson_ci_percentage_points": [v * 100 for v in difference_ci],
            "pooled_two_sided_normal_p_value": p_value,
        },
        "sample_ratio_mismatch": {
            "method": "Pearson chi-square, 1 degree of freedom, asymptotic",
            "expected_variant_share": args.expected_variant_share,
            "observed_variant_share": nv / total,
            "p_value": srm_p,
            "investigation_threshold": args.srm_alpha,
            "investigate": srm_flag,
            "meaning": "A diagnostic flag, not proof of a bug; no flag does not establish valid randomization. Use all assigned eligible units, not converters or a post-treatment subset.",
        },
        "warnings": warnings,
    }


def pricing(args):
    if not re.fullmatch(r"[A-Za-z]{3}", args.currency):
        raise ValueError("currency must be a three-letter label such as USD; no currency conversion is performed")
    if not 0 <= args.display_decimals <= 6:
        raise ValueError("display-decimals must be between 0 and 6")
    with localcontext() as context:
        context.prec = 60
        monthly, annual = args.monthly_price, args.annual_price
        monthly_year = monthly * 12
        savings = monthly_year - annual
        percent_exact = Fraction(savings) * 100 / Fraction(monthly_year)
        percent_decimal = Decimal(percent_exact.numerator) / Decimal(percent_exact.denominator)
        equivalent_exact = Fraction(annual) / 12
        equivalent = annual / 12
        shown_equivalent = equivalent.quantize(Decimal(1).scaleb(-args.display_decimals))
        currency = args.currency.upper()
        relation = "discount" if savings > 0 else "surcharge" if savings < 0 else "same_total"
        approx = "approximately " if shown_equivalent != equivalent else ""
        return {
            "command": "pricing",
            "currency_label": currency,
            "monthly_price": decimal_text(monthly),
            "annual_price": decimal_text(annual),
            "twelve_monthly_payments": decimal_text(monthly_year),
            "comparison": relation,
            "annual_amount_saved_vs_monthly": decimal_text(savings),
            "percent_saved_vs_monthly": decimal_text(percent_decimal),
            "percent_saved_exact_fraction": fraction_text(percent_exact),
            "annual_plan_monthly_equivalent": decimal_text(equivalent),
            "monthly_equivalent_exact_fraction": fraction_text(equivalent_exact),
            "billing_label": f"{currency} {decimal_text(annual)} per year, billed annually ({approx}{currency} {format(shown_equivalent, 'f')} per month equivalent)",
            "notes": [
                "Positive savings are a discount; negative savings are a surcharge. Both plans must include the same scope for a fair comparison.",
                "Exact fractions preserve recurring values; decimal results use up to 60-digit precision. Display rounding does not change the billed annual price.",
                "Calculation covers only the supplied amounts; verify taxes, fees, seat minimums, usage, term, renewal price, and currency display rules before publishing.",
                "A monthly equivalent does not mean monthly billing. This arithmetic predicts no conversion improvement.",
            ],
        }


def rgb(value):
    match = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value)
    if not match:
        raise argparse.ArgumentTypeError("use an opaque 3- or 6-digit sRGB hex color, e.g. '#fff' or '#112233'")
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    return "#" + digits.upper()


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(weight * channel for weight, channel in zip((0.2126, 0.7152, 0.0722), linear))


def contrast(args):
    fg, bg = luminance(args.foreground), luminance(args.background)
    ratio = (max(fg, bg) + 0.05) / (min(fg, bg) + 0.05)
    return {
        "command": "contrast",
        "foreground": args.foreground,
        "background": args.background,
        "contrast_ratio": ratio,
        "wcag_2_aa_normal_text_4_5": ratio >= 4.5,
        "wcag_2_aa_large_text_3": ratio >= 3,
        "wcag_2_nontext_3_where_required": ratio >= 3,
        "notes": [
            "Opaque, uniform sRGB colors only; composite transparency and inspect images, gradients, hover, focus, disabled, and error states separately.",
            "Large text means at least 18 point regular or 14 point bold (approximately 24 or 18.67 CSS pixels); use the actual rendered font.",
            "Use the unrounded ratio for threshold decisions. Non-text requirements apply to relevant UI boundaries and meaningful graphics, with exceptions.",
            "Passing this color pair is not a complete accessibility or WCAG conformance audit and predicts no conversion lift.",
        ],
    }


def parser():
    top = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 cro_math.py plan-ab --baseline 0.05 --relative-mde 0.20 --eligible-users-per-day 1000
  python3 cro_math.py compare-ab --control-users 10000 --control-conversions 500 --variant-users 10000 --variant-conversions 600
  python3 cro_math.py pricing --monthly-price 24 --annual-price 228 --currency USD
  python3 cro_math.py contrast '#ffffff' '#2563eb'

Successful calculations emit JSON. Invalid input exits 2 with an error on stderr.
No network requests, telemetry, file writes, or automatic experiment decisions.
""")
    subs = top.add_subparsers(dest="command", required=True)
    plan = subs.add_parser("plan-ab", help="Approximate sample size for two equally sized arms")
    plan.add_argument("--baseline", type=probability, required=True, help="Control conversion fraction, e.g. 0.05")
    mde = plan.add_mutually_exclusive_group(required=True)
    mde.add_argument("--relative-mde", type=positive_number, help="Relative improvement, e.g. 0.20 for 20%%")
    mde.add_argument("--absolute-mde", type=positive_number, help="Absolute fraction, e.g. 0.01 for one percentage point")
    plan.add_argument("--alpha", type=probability, default=0.05)
    plan.add_argument("--power", type=probability, default=0.8)
    plan.add_argument("--eligible-users-per-day", type=positive_number, help="New eligible independent units/day, both arms combined")
    plan.set_defaults(run=plan_ab)
    comparison = subs.add_parser("compare-ab", help="Describe independent binary outcomes; never declares a winner")
    comparison.add_argument("--control-users", type=positive_count, required=True)
    comparison.add_argument("--control-conversions", type=count, required=True)
    comparison.add_argument("--variant-users", type=positive_count, required=True)
    comparison.add_argument("--variant-conversions", type=count, required=True)
    comparison.add_argument("--alpha", type=probability, default=0.05)
    comparison.add_argument("--expected-variant-share", type=probability, default=0.5)
    comparison.add_argument("--srm-alpha", type=probability, default=0.001, help="Diagnostic investigation threshold; default 0.001")
    comparison.set_defaults(run=compare_ab)
    price = subs.add_parser("pricing", help="Check annual billing arithmetic using exact decimal inputs")
    price.add_argument("--monthly-price", type=money, required=True)
    price.add_argument("--annual-price", type=money, required=True)
    price.add_argument("--currency", default="USD", help="Three-letter display label; no FX conversion")
    price.add_argument("--display-decimals", type=int, default=2, help="Monthly-equivalent display precision (0-6); adapt to currency")
    price.set_defaults(run=pricing)
    color = subs.add_parser("contrast", help="WCAG 2 contrast for two opaque sRGB hex colors")
    color.add_argument("foreground", type=rgb)
    color.add_argument("background", type=rgb)
    color.set_defaults(run=contrast)
    return top


def main():
    cli = parser()
    args = cli.parse_args()
    try:
        output = args.run(args)
        print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, OverflowError, ZeroDivisionError, InvalidOperation) as exc:
        cli.error(str(exc) or "numeric calculation is outside the supported range")


if __name__ == "__main__":
    main()
