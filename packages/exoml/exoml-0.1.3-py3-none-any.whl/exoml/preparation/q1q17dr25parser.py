import multiprocessing
from multiprocessing import Pool
import pandas as pd
import numpy as np

from preparation.parser_utils import CreateTargetInput, create_target_csv, create_triceratops_prob

def create_targets_df(tces_dir):
    # Merge TCEs DF and cumulative DF ignoring everything not from Kepler or K2
    # Mark TCEs as planet only if they have photometric and rv measurements
    # test_df = pd.read_csv(tces_dir + '/classified_tces.csv', comment='#')
    # test_df = test_df.sort_values(by=["object_id", "period"], ascending=True)
    # test_df = test_df[test_df['type'].isin(['fp', 'planet', 'planet_transit', 'tce'])]
    # test_df.to_csv(tces_dir + '/injected_objects_tces.csv')
    cfps_df = pd.read_csv(tces_dir + '/fpwg_2023.04.25_10.26.55.csv', comment='#')
    kois_df = pd.read_csv(tces_dir + '/cumulative_2023.06.30_13.09.52.csv', comment='#')
                          #usecols=['rowid','kepid','kepoi_name','kepler_name','koi_disposition','koi_vet_stat','koi_vet_date','koi_pdisposition','koi_score','koi_fpflag_nt','koi_fpflag_ss','koi_fpflag_co','koi_fpflag_ec','koi_disp_prov','koi_comment','koi_period','koi_time0bk','koi_time0','koi_eccen','koi_longp','koi_impact','koi_duration','koi_ingress','koi_depth','koi_ror','koi_srho','koi_fittype','koi_prad','koi_sma','koi_incl','koi_teq','koi_insol','koi_dor','koi_limbdark_mod','koi_ldm_coeff4','koi_ldm_coeff3','koi_ldm_coeff2','koi_ldm_coeff1','koi_parm_prov','koi_max_sngle_ev','koi_max_mult_ev','koi_model_snr','koi_count','koi_num_transits','koi_tce_plnt_num','koi_tce_delivname','koi_quarters','koi_bin_oedp_sig','koi_trans_mod','koi_model_dof','koi_model_chisq','koi_datalink_dvr','koi_datalink_dvs','koi_steff','koi_slogg','koi_smet','koi_srad','koi_smass','koi_sage','koi_sparprov','ra','dec','koi_kepmag','koi_gmag','koi_rmag','koi_imag','koi_zmag','koi_jmag','koi_hmag','koi_kmag','koi_fwm_stat_sig','koi_fwm_sra','koi_fwm_sdec','koi_fwm_srao','koi_fwm_sdeco','koi_fwm_prao','koi_fwm_pdeco','koi_dicco_mra','koi_dicco_mdec','koi_dicco_msky','koi_dikco_mra','koi_dikco_mdec','koi_dikco_msky'])
    tces_df = pd.read_csv(tces_dir + '/q1_q17_dr25_tce_2023.07.03_23.17.12.csv', comment='#')
    disc_df = pd.read_csv(tces_dir + '/PSCompPars_2023.06.30_07.30.12.csv', comment='#')
                          #usecols=['pl_name','hostname','tic_id','sy_snum','sy_pnum','discoverymethod','disc_year','disc_facility','rv_flag','tran_flag','pl_controv_flag','pl_orbper','pl_orbsmax','pl_rade','pl_radj','pl_bmasse','pl_bmassj','pl_bmassprov','pl_orbeccen','pl_insol','pl_eqt','ttv_flag','st_spectype','st_teff','st_rad','st_mass','st_met','st_metratio','st_logg','rastr','ra','decstr','dec','sy_dist','sy_vmag','sy_jmag','sy_hmag','sy_kmag','sy_gaiamag','sy_tmag','sy_kepmag','st_nphot','st_nrvc', 'disc_refname'])
    tces_df = tces_df[tces_df['tce_rogue_flag'] == 0]
    tces_df['cent_so'] = (tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2) ** 0.5
    tces_df['cent_so_err'] = (((tces_df['tce_fwm_srao'] / np.sqrt(tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2)) * tces_df['tce_fwm_srao_err']) ** 2 + \
                              ((tces_df['tce_fwm_sdeco'] / np.sqrt(tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2)) * tces_df['tce_fwm_sdeco_err']) ** 2) ** 0.5
    tces_df['cent_so_sigma'] = tces_df['cent_so'] / tces_df['cent_so_err']
    tces_df['source_offset_sigma'] = tces_df['tce_dicco_msky'] / tces_df['tce_dicco_msky_err']
    tces_df['kic_offset_sigma'] = tces_df['tce_dikco_msky'] / tces_df['tce_dikco_msky_err']
    # tces_df[~(((tces_df['tce_hap_stat'] / tces_df['tce_cap_stat'] > 1) |
    #            (tces_df['tce_hap_stat'] > 0) & (tces_df['tce_cap_stat'] < 0)) |
    #           (tces_df['tce_maxmes'] > 7.1) |
    #           (tces_df['cent_so_sigma'] > 3) |
    #           (tces_df['source_offset_sigma'] > 3) |
    #           (tces_df['kic_offset_sigma'] > 3)) & (tces_df['tce_model_snr'] > 3.5)]
    kois_df = pd.merge(kois_df, cfps_df, on=['kepoi_name'], how="outer", indicator=True)
    kois_df = kois_df[(kois_df['_merge'] == 'left_only') | (kois_df['_merge'] == 'both')]
    kois_df['kepid'] = kois_df['kepid_x']
    kois_df['pl_name'] = kois_df['kepler_name']
    kois_df['tce_period'] = kois_df['koi_period']
    kois_df['tce_period_round'] = kois_df['tce_period'].round(1)
    tces_df['tce_period_round'] = tces_df['tce_period'].round(1)
    tces_df = pd.merge(tces_df, kois_df, on=['kepid', 'tce_period_round'], how='outer')
    disc_df = disc_df[disc_df['disc_facility'] == 'Kepler']
    disc_df = disc_df[disc_df['discoverymethod'] == 'Transit']
    disc_df = pd.merge(tces_df, disc_df, on='pl_name', how='outer')
    disc_df['type'] = 'tce'
    disc_df.loc[disc_df['koi_disposition'] == 'FALSE POSITIVE', 'type'] = 'candidate'
    disc_df.loc[disc_df['koi_disposition'] == 'FALSE POSITIVE', 'type'] = 'candidate'
    disc_df.loc[(disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet_transit'
    disc_df.loc[(disc_df['rv_flag'] > 0) & (disc_df['tran_flag'] > 0) & (disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet'
    disc_df.loc[(disc_df['rv_flag'] == 0) & (disc_df['tran_flag'] > 0) & (disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet_transit'
    disc_df.loc[disc_df['koi_disposition'] == 'FALSE POSITIVE', 'type'] = 'candidate'
    disc_df.loc[disc_df['koi_disposition'] == 'CANDIDATE', 'type'] = 'candidate'
    disc_df.loc[disc_df['fpwg_disp_status'] == 'CERTIFIED FP', 'type'] = 'fp'
    disc_df.loc[disc_df['fpwg_disp_status'] == 'CERTIFIED FA', 'type'] = 'fa'
    disc_df['object_id'] = 'KIC ' + disc_df['kepid'].astype('Int64').astype('str')
    disc_df['period'] = disc_df['tce_period_x']
    disc_df.loc[disc_df['period'].isna(), 'period'] = disc_df[disc_df['period'].isna()]['tce_period_y']
    disc_df.loc[disc_df['period'].isna(), 'period'] = disc_df[disc_df['period'].isna()]['pl_orbper']
    disc_df['epoch'] = disc_df['tce_time0bk']
    disc_df.loc[disc_df['epoch'].isna(), 'epoch'] = disc_df[disc_df['epoch'].isna()]['koi_time0bk']
    disc_df.loc[disc_df['epoch'].isna(), 'epoch'] = disc_df[disc_df['epoch'].isna()]['pl_tranmid'] - 2454833.0
    disc_df['duration(h)'] = disc_df['pl_trandur']
    disc_df.loc[disc_df['duration(h)'].isna(), 'duration(h)'] = disc_df[disc_df['duration(h)'].isna()]['koi_duration']
    disc_df.loc[disc_df['duration(h)'].isna(), 'duration(h)'] = disc_df[disc_df['duration(h)'].isna()]['tce_duration']
    disc_df['depth_primary'] = disc_df['pl_trandep']
    disc_df.loc[disc_df['depth_primary'].isna(), 'depth_primary'] = disc_df[disc_df['depth_primary'].isna()]['koi_depth']
    disc_df.loc[disc_df['depth_primary'].isna(), 'depth_primary'] = disc_df[disc_df['depth_primary'].isna()]['tce_depth']
    disc_df['radius(earth)'] = disc_df['pl_rade']
    disc_df.loc[disc_df['radius(earth)'].isna(), 'radius(earth)'] = disc_df[disc_df['radius(earth)'].isna()]['koi_prad']
    disc_df.loc[disc_df['radius(earth)'].isna(), 'radius(earth)'] = disc_df[disc_df['radius(earth)'].isna()]['tce_prad']
    disc_df = disc_df.sort_values(by=["object_id", "period"], ascending=True)
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
                (disc_df['tce_maxmes'] > 7.1), 'type'] = 'tce_secondary'
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
            (disc_df['cent_so_sigma'] > 3), 'type'] = 'tce_centroids_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
            ((disc_df['source_offset_sigma'] > 3) |
             (disc_df['kic_offset_sigma'] > 3)), 'type'] = 'tce_source_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
            (disc_df['tce_bin_oedp_stat'] > 9), 'type'] = 'tce_odd_even'
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
                (disc_df['tce_hap_stat'] > disc_df['tce_cap_stat']), 'type'] = 'tce_og'
    disc_df.loc[(disc_df['kepoi_name'].isna()) &
                      (disc_df['type'] == 'tce') &
                      (disc_df['tce_model_snr'] > 3.5), 'type'] = 'tce_candidate'
    #t[t['boot_fap'] > t['boot_mesmean']]
    last_target = ''
    last_period = 0.5
    last_index = -1
    left_match_index = []
    right_match_index = []
    unpaired_index = disc_df.index.values
    for index, target_row in disc_df.iterrows():
        period_diff = 0.2 / (last_period ** (1/2))
        period_diff = 0.05 if period_diff > 0.05 else period_diff
        current_period = target_row['period']
        if last_target == target_row['object_id'] and np.abs(current_period - last_period) < period_diff * last_period:
            right_match_index = right_match_index + [index]
            if last_index not in left_match_index:
                left_match_index = left_match_index + [last_index]
            if last_index in unpaired_index:
                unpaired_index = unpaired_index[unpaired_index != last_index]
            if index in unpaired_index:
                unpaired_index = unpaired_index[unpaired_index != index]
        else:
            last_period = current_period
            last_index = index
        last_target = target_row['object_id']
    #disc_df = disc_df.loc[left_match_index].combine_first(disc_df.loc[right_match_index])
    result_df = disc_df.loc[unpaired_index]
    for i, index in enumerate(left_match_index):
        result = disc_df.loc[index].combine_first(disc_df.loc[right_match_index[i]])
        result_df = pd.concat([result_df, result.to_frame().T], ignore_index=True)
    result_df.drop(result_df[result_df['duration(h)'].isnull()].index, inplace=True)
    result_df.drop(result_df[result_df['object_id'] == 'KIC <NA>'].index, inplace=True)
    # Remove latest KIC from the catalogue
    result_df.drop(result_df[result_df['object_id'] == 'KIC 100001645'].index, inplace=True)
    result_df.to_csv(tces_dir + '/classified_tces.csv')
    results_df_no_validated = result_df.copy()
    results_df_no_validated.loc[results_df_no_validated['disc_refname'].str.contains('Valizadegan', na=False), ['type']] = 'candidate'
    results_df_no_validated.loc[results_df_no_validated['disc_refname'].str.contains('Armstrong et al. 2021', na=False), ['type']] = 'candidate'
    results_df_no_validated.to_csv(tces_dir + '/classified_tces_no_val.csv')
    #disc_df[disc_df['object_id'] == 'KIC 7377200'].iloc[0]['epoch']
    tce_candidate_df = result_df[result_df['type'].isin(['tce_candidate'])]
    tce_candidate_df.to_csv(tces_dir + '/injected_objects_tce_candidates.csv')
    candidate_df = result_df[result_df['type'].isin(['candidate', 'tce_candidate'])]
    candidate_df.to_csv(tces_dir + '/injected_objects_candidates.csv')
    candidate_df_no_val = results_df_no_validated[results_df_no_validated['type'].isin(['candidate', 'tce_candidate'])]
    candidate_df_no_val.to_csv(tces_dir + '/injected_objects_candidates_no_val.csv')
    result_df = result_df[result_df['type'].isin(['fp', 'fa', 'planet', 'planet_transit', 'tce', 'tce_og',
                                                  'tce_secondary', 'tce_source_offset', 'tce_centroids_offset',
                                                  'tce_odd_even'])]
    result_df = result_df[~result_df['radius(earth)'].isna()]
    result_df.to_csv(tces_dir + '/injected_objects_tces.csv')
    results_df_no_validated = results_df_no_validated[results_df_no_validated['type'].isin(['fp', 'fa', 'planet', 'planet_transit', 'tce', 'tce_og',
                                                  'tce_secondary', 'tce_source_offset', 'tce_centroids_offset',
                                                  'tce_odd_even'])]
    results_df_no_validated = results_df_no_validated[~results_df_no_validated['radius(earth)'].isna()]
    results_df_no_validated.to_csv(tces_dir + '/injected_objects_tces_no_val.csv')


def create_targets_multi_df(tces_dir):
    # Merge TCEs DF and cumulative DF ignoring everything not from Kepler or K2
    # Mark TCEs as planet only if they have photometric and rv measurements
    # test_df = pd.read_csv(tces_dir + '/classified_tces.csv', comment='#')
    # test_df = test_df.sort_values(by=["object_id", "period"], ascending=True)
    # test_df = test_df[test_df['type'].isin(['fp', 'planet', 'planet_transit', 'tce'])]
    # test_df.to_csv(tces_dir + '/injected_objects_tces.csv')
    cfps_df = pd.read_csv(tces_dir + '/fpwg_2023.04.25_10.26.55.csv', comment='#')
    kois_df = pd.read_csv(tces_dir + '/cumulative_2023.06.30_13.09.52.csv', comment='#')
    tces_df = pd.read_csv(tces_dir + '/q1_q17_dr25_tce_2023.07.03_23.17.12.csv', comment='#')
    disc_df = pd.read_csv(tces_dir + '/PSCompPars_2023.06.30_07.30.12.csv', comment='#')
    tces_df = tces_df[tces_df['tce_rogue_flag'] == 0]
    tces_df['cent_so'] = (tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2) ** 0.5
    tces_df['cent_so_err'] = (((tces_df['tce_fwm_srao'] / np.sqrt(tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2)) * tces_df['tce_fwm_srao_err']) ** 2 + \
                              ((tces_df['tce_fwm_sdeco'] / np.sqrt(tces_df['tce_fwm_srao'] ** 2 + tces_df['tce_fwm_sdeco'] ** 2)) * tces_df['tce_fwm_sdeco_err']) ** 2) ** 0.5
    tces_df['cent_so_sigma'] = tces_df['cent_so'] / tces_df['cent_so_err']
    tces_df['source_offset_sigma'] = tces_df['tce_dicco_msky'] / tces_df['tce_dicco_msky_err']
    tces_df['kic_offset_sigma'] = tces_df['tce_dikco_msky'] / tces_df['tce_dikco_msky_err']
    # tces_df[~(((tces_df['tce_hap_stat'] / tces_df['tce_cap_stat'] > 1) |
    #            (tces_df['tce_hap_stat'] > 0) & (tces_df['tce_cap_stat'] < 0)) |
    #           (tces_df['tce_maxmes'] > 7.1) |
    #           (tces_df['cent_so_sigma'] > 3) |
    #           (tces_df['source_offset_sigma'] > 3) |
    #           (tces_df['kic_offset_sigma'] > 3)) & (tces_df['tce_model_snr'] > 3.5)]
    kois_df = pd.merge(kois_df, cfps_df, on=['kepoi_name'], how="outer", indicator=True)
    kois_df = kois_df[(kois_df['_merge'] == 'left_only') | (kois_df['_merge'] == 'both')]
    kois_df['kepid'] = kois_df['kepid_x']
    kois_df['pl_name'] = kois_df['kepler_name']
    kois_df['tce_period'] = kois_df['koi_period']
    kois_df['tce_period_round'] = kois_df['tce_period'].round(1)
    tces_df['tce_period_round'] = tces_df['tce_period'].round(1)
    tces_df = pd.merge(tces_df, kois_df, on=['kepid', 'tce_period_round'], how='outer')
    disc_df = disc_df[disc_df['disc_facility'] == 'Kepler']
    disc_df = disc_df[disc_df['discoverymethod'] == 'Transit']
    disc_df = pd.merge(tces_df, disc_df, on='pl_name', how='outer')
    disc_df['type'] = 'tce'
    disc_df['multitype'] = ''
    disc_df.loc[(disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet_transit'
    disc_df.loc[(disc_df['rv_flag'] > 0) & (disc_df['tran_flag'] > 0) & (disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet'
    disc_df.loc[(disc_df['rv_flag'] == 0) & (disc_df['tran_flag'] > 0) & (disc_df['koi_disposition'] == 'CONFIRMED'), 'type'] = 'planet_transit'
    disc_df.loc[disc_df['koi_disposition'] == 'FALSE POSITIVE', 'type'] = 'candidate'
    disc_df.loc[disc_df['koi_disposition'] == 'CANDIDATE', 'type'] = 'candidate'
    disc_df.loc[disc_df['fpwg_disp_status'] == 'CERTIFIED FP', 'type'] = 'fp'
    disc_df.loc[disc_df['fpwg_disp_status'] == 'CERTIFIED FA', 'type'] = 'fa'
    disc_df['object_id'] = 'KIC ' + disc_df['kepid'].astype('Int64').astype('str')
    disc_df['period'] = disc_df['tce_period_x']
    disc_df.loc[disc_df['period'].isna(), 'period'] = disc_df[disc_df['period'].isna()]['tce_period_y']
    disc_df.loc[disc_df['period'].isna(), 'period'] = disc_df[disc_df['period'].isna()]['pl_orbper']
    disc_df['epoch'] = disc_df['tce_time0bk']
    disc_df.loc[disc_df['epoch'].isna(), 'epoch'] = disc_df[disc_df['epoch'].isna()]['koi_time0bk']
    disc_df.loc[disc_df['epoch'].isna(), 'epoch'] = disc_df[disc_df['epoch'].isna()]['pl_tranmid'] - 2454833.0
    disc_df['duration(h)'] = disc_df['pl_trandur']
    disc_df.loc[disc_df['duration(h)'].isna(), 'duration(h)'] = disc_df[disc_df['duration(h)'].isna()]['koi_duration']
    disc_df.loc[disc_df['duration(h)'].isna(), 'duration(h)'] = disc_df[disc_df['duration(h)'].isna()]['tce_duration']
    disc_df['depth_primary'] = disc_df['pl_trandep']
    disc_df.loc[disc_df['depth_primary'].isna(), 'depth_primary'] = disc_df[disc_df['depth_primary'].isna()]['koi_depth']
    disc_df.loc[disc_df['depth_primary'].isna(), 'depth_primary'] = disc_df[disc_df['depth_primary'].isna()]['tce_depth']
    disc_df['radius(earth)'] = disc_df['pl_rade']
    disc_df.loc[disc_df['radius(earth)'].isna(), 'radius(earth)'] = disc_df[disc_df['radius(earth)'].isna()]['koi_prad']
    disc_df.loc[disc_df['radius(earth)'].isna(), 'radius(earth)'] = disc_df[disc_df['radius(earth)'].isna()]['tce_prad']
    disc_df = disc_df.sort_values(by=["object_id", "period"], ascending=True)
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_maxmes'] > 7.1), 'type'] = 'tce_secondary'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_maxmes'] > 7.1), 'multitype'] = \
        disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_maxmes'] > 7.1), 'multitype'] + ',tce_secondary'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['cent_so_sigma'] > 3), 'type'] = 'tce_centroids_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['cent_so_sigma'] > 3), 'multitype'] = \
        disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['cent_so_sigma'] > 3), 'multitype'] + ',tce_centroids_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & ((disc_df['source_offset_sigma'] > 3) | (disc_df['kic_offset_sigma'] > 3)), 'type'] = 'tce_source_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & ((disc_df['source_offset_sigma'] > 3) | (disc_df['kic_offset_sigma'] > 3)), 'multitype'] = \
        disc_df.loc[(disc_df['kepoi_name'].isna()) & ((disc_df['source_offset_sigma'] > 3) | (disc_df['kic_offset_sigma'] > 3)), 'multitype'] + \
        ',tce_source_offset'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_bin_oedp_stat'] > 9), 'type'] = 'tce_odd_even'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_bin_oedp_stat'] > 9), 'multitype'] = \
        disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_bin_oedp_stat'] > 9), 'multitype'] + ',tce_odd_even'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_hap_stat'] > disc_df['tce_cap_stat']), 'type'] = 'tce_og'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_hap_stat'] > disc_df['tce_cap_stat']), 'multitype'] = \
        disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['tce_hap_stat'] > disc_df['tce_cap_stat']), 'multitype'] + ',tce_og'
    disc_df.loc[(disc_df['kepoi_name'].isna()) & (disc_df['type'] == 'tce') & (disc_df['tce_model_snr'] > 3.5), 'type'] = 'tce_candidate'
    disc_df.loc[disc_df['disc_refname'].str.contains('Valizadegan', na=False), ['multitype']] = \
        disc_df.loc[disc_df['disc_refname'].str.contains('Valizadegan', na=False), ['multitype']] + ',planet_validated'
    disc_df.loc[disc_df['disc_refname'].str.contains('Armstrong et al. 2021', na=False), ['multitype']] = \
        disc_df.loc[disc_df['disc_refname'].str.contains('Armstrong et al. 2021', na=False), ['multitype']] + ',planet_validated'
    disc_df.loc[((disc_df['multitype'] == '') | (disc_df['multitype'].isna()) | (disc_df['multitype'] == 'nan')), 'multitype'] = disc_df.loc[((disc_df['multitype'] == '') | (disc_df['multitype'].isna()) | (disc_df['multitype'] == 'nan')), 'type']
    last_target = ''
    last_period = 0.5
    last_index = -1
    left_match_index = []
    right_match_index = []
    unpaired_index = disc_df.index.values
    for index, target_row in disc_df.iterrows():
        period_diff = 0.2 / (last_period ** (1/2))
        period_diff = 0.05 if period_diff > 0.05 else period_diff
        current_period = target_row['period']
        if last_target == target_row['object_id'] and np.abs(current_period - last_period) < period_diff * last_period:
            right_match_index = right_match_index + [index]
            if last_index not in left_match_index:
                left_match_index = left_match_index + [last_index]
            if last_index in unpaired_index:
                unpaired_index = unpaired_index[unpaired_index != last_index]
            if index in unpaired_index:
                unpaired_index = unpaired_index[unpaired_index != index]
        else:
            last_period = current_period
            last_index = index
        last_target = target_row['object_id']
    #disc_df = disc_df.loc[left_match_index].combine_first(disc_df.loc[right_match_index])
    result_df = disc_df.loc[unpaired_index]
    for i, index in enumerate(left_match_index):
        result = disc_df.loc[index].combine_first(disc_df.loc[right_match_index[i]])
        result_df = pd.concat([result_df, result.to_frame().T], ignore_index=True)
    result_df.drop(result_df[result_df['duration(h)'].isnull()].index, inplace=True)
    result_df.drop(result_df[result_df['object_id'] == 'KIC <NA>'].index, inplace=True)
    # Remove latest KIC from the catalogue
    result_df.drop(result_df[result_df['object_id'] == 'KIC 100001645'].index, inplace=True)
    result_df.to_csv(tces_dir + '/classified_tces_multi.csv')
    #disc_df[disc_df['object_id'] == 'KIC 7377200'].iloc[0]['epoch']
    result_df = result_df[result_df['type'].isin(['fp', 'fa', 'planet', 'planet_transit', 'tce', 'tce_og',
                                                  'tce_secondary', 'tce_source_offset', 'tce_centroids_offset',
                                                  'tce_odd_even'])]
    result_df = result_df[~result_df['radius(earth)'].isna()]
    #TODO this next statement is to prevent confirmed planets not matching any tce nor koi
    #result_df = result_df[~result_df['object_id'].str.contains('<NA')]
    result_df.to_csv(tces_dir + '/injected_objects_tces_multi.csv')


def create_target_csvs(csv, target_dir, cache_dir, cores=multiprocessing.cpu_count() - 1, force=False, ids=None,
                       mode='all'):
    tces_df = pd.read_csv(csv, comment='#')
    tces_df = tces_df.sort_values(by=["kepid"], ascending=True)
    #tces_df = tces_df.drop_duplicates(subset=["kepid"], keep='last')
    tces_df = tces_df.sort_values(by=["period"], ascending=True)
    #tces_df = tces_df.sample(frac=1).reset_index(drop=True)
    inputs = []
    if ids is not None:
        tces_df = tces_df[tces_df['object_id'].isin(ids)]
    tces_df = tces_df.reset_index(drop=True)
    ranges = range(0, len(tces_df))
    print("Total number of targets is " + str(len(tces_df)))
    for index in ranges:
        tce_row = tces_df.iloc[index]
        inputs = inputs + [CreateTargetInput('KIC', tce_row['object_id'], None, target_dir, None, tce_row, cache_dir, index, force=force, mode=mode)]
    with Pool(processes=cores, maxtasksperchild=1) as pool:
        pool.map(create_target_csv, inputs, chunksize=1)

def create_triceratops_probs(csv, target_dir, cache_dir, cores=multiprocessing.cpu_count() - 1, force=False, ids=None):
    tces_df = pd.read_csv(csv, comment='#')
    tces_df = tces_df.sort_values(by=["kepid"], ascending=True)
    # tces_df = tces_df.drop_duplicates(subset=["kepid"], keep='last')
    #tces_df = tces_df.sample(frac=1).reset_index(drop=True)
    if not force and 'tric_tp_total' in tces_df.columns:
        tces_df = tces_df.loc[tces_df['tric_tp_total'].isna()]
    print("Total number of targets is " + str(len(tces_df)))
    inputs = []
    if ids is not None:
        tces_df = tces_df[tces_df['object_id'].isin(ids)]
    for index, tce_row in tces_df.iterrows():
        inputs = inputs + [
            CreateTargetInput('KIC', tce_row['object_id'], None, target_dir, None, tce_row, cache_dir, force=force)]
    with Pool(processes=cores, maxtasksperchild=1) as pool:
        pool.map(create_triceratops_prob, inputs, chunksize=1)
