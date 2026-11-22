"""Evaluate a randomized marketplace A/B experiment; descriptive and inferential results."""
import json
from pathlib import Path
import math
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'experiment_users.csv'
OUT = ROOT / 'outputs'
ALPHA = 0.05


def validate(df):
    required = ['user_id','variant','country','device','prior_buyer','clicked_listing','purchased_7d','order_value_eur','refunded_7d']
    missing = set(required) - set(df.columns)
    if missing: raise ValueError(f'Missing columns: {sorted(missing)}')
    if df.user_id.duplicated().any(): raise ValueError('Duplicated randomized user IDs')
    if set(df.variant.unique()) != {'control','treatment'}: raise ValueError('Expected control and treatment')
    for col in ['clicked_listing','purchased_7d','refunded_7d']:
        if not df[col].isin([0,1]).all(): raise ValueError(f'Invalid binary value: {col}')
    if (df.order_value_eur < 0).any(): raise ValueError('Negative order value')
    if ((df.purchased_7d == 0) & (df.order_value_eur > 0)).any(): raise ValueError('Revenue without purchase')
    if ((df.refunded_7d == 1) & (df.purchased_7d == 0)).any(): raise ValueError('Refund without purchase')


def difference_in_proportions(x_c,n_c,x_t,n_t):
    """Two-sided pooled z-test plus unpooled 95% CI for treatment minus control."""
    p_c, p_t = x_c/n_c, x_t/n_t
    delta = p_t - p_c
    pooled = (x_c+x_t)/(n_c+n_t)
    se_null = math.sqrt(pooled*(1-pooled)*(1/n_c+1/n_t))
    z = delta/se_null if se_null else 0.
    p_value = float(2*norm.sf(abs(z))) if se_null else 1.
    se_ci = math.sqrt(p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t)
    bound = norm.ppf(.975)*se_ci
    return {'control_rate':p_c,'treatment_rate':p_t,'absolute_lift_pp':100*delta,
            'relative_lift_pct':100*delta/p_c if p_c else None,
            'ci_lower_pp':100*(delta-bound),'ci_upper_pp':100*(delta+bound),
            'z_statistic':z,'p_value':p_value}


def analyze(df):
    validate(df)
    counts=df.groupby('variant')['purchased_7d'].agg(['sum','count'])
    c=counts.loc['control']; t=counts.loc['treatment']
    primary=difference_in_proportions(int(c['sum']),int(c['count']),int(t['sum']),int(t['count']))
    summary=df.groupby('variant',sort=True).agg(
        users=('user_id','count'), purchasers=('purchased_7d','sum'),
        listing_clicks=('clicked_listing','sum'), gross_order_value_eur=('order_value_eur','sum'),
        refunds=('refunded_7d','sum'))
    summary['purchase_conversion']=summary.purchasers/summary.users
    summary['click_through']=summary.listing_clicks/summary.users
    summary['gross_value_per_user_eur']=summary.gross_order_value_eur/summary.users
    summary['refunds_per_purchaser']=summary.refunds/summary.purchasers
    # Balance diagnostics for pre-treatment covariates; not post-treatment filters.
    balance=pd.crosstab(df['variant'],df['prior_buyer'],normalize='index')
    segments=df.groupby(['country','variant']).agg(users=('user_id','count'),purchasers=('purchased_7d','sum')).reset_index()
    segments['conversion']=segments.purchasers/segments.users
    result={
        'experiment': 'Synthetic item-recommendation entry point',
        'hypothesis': 'New entry point increases 7-day purchase conversion per randomized user',
        'primary_metric': 'purchased_7d', 'analysis_unit':'randomized user',
        'alpha':ALPHA,'n_total':len(df),'primary':primary,
        'balance_prior_buyer_share':{k:float(v) for k,v in balance[1].to_dict().items()},
        'decision': ('Evidence of a positive conversion lift in this simulated sample' if
             primary['p_value']<ALPHA and primary['ci_lower_pp']>0 else
             'Insufficient evidence of a positive conversion lift in this simulated sample'),
        'cautions':['Synthetic observations; no real Vinted users or transactions',
                    'Results are illustrative, not externally validated',
                    'Country comparisons are exploratory and not corrected for multiple testing',
                    'Order value and refunds are descriptive secondary/guardrail metrics']
    }
    return result,summary,segments


def save(result,summary,segments):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'experiment_results.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    summary.to_csv(OUT/'variant_summary.csv',float_format='%.6f')
    segments.to_csv(OUT/'country_exploration.csv',index=False,float_format='%.6f')
    values=summary.reindex(['control','treatment'])['purchase_conversion']*100
    fig,ax=plt.subplots(figsize=(7,4.5))
    bars=ax.bar(values.index, values.values, color=['#94a3b8','#2563eb'],width=.55)
    ax.set_ylabel('7-day purchase conversion (%)');ax.set_title('Purchase conversion by assigned variant (synthetic data)')
    ax.set_ylim(0,max(values)*1.32)
    for b,val in zip(bars,values.values): ax.text(b.get_x()+b.get_width()/2,b.get_height()+.1,f'{val:.2f}%',ha='center')
    fig.tight_layout();fig.savefig(OUT/'conversion_by_variant.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4.5))
    data=segments.pivot(index='country',columns='variant',values='conversion').reindex(columns=['control','treatment'])*100
    ind=np.arange(len(data));width=.35
    ax.bar(ind-width/2,data['control'],width,label='Control',color='#94a3b8')
    ax.bar(ind+width/2,data['treatment'],width,label='Treatment',color='#2563eb')
    ax.set_xticks(ind,data.index); ax.set_ylabel('7-day purchase conversion (%)')
    ax.set_title('Exploratory country comparison (synthetic data)');ax.legend()
    fig.tight_layout();fig.savefig(OUT/'conversion_by_country.png',dpi=160);plt.close(fig)


def main():
    df=pd.read_csv(DATA)
    result,summary,segments=analyze(df)
    save(result,summary,segments)
    print(summary[['users','purchasers','purchase_conversion','gross_value_per_user_eur']].to_string())
    print(json.dumps({'primary':result['primary'],'decision':result['decision']},indent=2))

if __name__=='__main__':main()
