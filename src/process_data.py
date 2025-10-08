import pandas as pd
import numpy as np
from pathlib import Path

# Define the base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the data
email_df = pd.read_csv(BASE_DIR / 'data' / 'email_campaigns.csv')
ppc_df = pd.read_csv(BASE_DIR / 'data' / 'ppc_spend.csv')
social_media_df = pd.read_csv(BASE_DIR / 'data' / 'social_media_ads.csv')
website_df = pd.read_csv(BASE_DIR / 'data' / 'website_conversions.csv')

# Rename duplicate columns in source dataframes
email_df.rename(columns={'clicks': 'clicks_email'}, inplace=True)
ppc_df.rename(columns={'spend': 'spend_ppc'}, inplace=True)
social_media_df.rename(
    columns={
        'clicks': 'clicks_social', 
        'spend': 'spend_social', 
        'impressions': 'impressions_social'
    },
    inplace=True
)

# Merge email data
full_df = pd.merge(website_df, email_df, how='left', on='date')
mask_email = full_df['channel'] != 'Email'
full_df.loc[mask_email, ['clicks_email', 'emails_sent']] = np.nan

# Merging PPC data
full_df = pd.merge(full_df, ppc_df, how='left', on='date')
mask_ppc = full_df['channel'] != 'PPC'
full_df.loc[mask_ppc, 'spend_ppc'] = np.nan

# Merging social media data
full_df = pd.merge(full_df, social_media_df, how='left', on='date')
mask_sm = full_df['channel'] != 'Social Media'
full_df.loc[mask_sm, ['spend_social', 'clicks_social', 'impressions_social']] = np.nan

# Combining 'clicks' columns
full_df['clicks'] = full_df['clicks_social'].combine_first(full_df['clicks_email'])
full_df.drop(columns=['clicks_email', 'clicks_social'], inplace=True)

# Combining 'spend' columns
full_df['spend'] = full_df['spend_ppc'].combine_first(full_df['spend_social'])
full_df.drop(columns=['spend_ppc', 'spend_social'], inplace=True)

# Convert 'date' to datetime
full_df['date'] = pd.to_datetime(full_df['date'])

# Save the output
full_df.to_csv(BASE_DIR / 'data' / 'aggregated_data.csv', index=False)