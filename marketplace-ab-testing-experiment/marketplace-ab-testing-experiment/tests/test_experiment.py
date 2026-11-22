import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from generate_data import generate
from analyze_experiment import validate, analyze, difference_in_proportions


def test_seed_reproducible():
    assert generate(200,seed=5).equals(generate(200,seed=5))


def test_exact_assignment_balance():
    df=generate(200,seed=10)
    assert (df.variant=='control').sum()==100
    assert (df.variant=='treatment').sum()==100


def test_valid_data_and_analysis():
    df=generate(1000,seed=12)
    validate(df)
    result,summary,segments=analyze(df)
    assert result['n_total']==1000
    assert summary['users'].sum()==1000
    assert len(segments)==8


def test_zero_effect_has_one_p_value():
    x=difference_in_proportions(10,100,10,100)
    assert x['absolute_lift_pp']==0
    assert x['p_value']==1
